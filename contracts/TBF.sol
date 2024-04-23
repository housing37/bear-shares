// SPDX-License-Identifier: UNLICENSED
// ref: https://ethereum.org/en/history
//  code size limit = 24576 bytes (a limit introduced in Spurious Dragon _ 2016)
//  code size limit = 49152 bytes (a limit introduced in Shanghai _ 2023)
pragma solidity ^0.8.24;        

// inherited contracts
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; // deploy
// import "@openzeppelin/contracts/access/Ownable.sol"; // deploy

// local _ $ npm install @openzeppelin/contracts
import "./node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol"; 
import "./node_modules/@openzeppelin/contracts/access/Ownable.sol";

contract TheBotFckr is ERC20, Ownable {
    address public constant TOK_WPLS = address(0xA1077a294dDE1B09bB078844df40758a5D0f9a27);
    address public constant BURN_ADDR = address(0x0000000000000000000000000000000000000369);

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    string public tVERSION = '4.3'; // 3.0 deployed with 50 TBF in LP
    string private TOK_SYMB = string(abi.encodePacked("TBF", tVERSION));
    // string private TOK_NAME = string(abi.encodePacked("tTheBotFckr_", tVERSION));
    // string private TOK_SYMB = "TBF";
    string private TOK_NAME = "TheBotFckr";

    /* _ ADMIN SUPPORT _ */
    address public KEEPER;
    bool private OPEN_BUY;
    bool private OPEN_SELL;
    address[] private WHITELIST_ADDRS;
    address[] private WHITELIST_LPS;
    mapping(address => bool) public WHITELIST_ADDR_MAP;
    mapping(address => bool) public WHITELIST_LP_MAP;

    /* -------------------------------------------------------- */
    /* STRUCTS                                        
    /* -------------------------------------------------------- */

    /* -------------------------------------------------------- */
    /* EVENTS                                        
    /* -------------------------------------------------------- */
    event KeeperTransfer(address _prev, address _new);
    event TokenNameSymbolUpdated(string TOK_NAME, string TOK_SYMB);
    event OpenBuySellUpdated(bool _prev_0, bool _prev_1, bool _new_0, bool _new_1);
    event WhitelistAddressUpdated(address _address, bool _add);
    event WhitelistAddressUpdatedLP(address _address, bool _add);

    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(TOK_NAME, TOK_SYMB) Ownable(msg.sender) {
        // set default globals
        OPEN_BUY = true; // start w/ open buys enabled
        OPEN_SELL = false; // start w/ open sells disabled
        KEEPER = msg.sender;
        _editWhitelistAddress(KEEPER, true); // true = _add
        _mint(KEEPER, _initSupply * 10**uint8(decimals())); // 'emit Transfer'

        // add default routers: pulsex x2 (for creating LPs)
        _editWhitelistAddress(address(0x98bf93ebf5c380C0e6Ae8e192A7e2AE08edAcc02), true); // pulseX v1, true = add
        _editWhitelistAddress(address(0x165C3410fC91EF562C50559f7d2289fEbed552d9), true); // pulseX v2, true = add        

        // add default EOA whitelisted
        _editWhitelistAddress(address(0xEEd80539c314db19360188A66CccAf9caC887b22), true); // EOA test, true = add
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
    function KEEPER_setKeeper(address _newKeeper) external onlyKeeper {
        require(_newKeeper != address(0), ' 0 address :/ ');
        address prev = address(KEEPER);
        KEEPER = _newKeeper;
        emit KeeperTransfer(prev, KEEPER);
    }
    function KEEPER_setTokNameSymb(string memory _tok_name, string memory _tok_symb) external onlyKeeper() {
        require(bytes(_tok_name).length > 0 && bytes(_tok_symb).length > 0, ' invalid input  :<> ');
        TOK_NAME = _tok_name;
        TOK_SYMB = _tok_symb;
        emit TokenNameSymbolUpdated(TOK_NAME, TOK_SYMB);
    }
    // set 'transfer' on|off for non-whitelist wallets and LPs
    function KEEPER_setOpenBuySell(bool _openBuy, bool _openSell) external onlyKeeper() {
        bool prev_0 = _openBuy;
        bool prev_1 = _openSell;
        OPEN_BUY = _openBuy;
        OPEN_SELL = _openSell;
        emit OpenBuySellUpdated(prev_0, prev_1, OPEN_BUY, OPEN_SELL);
    }
    function KEEPER_editWhitelistAddress(address _address, bool _add) external onlyKeeper() {
        require(_address != address(0), ' 0 address :/ ');
        _editWhitelistAddress(_address, _add);
        emit WhitelistAddressUpdated(_address, _add);
    }
    function KEEPER_editWhitelistAddressLP(address _address, bool _add) external onlyKeeper() {
        require(_address != address(0), ' 0 address :/ ');
        _editWhitelistAddressLP(_address, _add);
        emit WhitelistAddressUpdatedLP(_address, _add);
    }
    

    /* -------------------------------------------------------- */
    /* PUBLIC - ACCESSORS
    /* -------------------------------------------------------- */
    function getWhitelistAddressesLP() external view returns (address[] memory) {
        return WHITELIST_LPS;
    }
    function getWhitelistAddresses() external view returns (address[] memory) {
        return WHITELIST_ADDRS;
    }
    function getOpenBuySell() external view returns (bool, bool) {
        return (OPEN_BUY, OPEN_SELL);
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE - TBF
    /* -------------------------------------------------------- */
    // randomly mix up balances of all wallets within '_wallets'
    //  using '_transfer': forces execution of 'emit Transfer(from, to, value);'
    //   (ie. dexes and explorers pickup on 'Transfer' events)
    // NOTE: ensures all addresses in '_wallets' are whitelisted for transfers
    //
    // Enter params for: "KEEPER_mixAmntRand(address[])"
    // > [0x23F953a5cDB6A2fE4b4B5119dA9B62fCCc6280AB,0x6EA731608dfab76Cfb9D2DEf2C71b25cA3985f1b,0xEEd80539c314db19360188A66CccAf9caC887b22]
    function KEEPER_mixAmntRand(address[] memory _wallets) external onlyKeeper { // chatGPT :-)
        require(_wallets.length > 1, " invalid inputs :( ");
        // uint totalWallets = _wallets.length;

        for (uint8 i = 0; i < _wallets.length;) {            
            // get random amount lower than balance of _wallets[i]
            uint validRandAmnt = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % balanceOf(_wallets[i]);

            // Select a random recipient different from sender (ie. _wallets[i])
            uint recipientIndex = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % _wallets.length;
            while (recipientIndex == i) {
                recipientIndex = uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, recipientIndex))) % _wallets.length;
            }
            _transfer(_wallets[i], _wallets[recipientIndex], validRandAmnt);

            // ensure wallet is whitelisted for transfers
            _editWhitelistAddress(_wallets[i], true); // true = _add
            unchecked { i++; }
        }
    }

    // randomly distribute '_distrAmnt' from msg.sender token balance
    //  distribute randomly among '_wallets'
    // NOTE: ensure all addresses in '_wallets' are whitelisted for transfers
    //
    // Enter params for: "distrAmntRand(uint64,address[])"
    // > 1000 [0x23F953a5cDB6A2fE4b4B5119dA9B62fCCc6280AB,0x6EA731608dfab76Cfb9D2DEf2C71b25cA3985f1b,0xEEd80539c314db19360188A66CccAf9caC887b22]
    function distrAmntRand(uint64 _distrAmnt, address[] memory _wallets) external { // chatGPT :-)
        require(_distrAmnt > 0 && _wallets.length > 0, " invalid input :( ");
        require(balanceOf(msg.sender) >= _distrAmnt, ' low balance :{} ');
        
        uint remainingAmount = _distrAmnt;
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
            uint transAmnt = (portions[x] * _distrAmnt) / totalPortions;
            _transfer(msg.sender, _wallets[x], transAmnt); // send transAmnt payout

            // ensure wallet is whitelisted for transfers
            _editWhitelistAddress(_wallets[x], true); // true = _add
            unchecked { x++; }
        }
    }

    /* -------------------------------------------------------- */
    /* PUBLIC - USER INTERFACE
    /* -------------------------------------------------------- */
    // handle contract USD value deposits (convert PLS to USD stable)
    receive() external payable {
        // extract PLS value sent
        // uint256 amntIn = msg.value;
        // address from = msg.sender;
    }

    /* -------------------------------------------------------- */
    /* PRIVATE - SUPPORTING                                     */
    /* -------------------------------------------------------- */
    function _editWhitelistAddressLP(address _address, bool _add) private { // allows duplicates
        WHITELIST_LP_MAP[_address] = _add;
        if (_add) {
            WHITELIST_LPS = _addAddressToArraySafe(_address, WHITELIST_LPS, true); // true = no dups            
        } else {
            WHITELIST_LPS = _remAddressFromArray(_address, WHITELIST_LPS);
        }
    }
    function _editWhitelistAddress(address _address, bool _add) private { // allows duplicates
        WHITELIST_ADDR_MAP[_address] = _add;
        if (_add) {
            WHITELIST_ADDRS = _addAddressToArraySafe(_address, WHITELIST_ADDRS, true); // true = no dups            
        } else {
            WHITELIST_ADDRS = _remAddressFromArray(_address, WHITELIST_ADDRS);
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
    // function _perc_of_uint64(uint32 _perc, uint64 _num) private pure returns (uint64) {
    //     require(_perc <= 10000, 'err: invalid percent');
    //     return _perc_of_uint64_unchecked(_perc, _num);
    // }
    // function _perc_of_uint64_unchecked(uint32 _perc, uint64 _num) private pure returns (uint64) {
    //     // require(_perc <= 10000, 'err: invalid percent');
    //     uint32 aux_perc = _perc * 100; // Multiply by 100 to accommodate decimals
    //     uint64 result = (_num * uint64(aux_perc)) / 1000000; // chatGPT equation
    //     return result; // uint64 max USD: ~18T -> 18,446,744,073,709.551615 (6 decimals)

    //     // NOTE: more efficient with no local vars allocated
    //     // return (_num * uint64(uint32(_perc) * 100)) / 1000000; // chatGPT equation
    // }
    // function _uint64_from_uint256(uint256 value) private pure returns (uint64) {
    //     require(value <= type(uint64).max, "Value exceeds uint64 range");
    //     uint64 convertedValue = uint64(value);
    //     return convertedValue;
    // }

    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    function symbol() public view override returns (string memory) {
        return TOK_SYMB; // return _symbol;
    }
    function name() public view override returns (string memory) {
        return TOK_NAME; // return _name;
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

    /** # tTBF2.1: 0xb945c455b1Ed7Ebd4a92c8C9A41BBD9f64bA0890 -> LP wiped */
    // // transfer executes when this contract is the swap 'in' token 
    // //      (ie. is 'buy' | transfer from LP)
    // //  'msg.sender' = LP address
    // //          'to' = buyer address
    // //
    // // NOTE: live testing ... a sell w/ 'transfer'
    // //   'msg.sender' = non-whitelist address
    // //           'to' = whitelist LP address
    // function transfer(address to, uint256 value) public override returns (bool) {

    //     // if open buy and open sell, let it go through
    //     if (OPEN_BUY && OPEN_SELL) {
    //         return super.transfer(to, value);
    //     }

    //     // if involving a whitelisted address, let it always go through
    //     if (WHITELIST_ADDR_MAP[msg.sender] || WHITELIST_ADDR_MAP[to]) {
    //         return super.transfer(to, value);
    //     }

    //     // if transfer 'to' is an LP, then its a 'sell'
    //     //  if OPEN_SELL not enabled, simualte error
    //     if (WHITELIST_LP_MAP[to] && !OPEN_SELL) {
    //         revert ERC20InvalidSender(msg.sender); // _transfer
    //     }

    //     // if transfer 'msg.sender' is an LP, then its a 'buy'
    //     //  if OPEN_BUY not enabled, simulate error
    //     if (WHITELIST_LP_MAP[msg.sender] && !OPEN_BUY) {
    //         revert ERC20InvalidSender(msg.sender); // _transfer
    //     }

    //     // all other cases, let it go through
    //     return super.transfer(to, value);
        
    // }

    // // transferFrom executes when this contract is the swap 'out' token 
    // //      (ie. is 'sell' | transfer to LP)
    // //  'from' = seller address
    // //    'to' = LP address
    // function transferFrom(address from, address to, uint256 value) public override returns (bool) {

    //     // if open buy and open sell, let it go through
    //     if (OPEN_BUY && OPEN_SELL) {
    //         return super.transferFrom(from, to, value);
    //     }

    //     // if involving a whitelisted address, let it always go through
    //     if (WHITELIST_ADDR_MAP[from] || WHITELIST_ADDR_MAP[to]) {
    //         return super.transferFrom(from, to, value);
    //     }

    //     // if transferFrom 'to' is an LP, then its a 'sell'
    //     //  if OPEN_SELL not enabled, simulate error
    //     if (WHITELIST_LP_MAP[to] && !OPEN_SELL) {
    //         revert ERC20InvalidReceiver(to); // _transfer
    //     }

    //     // if transferFrom 'from' is an LP, then its a 'buy'
    //     //  if OPEN_BUY not enabled, simulate error
    //     if (WHITELIST_LP_MAP[from] && !OPEN_BUY) {
    //         revert ERC20InvalidReceiver(to); // _transfer
    //     }

    //     // all other cases, let it go through
    //     return super.transferFrom(from, to, value);
    // }

    /** LEGACY re-tested_042124: 
        # tTBF3.0: 0x8fd10330363C85F6a2bE61EbDeCB66894f545Be7 -> LP created
        - note_042224: https://otter.pulsechain.com/tx/0x36409ccc2c693b02ee7c75158f51c321ef11664aa6ac40b6b42a34afc2f67cdb/trace
            - found successful sell from non-whitelist account w/ options set: yes open buy, no open sell
                tx hash: 0x36409ccc2c693b02ee7c75158f51c321ef11664aa6ac40b6b42a34afc2f67cdb
                used: 'transfer' w/ 'to' = PLP3.0 (0x41e191f8E957c5CfCA6706F54455e1428943B480)
		- the following works as expected…
			- from my whitelist accounts: yes buy, yes sell
			- from my non-whitelist accounts: yes buy, no sell
			- from my non-whitelist accounts: yes buy, yes sell
			- from my non-whitelist accounts: no buy, yes sell
			- from my non-whitelist accounts: no buy, no sell
		- simplified…
			open buy  = on|off …. works as expected for both whitelist and non-whitelist
			open sell = on|off …. works as expected for both whitelist and non-whitelist
     */
    /** LEGACY -> # tTBF0: 0x588bDc5F0b1aE0AB2AB45995EFD368D8f1A09D04 -> LP wiped */
    // transfer executes when this contract is the swap 'in' token 
    //      (ie. is 'buy' | transfer from LP)
    //  'msg.sender' = LP address
    //          'to' = buyer address
    function transfer(address to, uint256 value) public override returns (bool) {
        // fix_attempt: found successful sell from non-whitelist account w/ OPEN_SELL==false
        //  TESTED w/ TBF4.0 (then disabled)
        //  NOTE: requires adding LP created to WHITELIST_ADDR_MAP (else, if statement fails for all swaps)
        //          tested OK: rejects all non-whitelisted sells & accepts all whitelisted sells
        //                      rejects all non-whitelisted 'transfers'
        //          might want to disabled this check (since people can't freely use transfer)
        //          maybe update this check to use WHITELIST_LP_MAP instead?
        // if (!WHITELIST_ADDR_MAP[msg.sender] && !OPEN_SELL) {
        //     // else, simulate error: invalid LP address
        //     revert ERC20InvalidSender(msg.sender); // _transfer            
        // }

        // allow if buyer is white listed | OPEN_BUY enabled
        if (WHITELIST_ADDR_MAP[to] || OPEN_BUY) {
            return super.transfer(to, value);
        }
 
        // else, simulate error: invalid LP address
        revert ERC20InvalidSender(msg.sender); // _transfer
    }
 
    // transferFrom executes when this contract is the swap 'out' token 
    //      (ie. is 'sell' | transfer to LP)
    //  'from' = seller address
    //    'to' = LP address
    function transferFrom(address from, address to, uint256 value) public override returns (bool) {
        // allow if sell is whitelisted | OPEN_SELL enabled
        if (WHITELIST_ADDR_MAP[from] || OPEN_SELL) {
            return super.transferFrom(from, to, value);
        }
 
        // else, simulate error: invalid LP address
        revert ERC20InvalidReceiver(to); // _transfer
    }
}

// // simulate error: if not whitelist of open buy|sell is off
// revert ERC20InvalidSender(address(0)); // _transfer
// revert ERC20InvalidReceiver(address(0)); // _transfer
// revert ERC20InsufficientBalance(from, fromBalance, value); // _transfer -> _update
// revert ERC20InsufficientAllowance(spender, currentAllowance, value); // transferFrom -> _spendAllowance
