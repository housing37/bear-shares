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
// import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // deploy


// local _ $ npm install @openzeppelin/contracts
// local _ $ git clone https://github.com/balancer/balancer-v2-monorepo.git
// import "./pkg-balancer/interfaces/contracts/vault/IVault.sol";
// import "./pkg-balancer/interfaces/contracts/vault/IFlashLoanRecipient.sol";
import "./node_modules/@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Callee.sol';
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol';
import "./node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LPCleaner is IUniswapV2Callee {
    /* -------------------------------------------------------- */
    /* PUBLIC - GLOBALS                                          
    /* -------------------------------------------------------- */
    /* _ ADMIN SUPPORT _ */
    string public tVERSION = '11.5';
    address public KEEPER;
    // address[] public USWAP_V2_ROUTERS;
    address public constant BURN_ADDR = address(0x0000000000000000000000000000000000000369);

    /* -------------------------------------------------------- */
    /* PRIVATE - FLASHLOANS SUPPORT                                 
    /* -------------------------------------------------------- */    
    // address private constant TOK_ATROPA = address(0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6);
    // address private constant TOK_TSFi = address(0x4243568Fa2bbad327ee36e06c16824cAd8B37819);
    // address private constant TOK_R = address(0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622);
    // address private constant TOK_BEAR9 = address(0x1f737F7994811fE994Fe72957C374e5cD5D5418A);

    // address private constant TOK_pWBTC = address(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    // address private constant TOK_pUSDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    // address private constant TOK_pWETH = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    // address private constant TOK_pUSDT = address(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    /* -------------------------------------------------------- */
    /* STRUCTS                                        
    /* -------------------------------------------------------- */

    /* -------------------------------------------------------- */
    /* EVENTS                                        
    /* -------------------------------------------------------- */    
    event KeeperMaintenance(address _tokAddr, uint256 _tokAmnt);
    event KeeperWithdrawel(uint256 _natAmnt);
    event KeeperTransfered(address _prev, address _new);
    event UniswapCallback(uint _index, uint _data0, uint _data1, uint _data2, uint _data3);
    event UniswapCallbackAlt(uint _index, uint _data0, uint _data1, address[] _data2);

    /* -------------------------------------------------------- */
    /* FLASH-SWAP SUPPORT
    /* -------------------------------------------------------- */
    address public constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);
    address public constant TOK_weDAI = address(0xefD766cCb38EaF1dfd701853BFCe31359239F305);
    address public constant TOK_PDRIP = address(0xeB2CEed77147893Ba8B250c796c2d4EF02a72B68);
    address public constant TOK_BEAR = address(0xd6c31bA0754C4383A41c0e9DF042C62b5e918f6d);

    address public constant PLP_BEAR_PDRIP = address(0xFAB2861E5AD61747CfDb4c2fb6193778D957714A); // pulsex v2
    address public constant PLP_BEAR_WPLS = address(0x31eF9a41500E6BD18524404aC9c5B88D04AA924E); // pulsex v2
    address public constant PLP_PDRIP_WPLS = address(0x25D240831a9c0CB981506538E810d32487D291Af); // pulsex v2

    address private constant TOK_PTP = address(0x880Dd541e00B966d829968c3198F11C8ca38A877);
    address private constant TOK_PEPE = address(0x6982508145454Ce325dDbE47a25d4ec3d2311933);
    address private constant TOK_FOTTIE = address(0x8445FBBa95Cc8c965c5c8F3a10b6F7ce53A4ef24);

    address private constant PLP_PTP_WPLS = address(0xb8eFCcb3FA5D4Bc68524989173Dc603E1ACC0362); // pulsex v2
    address private constant PLP_PTP_PEPE = address(0xb2E488CC039760F1efc886d4A8eB5b457BBE3060); // pulsex v2
    address private constant PLP_PEPE_WPLS = address(0x11659a752AC07452B9F139B897c917338e2dFB16); // pulsex v2
    address private constant PLP_PTP_FOTTIE = address(0xfCC81f1fA6C0B700d8D598a4f391f460fD9BD66C); // pulsex v2

    // IUniswapV2Pair lp_0 = IUniswapV2Pair(PLP_PTP_WPLS);
    // IUniswapV2Pair lp_1 = IUniswapV2Pair(PLP_PTP_PEPE);
    // IUniswapV2Pair lp_2 = IUniswapV2Pair(PLP_PTP_FOTTIE);
    // IUniswapV2Pair lp_3 = IUniswapV2Pair(PLP_PEPE_WPLS);

    IUniswapV2Pair lp_0 = IUniswapV2Pair(PLP_BEAR_WPLS);
    IUniswapV2Pair lp_1 = IUniswapV2Pair(PLP_BEAR_PDRIP);
    IUniswapV2Pair lp_3 = IUniswapV2Pair(PLP_PDRIP_WPLS);

    mapping(IUniswapV2Pair => address) private PLP_ADDR_MAP;    

    address pulsex_v1_router = address(0x98bf93ebf5c380C0e6Ae8e192A7e2AE08edAcc02);
    address pulsex_v2_router = address(0x165C3410fC91EF562C50559f7d2289fEbed552d9);
    IUniswapV2Router02 PULSEX_V1 = IUniswapV2Router02(pulsex_v1_router);
    IUniswapV2Router02 PULSEX_V2 = IUniswapV2Router02(pulsex_v2_router);

    /* -------------------------------------------------------- */
    /* CONTRUCTOR                                        
    /* -------------------------------------------------------- */
    constructor() {
        KEEPER = msg.sender;

        PLP_ADDR_MAP[lp_0] = address(PLP_PTP_WPLS);
        PLP_ADDR_MAP[lp_1] = address(PLP_PTP_PEPE);
        // PLP_ADDR_MAP[lp_2] = address(PLP_PTP_FOTTIE);
        PLP_ADDR_MAP[lp_3] = address(PLP_PEPE_WPLS);
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
    // function KEEPER_editDexRouters(address _router, bool _add) external onlyKeeper {
    //     require(_router != address(0x0), "0 address");
    //     _editDexRouters(_router, _add);
    //     emit DexRouterUpdated(_router, _add);
    // }
    /* -------------------------------------------------------- */
    /* PUBLIC - ACCESSORS
    /* -------------------------------------------------------- */
    // function getDexRouters() external view returns (address[] memory) {
    //     return USWAP_V2_ROUTERS;
    // }

    // 10000 = 100.00%
    function _perc_of_uint256(uint32 _perc, uint256 _num) private pure returns (uint256) {
        require(_perc <= 10000, 'err: invalid percent');
        return _perc_of_uint256_unchecked(_perc, _num);
    }
    function _perc_of_uint256_unchecked(uint32 _perc, uint256 _num) private pure returns (uint256) {
        // require(_perc <= 10000, 'err: invalid percent');
        uint32 aux_perc = _perc * 100; // Multiply by 100 to accommodate decimals
        uint256 result = (_num * uint256(aux_perc)) / 1000000; // chatGPT equation
        return result; // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)

        // NOTE: more efficient with no local vars allocated
        // return (_num * uint64(uint32(_perc) * 100)) / 1000000; // chatGPT equation
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE
    /* -------------------------------------------------------- */
    function cleanLiquidityPool() external {

        // IUniswapV2Pair lp_0 = IUniswapV2Pair(PLP_PTP_WPLS);
        // IUniswapV2Pair lp_1 = IUniswapV2Pair(PLP_PTP_PEPE);
        // IUniswapV2Pair lp_2 = IUniswapV2Pair(PLP_PTP_FOTTIE);
        // IUniswapV2Pair lp_3 = IUniswapV2Pair(PLP_PEPE_WPLS);

        // get reserves to work with
        // (uint112 res_ptp_lp_0, uint112 res_wpls_lp_0, uint32 bts_lp_0) = lp_0.getReserves();
        // (uint112 res_ptp_lp_1, uint112 res_pepe_lp_1, uint32 bts_lp_1) = lp_1.getReserves();
        // (uint112 res_ptp_lp_2, uint112 res_fottie_lp_2, uint32 bts_lp_2) = lp_2.getReserves();
        // (uint112 res_pepe_lp_3, uint112 res_wpls_lp_3, uint32 bts_lp_3) = lp_3.getReserves();

        // function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data)

        // // pull out all ptp (reserves0) from ptp:pepe (lp_1)
        // (uint112 res_tok0_lp_1, uint112 res_tok1_lp_1, uint32 bts_lp_1) = lp_1.getReserves();
        // // bytes memory data = abi.encode(_pairAddress);
        // // bytes memory encodedData = abi.encode(lp_1.kLast(), res_tok0_lp_1, res_tok1_lp_1, bts_lp_1);
        // bytes memory encodedData = abi.encode(res_tok0_lp_1, res_tok1_lp_1);
        // // uint112 ptp_resrve = lp_1.token0() == TOK_PTP ? res_tok0_lp_1 : res_tok1_lp_1;
        // (uint112 ptp_resrve, uint112 pepe_resrve) = lp_1.token0() == TOK_PTP ? (res_tok0_lp_1, res_tok1_lp_1) : (res_tok1_lp_1, res_tok0_lp_1);
        // // uint256 ptp_amnt_use = ptp_resrve - _perc_of_uint256(100, ptp_resrve); // 100 = 1.00%
        // if (lp_1.token0() == TOK_PTP) // found ptp:pepe
        //     // lp_1.swap(res_tok0_lp_1 - 1, 0, address(this), new bytes(1)); // data: 1 = invoke 'uniswapV2Call'
        //     // lp_1.swap(ptp_resrve -1, 0, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
        //     lp_1.swap(ptp_resrve - 10**18, 0, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
        //     // lp_1.swap(ptp_amnt_use, 0, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
            
        // else // found pepe:ptp
        //     // lp_1.swap(0, res_tok0_lp_1 - 1, address(this), new bytes(1)); // data: 1 = invoke 'uniswapV2Call'
        //     // lp_1.swap(0, ptp_resrve -1, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
        //     lp_1.swap(0, ptp_resrve - 10**18, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
        //     // lp_1.swap(0, ptp_amnt_use, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'

        // NOTE: 'uniswapV2Call' will then be invoked with res_ptp_lp_1 amount of PTP available to spend
        //      0) calc pepe owed for this ptp received (from lp_1)
        //      1) swap that ptp received for as much wpls as possible in lp_0
        //      2) swap as little wpls as possible for pepe owed to lp_1
        //      3) pay back pepe owed to lp_1

        // pull max BEAR we can from pair bear:pdrip (lp_1)
        //  NOTE: respective to max pdrip reserve available in pdrip:wpls (lp_3)
        (uint112 res_tok0_lp_3, uint112 res_tok1_lp_3, uint32 bts_lp_3) = lp_3.getReserves();
        (uint112 pdrip_resrve_3, uint112 wpls_resrve_3) = lp_3.token0() == TOK_PDRIP ? (res_tok0_lp_3, res_tok1_lp_3) : (res_tok1_lp_3, res_tok0_lp_3);
        address[] memory path_pdrip_bear = new address[](2);
        path_pdrip_bear[0] = TOK_PDRIP;
        path_pdrip_bear[1] = TOK_BEAR;
        uint256[] memory bear_in_arr = PULSEX_V2.getAmountsOut(pdrip_resrve_3, path_pdrip_bear); // for 'out' use '.length-1'
        uint256 bear_in = bear_in_arr[bear_in_arr.length-1]; 
        if (lp_1.token0() == TOK_BEAR) // found ptp:
            lp_1.swap(bear_in, 0, address(this), new bytes(1)); // data: 1 = invoke 'uniswapV2Call'
        else
            lp_1.swap(0, bear_in, address(this), new bytes(1)); // data: 1 = invoke 'uniswapV2Call'

        // // pull all BEAR from pair bear:pdrip
        // (uint112 res_tok0_lp_1, uint112 res_tok1_lp_1, uint32 bts_lp_1) = lp_1.getReserves();
        // bytes memory encodedData = abi.encode(res_tok0_lp_1, res_tok1_lp_1);
        // (uint112 bear_resrve, uint112 pdrip_resrve) = lp_1.token0() == TOK_BEAR ? (res_tok0_lp_1, res_tok1_lp_1) : (res_tok1_lp_1, res_tok0_lp_1);
        // if (lp_1.token0() == TOK_BEAR) // found ptp:
        //     lp_1.swap(bear_resrve - 10**18, 0, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
        // else
        //     lp_1.swap(0, bear_resrve - 10**18, address(this), encodedData); // data: 1 = invoke 'uniswapV2Call'
    }


    receive() external payable {}

    /* -------------------------------------------------------- */
    /* PUBLIC - DEX SUPPORTING                                   
    /* -------------------------------------------------------- */
    // ref: https://docs.uniswap.org/contracts/v2/guides/smart-contract-integration/using-flash-swaps
    //  NOTE: 'sender' = 'msg.sender' that called 'IUniswapV2Pair(pair).swap'
    function uniswapV2Call(address sender, uint amount0, uint amount1, bytes calldata data) external {
        // fetch addresses of msg.sender's tokens & validate they are msg.sender's pair
        require(msg.sender == IUniswapV2Factory(PULSEX_V2.factory()).getPair(IUniswapV2Pair(msg.sender).token0(), IUniswapV2Pair(msg.sender).token1()), ' invalid msg.sender :{} ');        

        uint256 bear_received = lp_1.token0() == TOK_BEAR ? amount0 : amount1;
        require(IERC20(TOK_BEAR).balanceOf(address(this)) >= bear_received, ' .swap failed _ 0 :/ ');

        // get / calc pdrip_owed for later
        address[] memory path_pdrip_bear = new address[](2);
        path_pdrip_bear[0] = TOK_PDRIP;
        path_pdrip_bear[1] = TOK_BEAR;
        uint256 pdrip_owed = PULSEX_V2.getAmountsIn(bear_received, path_pdrip_bear)[0]; // for 'in' use '0'
        emit UniswapCallbackAlt(0, pdrip_owed, bear_received, path_pdrip_bear);

        // swap bear_received for as much WPLS as possible
        address[] memory path_bear_wpls = new address[](2);
        path_bear_wpls[0] = TOK_BEAR;
        path_bear_wpls[1] = TOK_WPLS;
        uint256 wpls_amnt_out = _swap_v2(path_bear_wpls, pulsex_v2_router, bear_received, 0, address(this), false); // approve & execute swap
        emit UniswapCallbackAlt(1, wpls_amnt_out, bear_received, path_bear_wpls);

        // calc wpls_in required to get pdrip_owed
        address[] memory path_wpls_pdrip = new address[](2);
        path_wpls_pdrip[0] = TOK_WPLS;
        path_wpls_pdrip[1] = TOK_PDRIP;
        uint256 wpls_in = PULSEX_V2.getAmountsIn(pdrip_owed, path_wpls_pdrip)[0]; // for 'in' use '0'
        emit UniswapCallbackAlt(2, wpls_in, pdrip_owed, path_wpls_pdrip);

        // (NOTE: require wpls_amnt_out > wpls_in, else no profit)
        require(wpls_amnt_out > wpls_in, ' calc no WPLS profit :( ');

        // swap wpls_in for pdrip_owed
        uint256 pdrip_amnt_out = _swap_v2_wrap(path_wpls_pdrip, pulsex_v2_router, wpls_in, address(this), false); // true = fromETH
        uint256 pdrip_bal = IERC20(TOK_PDRIP).balanceOf(address(this));
        emit UniswapCallbackAlt(3, pdrip_amnt_out, wpls_in, path_wpls_pdrip);
        require(pdrip_bal >= pdrip_owed, ' .swap failed _ 1 :/ ');
        revert(' made it this far!! ');

        // 3) pay back pepe owed to lp_1
        IERC20(TOK_PDRIP).transfer(PLP_ADDR_MAP[lp_1], pdrip_owed);

        // // uint112 wpls_res;
        // // uint112 ptp_res;
        // // uint112 pepe_res;

        // // verifiy received all the ptp (reserves0) requested from lp_1
        // // uint256 ptp_bal = IERC20(TOK_PTP).balanceOf(address(this));
        // // uint256 ptp_received = lp_1.token0() == TOK_PTP ? amount0 : amount1;
        // // require(IERC20(TOK_PTP).balanceOf(address(this)) >= ptp_received, ' .swap failed _ 0 :/ ');

        // // 0) calc pepe owed for this ptp received (from lp_1)
        // // calc amount of pepe (reserves1) owed to ptp:pepe (lp_1)
        // //  ie. from "lp_1.swap(res_ptp_lp_1, 0, address(this), new bytes(1));"
        // // (uint112 res_tok0_lp_1, uint112 res_tok1_lp_1, uint32 bts_lp_1) = lp_1.getReserves();
        // // (uint256 kLast, uint112 res_tok0_lp_1, uint112 res_tok1_lp_1, uint32 bts_lp_1) = abi.decode(data, (uint256, uint112, uint112, uint32));
        // // (uint112 res_tok0_lp_1, uint112 res_tok1_lp_1) = abi.decode(data, (uint112, uint112));

        // // // default ptp:pepe
        // // ptp_res = res_tok0_lp_1;
        // // pepe_res = res_tok1_lp_1;

        // // // found pepe:ptp
        // // if (lp_1.token1() == TOK_PTP) { 
        // //     pepe_res = res_tok0_lp_1;
        // //     ptp_res = res_tok1_lp_1;
        // // }

        // // calc PEPE to be owed at the end
        // // uint256 pepe_owed = PULSEX_V2.getAmountIn(ptp_received, pepe_res, ptp_res);
        // address[] memory path_pepe_ptp = new address[](2);
        // path_pepe_ptp[0] = TOK_PEPE;
        // path_pepe_ptp[1] = TOK_PTP;
        // uint256 pepe_owed = PULSEX_V2.getAmountsIn(ptp_received, path_pepe_ptp)[0]; // for 'in' use '0'
        // emit UniswapCallbackAlt(0, pepe_owed, ptp_received, path_pepe_ptp);

        // // TEST OG SWAPPING (inside flash swap callback, w/ non-related tokens & LP)
        // address[] memory path_dai_wpls = new address[](2);
        // path_dai_wpls[0] = TOK_weDAI;
        // path_dai_wpls[1] = TOK_WPLS;
        // uint256 amnt_dai_in = 10; // NOTE: required to send 10 TOK_weDAI to this contract | address(this) 
        // uint256 wpls_amnt_out_test = _swap_v2(path_dai_wpls, pulsex_v2_router, amnt_dai_in, 0, address(this), false); // approve & execute swap

        // // 1) swap that ptp received for as much wpls as possible in lp_0
        // // calc amount of wpls_owed (reserves1) to get from lp_0 (ptp:wpls) if sent ptp_received amount
        // //  then .transfer ptp_received amount
        // //  then pull (.swap) wpls_owed
        // // (uint112 res_tok0_lp_0, uint112 res_tok1_lp_0, uint32 bts_lp_0) = lp_0.getReserves();
        
        // // // default ptp:wpls
        // // ptp_res = res_tok0_lp_0;
        // // wpls_res = res_tok1_lp_0;

        // // // found wpls:ptp
        // // if (lp_0.token1() == TOK_PTP) { 
        // //     wpls_res = res_tok0_lp_0;
        // //     ptp_res = res_tok1_lp_0;
        // // }

        // // uint256 memory WPLS_amnt_0 = UNISWAP_V2.getAmountsOut(PTP_amnt_0, path_ptp_wpls)[-1];
        // // uint256 memory PTP_amnt_1 = UNISWAP_V2.getAmountsIn(WPLS_amnt_0, path_ptp_wpls)[0];
        // // PTP_amnt_1 == PTP_amnt_0 // <- is this true?

        // // calc WPLS to recieve
        // // uint256 wpls_owed = PULSEX_V2.getAmountOut(ptp_received, ptp_res, wpls_res);
        // // emit UniswapCallback(1, wpls_owed, ptp_received, ptp_res, wpls_res);
        // address[] memory path_ptp_wpls = new address[](2);
        // path_ptp_wpls[0] = TOK_PTP;
        // path_ptp_wpls[1] = TOK_WPLS;
        // // uint256 wpls_amnt_out = _swap_v2_wrap(path_ptp_wpls, pulsex_v2_router, ptp_received, address(this), false); // true = fromETH
        // uint256 wpls_amnt_out = _swap_v2(path_ptp_wpls, pulsex_v2_router, ptp_received, 0, address(this), false); // approve & execute swap

        // // uint256[] memory wpls_owed_arr = PULSEX_V2.getAmountsOut(ptp_received, path_ptp_wpls); // fee taken out within "getAmount(s)In|Out"
        // // uint256 wpls_owed = wpls_owed_arr[wpls_owed_arr.length-1]; // for 'out' use '-1'
        // // // uint256 wpls_owed = 10420904517333898665288407;
        // // // uint256 wpls_owed = 10420900000000000000000000;
        // // // emit UniswapCallback(1, wpls_owed, ptp_received, path_ptp_wpls);
        // // emit UniswapCallbackAlt(1, wpls_owed, ptp_received, path_ptp_wpls);

        // // // calc / verify new 'k' vs. old 'k'
        // // // uint256 og_k_lp_0 = ptp_res * wpls_res;
        // // // uint256 new_k  = (ptp_res + ptp_received) * (wpls_res - wpls_owed);
        // // // require(new_k >= og_k_lp_0, ' old / new k fucked :() ');

        // // // send PTP
        // // IERC20(TOK_PTP).transfer(PLP_ADDR_MAP[lp_0], ptp_received);

        // // // get WPLS (minus 0.3% fee)
        // // wpls_owed = wpls_owed - _perc_of_uint256(29, wpls_owed); // 10000 = 100.00%
        // // // emit UniswapCallback(2, wpls_owed, ptp_received, ptp_res, wpls_res);
        // // emit UniswapCallbackAlt(2, wpls_owed, ptp_received, path_ptp_wpls);

        // // if (lp_0.token0() == TOK_PTP) // found ptp:wpls
        // //     lp_0.swap(0, wpls_owed -1, address(this), new bytes(0)); // data: 0 = DO NOT invoke 'uniswapV2Call' callback
        // // else // found wpls:ptp
        // //     lp_0.swap(wpls_owed -1, 0, address(this), new bytes(0)); // data: 0 = DO NOT invoke 'uniswapV2Call' callback


        // /** 2) use '.swap(...)' */
        // // 2) swap as little wpls as possible for pepe (in lp_3) to payback lp_1 (remaining WPLS is our profit)
        // // calc amount of wpls required to get pepe_owed amount
        // //  then .transfer wpls required
        // //  then pull (.swap) pepe_owed (and verify)
        // // (uint112 res_tok0_lp_3, uint112 res_tok1_lp_3, uint32 bts_lp_3) = lp_3.getReserves();

        // // // default pepe:wpls
        // // uint112 pepe_res_1 = res_tok0_lp_3;
        // // uint112 wpls_res_1 = res_tok1_lp_3;

        // // // found wpls:pepe
        // // if (lp_3.token1() == TOK_PEPE) { 
        // //     wpls_res_1 = res_tok0_lp_3;
        // //     pepe_res_1 = res_tok1_lp_3;
        // // }

        // // calc WPLS to send
        // // uint256 wpls_in = PULSEX_V2.getAmountIn(pepe_owed, wpls_res_1, pepe_res_1);
        // // emit UniswapCallback(3, wpls_in, pepe_owed, pepe_res_1, wpls_res_1);
        // address[] memory path_wpls_pepe = new address[](2);
        // path_wpls_pepe[0] = TOK_WPLS;
        // path_wpls_pepe[1] = TOK_PEPE;
        // uint256 wpls_in = PULSEX_V2.getAmountsIn(pepe_owed, path_wpls_pepe)[0]; // for 'in' use '0'
        // emit UniswapCallbackAlt(3, wpls_in, pepe_owed, path_wpls_pepe);

        // // send WPLS (plus 0.3% fee)
        // // wpls_in = wpls_in + _perc_of_uint256(30, wpls_in); // 10000 = 100.00%
        // IERC20(TOK_WPLS).transfer(PLP_ADDR_MAP[lp_3], wpls_in);
        // // emit UniswapCallback(4, wpls_in, pepe_owed, pepe_res_1, wpls_res_1);
        // emit UniswapCallbackAlt(4, wpls_in, pepe_owed, path_wpls_pepe);

        // // get PEPE
        // if (lp_3.token0() == TOK_PEPE) // found pepe:wpls
        //     lp_3.swap(pepe_owed, 0, address(this), new bytes(0)); // data: 1 = invoke 'uniswapV2Call'
        // else // found wpls:pepe
        //     lp_3.swap(0, pepe_owed, address(this), new bytes(0)); // data: 1 = invoke 'uniswapV2Call'
        
        // uint256 pepe_bal = IERC20(TOK_PEPE).balanceOf(address(this));
        // require(pepe_bal >= pepe_owed, ' .swap failed _ 1 :/ ');
        // revert(' made it this far! ');

        // /** 2) use '_swap_v2_wrap' */
        // // address[] memory wpls_pepe_path = new address[](2);
        // // wpls_pepe_path[0] = TOK_WPLS;
        // // wpls_pepe_path[1] = TOK_PEPE;
        // // uint256[] memory amountsIn = PULSEX_V2.getAmountsIn(pepe_owed, wpls_pepe_path); // quote swap
        // // uint256 wpls_in = amountsIn[amountsIn.length-1];
        // // emit UniswapCallback(3, wpls_in, pepe_owed, ptp_res, wpls_res);

        // // uint256 pepe_amnt_out = _swap_v2_wrap(wpls_pepe_path, pulsex_v2_router, wpls_in, address(this), false); // true = fromETH
        // // uint256 pepe_bal = IERC20(TOK_PEPE).balanceOf(address(this));
        // // emit UniswapCallback(4, wpls_in, pepe_owed, pepe_amnt_out, pepe_bal);
        // // require(pepe_bal >= pepe_owed, ' .swap failed _ 1 :/ ');
        // // revert(' made it this far!! ');

        // // 3) pay back pepe owed to lp_1
        // IERC20(TOK_PEPE).transfer(PLP_ADDR_MAP[lp_1], pepe_owed);
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    // function _editDexRouters(address _router, bool _add) private {
    //     require(_router != address(0x0), "0 address");
    //     if (_add) {
    //         USWAP_V2_ROUTERS = _addAddressToArraySafe(_router, USWAP_V2_ROUTERS, true); // true = no dups
    //     } else {
    //         USWAP_V2_ROUTERS = _remAddressFromArray(_router, USWAP_V2_ROUTERS); // removes only one & order NOT maintained
    //     }
    // }
    // function _addAddressToArraySafe(address _addr, address[] memory _arr, bool _safe) private pure returns (address[] memory) {
    //     if (_addr == address(0)) { return _arr; }

    //     // safe = remove first (no duplicates)
    //     if (_safe) { _arr = _remAddressFromArray(_addr, _arr); }

    //     // perform add to memory array type w/ static size
    //     address[] memory _ret = new address[](_arr.length+1);
    //     for (uint i=0; i < _arr.length;) { _ret[i] = _arr[i]; unchecked {i++;}}
    //     _ret[_ret.length-1] = _addr;
    //     return _ret;
    // }
    // function _remAddressFromArray(address _addr, address[] memory _arr) private pure returns (address[] memory) {
    //     if (_addr == address(0) || _arr.length == 0) { return _arr; }
        
    //     // NOTE: remove algorithm does NOT maintain order & only removes first occurance
    //     for (uint i = 0; i < _arr.length;) {
    //         if (_addr == _arr[i]) {
    //             _arr[i] = _arr[_arr.length - 1];
    //             assembly { // reduce memory _arr length by 1 (simulate pop)
    //                 mstore(_arr, sub(mload(_arr), 1))
    //             }
    //             return _arr;
    //         }

    //         unchecked {i++;}
    //     }
    //     return _arr;
    // }

    /* -------------------------------------------------------- */
    /* PRIVATE - DEX SUPPORT                                    
    /* -------------------------------------------------------- */
    function _swap_v2_quote(address _dexRouter, address[] memory _path, uint256 _amntIn) private view returns (uint256) {
        uint256[] memory amountsOut = IUniswapV2Router02(_dexRouter).getAmountsOut(_amntIn, _path); // quote swap
        return amountsOut[amountsOut.length -1];
    }
    // uniwswap v2 protocol based: get quote and execute swap
    function _swap_v2_wrap(address[] memory path, address router, uint256 amntIn, address outReceiver, bool fromETH) private returns (uint256) {
        require(path.length >= 2, 'err: path.length :/');
        // uint256[] memory amountsOut = IUniswapV2Router02(router).getAmountsOut(amntIn, path); // quote swap
        // uint256 amntOut = _swap_v2(router, path, amntIn, amountsOut[amountsOut.length -1], outReceiver, fromETH); // approve & execute swap

        uint256 amntOutQuote = _swap_v2_quote(router, path, amntIn);
        uint256 amntOut = _swap_v2(path, router, amntIn, amntOutQuote, outReceiver, fromETH); // approve & execute swap
                
        // verifiy new balance of token received
        uint256 new_bal = IERC20(path[path.length -1]).balanceOf(outReceiver);
        require(new_bal >= amntOut, " _swap: receiver bal too low :{ ");
        
        return amntOut;
    }
    
    // v2: solidlycom, kyberswap, pancakeswap, sushiswap, uniswap v2, pulsex v1|v2, 9inch
    function _swap_v2(address[] memory path, address router, uint256 amntIn, uint256 amntOutMin, address outReceiver, bool fromETH) private returns (uint256) {
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
