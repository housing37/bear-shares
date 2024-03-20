// SPDX-License-Identifier: MIT
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.20;        

// inherited contracts
import "./BSTSwapTools.sol"; // deploy|local
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; // deploy
// import "@openzeppelin/contracts/access/Ownable.sol"; // deploy
import "./node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol"; // local _ $ npm install @openzeppelin/contracts
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";  // local _ $ npm install @openzeppelin/contracts

/* TERMS...
    BST = BearSharesTrinity
*/
contract BearSharesTrinity is ERC20, Ownable, BSTSwapTools {
    uint8 public VERSION = 0;

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    string private constant tok_symb = "tBST";
    // string private constant tok_name = "Trinity";
    string private tok_name = string(abi.encodePacked("tTrinity_", VERSION));

    /* _ ADMIN SUPPORT _ */
    address public KEEPER;
    bool public ENABLE_MARKET_QUOTE = false; // set BST pay & burn val w/ market quote (else 1:1)
    bool public ENABLE_MARKET_BUY = false; // cover BST pay & burn val w/ market buy (else use holdings & mint)
    uint8 public SERVICE_FEE_PERC = 0; // 0%
    uint8 public SERVICE_BURN_PERC = 0; // 0%
    uint8 public BUY_BACK_FEE_PERC = 0; // 0%
    
    /* _ ACCOUNT SUPPORT _ */
    // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
    mapping(address => uint64) public ACCT_USD_BALANCES;
    mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;

    address[] public USWAP_V2_ROUTERS;
    address[] public WHITELIST_USD_STABLES;
    mapping(address => uint8) public USD_STABLE_DECS;

    /* -------------------------------------------------------- */
    /* EVENTS & STRUCTS                                         */
    /* -------------------------------------------------------- */
    struct ACCT_PAYOUT {
        address receiver;
        uint64 usdAmnt; // USD total ACCT deduction
        uint64 usdFee; // USD service fee amount
        uint64 usdBurn; // USD burn value
        uint64 usdPayout; // USD payout value
        uint64 bstBurn; // BST burn amount
        uint64 bstPayout; // BST payout amount
    }

    // LEFT OFF HERE ... probably need some events for stuff
    //  on receive() deposits
    //  on payOutBST
    //  on tradeInBST
    
    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(tok_name, tok_symb) Ownable(msg.sender) {
        SERVICE_FEE_PERC = 5;  // 5%
        SERVICE_BURN_PERC = 5; // 5%
        BUY_BACK_FEE_PERC = 2; // 2%
        _mint(msg.sender, _initSupply * 10**uint8(decimals())); // 'emit Transfer'
        KEEPER = msg.sender;
    }

    /* -------------------------------------------------------- */
    /* MODIFIERS                                                
    /* -------------------------------------------------------- */
    modifier onlyKeeper() {
        require(msg.sender == KEEPER, "!keeper :p");
        _;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER SUPPORT            
    /* -------------------------------------------------------- */
    function KEEPER_maintenance(uint64 _usdAmnt, address _usdStable) external onlyKeeper() {
        require(IERC20(_usdStable).balanceOf(address(this)) >= _usdAmnt, 'err: not enough stable');
        IERC20(_usdStable).transfer(KEEPER, _usdAmnt);
    }
    function KEEPER_setKeeper(address _newKeeper) external onlyKeeper {
        require(_newKeeper != address(0), 'err: 0 address');
        KEEPER = _newKeeper;
    }
    function KEEPER_setServiceFeePerc(uint8 _perc) public onlyKeeper() {
        require(_perc + SERVICE_BURN_PERC <= 100, 'err: fee + burn percs > 100 :/');
        SERVICE_FEE_PERC = _perc;
    }
    function KEEPER_setServiceBurnPerc(uint8 _perc) public onlyKeeper() {
        require(SERVICE_FEE_PERC + _perc <= 100, 'err: fee + burn percs > 100 :/');
        SERVICE_BURN_PERC = _perc;
    }
    function KEEPER_setBuyBackFeePerc(uint8 _perc) public onlyKeeper() {
        require(_perc <= 100, 'err: _perc > 100%');
        BUY_BACK_FEE_PERC = _perc;
    }
    function KEEPER_enableMarketBuy(bool _enable) public onlyKeeper() {
        ENABLE_MARKET_BUY = _enable;
    }
    function KEEPER_enableMarketQuote(bool _enable) public onlyKeeper() {
        ENABLE_MARKET_QUOTE = _enable;
    }
    function KEEPER_editWhitelistStable(address _usdStable, uint8 _decimals, bool _remove) external onlyKeeper { // allows duplicates
        require(_usdStable != address(0), 'err: 0 address');
        if (!_remove) {
            WHITELIST_USD_STABLES = _addAddressToArraySafe(_usdStable, WHITELIST_USD_STABLES, true); // true = no dups
            USD_STABLE_DECS[_usdStable] = _decimals;
            // USD_STABLE_DECS[_usdStable] = IERC20(_usdStable).decimals();
        } else {
            WHITELIST_USD_STABLES = _remAddressFromArray(_usdStable, WHITELIST_USD_STABLES);
            USD_STABLE_DECS[_usdStable] = 0;
        }
    }
    function KEEPER_editDexRouter(address _router, bool _remove) external onlyKeeper returns (bool) {
        require(_router != address(0x0), "0 address");
        if (!_remove) {
            USWAP_V2_ROUTERS = _addAddressToArraySafe(_router, USWAP_V2_ROUTERS, true); // true = no dups
            return true;
        } else {
            USWAP_V2_ROUTERS = _remAddressFromArray(_router, USWAP_V2_ROUTERS); // removes only one & order NOT maintained
            return true;
        }
    }

    /* -------------------------------------------------------- */
    /* PUBLIC ACCESSORS / MUTATORS
    /* -------------------------------------------------------- */
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

    // handle account payouts
    function payOutBST(uint64 _usdAmnt, address _payTo) external {
        require(ACCT_USD_BALANCES[msg.sender] >= _usdAmnt, 'err: low acct balance :{}');
        require(_payTo != address(0), 'err: _payTo address');

        // NOTE: payOutBST runs a total of 7 loops embedded
        //  invokes _getStableTokenHighMarketValue -> _best_swap_v2_router_idx_quote
        //  invokes _getBstMarketValueForUsdAmnt -> _best_swap_v2_router_idx_quote
        //  invokes _getStableHeldLowMarketValue -> _getStableTokenLowMarketValue -> _best_swap_v2_router_idx_quote

        // calc & remove service fee & burn amount
        uint64 usdFee = _perc_of_uint64(SERVICE_FEE_PERC, _usdAmnt);
        uint64 usdBurn = _perc_of_uint64(SERVICE_BURN_PERC, _usdAmnt);
        uint64 usdPayout = _usdAmnt - usdFee - usdBurn;

        // NOTE: maintain 1:1 if ENABLE_MARKET_QUOTE == false
        //  else, get BST value quotes at high market whitelist stable
        uint64 bstPayout = usdPayout;
        uint64 bstBurn = usdBurn;
        if (ENABLE_MARKET_QUOTE) {
            // NOTE: integration runs 4 embedded loops
            //  choose whitelist stable with highest market value
            //  then get BST quote against that high market stable (results in least amnt of BST)
            //   ie. least amount of BST used from holdings (to be burned, paid out, or minted)
            address highStable = _getStableTokenHighMarketValue(WHITELIST_USD_STABLES, USWAP_V2_ROUTERS); // 2 loops embedded
            bstPayout = _getBstMarketValueForUsdAmnt(usdPayout, highStable); // 1 loop embedded
            bstBurn = _getBstMarketValueForUsdAmnt(usdBurn, highStable); // 1 loop embedded
        }
        
        // NOTE: integration runs 3 embedded loops 
        //  get whitelist stables with holdings that can cover usdPayout
        //  then choose stable with lowest market value (results in most amnt of BST)
        //   ie. most amount of BST bought from open market (to be burned or paid out)
        // NOTE: if no stables held can cover 'usdPayout', then lowStableHeld = address(0x0)
        //  this is indeed ok as '_exeBstPayout' and '_exeBstBurn' checks for this case
        address lowStableHeld = _getStableHeldLowMarketValue(usdPayout, WHITELIST_USD_STABLES, USWAP_V2_ROUTERS); // 3 loops embedded

        /** ALGORITHMIC LOGIC ... (for BST ENABLE_MARKET_BUY from dex = ON|OFF)
             if ENABLE_MARKET_BUY, pay|burn BST from market buy
             else, pay|burn w/ contract BST holdings first
                after holdings runs out, pay w/ newly minted BST (no burn)
         */
        _exeBstPayout(_payTo, bstPayout, usdPayout, lowStableHeld);
        _exeBstBurn(bstBurn, usdBurn, lowStableHeld);

        // update account balance
        ACCT_USD_BALANCES[msg.sender] = ACCT_USD_BALANCES[msg.sender] - _usdAmnt;

        // log this payout
        ACCT_USD_PAYOUTS[msg.sender].push(ACCT_PAYOUT(_payTo, _usdAmnt, usdFee, usdBurn, usdPayout, bstBurn, bstPayout));
    }
    
    // handle contract BST buy-backs
    function tradeInBST(uint64 _bstAmnt) external {
        require(balanceOf(msg.sender) >= _bstAmnt,'err: not enough BST');

        // buy-back value is always 1:1        
        uint64 usdBuyBackVal = _bstAmnt; 
        
        // calc usd trade in value (1:1, minus buy back fee)
        uint64 usdBuyBackFee = _perc_of_uint64(BUY_BACK_FEE_PERC, usdBuyBackVal);
        uint64 usdTradeVal = usdBuyBackVal - usdBuyBackFee;

        // get / verify available whitelist stable that covers trade in value
        //  want to use lowest market value stable possible (ie. contract maintains high market stables)
        address usdStable = _getStableHeldLowMarketValue(usdTradeVal, WHITELIST_USD_STABLES, USWAP_V2_ROUTERS);
        require(usdStable != address(0x0), 'err: not enough stable to cover tradeIn');

        // transfer BST in / USD stable out
        _transfer(msg.sender, address(this), _bstAmnt);
        IERC20(usdStable).transfer(msg.sender, usdTradeVal);
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    function _getStableHeldHighMarketValue(uint64 _usdAmntReq, address[] memory _stables, address[] memory _routers) private view returns (address) {

        address[] memory _stablesHeld;
        for (uint i=0; i <= _stables.length;) {
            if (_stableHoldingsCovered(_usdAmntReq, _stables[i]))
                _stablesHeld = _addAddressToArraySafe(_stables[i], _stablesHeld, true); // true = no dups

            unchecked {
                i++;
            }
        }
        return _getStableTokenHighMarketValue(_stablesHeld, _routers); // returns 0x0 if empty _stablesHeld
    }
    function _getStableHeldLowMarketValue(uint64 _usdAmntReq, address[] memory _stables, address[] memory _routers) private view returns (address) {

        address[] memory _stablesHeld;
        for (uint i=0; i <= _stables.length;) {
            if (_stableHoldingsCovered(_usdAmntReq, _stables[i]))
                _stablesHeld = _addAddressToArraySafe(_stables[i], _stablesHeld, true); // true = no dups

            unchecked {
                i++;
            }
        }
        return _getStableTokenLowMarketValue(_stablesHeld, _routers); // returns 0x0 if empty _stablesHeld
    }
    function _stableHoldingsCovered(uint64 _usdAmnt, address _usdStable) private view returns (bool) {
        if (_usdStable == address(0x0)) 
            return false;
        return IERC20(_usdStable).balanceOf(address(this)) >= _usdAmnt;
    }
    function _exeBstPayout(address _payTo, uint256 _bstPayout, uint64 _usdPayout, address _usdStable) private {
        uint256 thisBstBal = balanceOf(address(this));
        bool stableHoldings_OK = _stableHoldingsCovered(_usdPayout, _usdStable);
        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY, pay BST from market buy
             else, pay w/ contract BST holdings first
                after holdings runs out, pay with newly minted BST
         */
        if (ENABLE_MARKET_BUY && stableHoldings_OK) {
            uint256 bst_amnt_out = _exeSwapStableForBst(_usdPayout, _usdStable);
            if (_bstPayout < bst_amnt_out) 
                bst_amnt_out = _bstPayout;
            _transfer(address(this), _payTo, bst_amnt_out);
        } else {
            /** ALGORITHMIC LOGIC ...
                 if contract holdings is greater then _bstPayout
                  pay all from contract holdings
                 if contract holdings is less than _bstPayout
                  pay with remaining holdings & mint the rest
                 if no contract holdings at all
                  mint all of _bstPayout needed
             */
            if (thisBstBal >= _bstPayout) {
                _transfer(address(this), _payTo, _bstPayout);
            } else if (thisBstBal > 0) {
                _transfer(address(this), _payTo, thisBstBal);
                uint256 bstPayoutRem = _bstPayout - thisBstBal; 
                _mint(_payTo, bstPayoutRem);
            } else {
                _mint(_payTo, _bstPayout);
            }
        }
    }
    function _exeBstBurn(uint256 _bstBurnAmnt, uint64 _usdBurn, address _usdStable) private {
        uint256 thisBstBal = balanceOf(address(this));
        bool stableHoldings_OK = _stableHoldingsCovered(_usdBurn, _usdStable);
        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY, burn BST from market buy
             else, burn w/ contract BST holdings
                NOTE: less|no burn, if holdings < _bstBurnAmnt 
         */
        if (ENABLE_MARKET_BUY && stableHoldings_OK) {
            uint256 bst_amnt_out = _exeSwapStableForBst(_usdBurn, _usdStable);
            if (_bstBurnAmnt < bst_amnt_out) 
                bst_amnt_out = _bstBurnAmnt;
            _transfer(address(this), address(0), bst_amnt_out);
        } else {
            /** ALGORITHMIC LOGIC ...
                 if contract holdings > _bstBurnAmnt
                  burn all from contract holdings
                 if contract holdings < _bstBurnAmnt
                  burn remaining holdings
                 NOTE: burn less, if holdings < _bstBurnAmnt
             */
            if (thisBstBal >= _bstBurnAmnt) { // burn all of _bstBurnAmnt
                _transfer(address(this), address(0x0), _bstBurnAmnt);
            } else if (thisBstBal > 0) { // burn all of thisBstBal
                _transfer(address(this), address(0x0), thisBstBal);
                uint256 bstBurnRem = _bstBurnAmnt - thisBstBal; // calc remaining burn
                // NOTE: burn less, if holdings < _bstBurnAmnt
            } else {
                // NOTE: burn nothing, if holdings = 0
            }
        }
    }
    function _getBstMarketValueForUsdAmnt(uint64 _usdAmnt, address _usdStable) private view returns (uint64) {
        address[] memory stab_bst_path = new address[](2);
        stab_bst_path[0] = _usdStable;
        stab_bst_path[1] = address(this);
        (uint8 rtrIdx, uint256 bst_amnt) = _best_swap_v2_router_idx_quote(stab_bst_path, uint256(_usdAmnt), USWAP_V2_ROUTERS);
        return _uint256_to_uint64(bst_amnt); 
    }
    function _perc_of_uint64(uint8 _perc, uint64 _num) private pure returns (uint64) {
        require(_perc <= 100, 'err: invalid percent');
        uint32 aux_perc = _perc * 100;
        uint64 result = (_num * aux_perc) / 10000; // chatGPT equation
        return result;
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
    function _exeSwapStableForBst(uint256 _usdAmnt, address _usdStable) private returns (uint256) {
        address[] memory stab_bst_path = new address[](2);
        stab_bst_path[0] = _usdStable;
        stab_bst_path[1] = address(this);
        (uint8 rtrIdx, uint256 bst_amnt) = _best_swap_v2_router_idx_quote(stab_bst_path, _usdAmnt, USWAP_V2_ROUTERS);
        uint256 bst_amnt_out = _swap_v2_wrap(stab_bst_path, USWAP_V2_ROUTERS[rtrIdx], _usdAmnt, address(this), false); // true = fromETH
        return bst_amnt_out;
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

    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    function decimals() public pure override returns (uint8) {
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
    function transferFrom(address from, address to, uint256 value) public override returns (bool) {
        if (from != address(this)) {
            return super.transferFrom(from, to, value);
        } else {
            _transfer(from, to, value); // balance checks, etc. indeed occur
        }
        return true;
    }
}
