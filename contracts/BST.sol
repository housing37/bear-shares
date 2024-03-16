// SPDX-License-Identifier: MIT
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.20;        

// interfaces
import "./IGTADelegate.sol";
import "./IGTALib.sol";

// inherited contracts
import "./GTASwapTools.sol"; // deploy|local
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
contract BearSharesTrinity is ERC20, Ownable, GTASwapTools {
    uint8 public VERSION = 0;

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ ADMIN SUPPORT _ */
    // IGTADelegate private GTAD; // 'keeper' maintained within
    // IGTALib private GTAL;
    
    /* _ TOKEN INIT SUPPORT _ */
    string private constant tok_name = "BearSharesTrinity";
    string private constant tok_symb = "BST";
    // string private tok_name = string(abi.encodePacked("tGTA ", VERSION));
    
    struct ACCT_PAYOUT {
        address receiver;
        uint64 usdAmnt; // USD total ACCT deduction
        uint46 usdFee; // USD service fee amount
        uint46 usdBurn; // USD burn value
        uint46 usdPayout; // USD payout value
        uint64 bstBurn; // BST burn amount
        uint46 bstPayout; // BST payout amount
    }
    // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)
    mapping(address => uint64) public ACCT_USD_BALANCES;
    uint8 public SERVICE_FEE_PERC = 0; // 0%
    uint8 public SERVICE_BURN_PERC = 0; // 0%
    bool public ENABLE_BUY_BURN = false;

    mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;
    // address[] private creditsAddrArray;

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
        setServiceFeePerc(5);
        setServiceBurnPerc(5);
        _mint(msg.sender, _initSupply * 10**uint8(decimals())); // 'emit Transfer'
    }

    /* -------------------------------------------------------- */
    /* MODIFIERS                                                */
    /* -------------------------------------------------------- */
    // modifier onlyKeeper() {
    //     require(msg.sender == GTAD.keeper(), "!keeper :p");
    //     _;
    // }
    // modifier onlyHolder(uint256 _requiredAmount) {
    //     require(balanceOf(msg.sender) >= _requiredAmount || msg.sender == GTAD.keeper(), 'GTA bal');
    //     _;
    // }

    /* -------------------------------------------------------- */
    /* PUBLIC ACCESSORS - KEEPER SUPPORT                        */
    /* -------------------------------------------------------- */
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
    function payBSD(uint64 _usdAmnt, address _to) public {
        require(ACCT_USD_BALANCES[msg.sender] >= _usdAmnt, 'err: low acct balance :{}');
        require(_to != address(0), 'err: _to address');

        // calc & remove service fee & burn amount
        uint64 usdFee = _usdAmnt * (SERVICE_FEE_PERC/100); 
        uint64 usdBurn = _usdAmnt * (SERVICE_BURN_PERC/100); 
        uint64 usdPayout = _usdAmnt - usdFee - usdBurn;
        uint64 bstBurn = _getBstValueForUsdAmnt(usdBurn);
        uint64 bstPayout = _getBstValueForUsdAmnt(usdPayout);
        uint64 bstPayoutRem = 0;
        uint64 bstBurnRem = 0;
        uint64 thisBstBal = IERC20(address(this)).balanceOf(address(this));

        // log this payout
        ACCT_USD_PAYOUTS[msg.sender].push(ACCT_PAYOUT(_usdAmnt, usdFee, usdBurn, usdPayout, bstBurn, bstPayout));

        // update account balance
        ACCT_USD_BALANCES[msg.sender] = ACCT_USD_BALANCES[msg.sender] - _usdAmnt;

        // ALGORITHMIC INTEGRATION...
        //  1) always pay w/ contract BST holdings first
        //  2) after holdings runs out, 
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstPayoutRem
        //      else, mint new BST for bstPayoutRem
        //  3) if no BST holdings at all,
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstPayout
        //      else, mint new BST for bstPayout
        // execute payout requirements
        if (thisBstBal >= bstPayout) {
            // transfer all of bstPayout to '_to'
            _transfer(address(this), _to, bstPayout);
        } else if (thisBstBal > 0) {
            // transfer all of thisBstBal to '_to'
            _transfer(address(this), _to, thisBstBal);
            bstPayoutRem = bstPayout - thisBstBal;

            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... 
                //  buy 'bstPayoutRem' from dex
                //  then, transfer 'bstPayoutRem' over to '_to'
            } else {
                // mint remaining bstPayout thats owed
                _mint(_to, bstPayoutRem);
            }

        } else {
            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... 
                //  buy 'bstPayout' from dex
                //  then, transfer 'bstPayout' over to '_to'
            } else {
                // mint all of bstPayout owed
                _mint(_to, bstPayout);
            }
        }

        // ALGORITHMIC INTEGRATION...
        //  1) always burn from contract BST holdings first
        //  2) after holdings runs out, 
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstBurnRem
        //      else, do nothing (don't mint bstBurnRem)
        //  3) if no BST holdings at all,
        //      if ENABLE_BUY_BURN, buy BST from dexes for bstBurn
        //      else, do nothing (don't mint bstBurn)
        // execute burn requirements
        if (thisBstBal >= bstBurn) {
            // burn all of bstBurn to 0x0
            _transfer(address(this), 0x0, bstBurn);
        } else if (thisBstBal > 0) {
            // burn all of thisBstBal to 0x0
            _transfer(address(this), 0x0, thisBstBal);
            bstBurnRem = bstBurn - thisBstBal;

            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... 
                //  buy 'bstBurnRem' from dex
                //  then, burn 'bstBurnRem'
            } else {
                // mint remaining bstPayout thats owed
                // _mint(_to, bstBurnRem);
                // ... don't mint anything?
            }
        } else {
            if (ENABLE_BUY_BURN) {
                // LEFT OFF HERE ... 
                //  buy 'bstPayout' from dex
                //  then, burn 'bstPayout'
            } else {
                // mint all of bstPayout owed
                // _mint(_to, bstPayout);
                // ... do nothing?
            }
        }
    }
    function _getBstValueForUsdAmnt(uint64 _usdAmnt) private returns (uint64) {
        return 37; 
        // LEFT OFF HERE ... TODO
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
    receive() external payable {
        // Handle Ether sent without any data
        // This function will be called when Ether is sent without any data
        // Extract sender's address and amount received
        sender = msg.sender;
        amountReceived = msg.value;

        // LEFT OFF HERE ... swap 'amountReceived' PLS for USD stable
        //  then update ACCT_USD_BALANCES for msg.sender
        //  NOTE: 'amountReceived' needs to have some min required

        // ACCT_USD_BALANCES[msg.sender] += <usd_stable_amnt>
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

    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    function decimals() public view override returns (uint8) {
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
