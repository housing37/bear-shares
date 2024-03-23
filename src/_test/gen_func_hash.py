from hashlib import sha3_256

def generate_function_hash(signature):
    # Step 1: Concatenate the function signature
    concatenated_signature = signature.encode()

    # Step 2: Hash the concatenated string using Keccak-256
    hashed_signature = sha3_256(concatenated_signature).hexdigest()

    # Step 3: Take the first 4 bytes (8 hexadecimal characters) of the resulting hash
    function_hash = hashed_signature[:8]

    return function_hash

def main(_function_signatures):
    # Generate and print function hashes
    for signature, expected_hash in _function_signatures.items():
        generated_hash = generate_function_hash(signature)
        print(f"Expected Hash: {expected_hash}, Generated Hash: {generated_hash}")

# Example function signatures and corresponding hashes
function_signatures = {
    "KEEPER_setKeeper(address)": "11851737", # gas used: 62,434
    "ACCT_USD_BALANCES(address)": "c67483dc",
    "ACCT_USD_PAYOUTS(address,uint256)": "8b47da26",
    "BUY_BACK_FEE_PERC()": "aa21f232",
    "ENABLE_MARKET_BUY()": "405d2a83",
    "ENABLE_MARKET_QUOTE()": "46538f8c",
    "KEEPER()": "862a179e",
    "KEEPER_editDexRouters(address,bool)": "bceeba33",
    "KEEPER_editWhitelistStables(address,uint8,bool)": "b290b9bf",
    "KEEPER_enableMarketBuy(bool)": "bc47b906",
    "KEEPER_enableMarketQuote(bool)": "624b3abe",
    "KEEPER_maintenance(uint64,address)": "3015d747",
    "KEEPER_setBuyBackFeePerc(uint8)": "dd8645c2",
    "KEEPER_setServiceBurnPerc(uint8)": "66eff5cf",
    "KEEPER_setServiceFeePerc(uint8)": "61cad1db",
    "SERVICE_BURN_PERC()": "c364daa4",
    "SERVICE_FEE_PERC()": "a004d00d",
    "USD_STABLE_DECIMALS(address)": "7f8754f4",
    "USWAP_V2_ROUTERS(uint256)": "ee80b054",
    "WHITELIST_USD_STABLES(uint256)": "593d1bf7",
    "allowance(address,address)": "dd62ed3e",
    "approve(address,uint256)": "095ea7b3",
    "balanceOf(address)": "70a08231",
    "decimals()": "313ce567",
    "name()": "06fdde03",
    "owner()": "8da5cb5b",
    "payOutBST(uint64,address)": "031cc420",
    "renounceOwnership()": "715018a6",
    "symbol()": "95d89b41",
    "tVERSION()": "9a60f330",
    "totalSupply()": "18160ddd",
    "tradeInBST(uint64)": "d8785767",
    "transfer(address,uint256)": "a9059cbb",
    "transferFrom(address,address,uint256)": "23b872dd",
    "transferOwnership(address)": "f2fde38b"
}

main(function_signatures)

# remix generated _ 032224 _ (BST.sol)
# {
# 	"11851737": "KEEPER_setKeeper(address)",
# 	"c67483dc": "ACCT_USD_BALANCES(address)",
# 	"8b47da26": "ACCT_USD_PAYOUTS(address,uint256)",
# 	"aa21f232": "BUY_BACK_FEE_PERC()",
# 	"405d2a83": "ENABLE_MARKET_BUY()",
# 	"46538f8c": "ENABLE_MARKET_QUOTE()",
# 	"862a179e": "KEEPER()",
# 	"bceeba33": "KEEPER_editDexRouters(address,bool)",
# 	"b290b9bf": "KEEPER_editWhitelistStables(address,uint8,bool)",
# 	"bc47b906": "KEEPER_enableMarketBuy(bool)",
# 	"624b3abe": "KEEPER_enableMarketQuote(bool)",
# 	"3015d747": "KEEPER_maintenance(uint64,address)",
# 	"dd8645c2": "KEEPER_setBuyBackFeePerc(uint8)",
# 	"66eff5cf": "KEEPER_setServiceBurnPerc(uint8)",
# 	"61cad1db": "KEEPER_setServiceFeePerc(uint8)",
# 	"c364daa4": "SERVICE_BURN_PERC()",
# 	"a004d00d": "SERVICE_FEE_PERC()",
# 	"7f8754f4": "USD_STABLE_DECIMALS(address)",
# 	"ee80b054": "USWAP_V2_ROUTERS(uint256)",
# 	"593d1bf7": "WHITELIST_USD_STABLES(uint256)",
# 	"dd62ed3e": "allowance(address,address)",
# 	"095ea7b3": "approve(address,uint256)",
# 	"70a08231": "balanceOf(address)",
# 	"313ce567": "decimals()",
# 	"06fdde03": "name()",
# 	"8da5cb5b": "owner()",
# 	"031cc420": "payOutBST(uint64,address)",
# 	"715018a6": "renounceOwnership()",
# 	"95d89b41": "symbol()",
# 	"9a60f330": "tVERSION()",
# 	"18160ddd": "totalSupply()",
# 	"d8785767": "tradeInBST(uint64)",
# 	"a9059cbb": "transfer(address,uint256)",
# 	"23b872dd": "transferFrom(address,address,uint256)",
# 	"f2fde38b": "transferOwnership(address)"
# }