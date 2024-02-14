//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {ERC404} from "./ERC404.sol";
// import {ERC404MerkleClaim} from "./extensions/ERC404MerkleClaim.sol";

// remote
// import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
// import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

// local _ $ npm install @openzeppelin/contracts
import {Ownable} from "./node_modules/@openzeppelin/contracts/access/Ownable.sol"; 
import {Strings} from "./node_modules/@openzeppelin/contracts/utils/Strings.sol";
import "./IGTALib.sol";

// contract BearShares is Ownable, ERC404, ERC404MerkleClaim {
contract BearShares is Ownable, ERC404 {

    /* _ UTILITY SUPPORT _ */
    IGTALib private GTAL;

    /* _ TOKEN INIT SUPPORT _ */
    string public NAME = "TSHARES"; // token name
    string public SYMBOL = "Teddy Shares"; // token symbol
    uint8 public DECIMALS = 18; // for ERC-20 representation
    uint256 public INIT_TOT_SUPPLY_ERC721 = 10000;
    // uint256 public MAX_TOT_SUPPLY_ERC721 = 10000;

    /* _ TRANSPARENCY / SECURITY SUPPORT _ */
    address[] public ERC721_TRANSFER_EXEMPTS; // for gas savings (pairs, routers, etc)
    
    // NOTE: ERC404 constructor hard codes global 'units' (for ERC-20 representation)
    //  units = 10 ** DECIMALS;
    constructor(address _gtal) ERC404(NAME, SYMBOL, DECIMALS) Ownable(msg.sender) {
        GTAL = IGTALib(_gtal);
        address initialMintRecipient_ = msg.sender;
        
        // NOTE: setting initialMintRecipient_ to indeed exempt
        //  because we ONLY want to mint ERC20s (ie. w/o corresponding ERC721s)
        _updateERC721TransferExempt(initialMintRecipient_, true); // true = exempt
        _mintERC20(initialMintRecipient_, INIT_TOT_SUPPLY_ERC721 * units, false); // (to_, value_, mintCorrespondingERC721s_)
    }

    function tokenURI(uint256 id_) public pure override returns (string memory) {
        return string.concat("https://example.com/token/", Strings.toString(id_));
    }

    function setERC721TransferExempt(address account_, bool value_) external onlyOwner {
        _updateERC721TransferExempt(account_, value_);
    }

    function _updateERC721TransferExempt(address _account, bool _exempt) private {
        // Addresses that are exempt from ERC-721 transfer, typically for gas savings (pairs, routers, etc)
        _setERC721TransferExempt(_account, _exempt);
        if (_exempt)
            ERC721_TRANSFER_EXEMPTS = GTAL.addAddressToArraySafe(_account, ERC721_TRANSFER_EXEMPTS, true); // true = no dups
        else
            ERC721_TRANSFER_EXEMPTS = GTAL.remAddressFromArray(_account, ERC721_TRANSFER_EXEMPTS);
    }
}