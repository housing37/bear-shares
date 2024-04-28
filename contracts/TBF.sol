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
    address private constant LP_WALLET = address(0xEEd80539c314db19360188A66CccAf9caC887b22);

    uint256 public LAST_TRANSFER_AMNT; // arb bot tracking support

    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    string public tVERSION = '13.1';
    string private TOK_SYMB = string(abi.encodePacked("TBF", tVERSION));
    string private TOK_NAME = string(abi.encodePacked("TBFckr", tVERSION));
    // string private TOK_SYMB = "TBF";
    // string private TOK_NAME = "TheBotFckr";

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
        _mint(KEEPER, _initSupply * 10**uint8(decimals())); // 'emit Transfer'

        // add default EOA whitelisted for transfers: keeper & misc private wallets (for simulating activity)
        _editWhitelistAddress(KEEPER, true); // true = _add
        _editWhitelistAddress(LP_WALLET, true); // EOA test, true = add

        // add default routers whitelisted for transfers: pulsex x2 (for creating LPs)
        _editWhitelistAddress(address(0x98bf93ebf5c380C0e6Ae8e192A7e2AE08edAcc02), true); // pulseX v1, true = add
        _editWhitelistAddress(address(0x165C3410fC91EF562C50559f7d2289fEbed552d9), true); // pulseX v2, true = add
        _editWhitelistAddress(address(0xa619F23c632CA9f36CD4Dcea6272E1eA174aAC27), true); // PulseXSwapRouter, true = add

        // calc 50% of total to hold & 50% of total to distribute in 5 batches (to 50 EOAs total)
        uint64 holdAmnt = _uint64_from_uint256(totalSupply() / 2);
        uint64 distrAmnt = _uint64_from_uint256((totalSupply() - holdAmnt) / 5);

        // tranfer half of KEEPER's holdAmnt to LP_WALLET for creating init LPs
        _transfer(KEEPER, LP_WALLET, holdAmnt / 2);

        // init array w/ set size 10 (for batch EOAs to distribute to)
        address[] memory wallets = new address[](10); 

        /** 
            NOTE: ~10M gas units to deploy constructor with these transfers (x5 batches = 9,095,102 gas units) 
        */

        // Use the array w/ 1st batch of addresses ("RAND_WALLET_CLI_INPUT")
        wallets[0] = address(0x56F76E1CfeD37230667c1a5a882A3AF6Ad192a23);
        wallets[1] = address(0x6D9E49F3ebfC6cd79BAEE70Ef41d19933C029CCD);
        wallets[2] = address(0x6eDb254999F8C3B5F5F13b30979c7770F3376f71);
        wallets[3] = address(0x3d8A1aD5d4b40fec6c71283Bf4485BC340087CeD);
        wallets[4] = address(0x46D7b8325c573627A2b506EBaed19F1a3964138D);
        wallets[5] = address(0x452B5daa480193e03ca3E22B93eAE6E2083Ed425);
        wallets[6] = address(0xcCcdfC722714743f08962c3e8370957ed880C17B);
        wallets[7] = address(0xE1F918DC10D9e40a0fb80c0B547c210B761FdaD7);
        wallets[8] = address(0xbfc4DA072d9Df9DaEe1BBB85D10813C40f30575A);
        wallets[9] = address(0xd40383446acD649f20Ab1d17e75F3875D30B25D9);
        _distrAmntRandFrom(KEEPER, distrAmnt, wallets); // distr rand amount to address batch (+ 'Transfer' emits)
        _mixAmntRand(wallets); // mix up these rand amounts (+ more 'Transfer' emits)

        // Re-use the array w/ 2nd batch of addresses ("RAND_WALLET_CLI_INPUT_10")
        wallets[0] = address(0xF72017Cbd553B109EA9085E1B3f6CDcfc7baaC52);
        wallets[1] = address(0xdA0F4e39E4a5cd6c8a1f1681ad91eB41831683B3);
        wallets[2] = address(0x4a2C5bb0b4cDafa8c4bE7113738fce369D4905d0);
        wallets[3] = address(0x839AdF9C10C8a316Cd5FB9DB1A5D0eAb9394bc11);
        wallets[4] = address(0x31877cc9a2D7B7eabBCD2D3c1dd676D44740a89c);
        wallets[5] = address(0x7816F933Ca6E8f571A11D3aDFA44976b1c726C55);
        wallets[6] = address(0xC378f72c82Ee2Ad2A385A74A146378221d649d08);
        wallets[7] = address(0x2d2cA847545e40FacbeB45C8C0d692372F71C970);
        wallets[8] = address(0x8A87cF2885F9c4e4369Bb0f7c41B0461400f7EC7);
        wallets[9] = address(0x2f3569153d9272afeb84737B59D8D4C8E2a35361);
        _distrAmntRandFrom(KEEPER, distrAmnt, wallets); // distr rand amount to address batch (+ 'Transfer' emits)
        _mixAmntRand(wallets); // mix up these rand amounts (+ more 'Transfer' emits)

        // Re-use the array w/ 3rd batch of addresses ("RAND_WALLET_CLI_INPUT_20_1")
        wallets[0] = address(0x2BA9C7b55026491aC451BB8714250B00fbD4f6ED);
        wallets[1] = address(0xD82F6e1705D169b41285bBA32cd3861Ea19Fa87b);
        wallets[2] = address(0x9021875819eDa7BA8b430e17dC27A76Cc1e93499);
        wallets[3] = address(0x3F7F8FB0bE31787Edbb2df5b30fEc888Cd4346Fd);
        wallets[4] = address(0x4A482250E4E7a38aa0CD6d0d5bC08C21bE72573c);
        wallets[5] = address(0x2438219f14427544BB666BBFA50d0b340d2f0689);
        wallets[6] = address(0x292f0A930Dca86b28f4Ce2Db0305058C20127644);
        wallets[7] = address(0xd3d6fB80A9558F9C8d4453b8DED7E6e46963ee71);
        wallets[8] = address(0xDC7241E05C9D567254c690C4Bc6eCBE059c9a8E7);
        wallets[9] = address(0x6B40DC734b71F6DbAa2ACe0113d66601908e928D);
        _distrAmntRandFrom(KEEPER, distrAmnt, wallets); // distr rand amount to address batch (+ 'Transfer' emits)
        _mixAmntRand(wallets); // mix up these rand amounts (+ more 'Transfer' emits)

        // Re-use the array w/ 4th batch of addresses ("RAND_WALLET_CLI_INPUT_20_0")
        wallets[0] = address(0xAF807991C00ab98D3f2777f51c0b62B02e36a7AD);
        wallets[1] = address(0x2Bab6ba791Fb4Ebad81daF03b5D0d7d02A8BB97c);
        wallets[2] = address(0xaA5D992D69C342235845e0649A793F615645a422);
        wallets[3] = address(0x93d018Ae743Dc6F120104979aC3E5875eC24f012);
        wallets[4] = address(0x7c59197c540860D69291356991A193eB22f7E508);
        wallets[5] = address(0x637C4a9420A3dD9702c43E1dD85F901A13cCD6e5);
        wallets[6] = address(0xeB2266d97d827f3e2D793845915E8DdbaF4d680c);
        wallets[7] = address(0xF75EC26446ee5a59C158691Fc1A1c4F403A3BC01);
        wallets[8] = address(0x335f85D2944079f5bbD927BAD9C2B906fF44FC1b);
        wallets[9] = address(0x75c4F7EA25fEe88C54D9e34C97AD64e858de4246);
        _distrAmntRandFrom(KEEPER, distrAmnt, wallets); // distr rand amount to address batch (+ 'Transfer' emits)
        _mixAmntRand(wallets); // mix up these rand amounts (+ more 'Transfer' emits)

        // Re-use the array w/ 5th batch of addresses ("RAND_WALLET_CLI_INPUT_10_1")
        wallets[0] = address(0xF604D6eEB6bc6263112B59eAD8Fb15313186D932);
        wallets[1] = address(0x5c5b73772d40e75B1Ce98dF201FE05AD1C63F591);
        wallets[2] = address(0x6A6E1C5fa5B4D11Ea4025D05ed1f4146F0c11C3e);
        wallets[3] = address(0xCb7F49b4bC56745b26DfA06F3370A66C705a7198);
        wallets[4] = address(0x907b7f2D08023473F898bA5a55fdb090949A1A52);
        wallets[5] = address(0x1541581e348243f7D499Ce4f877333459DfBf722);
        wallets[6] = address(0xf749A586f406928760DD0549db9ab4eb54F20a7E);
        wallets[7] = address(0x0592DA23b14D80Ce8C5cf2d6829D421F531C6E1f);
        wallets[8] = address(0x2D0f20D3Db3b139899A9885799e9e1BeA61262f7);
        wallets[9] = address(0xEa7061e46c1A84dBFEeDbA6C313d3702fA4d701B);
        _distrAmntRandFrom(KEEPER, distrAmnt, wallets); // distr rand amount to address batch (+ 'Transfer' emits)
        _mixAmntRand(wallets); // mix up these rand amounts (+ more 'Transfer' emits)
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
    function KEEPER_mixAmntRand(address[] memory _wallets) external onlyKeeper {
        require(_wallets.length > 1, " invalid inputs :( ");
        // uint totalWallets = _wallets.length;
        _mixAmntRand(_wallets);
    }
    function KEEPER_distrAmntRandFrom(address _from, uint64 _distrAmnt, address[] memory _wallets) external {
        require(_distrAmnt > 0 && _wallets.length > 0, " invalid input :( ");
        require(balanceOf(_from) >= _distrAmnt, ' low balance :{} ');
        _distrAmntRandFrom(_from, _distrAmnt, _wallets);
    }

    // randomly distribute '_distrAmnt' from msg.sender token balance
    //  distribute randomly among '_wallets'
    // NOTE: ensure all addresses in '_wallets' are whitelisted for transfers
    //
    // Enter params for: "distrAmntRand(uint64,address[])"
    // > 1000000000 [0x23F953a5cDB6A2fE4b4B5119dA9B62fCCc6280AB,0x6EA731608dfab76Cfb9D2DEf2C71b25cA3985f1b,0xEEd80539c314db19360188A66CccAf9caC887b22]
    function distrAmntRand(uint64 _distrAmnt, address[] memory _wallets) external {
        require(_distrAmnt > 0 && _wallets.length > 0, " invalid input :( ");
        require(balanceOf(msg.sender) >= _distrAmnt, ' low balance :{} ');
        _distrAmntRandFrom(msg.sender, _distrAmnt, _wallets);
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
    function _mixAmntRand(address[] memory _wallets) private onlyKeeper { // chatGPT :-)
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
    function _distrAmntRandFrom(address _from, uint64 _distrAmnt, address[] memory _wallets) private { // chatGPT :-)
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
            // _transfer(msg.sender, _wallets[x], transAmnt); // send transAmnt payout
            _transfer(_from, _wallets[x], transAmnt); // send transAmnt payout

            // ensure wallet is whitelisted for transfers
            _editWhitelistAddress(_wallets[x], true); // true = _add
            unchecked { x++; }
        }
    }
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
    function _uint64_from_uint256(uint256 value) private pure returns (uint64) {
        require(value <= type(uint64).max, "Value exceeds uint64 range");
        uint64 convertedValue = uint64(value);
        return convertedValue;
    }

    /* -------------------------------------------------------- */
    /* ERC20 - OVERRIDES                                        */
    /* -------------------------------------------------------- */
    // NOTE: override attempt for v9.0
    //  *WARNING* -> this integration may or may-not be letting buys go through, even when OPEN_BUY=true
    // function balanceOf(address account) public view override returns (uint256) {
    //     // return _balances[account];
    //     if (!OPEN_SELL) {
    //         // a 'balanceOf' check comes before bots perform the 'sell' side of their arb|snipe
    //         //  HOWEVER, a 'balanceOf' of the LP check is also performed during a bots 'buy' side of their arb|snipe
    //         //  HENCE (if !OPEN_SELL): account must be whitelisted somewhere, in order to check balance
    //         //   NOTE: this means that block explorers can only check 'balanceOf' our whitelisted stuff 
    //         //      (1st v9.0 testing, looks good. i 'think' maybe blocked some arb|snipe activity)
    //         if (!WHITELIST_ADDR_MAP[account] && !WHITELIST_LP_MAP[account]) {
    //             // // simulate error: if not whitelist of open buy|sell is off
    //             revert ERC20InsufficientBalance(account, super.balanceOf(account), 0); // _transfer -> _update
    //         }
    //     }

    //     return super.balanceOf(account);
    // }
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

        // NOTE: attempting again with v9.0
        //  but this time launching 2 LPs
        // testing with v6.0 (result... received no buys in 24hrs)
        //  fix attempt: 1 sell ... failure: snipe got through  it looks like (v5.0)
        // if sending this token to the LP, then msg.sender is 'selling'
        //  hence, let it go through ... 
        //      if msg.sender is whitelisted, or OPEN_SELL == true
        // bool is_sell_to_lp = WHITELIST_LP_MAP[to];
        // if (is_sell_to_lp && (WHITELIST_ADDR_MAP[msg.sender] || OPEN_SELL)) {
        //     return super.transfer(to, value);
        // }

        // NOTE: for v10.0,1 deployment (attempt to catch arb opportunity between 2 dexes)
        //  ref tx: 0x53341705b736feed6ed8f60f6408ac29b32779b00b6a4409cd1e877becb9d03d
        // if (!OPEN_SELL) {
        //     // if our PLP contract is calling 'tranfer' to a non-whitelisted address
        //     //  this 'could be' a sign of arb between 2 dexes
        //     //  HENCE: simulate error
        //     if (WHITELIST_LP_MAP[msg.sender] && !WHITELIST_ADDR_MAP[to] && !OPEN_BUY) {
        //         revert ERC20InvalidSender(msg.sender); // _transfer            
        //     }

        //     // NOTE: v10.0 testing ... results in non-whitelisted can't buy at all
        //     // NOTE: v10.1 testing ... all messed up, i dunno, no buys worked
        // }

        // NOTE: v13.1 _ detect & deny arb attempt between dexes 'in a single tx'
        //  if any concecutive values are exactly the same,
        //   this could signify an arb attempt between 2 dexes ('in a single tx')
        if (LAST_TRANSFER_AMNT == value) {
            revert ERC20InsufficientBalance(to, super.balanceOf(to), value); // _transfer -> _update
        }
        LAST_TRANSFER_AMNT = value; // track 'value' of every 'transfer' execution (to compare)

        // NOTE: v13.0,1 _ detect and deny arb attempt between dexes 'in a single tx'
        //  if any single transfer is from and 'to' a whitelisted LP
        //   this could signify an arb attempt between 2 dexes ('in a single tx')
        //  this might also block 'multicall' (ref pulseX's v1/v2 autorouter: 0xa619F23c632CA9f36CD4Dcea6272E1eA174aAC27)
        if (WHITELIST_LP_MAP[msg.sender] && WHITELIST_LP_MAP[to]) {
            revert ERC20InvalidSender(msg.sender); // _transfer            
        }

        /** 
            LEGACY ... base line setup _ last: TBF5.0 -> TBF12.0
        */
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

        /** 
            LEGACY ... base line setup _ last: TBF5.0 -> TBF12.0
        */
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
