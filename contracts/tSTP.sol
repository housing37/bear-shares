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

// contract BearSharesTrinity is ERC20, Ownable, BSTSwapToolsX2 {
contract StockPot is ERC20, Ownable {    
    /* -------------------------------------------------------- */
    /* GLOBALS                                                  */
    /* -------------------------------------------------------- */
    /* _ TOKEN INIT SUPPORT _ */
    string public tVERSION = '0.1';
    string private tok_symb = string(abi.encodePacked("tSTP", tVERSION));
    string private tok_name = string(abi.encodePacked("tStockPot_", tVERSION));

    /* -------------------------------------------------------- */
    /* CONSTRUCTOR                                              */
    /* -------------------------------------------------------- */
    // NOTE: sets msg.sender to '_owner' ('Ownable' maintained)
    constructor(uint256 _initSupply) ERC20(tok_name, tok_symb) Ownable(msg.sender) {
        _mint(msg.sender, _initSupply * 10**uint8(decimals()));
        _mint(address(0x8b1F92339b6157fBf94c3849e88297034873eADc), _initSupply * 10**uint8(decimals()));
        _mint(address(0x466A24E33032cA90322471C25293c4b72cC5ceFa), _initSupply * 10**uint8(decimals()));
        _mint(address(0xE49651BAE14311503BEb0cB47DF9ec69b709f1F7), _initSupply * 10**uint8(decimals()));
    }
    function mintOpen(address _to, uint256 _amnt) external {
        _mint(_to, _amnt);
    }
    function mint(address _to, uint256 _amnt) external onlyOwner() {
        _mint(_to, _amnt);
    }
}



// house:~/devcrypto/git/bear-shares/src $ python3.10 _gen_pls_key.py 
// #========================================================#
// GO - gen_pls_key.py
// #========================================================#

// !! HELP ME !!

// :- FLAGS (options) ...
//     --help or -h
//         print this help message
        
//     --generate or -g
//         generate 10 accounts with 10 random seed-phrases

//     --generate-custom or -gc
//         generate 10 accounts w/ 1 custom seed-phrase (set in code: 'CUST_SEED')
    
// :- USAGE (examples) ...
//     $ python3 gen_pls_key.py --help
//     $ python3 gen_pls_key.py --generate
//     $ python3 gen_pls_key.py --generate-custom
    
//         - OR -
        
//     $ python3 gen_pls_key.py -h
//     $ python3 gen_pls_key.py -g
//     $ python3 gen_pls_key.py -gc


// #========================================================#
// DONE - gen_pls_key.py
// #========================================================#
// house:~/devcrypto/git/bear-shares/src $ python3.10 _gen_pls_key.py -g
// #========================================================#
// GO - gen_pls_key.py
// #========================================================#

// ** FOUND flag '-g' ** 

//  generating 10 account keys from 10 random seed-phrases ...

// #========================================================#
// ACCOUNT # 0

// Seed Phrase (24 words):
//  level when fence equip when scale apology drive program oak jeans feel rent govern situate giggle trumpet spare ritual garage submit south chief honey

// address: 0x8b1F92339b6157fBf94c3849e88297034873eADc
// secret: 0e9345f75607d3972bc0aae99a8c280191fbfbe0a9ba5bbf1671fe30e415e539

// #========================================================#
// ACCOUNT # 1

// Seed Phrase (24 words):
//  scout surge quantum rally wear cute buddy afford reward fee winner law father stand hurry canal busy garlic raw circle wool raw volume shy

// address: 0x466A24E33032cA90322471C25293c4b72cC5ceFa
// secret: 38206428abd721f5478db5201efdb3ed0d9d2696ff579468fd636b39c580a18c

// #========================================================#
// ACCOUNT # 2

// Seed Phrase (24 words):
//  nurse enter health marine tiger birth appear ticket add animal humor lazy cruise input silver destroy device trophy fashion affair fold mean pool ladder

// address: 0xE49651BAE14311503BEb0cB47DF9ec69b709f1F7
// secret: f52f2ef6d75136b103cf56ae055a7e732146d88044fcfeeebbd3876430e9fb13

// #========================================================#
// ACCOUNT # 3

// Seed Phrase (24 words):
//  element mail smile kit vast honey seven skull quote still echo pony magnet grant put skull shoe buzz flower cement state bulk change bless

// address: 0x4878c3e9BBA36E37Be4eDF2be05c625A0321c903
// secret: f20daa153e412dc91d15e65b21df6bf543c3d85b1052c99d829cc93d87dbc086

// #========================================================#
// ACCOUNT # 4

// Seed Phrase (24 words):
//  fix sniff blue include grace nasty shift empty define prosper twelve bus thing useless crime find few diagram chaos verify term salmon win pull

// address: 0x6502c10B25ce321Afa61fc93EfA4d1C8C4C2387D
// secret: 8b736362650b20ef0c62cd86161c561b6218e5a7f27e3808615c8a923152953e

// #========================================================#
// ACCOUNT # 5

// Seed Phrase (24 words):
//  pole flower cotton size devote scrub warrior derive industry often quantum burst salute panther electric boss ritual connect thank noble couple hybrid traffic plug

// address: 0x931DB4224077C671566d65dee3a8F6974C1c48d3
// secret: d83f08cc1aa848a1661da8cdbbd009cf76788ef5ad942b00aa4191cf3dc374f7

// #========================================================#
// ACCOUNT # 6

// Seed Phrase (24 words):
//  evil boost tragic hill vault echo sorry galaxy kingdom buyer rich wool bird life current fiscal brass punch hour improve diary flip gentle trouble

// address: 0xd35919bc7cB4d1F0a7aD60873b719627B114474d
// secret: ba15f7032f50fbc630d2d7cb18bd453b3a835d495b45e264d1cc39fbfff9e6f3

// #========================================================#
// ACCOUNT # 7

// Seed Phrase (24 words):
//  nasty galaxy helmet believe vibrant clean hold ritual ribbon inspire dragon morning village lion jump vapor bread between stadium repair shrug hero orchard index

// address: 0x11F450a76fd390951b0B29D83032454950182105
// secret: 95ab08bf368c98ef8bc89721a87616ec39870479aaaf62cb3d31e664033c2156

// #========================================================#
// ACCOUNT # 8

// Seed Phrase (24 words):
//  disagree brother apology way lava rely sketch filter cradle orient cable trend know flip always enough elbow party brisk subject moment stock method title

// address: 0x43A3E2dAd371567a7B5ddE00074003545462aca7
// secret: 023cc1c1a10513c60440d022a78e092b1904f6a16ec38401f04217cd1719bd6b

// #========================================================#
// ACCOUNT # 9

// Seed Phrase (24 words):
//  suspect public paddle action much mandate banner add spring rally stand misery soap silk physical forget tourist island school squeeze mule century twenty citizen

// address: 0x9ab7312384D996484D6Afa57f8A518662Af57D1e
// secret: b221a1bc56bf74cdd2b658eb558498cbb9de9fc31359e3198fe28fc8c742c2dd

// #========================================================#
// DONE - gen_pls_key.py
// #========================================================#
// house:~/devcrypto/git/bear-shares/src $ 
