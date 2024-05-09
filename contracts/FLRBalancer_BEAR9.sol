// SPDX-License-Identifier: GPL-2.0-or-later
// house_102523 _ ref: https://docs.balancer.fi/reference/contracts/flash-loans.html#example-code
// house_050924 _ ref: .../git/defi-arb/contracts/BalancerFLR_test.sol
pragma solidity ^0.8.24;

// remix compile _ 
// import "@balancer-labs/v2-interfaces/contracts/vault/IVault.sol";
// import "@balancer-labs/v2-interfaces/contracts/vault/IFlashLoanRecipient.sol";

// local compile _ $ git clone https://github.com/balancer/balancer-v2-monorepo.git
import "./pkg-balancer/interfaces/contracts/vault/IVault.sol";
import "./pkg-balancer/interfaces/contracts/vault/IFlashLoanRecipient.sol";

contract FLRBalancerBEAR9 is IFlashLoanRecipient {
    // ref: https://docs.balancer.fi/reference/contracts/flash-loans.html#example-code
    IVault private constant vault = IVault(0xBA12222222228d8Ba445958a75a0704d566BF2C8);
    // pWETH: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 -> 203658647860394116213752201 / 10**18 == 203658647.86039412 ~= $12,228.2445082
    // pUSDC: 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 -> 23937491402753 / 10**6 == 23937491.402753 ~= $74,767.781978741
    // pWBTC: 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 -> 5994742939 / 10**8 == 59.94742939 ~= $13,208.5705829
    // pUSDT: 0xdAC17F958D2ee523a2206206994597C13D831ec7 -> 13296690613518 / 10**6 == 13296690.613518 ~= $39,213.741269448

    // pDOLA: 0x865377367054516e17014CcdED1e7d814EDC9ce4 -> 30614508079920854526255527 / 10**18 ~= $236.198849851
    // pAAVE: 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9 -> 2114928347848533872595 / 10**18 ~= $280.453860038

    // ERROR: LIQUIDITY < BALANCE
    // pBAL: 0xba100000625a3754423978a60c9317c58a424e3D ->  3946496821522180948639451 / 10**18 == 3946496.821522181 ~= $41,153.679623988
    // prETH: 0xae78736cd615f374d3085123a210448e74fc6393 -> 27843230642023975590639 / 10**18 ~= $8,067.713537987

    address public constant BURN_ADDR = address(0x0000000000000000000000000000000000000369);
    address public constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);
    
    address public constant TOK_ATROPA = address(0xCc78A0acDF847A2C1714D2A925bB4477df5d48a6);
    address public constant TOK_TSFi = address(0x4243568Fa2bbad327ee36e06c16824cAd8B37819);
    address public constant TOK_R = address(0x557F7e30aA6D909Cfe8a229A4CB178ab186EC622);
    address public constant TOK_BEAR9 = address(0x1f737F7994811fE994Fe72957C374e5cD5D5418A);

    address public constant TOK_pWBTC = address(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    address public constant TOK_pUSDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    address public constant TOK_pWETH = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    address public constant TOK_pUSDT = address(0xdAC17F958D2ee523a2206206994597C13D831ec7);
    
    // address private constant LP_WALLET = address(0xEEd80539c314db19360188A66CccAf9caC887b22);

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ ADMIN SUPPORT _ */
    string public tVERSION = '0.0';
    address public KEEPER;

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
    event FlashLoansReceived(IERC20[] tokens, uint256[] amounts, uint256[] feeAmounts, bytes userData);
    event FlashLoansReturned(IERC20[] _tokens, uint256[] _amounts, uint256[] _feeAmounts, uint256[] _amountsOwed);

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

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE
    /* -------------------------------------------------------- */
    // front-facing UI to initialize flash-loan
    function makeFlashLoan(IERC20[] memory _tokens, uint256[] memory _amounts, bytes memory _userData) external onlyKeeper {
        // require(msg.sender == owner(), "loan to owner only");
        vault.flashLoan(this, _tokens, _amounts, _userData);
        emit FlashLoansRequested(_tokens, _amounts, _userData);
    }

    // callback from vault with loaned funds
    function receiveFlashLoan(IERC20[] memory tokens, uint256[] memory amounts, uint256[] memory feeAmounts, bytes memory userData) external override {
        emit FlashLoansReceived(tokens, amounts, feeAmounts, userData);
        require(msg.sender == address(vault), " loan from vault only :o ");
        require(tokens.length == amounts.length && amounts.length == feeAmounts.length, ' array lengths mismatch :/ ');
        // (address router_0, address router_1, address[] memory path_0, address[] memory path_1, uint256 amntIn_0, uint256 amntOutMin_1) = abi.decode(userData, (address, address, address[], address[], uint256, uint256));
        
        uint256 bal = IERC20(tokens[0]).balanceOf(address(this));
        
        // payback loans
        uint256[] memory amountsOwed = new uint256[](amounts.length); 
        for (uint8 i=0; i < amountsOwed.length;) {
            amountsOwed[i] = amounts[i] + feeAmounts[i];
            IERC20(tokens[i]).transfer(address(vault), amountsOwed[i]);
            unchecked { i++; }
        }
        // amountsOwed[0] = amounts[0] + feeAmounts[0];
        // IERC20(tokens[0]).transfer(address(vault), amountsOwed[0]);
        emit FlashLoansReturned(tokens, amounts, feeAmounts, amountsOwed);
    }
    
    receive() external payable {}
}
