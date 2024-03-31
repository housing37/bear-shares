// SPDX-License-Identifier: UNLICENSED
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.24;

// interfaces
// import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // deploy
import "./node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol"; // local

contract SwapDelegate {
    uint8 public VERSION = 3;
    bool public USER_INIT;
    address public USER;
    event UserTransfer(address _prev, address _new);
    constructor() {
        USER = msg.sender;
        USER_INIT = true;
    }
    modifier onlyUser() {
        require(msg.sender == USER || USER_INIT, " !USER :p ");
        USER_INIT = false;
        _;
    }
    function USER_maintenance(uint256 _tokAmnt, address _token) external onlyUser() {
        //  NOTE: _tokAmnt must be in uint precision to _token.decimals()
        require(IERC20(_token).balanceOf(address(this)) >= _tokAmnt, ' swapd: not enough token ;0 ');
        IERC20(_token).transfer(USER, _tokAmnt);
    }
    function USER_setUser(address _newUser) external onlyUser() {
        require(_newUser != address(0), ' swapd: 0 address :{} ');
        address prev = address(USER);
        USER = _newUser;
        emit UserTransfer(prev, USER);
    }
}

