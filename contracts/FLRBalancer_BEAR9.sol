// SPDX-License-Identifier: GPL-2.0-or-later
// house_102523 _ ref: https://docs.balancer.fi/reference/contracts/flash-loans.html#example-code
// house_050924 _ ref: .../git/defi-arb/contracts/BalancerFLR_test.sol
pragma solidity ^0.8.24;

// remix compile _ 
// import "@balancer-labs/v2-interfaces/contracts/vault/IVault.sol";
// import "@balancer-labs/v2-interfaces/contracts/vault/IFlashLoanRecipient.sol";
// import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol"; // deploy
// import '@uniswap/v2-core/contracts/interfaces/IUniswapV2Callee.sol';
// import '@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';
// import '@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol';


// local compile _ $ git clone https://github.com/balancer/balancer-v2-monorepo.git
import "./pkg-balancer/interfaces/contracts/vault/IVault.sol";
import "./pkg-balancer/interfaces/contracts/vault/IFlashLoanRecipient.sol";
import "./node_modules/@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Callee.sol';
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol';

contract FLRBalancerBEAR9 is IFlashLoanRecipient, IUniswapV2Callee {
    /* -------------------------------------------------------- */
    /* PUBLIC - GLOBALS                                          
    /* -------------------------------------------------------- */
    /* _ ADMIN SUPPORT _ */
    string public tVERSION = '0.0';
    address public KEEPER;
    address[] public USWAP_V2_ROUTERS;

    /* -------------------------------------------------------- */
    /* PRIVATE - FLASHLOANS SUPPORT                                 
    /* -------------------------------------------------------- */
    // ref: https://docs.balancer.fi/reference/contracts/flash-loans.html#example-code
    IVault private constant BALANCER_VAULT = IVault(0xBA12222222228d8Ba445958a75a0704d566BF2C8);
        // pWETH: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 -> 203658647860394116213752201 / 10**18 == 203658647.86039412 ~= $12,228.2445082
        // pUSDC: 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 -> 23937491402753 / 10**6 == 23937491.402753 ~= $74,767.781978741
        // pWBTC: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 -> 5994742939 / 10**8 == 59.94742939 ~= $13,208.5705829
        // pUSDT: 0xdAC17F958D2ee523a2206206994597C13D831ec7 -> 13296690613518 / 10**6 == 13296690.613518 ~= $39,213.741269448

        // pDOLA: 0x865377367054516e17014CcdED1e7d814EDC9ce4 -> 30614508079920854526255527 / 10**18 ~= $236.198849851
        // pAAVE: 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9 -> 2114928347848533872595 / 10**18 ~= $280.453860038

        // ERROR: LIQUIDITY < BALANCE
        // pBAL: 0xba100000625a3754423978a60c9317c58a424e3D ->  3946496821522180948639451 / 10**18 == 3946496.821522181 ~= $41,153.679623988
        // prETH: 0xae78736cd615f374d3085123a210448e74fc6393 -> 27843230642023975590639 / 10**18 ~= $8,067.713537987
    address private constant BURN_ADDR = address(0x0000000000000000000000000000000000000369);
    address private constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);
    
    address private constant TOK_ATROPA = address(0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6);
    address private constant TOK_TSFi = address(0x4243568Fa2bbad327ee36e06c16824cAd8B37819);
    address private constant TOK_R = address(0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622);
    address private constant TOK_BEAR9 = address(0x1f737F7994811fE994Fe72957C374e5cD5D5418A);

    address private constant TOK_pWBTC = address(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    address private constant TOK_pUSDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    address private constant TOK_pWETH = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    address private constant TOK_pUSDT = address(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    /* -------------------------------------------------------- */
    /* PRIVATE - TRADE REQUIREMENTS (to mint BEAR9)                                 
    /* -------------------------------------------------------- */
    // ref: .../git/atropa-kb-priv/_tools/calc_returns/req_bear9.py
    address private constant TOK_YING = address(0x271197EFe41073681577CdbBFD6Ee1DA259BAa3c); // # 100 籯 (YingContract) _ (ç±¯ = E7B1AF)
    address private constant TOK_YU = address(0x52a4682880E990ebed5309764C7BD29c4aE22deB); // # 500 유 (YuContract) _ (ì = EC9CA0)
    address private constant TOK_BUL8 = address(0x2959221675bdF0e59D0cC3dE834a998FA5fFb9F4); // # 9 ⑧ (Bullion8Contract) _ (â§ = E291A7)
    address private constant TOK_HAR = address(0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622); // # 1 ʁ (HarContract) _ (Ê = CA81)
    address private constant TOK_BEAR_OG = address(0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d); // # 1,111,111,111 TEDDY BEAR (TeddyBearContract) _ 'BEAR' OG

    /* -------------------------------------------------------- */
    /* STRUCTS                                        
    /* -------------------------------------------------------- */

    /* -------------------------------------------------------- */
    /* EVENTS                                        
    /* -------------------------------------------------------- */    
    event KeeperMaintenance(address _tokAddr, uint256 _tokAmnt);
    event KeeperWithdrawel(uint256 _natAmnt);
    event KeeperTransfered(address _prev, address _new);
    event FlashLoansRequested(IERC20[] _tokens, uint256[] _amounts, bytes _userData);
    event FlashLoansReceived(IERC20[] _tokens, uint256[] _amounts, uint256[] _feeAmounts, bytes _userData);
    event FlashLoansReturned(IERC20[] _tokens, uint256[] _amounts, uint256[] _feeAmounts, uint256[] _amountsOwed);
    event DexRouterUpdated(address _router, bool _add);

    mapping(address => address) public TOKEN_ROUTER_MAP;
    mapping(address => address[]) public TOKEN_SWAP_PATH_MAP;
    mapping(address => uint16) public TOKEN_REDUND_SWAP_CNT_MAP;
    function _editTokenRouterMap(address _token, address _router) private {
        TOKEN_ROUTER_MAP[_token] = _router;
    }
    function _editTokenSwapPathMap(address _token, address[] memory _path) private {
        TOKEN_SWAP_PATH_MAP[_token] = _path;
    }
    function _editTokenRedundSwapCntMap(address _token, uint16 _swapCnt) private {
        TOKEN_REDUND_SWAP_CNT_MAP[_token] = _swapCnt;
    }

    /* -------------------------------------------------------- */
    /* CONTRUCTOR                                        
    /* -------------------------------------------------------- */
    constructor() {
        KEEPER = msg.sender;
    }

    /* -------------------------------------------------------- */
    /* MODIFIERS                                                
    /* -------------------------------------------------------- */
    modifier onlyKeeper() {
        require(msg.sender == KEEPER, " !keeper :p ");
        _;
    }
    
    /* -------------------------------------------------------- */
    /* PUBLIC - KEEPER SUPPORT            
    /* -------------------------------------------------------- */
    //  NOTE: _tokAmnt must be in uint precision to _tokAddr.decimals()
    function KEEPER_maintenance(address _tokAddr, uint256 _tokAmnt) external onlyKeeper() {
        require(IERC20(_tokAddr).balanceOf(address(this)) >= _tokAmnt, ' not enough amount for token :O ');
        IERC20(_tokAddr).transfer(KEEPER, _tokAmnt);
        emit KeeperMaintenance(_tokAddr, _tokAmnt);
    }
    function KEEPER_withdraw(uint256 _natAmnt) external onlyKeeper {
        require(address(this).balance >= _natAmnt, " Insufficient native PLS balance :[ ");
        payable(KEEPER).transfer(_natAmnt); // cast to a 'payable' address to receive ETH
        emit KeeperWithdrawel(_natAmnt);
    }
    function KEEPER_setKeeper(address _newKeeper) external onlyKeeper {
        require(_newKeeper != address(0), ' invalid address :) ');
        address prev = address(KEEPER);
        KEEPER = _newKeeper;
        emit KeeperTransfered(prev, KEEPER);
    }
    function KEEPER_editDexRouters(address _router, bool _add) external onlyKeeper {
        require(_router != address(0x0), "0 address");
        _editDexRouters(_router, _add);
        emit DexRouterUpdated(_router, _add);
    }
    /* -------------------------------------------------------- */
    /* PUBLIC - ACCESSORS
    /* -------------------------------------------------------- */
    function getDexRouters() external view returns (address[] memory) {
        return USWAP_V2_ROUTERS;
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE
    /* -------------------------------------------------------- */
    // front-facing UI to initialize flash-loan
    function makeFlashLoan(IERC20[] memory _tokens, uint256[] memory _amounts, bytes memory _userData) external onlyKeeper {
        // require(msg.sender == owner(), "loan to owner only");
        BALANCER_VAULT.flashLoan(this, _tokens, _amounts, _userData);
        emit FlashLoansRequested(_tokens, _amounts, _userData);
    }

    receive() external payable {}

    /* -------------------------------------------------------- */
    /* PUBLIC - IFlashLoanRecipient OVERRIDES
    /* -------------------------------------------------------- */
    function _redundentSwap(address _dexRouter, address _tokenIn, address[] _swapPath, uint256 _swapAmntIn, uint16 _swapCnt) private {
        uint256 ind_swapAmntIn = _swapAmntIn / _swapCnt;
        for (uint8 i = 0; i < _swapCnt;) {
            uint256 amnt_out_quote =  _swap_v2_quote(_dexRouter, _swapPath, ind_swapAmntIn);
            // LEFT OFF HERE ... need to somehow verify if slippage would occur
            unchecked { i++; }
        }
    }
    // callback from BALANCER_VAULT with loaned funds
    function receiveFlashLoan(IERC20[] memory tokens, uint256[] memory amounts, uint256[] memory feeAmounts, bytes memory userData) external override {
        emit FlashLoansReceived(tokens, amounts, feeAmounts, userData);
        require(msg.sender == address(BALANCER_VAULT), " loan from BALANCER_VAULT only :o ");
        require(tokens.length == amounts.length && amounts.length == feeAmounts.length, ' param array lengths mismatch :/ ');
        // (address router_0, address router_1, address[] memory path_0, address[] memory path_1, uint256 amntIn_0, uint256 amntOutMin_1) = abi.decode(userData, (address, address, address[], address[], uint256, uint256));
        
        uint256 bal = IERC20(tokens[0]).balanceOf(address(this));

        /** ALGORITHMIC DESIGN - FLASH SWAP */
        bytes memory data = new bytes(1); // 1 = invoke 'uniswapV2Call' callback to manually pay|return tokens owed
        // _swap_v2_flashSwap(address tokenA, address tokenB, uint amount0Out, uint amount1Out, address to, bytes calldata data);

        /** ALGORITHMIC DESIGN */
        // 1) loop through loaned 'tokens', for each ...
        //      execute redundent swap algorithm for TOK_pUSDC, TOK_pUSDT, TOK_pWETH, TOK_pWBTC -> TOK_ATROPA
        //      need to map out path arrays for each: 
        //          TOK_pUSDC, TOK_pUSDT, TOK_pWETH, TOK_pWBTC -> TOK_ATROPA
        for (uint8 i = 0; i < tokens.length;) {
            _redundentSwap(TOKEN_ROUTER_MAP[tokens[i]], tokens[i], TOKEN_SWAP_PATH_MAP[tokens[i]], amounts[i], TOKEN_REDUND_SWAP_CNT_MAP[tokens[i]]);
            unchecked { i++; }
        }
        // 2) execute redundent swap algorithm for TOK_ATROPA -> TOK_TSFi -> TOK_R
        //      required to ensure minimal loss on slippage
        //      need to verify 'amountsOut' after each swap executed (check for slippage in USD value)

        // 3) invoke trade-in|mint function from 'ITokenBear9(TOK_BEAR9)'
        //      TOK_BEAR9 interface needs to be manually declared above: 
        //          'interface ITokenBear9 { ... }'
        //      trade-in includes: TOK_R + 4 other tokens
        //      should result in receiving 1 TOK_BEAR9

        // 4) loop through loaned 'tokens', for each ...
        //      execute redundent swap algorithm for TOK_BEAR9 -> TOK_pWBTC -> TOK_pUSDC, TOK_pUSDT, TOK_pWETH
        //      swap amounts are respective to their flash-loan received 'amounts'
        //      everything that remains, is our profit
        //      need to map out path arrays for each: 
        //          TOK_BEAR9 -> TOK_pWBTC -> TOK_pUSDC, TOK_pUSDT, TOK_pWETH

        // 5) loop through loaned 'tokens'
        //      for each, payback their respective loan
        //      everything that remains, is our profit
        uint256[] memory amountsOwed = new uint256[](amounts.length); 
        for (uint8 i=0; i < amountsOwed.length;) {
            amountsOwed[i] = amounts[i] + feeAmounts[i];
            IERC20(tokens[i]).transfer(address(BALANCER_VAULT), amountsOwed[i]);
            unchecked { i++; }
        }
        emit FlashLoansReturned(tokens, amounts, feeAmounts, amountsOwed);
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - DEX SUPPORTING                                   
    /* -------------------------------------------------------- */
    // ref: https://docs.uniswap.org/contracts/v2/guides/smart-contract-integration/using-flash-swaps
    //  NOTE: 'sender' = 'msg.sender' that called 'IUniswapV2Pair(pair).swap'
    function uniswapV2Call(address sender, uint amount0, uint amount1, bytes calldata data) external {
        address token0 = IUniswapV2Pair(msg.sender).token0(); // fetch the address of token0
        address token1 = IUniswapV2Pair(msg.sender).token1(); // fetch the address of token1
        assert(msg.sender == IUniswapV2Factory(factoryV2).getPair(token0, token1)); // ensure that msg.sender is a V2 pair
        // rest of the function goes here!

        // NOTE: at this point, address(this) should have indeed received token0 & token1 amounts
        //  from pair requested in 'IUniswapV2Pair(pair).swap', and tokens are freely available to use
        
        // LEFT OFF HERE ... need to finish the deal (transfer tokens to LP msg.sender) return tokens taken | pay tokens owed)
        // return token taken ...
        //  ref: https://docs.uniswap.org/contracts/v2/guides/smart-contract-integration/using-flash-swaps#single-token
        //  use: DAIReservePre - DAIWithdrawn + (DAIReturned * .997) >= DAIReservePre
        //      ie. (DAIReturned * .997) - DAIWithdrawn >= 0
        //      ie. DAIReturned >= DAIWithdrawn / .997
        // pay tokens owed ...
        //  ref: https://docs.uniswap.org/contracts/v2/guides/smart-contract-integration/using-flash-swaps#multi-token
        //  use: 'getAmountIn'
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    function _editDexRouters(address _router, bool _add) private {
        require(_router != address(0x0), "0 address");
        if (_add) {
            USWAP_V2_ROUTERS = _addAddressToArraySafe(_router, USWAP_V2_ROUTERS, true); // true = no dups
        } else {
            USWAP_V2_ROUTERS = _remAddressFromArray(_router, USWAP_V2_ROUTERS); // removes only one & order NOT maintained
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

    /* -------------------------------------------------------- */
    /* PRIVATE - DEX SUPPORT                                    
    /* -------------------------------------------------------- */
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
    function _swap_v2_flashSwap(address tokenA, address tokenB, uint amount0Out, uint amount1Out, address to, bytes calldata data) private {
        // Get pair address
        address pair = IUniswapV2Factory(uniswapRouter.factory()).getPair(tokenA, tokenB);
        require(pair != address(0), "Pair not found");

        // Call swap function on pair
        IUniswapV2Pair(pair).swap(
            amount0Out,
            amount1Out,
            address(this), // Borrower contract
            data
        );

        // NOTE: data.length == 0: do not invoke 'uniswapV2Call' callback
        //       data.length >  0: indeed invoke 'uniswapV2Call' callback
    }
    function _swap_v2_quote(address _dexRouter, address[] _path, uint256 _amntIn) private view returns (uint256) {
        uint256[] memory amountsOut = IUniswapV2Router02(_dexRouter).getAmountsOut(_amntIn, _path); // quote swap
        return amountsOut[amountsOut.length -1];
    }
    // uniwswap v2 protocol based: get quote and execute swap
    function _swap_v2_wrap(address router, address[] memory path, uint256 amntIn, address outReceiver, bool fromETH) private returns (uint256) {
        require(path.length >= 2, 'err: path.length :/');
        // uint256[] memory amountsOut = IUniswapV2Router02(router).getAmountsOut(amntIn, path); // quote swap
        // uint256 amntOut = _swap_v2(router, path, amntIn, amountsOut[amountsOut.length -1], outReceiver, fromETH); // approve & execute swap

        uint256 amntOutQuote = _swap_v2_quote(router, path, amntIn);
        uint256 amntOut = _swap_v2(router, path, amntIn, amntOutQuote, outReceiver, fromETH); // approve & execute swap
                
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
}
