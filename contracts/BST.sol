// SPDX-License-Identifier: MIT
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.20;        

// interfaces
// import "./IGTADelegate.sol";
// import "./IGTALib.sol";

// inherited contracts
import "./BSTSwapTools.sol"; // deploy|local
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; // deploy
// import "@openzeppelin/contracts/access/Ownable.sol"; // deploy
import "./node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol"; // local _ $ npm install @openzeppelin/contracts
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";  // local _ $ npm install @openzeppelin/contracts

/* terminology...
                 join -> room, game, event, activity
             register -> seat, guest, delegates, users, participants, entrants
    payout/distribute -> rewards, winnings, earnings, recipients 
*/
// Import MyStruct from ContractB
// using IGTALib for IGTALib.Event_0;
contract BearSharesTrinity is ERC20, Ownable, BSTSwapTools {
    uint8 public VERSION = 0;

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ ADMIN SUPPORT _ */
    // IGTADelegate private GTAD; // 'keeper' maintained within
    // IGTALib private GTAL;
    address public KEEPER;
    
    /* _ TOKEN INIT SUPPORT _ */
    string private constant tok_name = "BearSharesTrinity";
    string private constant tok_symb = "BST";
    // string private tok_name = string(abi.encodePacked("tGTA ", VERSION));
    
    struct USD_STABLE {
        address tokAddr;
        uint8 tokDecimals;
    }
    struct ACCT_PAYOUT {
        address receiver;
        uint64 usdAmnt; // USD total ACCT deduction
        uint64 usdFee; // USD service fee amount
        uint64 usdBurn; // USD burn value
        uint64 usdPayout; // USD payout value
        uint64 bstBurn; // BST burn amount
        uint64 bstPayout; // BST payout amount
    }

    // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
    mapping(address => uint64) public ACCT_USD_BALANCES;
    uint8 public SERVICE_FEE_PERC = 0; // 0%
    uint8 public SERVICE_BURN_PERC = 0; // 0%
    uint8 public BUY_BACK_FEE_PERC = 0; // 0%
    bool public ENABLE_BUY_BURN = false;

    mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;
    // address[] private creditsAddrArray;

    address[] public USWAP_V2_ROUTERS;
    
    address[] public WHITELIST_USD_STABLES;
    mapping(address => uint64) public USD_STABLE_BALANCES;
    mapping(address => uint8) public USD_STABLE_DECS;

    /* -------------------------------------------------------- */
    /* EVENTS                                                   */
    /* -------------------------------------------------------- */


    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: pre-initialized 'GTADelegate' address required
    //      initializer w/ 'keeper' not required ('GTADelegate' maintained)
    //      sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(tok_name, tok_symb) Ownable(msg.sender) {
        setServiceFeePerc(5); // 5%
        setServiceBurnPerc(5); // 5%
        setBuyBackFeePerc(2); // 2%
        _mint(msg.sender, _initSupply * 10**uint8(decimals())); // 'emit Transfer'
    }

    /* -------------------------------------------------------- */
    /* MODIFIERS                                                */
    /* -------------------------------------------------------- */
    modifier onlyKeeper() {
        require(msg.sender == KEEPER, "!keeper :p");
        _;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER SUPPORT            
    /* -------------------------------------------------------- */
    function setKeeper(address _newKeeper) external onlyKeeper {
        KEEPER = _newKeeper;
    }
    function addWhitelistStable(address _usdStable, uint8 _decimals) external onlyKeeper { // allows duplicates
        require(_usdStable != address(0), 'err: 0 address');
        WHITELIST_USD_STABLES = _addAddressToArraySafe(_usdStable, WHITELIST_USD_STABLES, true); // true = no dups
        USD_STABLE_DECS[_usdStable] = _decimals;
    }
    function remWhitelistStable(address _usdStable) external onlyKeeper { // allows duplicates
        require(_usdStable != address(0), 'err: 0 address');
        WHITELIST_USD_STABLES = _remAddressFromArray(_usdStable, WHITELIST_USD_STABLES);
        USD_STABLE_DECS[_usdStable] = 0;
    }
    function addDexRouter(address _router) external onlyKeeper returns (bool) {
        require(_router != address(0x0), "0 address");
        USWAP_V2_ROUTERS = _addAddressToArraySafe(_router, USWAP_V2_ROUTERS, true); // true = no dups
        return true;
    }
    function remDexRouter(address router) external onlyKeeper returns (bool) {
        require(router != address(0x0), "0 address");
        USWAP_V2_ROUTERS = _remAddressFromArray(router, USWAP_V2_ROUTERS); // removes only one & order NOT maintained
        return true;
    }
    function setBuyBurnEnabled(bool _enable) public onlyOwner() {
        ENABLE_BUY_BURN = _enable;
    }
    function setServiceFeePerc(uint8 _perc) public onlyOwner() {
        require(_perc + SERVICE_BURN_PERC <= 100, 'err: fee + burn percs > 100 :/');
        SERVICE_FEE_PERC = _perc;
    }
    function setServiceBurnPerc(uint8 _perc) public onlyOwner() {
        require(SERVICE_FEE_PERC + _perc <= 100, 'err: fee + burn percs > 100 :/');
        SERVICE_BURN_PERC = _perc;
    }
    function setBuyBackFeePerc(uint8 _perc) public onlyOwner() {
        require(_perc <= 100, 'err: _perc more than 100%');
        BUY_BACK_FEE_PERC = _perc;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC ACCESSORS / MUTATORS
    /* -------------------------------------------------------- */
    function payOutBST(uint64 _usdAmnt, address _payTo) external {
        require(ACCT_USD_BALANCES[msg.sender] >= _usdAmnt, 'err: low acct balance :{}');
        require(_payTo != address(0), 'err: _payTo address');

        // calc & remove service fee & burn amount
        uint64 usdFee = _usdAmnt * (SERVICE_FEE_PERC/100); 
        uint64 usdBurn = _usdAmnt * (SERVICE_BURN_PERC/100); 
        uint64 usdPayout = _usdAmnt - usdFee - usdBurn;
        uint64 bstBurn = _getBstValueForUsdAmnt(usdBurn);
        uint64 bstPayout = _getBstValueForUsdAmnt(usdPayout);

        // log this payout
        ACCT_USD_PAYOUTS[msg.sender].push(ACCT_PAYOUT(_payTo, _usdAmnt, usdFee, usdBurn, usdPayout, bstBurn, bstPayout));

        // update account balance
        ACCT_USD_BALANCES[msg.sender] = ACCT_USD_BALANCES[msg.sender] - _usdAmnt;

        // ALGORITHMIC INTEGRATION... (for BST buy&burn from dex = ON|OFF)
        // When a payout occurs...
        //  1) always try to pay w/ contract BST holdings first
        //  2) then, after BST holdings runs out, 
        //      if buy&burn=ON, 
        //          buy BST from dexes to use for payout
        //      if buy&burn=OFF, 
        //          mint new BST to use for payout
        _exeBstPayout(_payTo, bstPayout);
        _exeBstBurn(bstBurn);
    }
    
    // handle contract USD value deposits (convert PLS to USD stable)
    receive() external payable {
        // extract PLS value sent
        uint256 amntIn = msg.value; 

        // get whitelisted stable with lowest market value (ie. receive most stable for swap)
        address usdSable = _getStableTokenLowMarketValue(WHITELIST_USD_STABLES, USWAP_V2_ROUTERS);

        // perform swap from PLS to stable
        uint256 stableAmntOut = _exeSwapPlsForStable(amntIn, usdSable);

        // convert and set/update balance for this sender
        uint64 amntConvert = _uint256_to_uint64(stableAmntOut);
        ACCT_USD_BALANCES[msg.sender] += amntConvert;
    }

    // handle contract BST buy-backs
    function tradeBST(uint64 _bstAmnt) external {
        require(balanceOf(msg.sender) >= _bstAmnt,'err: not enough BST');
        uint64 usdAmnt = _getUsdValueForBstAmnt(_bstAmnt); // should return 1:1
        (address usdStable, uint64 usdAvail) = _getBestUsdStableAndBalance(usdAmnt);
        
        // calc usd trade in value & verify balance
        uint64 usdTradeVal = usdAmnt - (usdAmnt * (BUY_BACK_FEE_PERC/100));
        require(usdAvail >= usdTradeVal, 'err: not enough stable');

        // transfer BST in / USD stable out
        _transfer(address(this), msg.sender, _bstAmnt);
        IERC20(usdStable).transfer(msg.sender, usdAmnt);
    }

    function usdDecimals() public pure returns (uint8) {
        return 6; // (6 decimals) 
            // * min USD = 0.000001 (6 decimals) 
            // uint16 max USD: ~0.06 -> 0.065535 (6 decimals)
            // uint32 max USD: ~4K -> 4,294.967295 USD (6 decimals)
            // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
        // return 18; // (18 decimals) 
            // * min USD = 0.000000000000000001 (18 decimals) 
            // uint64 max USD: ~18 -> 18.446744073709551615 (18 decimals)
            // uint128 max USD: ~340T -> 340,282,366,920,938,463,463.374607431768211455 (18 decimals)
    }

    /* -------------------------------------------------------- */
    /* PUBLIC ACCESSORS - GTA HOLDER SUPPORT                    */
    /* -------------------------------------------------------- */


    /* -------------------------------------------------------- */
    /* PUBLIC - HOST / PLAYER SUPPORT                           */
    /* -------------------------------------------------------- */


    /* -------------------------------------------------------- */
    /* KEEPER CALL-BACK                                         */
    /* -------------------------------------------------------- */


    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    // NOTE: this function has an embedded loop (ie. '_addAddressToArraySafe')
    //  and then a 3rd loop inside '_getStableTokenHighMarketValue'
    function _getBestUsdStableAndBalance(uint64 _reqUsdBal) private returns (address, uint64) {

        // loop through WHITELIST_USD_STABLES to find the highest market value
        //  that can cover a transfer of '_reqUsdBal'
        address[] memory availStables;
        for (uint i=0; i < WHITELIST_USD_STABLES.length;) {
            address stable_ = WHITELIST_USD_STABLES[i];
            uint256 stableBal = IERC20(stable_).balanceOf(address(this));
            if (_uint256_to_uint64(stableBal) >= _reqUsdBal) {
                availStables = _addAddressToArraySafe(stable_, availStables, true); // true = no dups
                USD_STABLE_BALANCES[stable_] = _uint256_to_uint64(stableBal);
            }
            
            unchecked {
                i++;
            }
        }
        address highStable = _getStableTokenHighMarketValue(availStables, USWAP_V2_ROUTERS);
        return (highStable, USD_STABLE_BALANCES[highStable]);
    }
    function _uint256_to_uint64(uint256 value) private pure returns (uint64) {
        require(value <= type(uint64).max, "Value exceeds uint64 range");
        uint64 convertedValue = uint64(value);
        return convertedValue;
    }
    function _exeSwapPlsForStable(uint256 _plsAmnt, address _usdStable) private returns (uint256) {
        address[] memory pls_stab_path = new address[](2);
        pls_stab_path[0] = TOK_WPLS;
        pls_stab_path[1] = _usdStable;
        (uint8 rtrIdx, uint256 stab_amnt) = _best_swap_v2_router_idx_quote(pls_stab_path, _plsAmnt, USWAP_V2_ROUTERS);
        uint256 stab_amnt_out = _swap_v2_wrap(pls_stab_path, USWAP_V2_ROUTERS[rtrIdx], _plsAmnt, address(this), true); // true = fromETH
        return stab_amnt_out;
    }
    function _exeBstPayout(address _payTo, uint256 _bstPayout) private {
        uint256 bstPayoutRem = 0;
        uint256 thisBstBal = IERC20(address(this)).balanceOf(address(this));
        // ALGORITHMIC INTEGRATION...
        //  1) always pay w/ contract BST holdings first
        //  2) after holdings runs out, 
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstPayoutRem
        //      else, mint new BST for bstPayoutRem
        //  3) if no BST holdings at all,
        //      if ENABLE_BUY_BURN, buy BST from dexes for _bstPayout
        //      else, mint new BST for _bstPayout
        // execute payout requirements
        if (thisBstBal >= _bstPayout) { // transfer all of _bstPayout
            _transfer(address(this), _payTo, _bstPayout);
        } else if (thisBstBal > 0) { // transfer all of thisBstBal
            _transfer(address(this), _payTo, thisBstBal);
            bstPayoutRem = _bstPayout - thisBstBal; // calc remaining bst owed

            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... buy 'bstPayoutRem' from dex
                //  then, transfer 'bstPayoutRem' over to '_payTo'
            } else {
                _mint(_payTo, bstPayoutRem); // mint remaining bst owed
            }

        } else {
            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... buy '_bstPayout' from dex
                //  then, transfer '_bstPayout' over to '_payTo'
            } else {
                _mint(_payTo, _bstPayout); // mint all of _bstPayout owed
            }
        }
    }
    function _exeBstBurn(uint256 _bstBurnAmnt) private {
        uint256 bstBurnRem = 0;
        uint256 thisBstBal = IERC20(address(this)).balanceOf(address(this));
        // ALGORITHMIC INTEGRATION...
        //  1) always burn from contract BST holdings first
        //  2) after holdings runs out, 
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstBurnRem
        //      else, do nothing (don't mint bstBurnRem)
        //  3) if no BST holdings at all,
        //      if ENABLE_BUY_BURN, buy BST from dexes for _bstBurnAmnt
        //      else, do nothing (don't mint _bstBurnAmnt)
        // execute burn requirements
        if (thisBstBal >= _bstBurnAmnt) { // burn all of _bstBurnAmnt
            _transfer(address(this), address(0x0), _bstBurnAmnt);
        } else if (thisBstBal > 0) { // burn all of thisBstBal
            _transfer(address(this), address(0x0), thisBstBal);
            bstBurnRem = _bstBurnAmnt - thisBstBal; // calc remaining burn

            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... buy 'bstBurnRem' from dex
                //  then, burn 'bstBurnRem'
            } else {
                // mint remaining bstPayout thats owed
                // _mint(_payTo, bstBurnRem);
                // ... don't mint anything?
            }
        } else {
            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... buy 'bstPayout' from dex
                //  then, burn 'bstPayout'
            } else {
                // mint all of bstPayout owed
                // _mint(_payTo, bstPayout);
                // ... do nothing?
            }
        }
    }
    function _addAddressToArraySafe(address _addr, address[] memory _arr, bool _safe) private pure returns (address[] memory) {
        if (_addr == address(0)) { return _arr; }

        // safe = remove first (no duplicates)
        if (_safe) { _arr = _remAddressFromArray(_addr, _arr); }

        // perform add to memory array type w/ static size
        address[] memory _ret = new address[](_arr.length+1);
        for (uint i=0; i < _arr.length; i++) { _ret[i] = _arr[i]; }
        _ret[_ret.length] = _addr;
        return _ret;
    }
    function _remAddressFromArray(address _addr, address[] memory _arr) private pure returns (address[] memory) {
        if (_addr == address(0) || _arr.length == 0) { return _arr; }
        
        // NOTE: remove algorithm does NOT maintain order & only removes first occurance
        for (uint i = 0; i < _arr.length; i++) {
            if (_addr == _arr[i]) {
                _arr[i] = _arr[_arr.length - 1];
                assembly { // reduce memory _arr length by 1 (simulate pop)
                    mstore(_arr, sub(mload(_arr), 1))
                }
                return _arr;
            }
        }
        return _arr;
    }
    function _getBstValueForUsdAmnt(uint64 _usdAmnt) private returns (uint64) {
        return 37; 
        // LEFT OFF HERE ... TODO
    }
    function _getUsdValueForBstAmnt(uint64 _bstAmnt) private returns (uint64) {
        // LEFT OFF HERE ... pretty sure this should always just return 1:1
        return _bstAmnt; 
    }


    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    function decimals() public pure override returns (uint8) {
        // return 18;
        return 6;
    }
    function transferFrom(address from, address to, uint256 value) public override returns (bool) {
        if (from != address(this)) {
            return super.transferFrom(from, to, value);
        } else {
            _transfer(from, to, value); // balance checks, etc. indeed occur
        }
        return true;
    }
}
