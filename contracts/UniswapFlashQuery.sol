//SPDX-License-Identifier: UNLICENSED
// pragma solidity >=0.6.12;
pragma solidity ^0.8.24;

// pragma experimental ABIEncoderV2;

// remix compile _ 
// import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol"; // deploy
// import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
// import '@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';
// import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // deploy

// local compile _
import "./node_modules/@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "./node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';
import "./node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";

abstract contract UniswapV2Factory  {
    mapping(address => mapping(address => address)) public getPair;
    address[] public allPairs;
    function allPairsLength() external view virtual returns (uint);
}

// In order to quickly load up data from Uniswap-like market, this contract allows easy iteration with a single eth_call
contract UniswapFlashQuery {
    // string public constant tVERSION = '2.8';
    string public constant tVERSION = '4.2';
    address public KEEPER;

    // NOTE: testing emit: comparing token0|1_in with client side printouts
    // event ReservesData(address _token0, address _token1, address _pair, uint256 _reserve0, uint256 _reserve1, uint256 _token0_in,uint256 _token1_in, uint256 _blocktimestamp);

    constructor() {
        KEEPER = msg.sender;
    }

    function getReservesByPairs(address[] calldata _pairs, address _uniswapRouter) external view returns (uint256[5][] memory) {
        uint256[5][] memory result = new uint256[5][](_pairs.length);
        for (uint i = 0; i < _pairs.length; i++) {
            // (result[i][0], result[i][1], result[i][4]) = _pairs[i].getReserves();
            // (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast) = _pairs[i].getReserves();
            
            // IUniswapV2Pair pair = IUniswapV2Pair(_pairs[i]);
            // (address token0, address token1) = (_pairs[i].token0(), _pairs[i].token1());
            // uint256 reserve0 = IERC20(token0).balanceOf(address(_pairs[i]));
            // uint256 reserve1 = IERC20(token1).balanceOf(address(_pairs[i]));
            // uint256 blockTimestampLast = block.timestamp;

            IUniswapV2Pair pair = IUniswapV2Pair(_pairs[i]);
            (address token0, address token1) = (pair.token0(), pair.token1());
            uint256 reserve0 = IERC20(token0).balanceOf(_pairs[i]);
            uint256 reserve1 = IERC20(token1).balanceOf(_pairs[i]);
            uint256 blockTimestampLast = block.timestamp;

            // (uint112 _reserve0, uint112 _reserve1, uint32 _blockTimestampLast)
            // (result_res[i][0], result_res[i][1], result_res[i][4]) = _uniswapPair.getReserves();

            // // // NOTE: v2.4, - 8
            // // // result[i][2] = the amnt of token[i][0] needed in, to take out all of token[i][1] (-1)
            // // // result[i][3] = the amnt of token[i][1] needed in, to take out all of token[i][0] (-1)
            // // result[i][2] = uint256(IUniswapV2Router02(_uniswapRouter).getAmountIn(result[i][1] -1, result[i][0], result[i][1]));
            // // result[i][3] = uint256(IUniswapV2Router02(_uniswapRouter).getAmountIn(result[i][0] -1, result[i][1], result[i][0]));
            // uint256 token0_in = uint256(IUniswapV2Router02(_uniswapRouter).getAmountIn(reserve1 -1, reserve0, reserve1));
            // uint256 token1_in = uint256(IUniswapV2Router02(_uniswapRouter).getAmountIn(reserve0 -1, reserve1, reserve0));
                // NOTE: with '-1', 'execution reverted' error occurs on client side (python)

            // NOTE: v3.0,1 - 5
            // result[i][2] = the amount of token0 needed in, to take out all of token1 (-1)
            // result[i][3] = the amount of token1 needed in, to take out all of token0 (-1)
            address[] memory path_out_1 = new address[](2);
            path_out_1[0] = token0;
            path_out_1[1] = token1;
            uint256 token0_in = IUniswapV2Router02(_uniswapRouter).getAmountsIn(reserve1 -1, path_out_1)[0];

            address[] memory path_out_0 = new address[](2);
            path_out_0[0] = token1;
            path_out_0[1] = token0;
            uint256 token1_in = IUniswapV2Router02(_uniswapRouter).getAmountsIn(reserve0 -1, path_out_0)[0];

            result[i][0] = reserve0;
            result[i][1] = reserve1;
            result[i][2] = token0_in;
            result[i][3] = token1_in;
            result[i][4] = blockTimestampLast;

            // NOTE: testing emit: comparing token0|1_in with client side printouts
            //  cannot emit events w/o using 'view' function modifier 
            // emit ReservesData(token0, token1, address(pair), reserve0, reserve1, token0_in, token1_in, blockTimestampLast);
        }
        return result;
    }

    // NOTE: house_051524: indeed testing just fine
    function getReservesByPairs_OG(IUniswapV2Pair[] calldata _pairs) external view returns (uint256[3][] memory) {
        uint256[3][] memory result = new uint256[3][](_pairs.length);
        for (uint i = 0; i < _pairs.length; i++) {
            (result[i][0], result[i][1], result[i][2]) = _pairs[i].getReserves();
        }
        return result;
    }

    // NOTE: house_051524: cannot get this working, keeep getting error for both read and write attempts
    function getPairsByIndexRange(address _uniswapFactory_, address _uniswapRouter, uint256 _start, uint256 _stop) external view returns (address[3][] memory, uint256[5][] memory)  {
        IUniswapV2Factory _uniswapFactory = IUniswapV2Factory(_uniswapFactory_);
        uint256 _allPairsLength = _uniswapFactory.allPairsLength();
        if (_stop > _allPairsLength) {
            _stop = _allPairsLength;
        }
        require(_stop >= _start, "start cannot be higher than stop");
        uint256 _qty = _stop - _start;
        address[3][] memory result = new address[3][](_qty);
        uint256[5][] memory result_res = new uint256[5][](_qty);
        for (uint i = 0; i < _qty; i++) {
            IUniswapV2Pair _uniswapPair = IUniswapV2Pair(_uniswapFactory.allPairs(_start + i));
            // result[i][0] = _uniswapPair.token0();
            // result[i][1] = _uniswapPair.token1();
            // result[i][2] = address(_uniswapPair);
            result[i][0] = address(_uniswapPair);
            result[i][1] = _uniswapPair.token0();
            result[i][2] = _uniswapPair.token1();

            // (uint112 _reserve0, uint112 _reserve1, uint32 _blockTimestampLast)
            (result_res[i][0], result_res[i][1], result_res[i][4]) = _uniswapPair.getReserves();

            // result_res[i][2] = IUniswapV2Router02(_uniswapRouter).getAmountIn(result_res[i][0], result_res[i][1], result_res[i][0]);
            // result_res[i][3] = IUniswapV2Router02(_uniswapRouter).getAmountIn(result_res[i][1], result_res[i][0], result_res[i][1]);

            address[] memory path_1_0 = new address[](2);
            path_1_0[0] = _uniswapPair.token1();
            path_1_0[1] = _uniswapPair.token0();
            result_res[i][2] = IUniswapV2Router02(_uniswapRouter).getAmountsIn(result_res[i][0], path_1_0)[0];
            
            address[] memory path_0_1 = new address[](2);
            path_0_1[0] = _uniswapPair.token0();
            path_0_1[1] = _uniswapPair.token1();
            result_res[i][3] = IUniswapV2Router02(_uniswapRouter).getAmountsIn(result_res[i][1], path_0_1)[0];
            // UniswapV2Library.getAmountsOut(factory, amountIn, path);
        }
        return (result, result_res);
    }

    // NOTE: house_051524: indeed testing just fine
    function getPairsByIndexRange_OG(UniswapV2Factory _uniswapFactory, uint256 _start, uint256 _stop) external view returns (address[3][] memory)  {
        uint256 _allPairsLength = _uniswapFactory.allPairsLength();
        if (_stop > _allPairsLength) {
            _stop = _allPairsLength;
        }
        require(_stop >= _start, "start cannot be higher than stop");
        uint256 _qty = _stop - _start;
        address[3][] memory result = new address[3][](_qty);
        for (uint i = 0; i < _qty; i++) {
            IUniswapV2Pair _uniswapPair = IUniswapV2Pair(_uniswapFactory.allPairs(_start + i));
            result[i][0] = _uniswapPair.token0();
            result[i][1] = _uniswapPair.token1();
            result[i][2] = address(_uniswapPair);
        }
        return result;
    }

    function getPair(address _factory, address _candA, address _candB) external view returns (address token0, address token1, address pair) {
        pair = IUniswapV2Factory(_factory).getPair(_candA, _candB);
        token0 = IUniswapV2Pair(pair).token0();
        token1 = IUniswapV2Pair(pair).token1();
    }
}
