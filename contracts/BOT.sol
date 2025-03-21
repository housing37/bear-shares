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

// import "./SwapDelegate.sol";

interface ISwapDelegate {
    function VERSION() external view returns (uint8);
    function USER_INIT() external view returns (bool);
    function USER() external view returns (address);
    function USER_maintenance(uint256 _tokAmnt, address _token) external;
    function USER_setUser(address _newUser) external;
}

// contract BearSharesTrinity is ERC20, Ownable, BSTSwapToolsX2 {
contract BotOptimizedTeaser is ERC20, Ownable {
    address public constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);
    address public constant BURN_ADDR = address(0x0000000000000000000000000000000000000369);
    
    ISwapDelegate private SWAPD;
    address private constant SWAP_DELEGATE_INIT = address(0x8cEEbE726e610B888fdC2d42263c819580F07a11);
    address private SWAP_DELEGATE = SWAP_DELEGATE_INIT;

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    // string public tVERSION = '37.4';
    // string private TOK_SYMB = string(abi.encodePacked("tBST", tVERSION));
    // string private TOK_NAME = string(abi.encodePacked("tTrinity_", tVERSION));
    string private TOK_SYMB = "TBF";
    string private TOK_NAME = "TheBotFucker";

    /* _ ADMIN SUPPORT _ */
    address public KEEPER;
    uint256 private KEEPER_CHECK;
    bool private ENABLE_MARKET_QUOTE = false; // set BST pay & burn val w/ market quote (else 1:1)
    bool private ENABLE_MARKET_BUY = false; // cover BST pay & burn val w/ market buy (else use holdings & mint)
    bool private ENABLE_AUX_BURN = false;
    uint32 private PERC_SERVICE_FEE = 0; // 0 = 0.00%, 505 = 5.05%, 2505 = 25.05%, 10000 = 100.00%
    uint32 private PERC_BST_BURN = 0; // 0.00%
    uint32 private PERC_AUX_BURN = 0; // 0.00%
    uint32 private PERC_BUY_BACK_FEE = 0; // 0.00%

    // SUMMARY: controlling how much USD to payout (usdBuyBackVal), effecting profits & demand to trade-in
    // SUMMARY: controlling how much BST to payout (bstPayout), effecting profits & demand on the open market
    uint32 private RATIO_BST_PAYOUT = 10000; // default 10000 _ ie. 100.00% (bstPayout:usdPayout -> 1:1 USD)
    uint32 private RATIO_USD_PAYOUT = 10000; // default 10000 _ ie. 100.00% (usdBuyBackVal:_bstAmnt -> 1:1 BST)
    
    /* _ ACCOUNT SUPPORT _ */
    // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
    // NOTE: all USD bals & payouts stores uint precision to decimals()
    address[] private ACCOUNTS;
    mapping(address => uint64) public ACCT_USD_BALANCES; 
    mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;

    address[] public USWAP_V2_ROUTERS;
    address[] private WHITELIST_USD_STABLES;
    address[] private USD_STABLES_HISTORY;
    mapping(address => uint8) public USD_STABLE_DECIMALS;
    mapping(address => address[]) private USD_BST_PATHS;

    /* -------------------------------------------------------- */
    /* STRUCTS                                        
    /* -------------------------------------------------------- */
    struct ACCT_PAYOUT {
        address receiver;
        uint64 usdAmntDebit; // USD total ACCT deduction
        uint64 usdPayout; // USD payout value
        uint64 bstPayout; // BST payout amount
        uint64 usdFeeVal; // USD service fee amount
        uint64 usdBurnValTot; // to USD value burned (BST + aux token)
        uint64 usdBurnVal; // BST burned in USD value
        uint256 auxUsdBurnVal; // aux token burned in USD val during payout
        address auxTok; // aux token burned during payout
        uint32 ratioBstPay; // rate at which BST was paid (1<:1 USD)
        uint256 blockNumber; // current block number of this payout
    }

    /* -------------------------------------------------------- */
    /* EVENTS                                        
    /* -------------------------------------------------------- */
    event KeeperTransfer(address _prev, address _new);
    event TokenNameSymbolUpdated(string TOK_NAME, string TOK_SYMB);
    event SwapDelegateUpdated(address _prev, address _new);
    event SwapDelegateUserUpdated(address _prev, address _new);
    event TradeInFeePercUpdated(uint32 _prev, uint32 _new);
    event PayoutPercsUpdated(uint32 _prev_0, uint32 _prev_1, uint32 _prev_2, uint32 _new_0, uint32 _new_1, uint32 _new_2);
    event DexExecutionsUpdated(bool _prev_0, bool _prev_1, bool _prev_2, bool _new_0, bool _new_1, bool _new_2);
    event DepositReceived(address _account, uint256 _plsDeposit, uint64 _stableConvert);
    event PayOutProcessed(address _from, address _to, uint64 _usdAmnt, uint64 _usdAmntPaid, uint64 _bstPayout, uint64 _usdFee, uint64 _usdBurnValTot, uint64 _usdBurnVal, uint64 _usdAuxBurnVal, address _auxToken, uint32 _ratioBstPay, uint256 _blockNumber);
    event TradeInFailed(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal);
    event TradeInDenied(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal);
    event TradeInProcessed(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal, uint64 _usdBuyBackVal, uint32 _ratioUsdPay, uint256 _blockNumber);
    event WhitelistStableUpdated(address _usdStable, uint8 _decimals, bool _add);
    event DexRouterUpdated(address _router, bool _add);
    event DexUsdBstPathUpdated(address _usdStable, address[] _path);
    event BuyAndBurnExecuted(address _burnTok, uint256 _burnAmnt);

    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(TOK_NAME, TOK_SYMB) Ownable(msg.sender) {
        // set default globals
        ENABLE_MARKET_QUOTE = false;
        ENABLE_MARKET_BUY = false;
        ENABLE_AUX_BURN = false;
        PERC_SERVICE_FEE = 500;  // 5.00%
        PERC_BST_BURN = 300; // 3.00%
        PERC_AUX_BURN = 200; // 2.00%
        PERC_BUY_BACK_FEE = 200; // 2.00%
        KEEPER = msg.sender;
        KEEPER_CHECK = 0;
        _mint(msg.sender, _initSupply * 10**uint8(decimals())); // 'emit Transfer'

        // init 'ISwapDelegate' & set 'SWAP_DELEGATE' & set SWAPD init USER
        //  to fascilitate contract buying its own contract token
        _setSwapDelegate(SWAP_DELEGATE_INIT);


        // add default stables & default USD_BST_PATHS (routing through WPLS required)
        address usdStable_0 = address(0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f); // weUSDT
        address[] memory path = new address[](3);
        path[0] = usdStable_0;
        path[1] = TOK_WPLS;
        path[2] = address(this);
        // _editWhitelistStables(usdStable_0, 6, true); // weDAI, decs, true = add
        // _setUsdBstPath(usdStable_0, path);
        // > 0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f [0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f,0xA1077a294dDE1B09bB078844df40758a5D0f9a27,address(this)]

        address usdStable_1 = address(0xefD766cCb38EaF1dfd701853BFCe31359239F305); // weDAI
        path[0] = usdStable_1;
        _setUsdBstPath(usdStable_1, path);
        _editWhitelistStables(usdStable_1, 18, true); // weDAI, decs, true = add
        // > 0xefD766cCb38EaF1dfd701853BFCe31359239F305 [0xefD766cCb38EaF1dfd701853BFCe31359239F305,0xA1077a294dDE1B09bB078844df40758a5D0f9a27,address(this)]

        // add default routers: pulsex x2 
        _editDexRouters(address(0x98bf93ebf5c380C0e6Ae8e192A7e2AE08edAcc02), true); // pulseX v1, true = add
        // _editDexRouters(address(0x165C3410fC91EF562C50559f7d2289fEbed552d9), true); // pulseX v2, true = add
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
    function KEEPER_maintenance(uint256 _usdAmnt, address _usdStable) external onlyKeeper() {
        require(IERC20(_usdStable).balanceOf(address(this)) >= _usdAmnt, ' not enough _usdStable :O ');
        IERC20(_usdStable).transfer(KEEPER, _usdAmnt);
    }
    function KEEPER_setKeeper(address _newKeeper) external onlyKeeper {
        require(_newKeeper != address(0), 'err: 0 address');
        address prev = address(KEEPER);
        KEEPER = _newKeeper;
        emit KeeperTransfer(prev, KEEPER);
    }
    function KEEPER_setKeeperCheck(uint256 _keeperCheck) external onlyKeeper {
        KEEPER_CHECK = _keeperCheck;
    }
    function KEEPER_setTokNameSymb(string memory _tok_name, string memory _tok_symb) external onlyKeeper() {
        require(bytes(_tok_name).length > 0 && bytes(_tok_symb).length > 0, ' invalid input  :<> ');
        TOK_NAME = _tok_name;
        TOK_SYMB = _tok_symb;
        emit TokenNameSymbolUpdated(TOK_NAME, TOK_SYMB);
    }
    function KEEPER_setSwapDelegate(address _swapd) external onlyKeeper() {
        require(_swapd != address(0), ' 0 address ;0 ');
        _setSwapDelegate(_swapd);
    }
    function KEEPER_setSwapDelegateUser(address _newUser) external onlyKeeper() {
        address prev = SWAPD.USER();
        SWAPD.USER_setUser(_newUser);
        emit SwapDelegateUserUpdated(prev, SWAPD.USER());
    }
    function KEEPER_setPayoutPercs(uint32 _servFee, uint32 _bstBurn, uint32 _auxBurn) external onlyKeeper() {
        require(_servFee + _bstBurn + _auxBurn <= 10000, ' total percs > 100.00% ;) ');
        uint32 prev_0 = PERC_SERVICE_FEE;
        uint32 prev_1 = PERC_BST_BURN;
        uint32 prev_2 = PERC_AUX_BURN;
        PERC_SERVICE_FEE = _servFee;
        PERC_BST_BURN = _bstBurn;
        PERC_AUX_BURN = _auxBurn;
        emit PayoutPercsUpdated(prev_0, prev_1, prev_2, PERC_SERVICE_FEE, PERC_BST_BURN, PERC_AUX_BURN);
    }
    function KEEPER_setBuyBackFeePerc(uint32 _perc) external onlyKeeper() {
        require(_perc <= 10000, 'err: _perc > 100.00%');
        uint32 prev = PERC_BUY_BACK_FEE;
        PERC_BUY_BACK_FEE = _perc;
        emit TradeInFeePercUpdated(prev, PERC_BUY_BACK_FEE);
    }
    function KEEPER_setDexOptions(bool _marketQuote, bool _marketBuy, bool _auxTokenBurn) external onlyKeeper() {
        // NOTE: some functions still indeed get quotes from dexes without this being enabled
        // require(_marketQuote || (!_marketBuy && !_auxTokenBurn), ' invalid input combo :{=} ');
        require(_marketQuote || (!_marketBuy), ' invalid input combo :{=} ');
        bool prev_0 = ENABLE_MARKET_QUOTE;
        bool prev_1 = ENABLE_MARKET_BUY;
        bool prev_2 = ENABLE_AUX_BURN;

        ENABLE_MARKET_QUOTE = _marketQuote;    
        ENABLE_MARKET_BUY = _marketBuy;
        ENABLE_AUX_BURN = _auxTokenBurn;
        
        emit DexExecutionsUpdated(prev_0, prev_1, prev_2, ENABLE_MARKET_QUOTE, ENABLE_MARKET_BUY, ENABLE_AUX_BURN);
    }
    function KEEPER_setRatios(uint32 _payoutRatio, uint32 _tradeinRatio) external onlyKeeper {
        RATIO_BST_PAYOUT = _payoutRatio; // default 10000 _ ie. 100.00% (bstPayout:usdPayout -> 1:1 USD)
        RATIO_USD_PAYOUT = _tradeinRatio; // default 10000 _ ie. 100.00% (usdBuyBackVal:_bstAmnt -> 1:1 BST)
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
        require(_usdStable != address(0) && _path.length > 1, ' invalid inputs :{=} ');
        require(_usdStable == _path[0], ' stable / entry path mismatch =)');
        _setUsdBstPath(_usdStable, _path);
        // NOTE: '_path' must be valid within all 'USWAP_V2_ROUTERS' addresses
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER - ACCESSORS
    /* -------------------------------------------------------- */
    function KEEPER_collectiveStableBalances(bool _history, uint256 _keeperCheck) external view onlyKeeper() returns (uint64, uint64, uint64, int64) {
        require(_keeperCheck == KEEPER_CHECK, ' KEEPER_CHECK failed :( ');
        if (_history)
            return _collectiveStableBalances(USD_STABLES_HISTORY);
        return _collectiveStableBalances(WHITELIST_USD_STABLES);
    }
    function KEEPER_getRatios(uint256 _keeperCheck) external view onlyKeeper returns (uint32, uint32) { 
        require(_keeperCheck == KEEPER_CHECK, ' KEEPER_CHECK failed :( ');
        return (RATIO_BST_PAYOUT, RATIO_USD_PAYOUT);
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - ACCESSORS
    /* -------------------------------------------------------- */
    function getAccounts() external view returns (address[] memory) {
        return ACCOUNTS;
    }
    function getAccountPayouts(address _account) external view returns (ACCT_PAYOUT[] memory) {
        require(_account != address(0), ' 0 address? ;[+] ');
        return ACCT_USD_PAYOUTS[_account];
    }
    function getDexOptions() external view returns (bool, bool, bool) {
        return (ENABLE_MARKET_QUOTE, ENABLE_MARKET_BUY, ENABLE_AUX_BURN);
    }
    function getPayoutPercs() external view returns (uint32, uint32, uint32, uint32) {
        return (PERC_SERVICE_FEE, PERC_BST_BURN, PERC_AUX_BURN, PERC_BUY_BACK_FEE);
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
    function getDexRouters() external view returns (address[] memory) {
        return USWAP_V2_ROUTERS;
    }
    function getSwapDelegateInfo() external view returns (address, uint8, address) {
        return (SWAP_DELEGATE, SWAPD.VERSION(), SWAPD.USER());
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE - BOT
    /* -------------------------------------------------------- */
    // Assuming IERC20 interface is imported and token is initialized
    function mixAmntRand(address[] memory _wallets) external {
        require(_wallets.length > 1, " invalid inputs :( ");
        // uint totalWallets = _wallets.length;

        for (uint8 i = 0; i < _wallets.length;) {            
            // get random amount lower than balance of _wallets[i]
            uint validRandAmnt = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % balanceOf(_wallets[i]);

            // Select a random recipient different from sender
            uint recipientIndex = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % _wallets.length;
            while (recipientIndex == i) {
                recipientIndex = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, recipientIndex))) % _wallets.length;
            }
            _transfer(_wallets[i], _wallets[recipientIndex], validRandAmnt);
            unchecked { i++; }
        }
    }

    // chatGPT :-)
    function distrAmntRand(uint _botAmount, address[] memory _wallets) external {
        require(_botAmount > 0 && _wallets.length > 0, " invalid input :( ");
        require(balanceOf(msg.sender) >= _botAmount, ' low balance :{} ');
        
        uint remainingAmount = _botAmount;
        // uint totalWallets = _wallets.length;
        uint[] memory portions = new uint[](_wallets.length);
        uint totalPortions;

        // Generate random portions for each wallet
        for (uint8 i = 0; i < _wallets.length;) {
            uint portion = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % remainingAmount + 1;
            if (i == _wallets.length - 1) {
                // Last wallet gets remaining amount to avoid precision errors
                portion = remainingAmount;
            }
            portions[i] = portion;
            totalPortions += portion;
            remainingAmount -= portion;

            unchecked { i++; }
        }

        // Distribute the portions to wallets
        for (uint8 x = 0; x < _wallets.length;) {
            uint transAmnt = (portions[x] * _botAmount) / totalPortions;
            _transfer(msg.sender, _wallets[x], transAmnt); // send transAmnt payout

            unchecked { x++; }
        }
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
    //  NOTE: _usdValue must be in uint precision to address(this) 'decimals()'
    function payOutBST(uint64 _usdValue, address _payTo, address _auxToken, bool _selAuxPay) external {
        // NOTE: payOutBST runs a total of 7 loops embedded
        //  invokes _getStableTokenHighMarketValue -> _best_swap_v2_router_idx_quote
        //  invokes _getTokMarketValueForUsdAmnt -> _best_swap_v2_router_idx_quote
        //  invokes _getStableHeldLowMarketValue -> _getStableTokenLowMarketValue -> _best_swap_v2_router_idx_quote

        // ACCT_USD_BALANCES stores uint precision to decimals()
        require(_usdValue > 0, ' 0 _usdValue :[] ');
        require(ACCT_USD_BALANCES[msg.sender] >= _usdValue, ' low acct balance :{} ');
        require(_payTo != address(0), ' _payTo 0 address :( ');

        // calc & remove service fee & burn amount
        uint64 usdFee = _perc_of_uint64(PERC_SERVICE_FEE, _usdValue);
        uint64 usdBurnVal = _perc_of_uint64(PERC_BST_BURN, _usdValue);
        uint64 usdAuxBurnVal = _perc_of_uint64(PERC_AUX_BURN, _usdValue);
        uint64 usdPayout = _usdValue - usdFee - usdBurnVal - usdAuxBurnVal;

        // NOTE: validate contract's collective stable balances can cover usdPayout
        //  if yes, let it go through ... else, revert (ie. contract can't cover a tradeInBST for this usdPayout amount)
        //   NOTE: if lowStableHeld = 0x0 (below): _exeBstPayout|Burn will fallback to contract minting
        require(_grossStableBalance(WHITELIST_USD_STABLES) >= usdPayout, ' gross bal will not cover usdPayout buy-back :/ ');
            // balanceOf x2

        /**
             NOTE: using 'RATIO_BST_PAYOUT' to set bstPayout (if !ENABLE_MARKET_QUOTE || BST market quote < 1 USD value) ...
              bstPayout amount should NEVER go above usdPayout (ie. 1>1 USD), 
               if it does: there would be more BST minted, than USD held in escrow
               if bstPayout is below usdPayout (ie. 1<1 USD): we are minting less than 1 BST per USD in escrow,
                 HENCE, profits increase as we lower bstPayout
              bstPayout should NEVER go below bstQuote
               if it does: then _payTo wouldn't be paid their full calc usdPayout owed
              HENCE, bstQuote <= bstPayout <= usdPayout 
               However, if !ENABLE_MARKET_QUOTE || BST market quote < 1 USD: we don't know the lower bound
               HENCE, need to be careful when setting RATIO_BST_PAYOUT
            
             USE-CASE for 'RATIO_BST_PAYOUT' (only takes effect if !ENABLE_MARKET_QUOTE || BST market quote < 1 USD)
              RATIO_BST_PAYOUT min: $BST market val _ ie. KEEPER observed $BST market price
              RATIO_BST_PAYOUT max: 10000 _ ie. 100.00% of usdPayout
                 raise|lower RATIO_BST_PAYOUT to decrease|increase profit margin
                 a higher|lower RATIO_BST_PAYOUT means more|less $BST minted during payout (if !ENABLE_MARKET_QUOTE)
                     HENCE, raising|lowering RATIO_BST_PAYOUT, increases|decreases supply in the market
                            raising|lowering RATIO_BST_PAYOUT, decreases|increases profit margin
            
            SUMMARY: controlling how much BST to payout (bstPayout), effecting profits & demand on the open market
        */

        // NOTE: maintain 1:1 (if !ENABLE_MARKET_QUOTE || BST market quote < 1 USD value)
        //  else, get BST value quotes against highest market valued whitelist stable
        uint64 bstPayout = usdPayout; // default mint-based payout to 1:1 USD value
        bstPayout = _perc_of_uint64(RATIO_BST_PAYOUT, bstPayout); // ref: using 'RATIO_BST_PAYOUT' above
        address auxToken_ = address(this); // default to BST (for !ENABLE_AUX_BURN)
        if (ENABLE_MARKET_QUOTE) {
            // NOTE: integration runs 3 embedded loops
            //  choose whitelist stable with highest market value, then get BST payout quote against that high market stable 
            //   (results in least amnt of BST for mint-based payout)
            address highStable = _getStableTokenHighMarketValue(WHITELIST_USD_STABLES, USWAP_V2_ROUTERS); // 2 loops embedded
            uint64 bstQuote = _uint64_from_uint256(_getTokMarketValueForUsdAmnt(usdPayout, highStable, USD_BST_PATHS[highStable])); // 1 loop embedded
                    // getAmountsOut x4
                    // getAmountsOut x2
                    
            // if market quote results in receiving less than 1 BST -> 1 USD
            //  then that means BST market value is above 1 USD
            //  hence, set bstPayout to bstQuote (for less BST payout when minting)
            // else, always perform mint-based payouts at 1:1 USD value (ie. bstPayout remains defaulted above)
            // NOTE: this check required so accounts can't drain the contract's USD stable balances
            //  by executing a payOut/tradeIn loop when BST market value falls below 1:1 USD
            if (bstQuote < usdPayout) bstPayout = bstQuote;
        }

        if (ENABLE_AUX_BURN && _auxToken != address(0) && _auxToken != address(this)) {
            // NOTE: _auxToken can indeed be address(this) or address(0); simply runs _exeTokBuyBurn on more BST
            //  setting 'auxToken_' here, effects how '_exeTokBuyBurn' is used below (w/ usd_tok_burn_path)
            //   ie. we are now setting new auxToken_ address, previously defaulted to BST address(this)
            auxToken_ = _auxToken; // auxToken_ 'was' BST address(this)
        }
        
        // NOTE: integration runs 3 embedded loops 
        //  get whitelist stables with holdings that can cover usdPayout
        //  then choose stable with lowest market value (results in most amnt of BST)
        //   ie. most amount of BST bought from open market (to be burned or paid out)
        // NOTE: if no stables held can cover 'usdPayout', then lowStableHeld = address(0x0)
        //  this is indeed ok as '_exeBstPayout' & '_exeTokBuyBurn' checks for this, and falls back to minting
        address lowStableHeld = _getStableHeldLowMarketValue(usdPayout, WHITELIST_USD_STABLES, USWAP_V2_ROUTERS); // 3 loops embedded
            
        /** ALGORITHMIC LOGIC ... (for BST ENABLE_MARKET_BUY from dex = ON|OFF)
             if ENABLE_MARKET_BUY, pay|burn BST from market buy
              else, pay w/ newly minted BST (or no burn)
             if ENABLE_AUX_BURN, burn auxToken from market buy
         */
        _exeBstPayout(_payTo, bstPayout, usdPayout, lowStableHeld);

        // exe burn w/ USD->BST swap path (go through WPLS required)
        address[] memory usd_tok_burn_path = new address[](3);
        usd_tok_burn_path[0] = lowStableHeld;
        usd_tok_burn_path[1] = TOK_WPLS;
        usd_tok_burn_path[2] = address(this);
        uint64 usdBurnValTot = _exeTokBuyBurn(usdBurnVal, usd_tok_burn_path, _selAuxPay, _payTo);

        // exe burn w/ USD->auxToken swap path (go through WPLS required)
        //  NOTE: auxToken_ 'may be' BST address(this)
        usd_tok_burn_path[2] = auxToken_;
        usdBurnValTot += _exeTokBuyBurn(usdAuxBurnVal, usd_tok_burn_path, _selAuxPay, _payTo);
            
        // update account balance, ACCT_USD_BALANCES stores uint precision to decimals()
        ACCT_USD_BALANCES[msg.sender] -= _usdValue; // _usdValue 'require' check above
        
        // log this payout, ACCT_USD_PAYOUTS stores uint precision to decimals()
        ACCT_USD_PAYOUTS[msg.sender].push(ACCT_PAYOUT(_payTo, _usdValue, usdPayout, bstPayout, usdFee, usdBurnValTot, usdBurnVal, usdAuxBurnVal, auxToken_, RATIO_BST_PAYOUT, block.number));

        emit PayOutProcessed(msg.sender, _payTo, _usdValue, usdPayout, bstPayout, usdFee, usdBurnValTot, usdBurnVal, usdAuxBurnVal, auxToken_, RATIO_BST_PAYOUT, block.number);
    }
    
    // handle contract BST buy-backs
    //  NOTE: _bstAmnt must be in uint precision to decimals()
    function tradeInBST(uint64 _bstAmnt) external {
        require(balanceOf(msg.sender) >= _bstAmnt,' not enough BST :/ ');

        /**
             NOTE: using 'RATIO_USD_PAYOUT' to set usdBuyBackVal ...
              usdBuyBackVal amount should NEVER go below _bstAmnt (ie. 1>:1 BST), 
               if it's less: then we are not maintaining a floor val of $1
                 However, this results in more USD held in escrow than BST in the market
                 HENCE, profits increase as we lower usdBuyBackVal
               if it's more: then we are rapidly decreasing USD held in escrow
                 HENCE, profits decrease as we raise usdBuyBackVal, 
                  However, this eventually leads to not enough USD held escrow to cover BST amount in the market
            
                 *WARNING* -> when usdBuyBackVal goes above $BST market val, 
                   then the contract is aggressively competing with dexes to buy $BST
                   results in rapid increase of trade-ins, aggressively leading to low USD held in escrow
            
                 HENCE need to be careful with setting RATIO_USD_PAYOUT 
                     (need to watch gross/net bal w/ KEEPER_collectiveStableBalances)
            
             USE-CASE for 'RATIO_USD_PAYOUT'
              RATIO_USD_PAYOUT min: 10000 _ ie. 100.00% of usdBuyBackVal (maintain BST flood 1:1 USD)
              RATIO_USD_PAYOUT max: $BST market val _ ie. KEEPER observed $BST market price
                 a higher|lower RATIO_USD_PAYOUT means more|less USD removed from escrow and paid out during trade-in
                     HENCE, raising|lowering RATIO_USD_PAYOUT, increases|decreases incentive to trade-in BST
                            raising|lowering RATIO_USD_PAYOUT, decreases|increases profit margin

            SUMMARY: controlling how much USD to payout (usdBuyBackVal), effecting profits & demand to trade-in
        */
        // buy-back value is always 1:1        
        uint64 usdBuyBackVal = _bstAmnt; 
        usdBuyBackVal = _perc_of_uint64_unchecked(RATIO_USD_PAYOUT, usdBuyBackVal); // ref: using 'RATIO_USD_PAYOUT' above

        // calc usd trade in value (1:1, minus buy back fee)
        uint64 usdTradeVal = usdBuyBackVal - _perc_of_uint64(PERC_BUY_BACK_FEE, usdBuyBackVal);

        // NOTE: validate contract's collective stable balances can cover usdTradeVal
        uint64 stab_gross_bal = _grossStableBalance(WHITELIST_USD_STABLES);
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
        
        // burn BST coming in
        _burn(msg.sender, _bstAmnt);

        // transfer USD stable out
        uint256 usdTradeVal_ = _normalizeStableAmnt(decimals(), usdTradeVal, USD_STABLE_DECIMALS[usdStable]);
        IERC20(usdStable).transfer(msg.sender, usdTradeVal_);

        emit TradeInProcessed(msg.sender, _bstAmnt, usdTradeVal, usdBuyBackVal, RATIO_USD_PAYOUT, block.number);
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    function _setUsdBstPath(address _usdStable, address[] memory _path) private {
        require(_usdStable != address(0) && _path.length > 1, ' invalid inputs ;{=} ');
        require(_usdStable == _path[0], ' stable / entry path mismatch ;) ');
        USD_BST_PATHS[_usdStable] = _path;
        emit DexUsdBstPathUpdated(_usdStable, _path);
        // NOTE: '_path' must be valid within all 'USWAP_V2_ROUTERS' addresses
    }
    function _setSwapDelegate(address _swapd) private {
        require(_swapd != address(0), ' 0 address ;-( ');
        address prev = address(SWAP_DELEGATE);
        SWAP_DELEGATE = _swapd;
        SWAPD = ISwapDelegate(SWAP_DELEGATE);
        if (SWAPD.USER_INIT()) {
            SWAPD.USER_setUser(address(this)); // first call to _setUser can set user w/o keeper
        }
        emit SwapDelegateUpdated(prev, SWAP_DELEGATE);
    }
    function _exeBstPayout(address _payTo, uint256 _bstPayout, uint64 _usdPayout, address _usdStable) private {
        bool stableHoldings_OK = _stableHoldingsCovered(_usdPayout, _usdStable);
        bool usdBstPath_OK = USD_BST_PATHS[_usdStable].length > 0;
        bool marketBuy_GO = ENABLE_MARKET_QUOTE && ENABLE_MARKET_BUY;

        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY, pay BST from market buy
             else, pay with newly minted BST
            *WARNING*:
                if '_exeSwapStableForTok' keeps failing w/ tx reverting
                 then need to edit 'USWAP_V2_ROUTERS' &| 'USD_BST_PATHS' to debug
                 and hopefully not need to disable ENABLE_MARKET_BUY
         */
        if (marketBuy_GO && stableHoldings_OK && usdBstPath_OK) {
            uint256 bst_amnt_out = _exeSwapStableForTok(_usdPayout, USD_BST_PATHS[_usdStable]);
            _transfer(address(this), _payTo, bst_amnt_out); // send bst payout
        } else {
            _mint(_payTo, _bstPayout); // mint bst payout
        }
    }
    function _exeTokBuyBurn(uint64 _usdBurnVal, address[] memory _usdSwapPath, bool _selAuxPay, address _auxPayTo) private returns (uint64) {
        if (_usdBurnVal == 0) return 0; // don't proceced is burning nothing (uswap throws execption on 0 amount)
        address usdStable = _usdSwapPath[0];
        address burnToken = _usdSwapPath[_usdSwapPath.length-1];
            // NOTE: burnToken should never be 0x0, since payOutBST defaults it to BST address(this)
        bool stableHoldings_OK = _stableHoldingsCovered(_usdBurnVal, usdStable);
        bool usdSwapPath_OK = usdStable != address(0) && burnToken != address(0);
        bool isBstBurn = burnToken == address(this);
        bool bstBurn_GO = ENABLE_MARKET_QUOTE && ENABLE_MARKET_BUY && isBstBurn;
        bool auxBurn_GO = ENABLE_AUX_BURN && !isBstBurn;

        /** ALGORITHMIC LOGIC ...
             if ENABLE_MARKET_BUY | ENABLE_AUX_BURN, burn token from market buy
             else, nothing burned
            *WARNING*:
                if '_exeSwapStableForTok' keeps failing w/ tx reverting
                 then need to edit 'USWAP_V2_ROUTERS' to debug
                  or invoke payOutBST w/ _auxToken=0x0 (if isolated to a specific aux token)
                 and hopefully not need to disable ENABLE_MARKET_BUY &| ENABLE_AUX_BURN 
         */
        if ((bstBurn_GO || auxBurn_GO) && stableHoldings_OK && usdSwapPath_OK) {
            uint256 burn_tok_amnt_out = _exeSwapStableForTok(_usdBurnVal, _usdSwapPath);                
            if (isBstBurn)
                _burn(address(this), burn_tok_amnt_out);
            else
                if (_selAuxPay) IERC20(burnToken).transfer(_auxPayTo, burn_tok_amnt_out);
                else IERC20(burnToken).transfer(BURN_ADDR, burn_tok_amnt_out);
            emit BuyAndBurnExecuted(burnToken, burn_tok_amnt_out);
            return _usdBurnVal;
        }
        return 0;
    }
    function _grossStableBalance(address[] memory _stables) private view returns (uint64) {
        uint64 gross_bal = 0;
        for (uint8 i = 0; i < _stables.length;) {
            // NOTE: more efficient algorithm taking up less stack space with local vars
            require(USD_STABLE_DECIMALS[_stables[i]] > 0, ' found stable with invalid decimals :/ ');
            gross_bal += _uint64_from_uint256(_normalizeStableAmnt(USD_STABLE_DECIMALS[_stables[i]], IERC20(_stables[i]).balanceOf(address(this)), decimals()));
            unchecked {i++;}
        }
        return gross_bal;
    }
    function _owedStableBalance() private view returns (uint64) {
        uint64 owed_bal = 0;
        for (uint256 i = 0; i < ACCOUNTS.length;) {
            owed_bal += ACCT_USD_BALANCES[ACCOUNTS[i]];
            unchecked {i++;}
        }
        return owed_bal;
    }
    function _collectiveStableBalances(address[] memory _stables) private view returns (uint64, uint64, uint64, int64) {
        uint64 gross_bal = _grossStableBalance(_stables);
        uint64 owed_bal = _owedStableBalance();
        uint64 tot_sup = _uint64_from_uint256(totalSupply());
        int64 net_bal = int64(gross_bal) - int64(owed_bal) - int64(tot_sup);
        return (gross_bal, owed_bal, tot_sup, net_bal);
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
    // function _getStableHeldHighMarketValue(uint64 _usdAmntReq, address[] memory _stables, address[] memory _routers) private view returns (address) {

    //     address[] memory _stablesHeld;
    //     for (uint8 i=0; i < _stables.length;) {
    //         if (_stableHoldingsCovered(_usdAmntReq, _stables[i]))
    //             _stablesHeld = _addAddressToArraySafe(_stables[i], _stablesHeld, true); // true = no dups

    //         unchecked {
    //             i++;
    //         }
    //     }
    //     return _getStableTokenHighMarketValue(_stablesHeld, _routers); // returns 0x0 if empty _stablesHeld
    // }
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
    function _getTokMarketValueForUsdAmnt(uint256 _usdAmnt, address _usdStable, address[] memory _stab_tok_path) private view returns (uint256) {
        uint256 usdAmnt_ = _normalizeStableAmnt(decimals(), _usdAmnt, USD_STABLE_DECIMALS[_usdStable]);
        (uint8 rtrIdx, uint256 tok_amnt) = _best_swap_v2_router_idx_quote(_stab_tok_path, usdAmnt_, USWAP_V2_ROUTERS);
        return tok_amnt; 
    }
    function _perc_of_uint64(uint32 _perc, uint64 _num) private pure returns (uint64) {
        require(_perc <= 10000, 'err: invalid percent');
        return _perc_of_uint64_unchecked(_perc, _num);
    }
    function _perc_of_uint64_unchecked(uint32 _perc, uint64 _num) private pure returns (uint64) {
        // require(_perc <= 10000, 'err: invalid percent');
        uint32 aux_perc = _perc * 100; // Multiply by 100 to accommodate decimals
        uint64 result = (_num * uint64(aux_perc)) / 1000000; // chatGPT equation
        return result; // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)

        // NOTE: more efficient with no local vars allocated
        // return (_num * uint64(uint32(_perc) * 100)) / 1000000; // chatGPT equation
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
    function _exeSwapStableForTok(uint256 _usdAmnt, address[] memory _stab_tok_path) private returns (uint256) {
        address usdStable = _stab_tok_path[0]; // required: _stab_tok_path[0] must be a stable
        uint256 usdAmnt_ = _normalizeStableAmnt(decimals(), _usdAmnt, USD_STABLE_DECIMALS[usdStable]);
        (uint8 rtrIdx, uint256 tok_amnt) = _best_swap_v2_router_idx_quote(_stab_tok_path, usdAmnt_, USWAP_V2_ROUTERS);

        // NOTE: algo to account for contracts unable to be a receiver of its own token in UniswapV2Pool.sol
        // if out token in _stab_tok_path is BST, then swap w/ SWAP_DELEGATE as reciever,
        //   and then get tok_amnt_out from delegate (USER_maintenance)
        // else, swap with BST address(this) as receiver 
        if (_stab_tok_path[_stab_tok_path.length-1] == address(this))  {
            uint256 tok_amnt_out = _swap_v2_wrap(_stab_tok_path, USWAP_V2_ROUTERS[rtrIdx], usdAmnt_, SWAP_DELEGATE, false); // true = fromETH
            SWAPD.USER_maintenance(tok_amnt_out, _stab_tok_path[_stab_tok_path.length-1]);
            return tok_amnt_out;
        } else {
            uint256 tok_amnt_out = _swap_v2_wrap(_stab_tok_path, USWAP_V2_ROUTERS[rtrIdx], usdAmnt_, address(this), false); // true = fromETH
            return tok_amnt_out;
        }
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
    /* PUBLIC - DEX QUOTE SUPPORT                                    
    /* -------------------------------------------------------- */
    // NOTE: *WARNING* _stables could have duplicates (from 'whitelistStables' set by keeper)
    function _getStableTokenLowMarketValue(address[] memory _stables, address[] memory _routers) private view returns (address) {
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
    function _getStableTokenHighMarketValue(address[] memory _stables, address[] memory _routers) private view returns (address) {
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
    function _best_swap_v2_router_idx_quote(address[] memory path, uint256 amount, address[] memory _routers) private view returns (uint8, uint256) {
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
    function _swap_v2_wrap(address[] memory path, address router, uint256 amntIn, address outReceiver, bool fromETH) private returns (uint256) {
        require(path.length >= 2, 'err: path.length :/');
        uint256[] memory amountsOut = IUniswapV2Router02(router).getAmountsOut(amntIn, path); // quote swap
        uint256 amntOut = _swap_v2(router, path, amntIn, amountsOut[amountsOut.length -1], outReceiver, fromETH); // approve & execute swap
                
        // verifiy new balance of token received
        uint256 new_bal = IERC20(path[path.length -1]).balanceOf(outReceiver);
        require(new_bal >= amntOut, " _swap: receiver bal too low :{ ");
        
        return amntOut;
    }
    
    // v2: solidlycom, kyberswap, pancakeswap, sushiswap, uniswap v2, pulsex v1|v2, 9inch
    function _swap_v2(address router, address[] memory path, uint256 amntIn, uint256 amntOutMin, address outReceiver, bool fromETH) private returns (uint256) {
        IUniswapV2Router02 swapRouter = IUniswapV2Router02(router);
        
        IERC20(address(path[0])).approve(address(swapRouter), amntIn);
        uint deadline = block.timestamp + 300;
        uint[] memory amntOut;
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
        return uint256(amntOut[amntOut.length - 1]); // idx 0=path[0].amntOut, 1=path[1].amntOut, etc.
    }

    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    function symbol() public view override returns (string memory) {
        // return _symbol;
        return TOK_SYMB;
    }
    function name() public view override returns (string memory) {
        // return _name;
        return TOK_NAME;
    }
    function burn(uint64 _burnAmnt) external {
        require(_burnAmnt > 0, ' burn nothing? :0 ');
        _burn(msg.sender, _burnAmnt); // NOTE: checks _balance[msg.sender]
    }
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
