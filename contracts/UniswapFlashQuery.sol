//SPDX-License-Identifier: UNLICENSED
// pragma solidity >=0.6.12;
pragma solidity ^0.8.24;

// pragma experimental ABIEncoderV2;

// remix compile _ 
// import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol"; // deploy

// local compile _
import "./node_modules/@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "./node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import './node_modules/@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol';

abstract contract UniswapV2Factory  {
    mapping(address => mapping(address => address)) public getPair;
    address[] public allPairs;
    function allPairsLength() external view virtual returns (uint);
}

// In order to quickly load up data from Uniswap-like market, this contract allows easy iteration with a single eth_call
contract UniswapFlashQuery {
    string public constant tVERSION = '1.0';
    address public KEEPER;
    constructor() {
        KEEPER = msg.sender;
    }

    // NOTE: house_051524: indeed testing just fine
    function getReservesByPairs(IUniswapV2Pair[] calldata _pairs) external view returns (uint256[3][] memory) {
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
}
