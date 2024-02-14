# teddy-shares
$TeadyShares NFT w/ ERC404 fixes

## Tokenomics (whitepaper copy)
    - one 'share' of 'teddy', earns you one NFT image

## TODO - TG updates
    - create TG bot account keys needed (on TG website)
    - add bot support for automated welcome messages
    - finish / test bot support for tracking invites (@user sent me)
    - deploy bot on t.em/BearShareNFT
    - change t.em/BearShareNFT to t.em/TeddyShares

## TODO - website updates
    DONE - clone https://github.com/PulseNauts/bearshare
    - launch https://github.com/PulseNauts/bearshare
        - create AWS server instance to host it
    - remove selective info (to hide from competition)
        - ie. artist features and adding new NFT images
    - register domain 'teddyshares.*'

    - follow up with TG: @DepthBySoul (tracky) on latest update requests
        - adding 'road map' section
        - adding embedded dexscreener section

## TeddyShares contract features to add
    - integrate algorithm for adding new NFT images
        - track wallet address of proposal
    - function artistProposeNewImage(img_url, img_name, img_desr)
    - function curatorDeployNewImage(img_url, data_uri, priority_rating)

## TODO - continue reviewing ERC404 v2.0
    - https://github.com/Pandora-Labs-Org/erc404
    - https://github.com/Pandora-Labs-Org/erc404/issues

## TODO - ERC404 updates - N / A
    - update 'whitelist' integration to make publically accessible (needs whitelist logging array)
    - remove Owanable.sol dependencies
    - fix _mint / _burn loop (maybe use mapping algorithm instead)
       ref TG: https://t.me/Fruits404
        🚀All right guys. We are going to launch on 9mm paired with pulse (PLS). Contract address will be published here in the chat 1-2 mins before launch (actual LP creation). 
        PLS or WPLS? Seems not everyone understand mechanics under this two entities. Short answer is: you should pick PLS on 9mm's frontend. 
        Also one more thing we didn't mention a lot (but you probably noticed in our roadmap), we are going launch coins staking. Anyways current main priority is an initial launch.🚀


        🚨Regarding stuck transactions some of you could have with another 404 tokens. 

        Short version:
        Just don't buy A LOT of tokens at one time. Try to do less than 100 per one transaction and you'll be fine.

        Longer version:
        Every time you transfer token (including buy\see on dex) it mints\burns NFTs (as a key mechanism of ERC404). It takes gas. Metamask along with some other tokens are not professional gas estimators (especially when we are talking about new technology which ERC\PRC404 is). I didn't dig deep into it, so don't know if it even sends it to blockchain, in that case you should get response from RPC or TX should be reverted. Anyways, just follow the "short version" to avoid issues. Wanna buy a lot? Better buy in few TXs than sit with a stuck one without a way to cancel it.