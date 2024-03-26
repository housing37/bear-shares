// SPDX-License-Identifier: UNLICENSED
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.24;        

// inherited contracts
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; // deploy
// import "@openzeppelin/contracts/access/Ownable.sol"; // deploy
// import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // deploy
// import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol"; // deploy

// local _ $ npm install @openzeppelin/contracts
import "./node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol"; 
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "./node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./node_modules/@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";


// contract BearSharesTrinity is ERC20, Ownable, BSTSwapToolsX2 {
contract BearSharesTrinity is ERC20, Ownable {
    address public constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    string public tVERSION = '23';
    string private tok_symb = string(abi.encodePacked("tBST", tVERSION));
    string private tok_name = string(abi.encodePacked("tTrinity_", tVERSION));
    // string private constant tok_symb = "BST";
    // string private constant tok_name = "Trinity";


    /* _ ADMIN SUPPORT _ */
    address public KEEPER;
    bool public ENABLE_MARKET_QUOTE = false; // set BST pay & burn val w/ market quote (else 1:1)
    bool public ENABLE_MARKET_BUY = false; // cover BST pay & burn val w/ market buy (else use holdings & mint)
    uint8 public SERVICE_FEE_PERC = 0; // 0%
    uint8 public SERVICE_BURN_PERC = 0; // 0%
    uint8 public BUY_BACK_FEE_PERC = 0; // 0%
    
    /* _ ACCOUNT SUPPORT _ */
    // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
    // NOTE: all USD bals & payouts stores uint precision to decimals()
    address[] public ACCOUNTS;
    mapping(address => uint64) public ACCT_USD_BALANCES; 
    mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;

    address[] public USWAP_V2_ROUTERS;
    address[] public WHITELIST_USD_STABLES;
    address[] public USD_STABLES_HISTORY;
    mapping(address => uint8) public USD_STABLE_DECIMALS;
    mapping(address => address[]) public USD_BST_PATHS;

    /* -------------------------------------------------------- */
    /* STRUCTS                                        
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

    /* -------------------------------------------------------- */
    /* EVENTS                                        
    /* -------------------------------------------------------- */
    event KeeperTransfer(address _prev, address _new);
    event ServiceFeeUpdate(uint8 _prev, uint8 _new);
    event ServiceBurnUpdate(uint8 _prev, uint8 _new);
    event TradeInFeeUpdate(uint8 _prev, uint8 _new);
    event MarketBuyEnabled(bool _prev, bool _new);
    event MarketQuoteEnabled(bool _prev, bool _new);
    event DepositReceived(address _account, uint256 _plsDeposit, uint64 _stableConvert);
    event PayOutProcessed(address _from, address _to, uint64 _usdAmnt);
    event TradeInFailed(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal);
    event TradeInDenied(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal);
    event TradeInProcessed(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal);
    event WhitelistStableUpdated(address _usdStable, uint8 _decimals, bool _add);
    event DexRouterUpdated(address _router, bool _add);
    event DexUsdBstPathUpdated(address _usdStable, address[] _path);

    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(tok_name, tok_symb) Ownable(msg.sender) {
        // set default globals
        ENABLE_MARKET_QUOTE = false;
        ENABLE_MARKET_BUY = false;
        SERVICE_FEE_PERC = 5;  // 5%
        SERVICE_BURN_PERC = 5; // 5%
        BUY_BACK_FEE_PERC = 2; // 2%
        KEEPER = msg.sender;
        _mint(msg.sender, _initSupply * 10**uint8(decimals())); // 'emit Transfer'

        // add default stables: weUSDT
        address usdStable = address(0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f); 
        uint8 decimals_ = 6;
        _editWhitelistStables(usdStable, decimals_, true); // true = add

        // add default routers: pulsex x2 
        address router_0 = address(0x98bf93ebf5c380C0e6Ae8e192A7e2AE08edAcc02);
        address router_1 = address(0x165C3410fC91EF562C50559f7d2289fEbed552d9);
        _editDexRouters(router_0, true); // true = add
        _editDexRouters(router_1, true); // true = add
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
    //  NOTE: _usdAmnt must be in uint precision to _usdStable.decimals()
    function KEEPER_maintenance(uint64 _usdAmnt, address _usdStable) external onlyKeeper() {
        require(IERC20(_usdStable).balanceOf(address(this)) >= _usdAmnt, 'err: not enough _usdStable');
        IERC20(_usdStable).transfer(KEEPER, _usdAmnt);
    }
    function KEEPER_setKeeper(address _newKeeper) external onlyKeeper {
        require(_newKeeper != address(0), 'err: 0 address');
        address prev = address(KEEPER);
        KEEPER = _newKeeper;
        emit KeeperTransfer(prev, KEEPER);
    }
    function KEEPER_setServiceFeePerc(uint8 _perc) external onlyKeeper() {
        require(_perc + SERVICE_BURN_PERC <= 100, 'err: fee + burn percs > 100 :/');
        uint8 prev = SERVICE_FEE_PERC;
        SERVICE_FEE_PERC = _perc;
        emit ServiceFeeUpdate(prev, SERVICE_FEE_PERC);
    }
    function KEEPER_setServiceBurnPerc(uint8 _perc) external onlyKeeper() {
        require(SERVICE_FEE_PERC + _perc <= 100, 'err: fee + burn percs > 100 :/');
        uint8 prev = SERVICE_BURN_PERC;
        SERVICE_BURN_PERC = _perc;
        emit ServiceBurnUpdate(prev, SERVICE_BURN_PERC);
    }
    function KEEPER_setBuyBackFeePerc(uint8 _perc) external onlyKeeper() {
        require(_perc <= 100, 'err: _perc > 100%');
        uint8 prev = BUY_BACK_FEE_PERC;
        BUY_BACK_FEE_PERC = _perc;
        emit TradeInFeeUpdate(prev, BUY_BACK_FEE_PERC);
    }
    function KEEPER_enableMarketBuy(bool _enable) external onlyKeeper() {
        bool prev = ENABLE_MARKET_BUY;
        ENABLE_MARKET_BUY = _enable;
        emit MarketBuyEnabled(prev, ENABLE_MARKET_BUY);
    }
    function KEEPER_enableMarketQuote(bool _enable) external onlyKeeper() {
        bool prev = ENABLE_MARKET_QUOTE;
        ENABLE_MARKET_QUOTE = _enable;
        emit MarketQuoteEnabled(prev, ENABLE_MARKET_QUOTE);
    }
    function KEEPER_editWhitelistStables(address _usdStable, uint8 _decimals, bool _add) external onlyKeeper {
        require(_usdStable != address(0), 'err: 0 address');
        _editWhitelistStables(_usdStable, _decimals, _add);
        emit WhitelistStableUpdated(_usdStable, _decimals, _add);
    }
    function KEEPER_editDexRouters(address _router, bool _add) external onlyKeeper {
        require(_router != address(0x0), "0 address");
        _editDexRouters(_router, _add);
        emit DexRouterUpdated(_router, _add);
    }
    function KEEPER_setUsdBstPath(address _usdStable, address[] memory _path) external onlyKeeper() {
        require(_usdStable != address(0) && _path.length > 1, 'err: invalid input :{=}');
        require(_usdStable == _path[0], 'err: stable / path mismatch =)');
        USD_BST_PATHS[_usdStable] = _path;
        emit DexUsdBstPathUpdated(_usdStable, _path);
        // NOTE: '_path' must be valid within all 'USWAP_V2_ROUTERS' addresses
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER - ACCESSORS
    /* -------------------------------------------------------- */
    function KEEPER_contractStableBalances() external view onlyKeeper() returns (uint64, uint64, int64) {
        return _contractStableBalances(USD_STABLES_HISTORY);
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - ACCESSORS
    /* -------------------------------------------------------- */
    function getAccounts() external view returns (address[] memory) {
        return ACCOUNTS;
    }
    function getUsdBstPath(address _usdStable) external view returns (address[] memory) {
        return USD_BST_PATHS[_usdStable];
    }    
    function getUsdStablesHistory() external view returns (address[] memory) {
        return USD_STABLES_HISTORY;
    }    
    function getWhitelistStables() external view returns (address[] memory) {
        return WHITELIST_USD_STABLES;
    }
    function getSwapRouters() external view returns (address[] memory) {
        return USWAP_V2_ROUTERS;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE
    /* -------------------------------------------------------- */
    // handle contract USD value deposits (convert PLS to USD stable)
    receive() external payable {
        // extract PLS value sent
        uint256 amntIn = msg.value; 

        // get whitelisted stable with lowest market value (ie. receive most stable for swap)
        address usdStable = _getStableTokenLowMarketValue(WHITELIST_USD_STABLES, USWAP_V2_ROUTERS);

        // perform swap from PLS to stable
        uint256 stableAmntOut = _exeSwapPlsForStable(amntIn, usdStable); // _normalizeStableAmnt

        // convert and set/update balance for this sender, ACCT_USD_BALANCES stores uint precision to decimals()
        uint64 amntConvert = _uint64_from_uint256(stableAmntOut);
        ACCT_USD_BALANCES[msg.sender] += amntConvert;
        ACCOUNTS = _addAddressToArraySafe(msg.sender, ACCOUNTS, true); // true = no dups

        emit DepositReceived(msg.sender, amntIn, amntConvert);
    }

    // handle account payouts
    //  NOTE: _usdValue must be in uint precision to decimals()
    function payOutBST(uint64 _usdValue, address _payTo) external {
        // NOTE: payOutBST runs a total of 7 loops embedded
        //  invokes _getStableTokenHighMarketValue -> _best_swap_v2_router_idx_quote
        //  invokes _getBstMarketValueForUsdAmnt -> _best_swap_v2_router_idx_quote
        //  invokes _getStableHeldLowMarketValue -> _getStableTokenLowMarketValue -> _best_swap_v2_router_idx_quote

        // ACCT_USD_BALANCES stores uint precision to decimals()
        require(_usdValue > 0, ' 0 _usdValue :[] ');
        require(ACCT_USD_BALANCES[msg.sender] >= _usdValue, ' low acct balance :{} ');
        require(_payTo != address(0), ' _payTo 0 address :( ');

        // calc & remove service fee & burn amount
        uint64 usdFee = _perc_of_uint64(SERVICE_FEE_PERC, _usdValue);
        uint64 usdBurn = _perc_of_uint64(SERVICE_BURN_PERC, _usdValue);
        uint64 usdPayout = _usdValue - usdFee - usdBurn;

        // NOTE: validate contract's collective stable balances can cover usdPayout
        //  if yes, let it go through ... else, revert (ie. contract can't cover a tradeInBST for usdPayout amount)
        //   NOTE: if lowStableHeld = 0x0 (below): _exeBstPayout|Burn will fallback to contract holdings / minting
        (uint64 stab_gross_bal, uint64 stab_owed_bal, int64 stab_net_bal) = _contractStableBalances(WHITELIST_USD_STABLES);
        require(stab_gross_bal >= usdPayout, ' gross bal will not cover usdPayout buy-back :/ ');

        // NOTE: maintain 1:1 if ENABLE_MARKET_QUOTE == false
        //  else, get BST value quotes against highest market valued whitelist stable
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
        //  this is indeed ok as '_exeBstPayout' & '_exeBstBurn' checks for this, and falls back to holdings / minting
        address lowStableHeld = _getStableHeldLowMarketValue(usdPayout, WHITELIST_USD_STABLES, USWAP_V2_ROUTERS); // 3 loops embedded

        /** ALGORITHMIC LOGIC ... (for BST ENABLE_MARKET_BUY from dex = ON|OFF)
             if ENABLE_MARKET_BUY, pay|burn BST from market buy
             else, pay|burn w/ contract BST holdings first
                after holdings runs out, pay w/ newly minted BST (no burn)
         */
        _exeBstPayout(_payTo, bstPayout, usdPayout, lowStableHeld);
        _exeBstBurn(bstBurn, usdBurn, lowStableHeld);

        // update account balance, ACCT_USD_BALANCES stores uint precision to decimals()
        ACCT_USD_BALANCES[msg.sender] -= _usdValue; // _usdValue 'require' check above

        // log this payout, ACCT_USD_PAYOUTS stores uint precision to decimals()
        ACCT_USD_PAYOUTS[msg.sender].push(ACCT_PAYOUT(_payTo, _usdValue, usdFee, usdBurn, usdPayout, bstBurn, bstPayout));

        emit PayOutProcessed(msg.sender, _payTo, _usdValue);
    }
    
    // handle contract BST buy-backs
    //  NOTE: _bstAmnt must be in uint precision to decimals()
    function tradeInBST(uint64 _bstAmnt) external {
        require(balanceOf(msg.sender) >= _bstAmnt,' not enough BST :/ ');

        // buy-back value is always 1:1        
        uint64 usdBuyBackVal = _bstAmnt; 
        
        // calc usd trade in value (1:1, minus buy back fee)
        uint64 usdBuyBackFee = _perc_of_uint64(BUY_BACK_FEE_PERC, usdBuyBackVal);
        uint64 usdTradeVal = usdBuyBackVal - usdBuyBackFee;

        // NOTE: validate contract's collective stable balances can cover usdTradeVal
        (uint64 stab_gross_bal, uint64 stab_owed_bal, int64 stab_net_bal) = _contractStableBalances(WHITELIST_USD_STABLES);
        if (stab_gross_bal < usdTradeVal) {
            emit TradeInFailed(msg.sender, _bstAmnt, usdTradeVal); // notify keeper maintenance needed
            revert(' failed: cannot cover usdTradeVal :/ ');
            // require(stab_gross_bal >= usdTradeVal, ' cannot cover usdTradeVal :/ ');
        }

        // get / verify available whitelist stable that covers trade in value
        //  want to use lowest market value stable possible (ie. contract maintains high market stables)
        address usdStable = _getStableHeldLowMarketValue(usdTradeVal, WHITELIST_USD_STABLES, USWAP_V2_ROUTERS);
        if (usdStable == address(0x0)) {
            emit TradeInDenied(msg.sender, _bstAmnt, usdTradeVal); // notify keeper maintenance needed
            revert(' denied: no single stable found to cover tradeIn :/ ');
            // require(usdStable != address(0x0), ' denied: no single stable found to cover tradeIn :/ ');
        }
        
        // transfer BST in
        _transfer(msg.sender, address(this), _bstAmnt);

        // transfer USD stable out
        uint256 usdTradeVal_ = _normalizeStableAmnt(decimals(), usdTradeVal, USD_STABLE_DECIMALS[usdStable]);
        IERC20(usdStable).transfer(msg.sender, usdTradeVal_);

        emit TradeInProcessed(msg.sender, _bstAmnt, usdTradeVal);
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    function _contractStableBalances(address[] memory _stables) private view returns (uint64, uint64, int64) {
        uint64 gross_bal = 0;
        for (uint8 i = 0; i < _stables.length;) {
            address stable = _stables[i];
            uint8 decimals_ = USD_STABLE_DECIMALS[stable];
            require(decimals_ > 0, 'err: invalid stables decimals :/');
            uint256 bal = IERC20(stable).balanceOf(address(this));
            uint256 norm_bal = _normalizeStableAmnt(decimals_, bal, decimals());
            gross_bal += _uint64_from_uint256(norm_bal);
            unchecked {i++;}
        }

        uint64 owed_bal = 0;
        for (uint256 i = 0; i < ACCOUNTS.length;) {
            owed_bal += ACCT_USD_BALANCES[ACCOUNTS[i]];
            unchecked {i++;}
        }

        int64 net_bal = int64(gross_bal) - int64(owed_bal);
        return (gross_bal, owed_bal, net_bal);
    }
    function _editWhitelistStables(address _usdStable, uint8 _decimals, bool _add) private { // allows duplicates
        if (_add) {
            WHITELIST_USD_STABLES = _addAddressToArraySafe(_usdStable, WHITELIST_USD_STABLES, true); // true = no dups
            USD_STABLES_HISTORY = _addAddressToArraySafe(_usdStable, USD_STABLES_HISTORY, true); // true = no dups
            USD_STABLE_DECIMALS[_usdStable] = _decimals;
        } else {
            WHITELIST_USD_STABLES = _remAddressFromArray(_usdStable, WHITELIST_USD_STABLES);
        }
    }
    function _editDexRouters(address _router, bool _add) private {
        require(_router != address(0x0), "0 address");
        if (_add) {
            USWAP_V2_ROUTERS = _addAddressToArraySafe(_router, USWAP_V2_ROUTERS, true); // true = no dups
        } else {
            USWAP_V2_ROUTERS = _remAddressFromArray(_router, USWAP_V2_ROUTERS); // removes only one & order NOT maintained
        }
    }
    function _getStableHeldHighMarketValue(uint64 _usdAmntReq, address[] memory _stables, address[] memory _routers) private view returns (address) {

        address[] memory _stablesHeld;
        for (uint8 i=0; i < _stables.length;) {
            if (_stableHoldingsCovered(_usdAmntReq, _stables[i]))
                _stablesHeld = _addAddressToArraySafe(_stables[i], _stablesHeld, true); // true = no dups

            unchecked {
                i++;
            }
        }
        return _getStableTokenHighMarketValue(_stablesHeld, _routers); // returns 0x0 if empty _stablesHeld
    }
    function _getStableHeldLowMarketValue(uint64 _usdAmntReq, address[] memory _stables, address[] memory _routers) private view returns (address) {
        // NOTE: if nothing in _stables can cover _usdAmntReq, then returns address(0x0)
        address[] memory _stablesHeld;
        for (uint8 i=0; i < _stables.length;) {
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
        uint256 usdAmnt_ = _normalizeStableAmnt(decimals(), _usdAmnt, USD_STABLE_DECIMALS[_usdStable]);
        return IERC20(_usdStable).balanceOf(address(this)) >= usdAmnt_;
    }
    function _exeBstPayout(address _payTo, uint256 _bstPayout, uint64 _usdPayout, address _usdStable) private {
        uint256 thisBstBal = balanceOf(address(this));
        bool stableHoldings_OK = _stableHoldingsCovered(_usdPayout, _usdStable);
        bool usdBstPath_OK = USD_BST_PATHS[_usdStable].length > 0;

        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY, pay BST from market buy
             else, pay w/ contract BST holdings first
                after holdings runs out, pay with newly minted BST
         */
        if (ENABLE_MARKET_BUY && stableHoldings_OK && usdBstPath_OK) {
            uint256 bst_amnt_out = _exeSwapStableForBst(_usdPayout, _usdStable, USD_BST_PATHS[_usdStable]);
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
        bool usdBstPath_OK = USD_BST_PATHS[_usdStable].length > 0;

        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY, burn BST from market buy
             else, burn w/ contract BST holdings
                NOTE: less|no burn, if holdings < _bstBurnAmnt 
         */
        if (ENABLE_MARKET_BUY && stableHoldings_OK && usdBstPath_OK) {
            uint256 bst_amnt_out = _exeSwapStableForBst(_usdBurn, _usdStable, USD_BST_PATHS[_usdStable]);
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
    function _getBstMarketValueForUsdAmnt(uint256 _usdAmnt, address _usdStable) private view returns (uint64) {
        address[] memory stab_bst_path = new address[](2);
        stab_bst_path[0] = _usdStable;
        stab_bst_path[1] = address(this);
        uint256 usdAmnt_ = _normalizeStableAmnt(decimals(), _usdAmnt, USD_STABLE_DECIMALS[_usdStable]);
        (uint8 rtrIdx, uint256 bst_amnt) = _best_swap_v2_router_idx_quote(stab_bst_path, usdAmnt_, USWAP_V2_ROUTERS);
        return _uint64_from_uint256(bst_amnt); 
    }
    function _perc_of_uint64(uint8 _perc, uint64 _num) private pure returns (uint64) {
        require(_perc <= 100, 'err: invalid percent');
        uint32 aux_perc = uint32(_perc) * 100;
        uint64 result = (_num * uint64(aux_perc)) / 10000; // chatGPT equation
        return result;
    }
    function _uint64_from_uint256(uint256 value) private pure returns (uint64) {
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
        stab_amnt_out = _normalizeStableAmnt(USD_STABLE_DECIMALS[_usdStable], stab_amnt_out, decimals());
        return stab_amnt_out;
    }
    function _exeSwapStableForBst(uint256 _usdAmnt, address _usdStable, address[] memory _stab_bst_path) private returns (uint256) {
        uint256 usdAmnt_ = _normalizeStableAmnt(decimals(), _usdAmnt, USD_STABLE_DECIMALS[_usdStable]);
        (uint8 rtrIdx, uint256 bst_amnt) = _best_swap_v2_router_idx_quote(_stab_bst_path, usdAmnt_, USWAP_V2_ROUTERS);
        uint256 bst_amnt_out = _swap_v2_wrap(_stab_bst_path, USWAP_V2_ROUTERS[rtrIdx], usdAmnt_, address(this), false); // true = fromETH
        return bst_amnt_out;
    }
    function _addAddressToArraySafe(address _addr, address[] memory _arr, bool _safe) private pure returns (address[] memory) {
        if (_addr == address(0)) { return _arr; }

        // safe = remove first (no duplicates)
        if (_safe) { _arr = _remAddressFromArray(_addr, _arr); }

        // perform add to memory array type w/ static size
        address[] memory _ret = new address[](_arr.length+1);
        for (uint i=0; i < _arr.length;) { _ret[i] = _arr[i]; unchecked {i++;}}
        _ret[_ret.length-1] = _addr;
        return _ret;
    }
    function _remAddressFromArray(address _addr, address[] memory _arr) private pure returns (address[] memory) {
        if (_addr == address(0) || _arr.length == 0) { return _arr; }
        
        // NOTE: remove algorithm does NOT maintain order & only removes first occurance
        for (uint i = 0; i < _arr.length;) {
            if (_addr == _arr[i]) {
                _arr[i] = _arr[_arr.length - 1];
                assembly { // reduce memory _arr length by 1 (simulate pop)
                    mstore(_arr, sub(mload(_arr), 1))
                }
                return _arr;
            }

            unchecked {i++;}
        }
        return _arr;
    }
    function _normalizeStableAmnt(uint8 _fromDecimals, uint256 _usdAmnt, uint8 _toDecimals) private pure returns (uint256) {
        require(_fromDecimals > 0 && _toDecimals > 0, 'err: invalid _from|toDecimals');
        if (_fromDecimals == _toDecimals) {
            return _usdAmnt;
        } else {
            if (_fromDecimals > _toDecimals) { // _fromDecimals has more 0's
                uint256 scalingFactor = 10 ** (_fromDecimals - _toDecimals); // get the diff
                return _usdAmnt / scalingFactor; // decrease # of 0's in _usdAmnt
            }
            else { // _fromDecimals has less 0's
                uint256 scalingFactor = 10 ** (_toDecimals - _fromDecimals); // get the diff
                return _usdAmnt * scalingFactor; // increase # of 0's in _usdAmnt
            }
        }
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

    /* -------------------------------------------------------- */
    /* PRIVATE - DEX SUPPORT                                    */
    /* -------------------------------------------------------- */
    // NOTE: *WARNING* _stables could have duplicates (from 'whitelistStables' set by keeper)
    function _getStableTokenLowMarketValue(address[] memory _stables, address[] memory _routers) internal view returns (address) {
        // traverse _stables & select stable w/ the lowest market value
        uint256 curr_high_tok_val = 0;
        address curr_low_val_stable = address(0x0);
        for (uint8 i=0; i < _stables.length;) {
            address stable_addr = _stables[i];
            if (stable_addr == address(0)) { continue; }

            // get quote for this stable (traverses 'uswapV2routers')
            //  looking for the stable that returns the most when swapped 'from' WPLS
            //  the more USD stable received for 1 WPLS ~= the less overall market value that stable has
            address[] memory wpls_stab_path = new address[](2);
            wpls_stab_path[0] = TOK_WPLS;
            wpls_stab_path[1] = stable_addr;
            (uint8 rtrIdx, uint256 tok_val) = _best_swap_v2_router_idx_quote(wpls_stab_path, 1 * 10**18, _routers);
            if (tok_val >= curr_high_tok_val) {
                curr_high_tok_val = tok_val;
                curr_low_val_stable = stable_addr;
            }

            // NOTE: unchecked, never more than 255 (_stables)
            unchecked {
                i++;
            }
        }
        return curr_low_val_stable;
    }

    // NOTE: *WARNING* _stables could have duplicates (from 'whitelistStables' set by keeper)
    function _getStableTokenHighMarketValue(address[] memory _stables, address[] memory _routers) internal view returns (address) {
        // traverse _stables & select stable w/ the highest market value
        uint256 curr_low_tok_val = 0;
        address curr_high_val_stable = address(0x0);
        for (uint8 i=0; i < _stables.length;) {
            address stable_addr = _stables[i];
            if (stable_addr == address(0)) { continue; }

            // get quote for this stable (traverses 'uswapV2routers')
            //  looking for the stable that returns the least when swapped 'from' WPLS
            //  the less USD stable received for 1 WPLS ~= the more overall market value that stable has
            address[] memory wpls_stab_path = new address[](2);
            wpls_stab_path[0] = TOK_WPLS;
            wpls_stab_path[1] = stable_addr;
            (uint8 rtrIdx, uint256 tok_val) = _best_swap_v2_router_idx_quote(wpls_stab_path, 1 * 10**18, _routers);
            if (tok_val >= curr_low_tok_val) {
                curr_low_tok_val = tok_val;
                curr_high_val_stable = stable_addr;
            }

            // NOTE: unchecked, never more than 255 (_stables)
            unchecked {
                i++;
            }
        }
        return curr_high_val_stable;
    }

    // uniswap v2 protocol based: get router w/ best quote in 'uswapV2routers'
    function _best_swap_v2_router_idx_quote(address[] memory path, uint256 amount, address[] memory _routers) internal view returns (uint8, uint256) {
        uint8 currHighIdx = 37;
        uint256 currHigh = 0;
        for (uint8 i = 0; i < _routers.length;) {
            uint256[] memory amountsOut = IUniswapV2Router02(_routers[i]).getAmountsOut(amount, path); // quote swap
            if (amountsOut[amountsOut.length-1] > currHigh) {
                currHigh = amountsOut[amountsOut.length-1];
                currHighIdx = i;
            }

            // NOTE: unchecked, never more than 255 (_routers)
            unchecked {
                i++;
            }
        }

        return (currHighIdx, currHigh);
    }

    // uniwswap v2 protocol based: get quote and execute swap
    function _swap_v2_wrap(address[] memory path, address router, uint256 amntIn, address outReceiver, bool fromETH) internal returns (uint256) {
        require(path.length >= 2, 'err: path.length :/');
        uint256[] memory amountsOut = IUniswapV2Router02(router).getAmountsOut(amntIn, path); // quote swap
        uint256 amntOut = _swap_v2(router, path, amntIn, amountsOut[amountsOut.length -1], outReceiver, fromETH); // approve & execute swap
                
        // verifiy new balance of token received
        uint256 new_bal = IERC20(path[path.length -1]).balanceOf(address(this));
        require(new_bal >= amntOut, "err: balance low :{");
        
        return amntOut;
    }
    
    // v2: solidlycom, kyberswap, pancakeswap, sushiswap, uniswap v2, pulsex v1|v2, 9inch
    function _swap_v2(address router, address[] memory path, uint256 amntIn, uint256 amntOutMin, address outReceiver, bool fromETH) private returns (uint256) {
        // emit logRFL(address(this), msg.sender, "logRFL 6a");
        IUniswapV2Router02 swapRouter = IUniswapV2Router02(router);
        
        // emit logRFL(address(this), msg.sender, "logRFL 6b");
        IERC20(address(path[0])).approve(address(swapRouter), amntIn);
        uint deadline = block.timestamp + 300;
        uint[] memory amntOut;
        // emit logRFL(address(this), msg.sender, "logRFL 6c");
        if (fromETH) {
            amntOut = swapRouter.swapExactETHForTokens{value: amntIn}(
                            amntOutMin,
                            path, //address[] calldata path,
                            outReceiver, // to
                            deadline
                        );
        } else {
            amntOut = swapRouter.swapExactTokensForTokens(
                            amntIn,
                            amntOutMin,
                            path, //address[] calldata path,
                            outReceiver, //  The address that will receive the output tokens after the swap. 
                            deadline
                        );
        }
        // emit logRFL(address(this), msg.sender, "logRFL 6d");
        return uint256(amntOut[amntOut.length - 1]); // idx 0=path[0].amntOut, 1=path[1].amntOut, etc.
    }
}
