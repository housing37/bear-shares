def verify_hash(hash_key, function_signature):
    import hashlib
    
    # Encode function signature to bytes
    signature_bytes = function_signature.encode()
    
    # Calculate hash of the function signature
    calculated_hash = hashlib.sha256(signature_bytes).hexdigest()
    
    # Compare calculated hash with provided hash key
    if calculated_hash == hash_key:
        print(f"Hash verification passed for {function_signature}.")
    else:
        print(f"Hash verification failed for {function_signature}.")

# Dictionary containing hash keys and function signatures
function_signatures = {
    "11851737": "KEEPER_setKeeper(address)",
    "c67483dc": "ACCT_USD_BALANCES(address)",
    "8b47da26": "ACCT_USD_PAYOUTS(address,uint256)",
    "aa21f232": "BUY_BACK_FEE_PERC()",
    "405d2a83": "ENABLE_MARKET_BUY()",
    "46538f8c": "ENABLE_MARKET_QUOTE()",
    "862a179e": "KEEPER()",
    "bceeba33": "KEEPER_editDexRouters(address,bool)",
    "b290b9bf": "KEEPER_editWhitelistStables(address,uint8,bool)",
    "bc47b906": "KEEPER_enableMarketBuy(bool)",
    "624b3abe": "KEEPER_enableMarketQuote(bool)",
    "3015d747": "KEEPER_maintenance(uint64,address)",
    "dd8645c2": "KEEPER_setBuyBackFeePerc(uint8)",
    "66eff5cf": "KEEPER_setServiceBurnPerc(uint8)",
    "61cad1db": "KEEPER_setServiceFeePerc(uint8)",
    "c364daa4": "SERVICE_BURN_PERC()",
    "a004d00d": "SERVICE_FEE_PERC()",
    "fa4a9870": "TOK_WPLS()",
    "7f8754f4": "USD_STABLE_DECIMALS(address)",
    "ee80b054": "USWAP_V2_ROUTERS(uint256)",
    "593d1bf7": "WHITELIST_USD_STABLES(uint256)",
    "dd62ed3e": "allowance(address,address)",
    "095ea7b3": "approve(address,uint256)",
    "70a08231": "balanceOf(address)",
    "313ce567": "decimals()",
    "c85ec1e0": "getSwapRouters()",
    "00f403e8": "getWhitelistStables()",
    "06fdde03": "name()",
    "8da5cb5b": "owner()",
    "031cc420": "payOutBST(uint64,address)",
    "715018a6": "renounceOwnership()",
    "95d89b41": "symbol()",
    "9a60f330": "tVERSION()",
    "18160ddd": "totalSupply()",
    "d8785767": "tradeInBST(uint64)",
    "a9059cbb": "transfer(address,uint256)",
    "23b872dd": "transferFrom(address,address,uint256)",
    "f2fde38b": "transferOwnership(address)"
}

# Verify each function signature
for hash_key, function_signature in function_signatures.items():
    verify_hash(hash_key, function_signature)

# from hashlib import sha3_256

# def generate_function_hash(signature):
#     # Step 1: Concatenate the function signature
#     concatenated_signature = signature.encode()

#     # Step 2: Hash the concatenated string using Keccak-256
#     hashed_signature = sha3_256(concatenated_signature).hexdigest()

#     # Step 3: Take the first 4 bytes (8 hexadecimal characters) of the resulting hash
#     function_hash = hashed_signature[:8]

#     return function_hash

# def main(_function_signatures):
#     # Generate and print function hashes
#     # for signature, expected_hash in _function_signatures.items():
#     for expected_hash, signature in _function_signatures.items():
#         generated_hash = generate_function_hash(signature)
#         print(f"Expected Hash: {expected_hash}, Generated Hash: {generated_hash}")

# # Example function signatures and corresponding hashes
# function_signatures = {
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
# 	"fa4a9870": "TOK_WPLS()",
# 	"7f8754f4": "USD_STABLE_DECIMALS(address)",
# 	"ee80b054": "USWAP_V2_ROUTERS(uint256)",
# 	"593d1bf7": "WHITELIST_USD_STABLES(uint256)",
# 	"dd62ed3e": "allowance(address,address)",
# 	"095ea7b3": "approve(address,uint256)",
# 	"70a08231": "balanceOf(address)",
# 	"313ce567": "decimals()",
# 	"c85ec1e0": "getSwapRouters()",
# 	"00f403e8": "getWhitelistStables()",
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

# main(function_signatures)

# # remix generated _ 032324 _ (BST.sol)


# function_signatures = {
#     "KEEPER_setKeeper": ["11851737", ["address"], []],
#     "ACCT_USD_BALANCES": ["c67483dc", ["address"], []],
#     "ACCT_USD_PAYOUTS": ["8b47da26", ["address","uint256"], []],
#     "BUY_BACK_FEE_PERC": ["aa21f232", [], []],
#     "ENABLE_MARKET_BUY": ["405d2a83", [], []],
#     "ENABLE_MARKET_QUOTE": ["46538f8c", [], []],
#     "KEEPER": ["862a179e", [], []],
#     "KEEPER_editDexRouters": ["bceeba33", ["address","bool"], []],
#     "KEEPER_editWhitelistStables": ["b290b9bf", ["address","uint8","bool"], []],
#     "KEEPER_enableMarketBuy": ["bc47b906", ["bool"], []],
#     "KEEPER_enableMarketQuote": ["624b3abe", ["bool"], []],
#     "KEEPER_maintenance": ["3015d747", ["uint64","address"], []],
#     "KEEPER_setBuyBackFeePerc": ["dd8645c2", ["uint8"], []],
#     "KEEPER_setServiceBurnPerc": ["66eff5cf", ["uint8"], []],
#     "KEEPER_setServiceFeePerc": ["61cad1db", ["uint8"], []],
#     "SERVICE_BURN_PERC": ["c364daa4", [], []],
#     "SERVICE_FEE_PERC": ["a004d00d", [], []],
#     "TOK_WPLS": ["fa4a9870", [], []],
#     "USD_STABLE_DECIMALS": ["7f8754f4", ["address"], []],
#     "USWAP_V2_ROUTERS": ["ee80b054", ["uint256"], []],
#     "WHITELIST_USD_STABLES": ["593d1bf7", ["uint256"], []],
#     "allowance": ["dd62ed3e", ["address","address"], []],
#     "approve": ["095ea7b3", ["address","uint256"], []],
#     "balanceOf": ["70a08231", ["address"], []],
#     "decimals": ["313ce567", [], []],
#     "getSwapRouters": ["c85ec1e0", [], []],
#     "getWhitelistStables": ["00f403e8", [], []],
#     "name": ["06fdde03", [], []],
#     "owner": ["8da5cb5b", [], []],
#     "payOutBST": ["031cc420", ["uint64","address"], []],
#     "renounceOwnership": ["715018a6", [], []],
#     "symbol": ["95d89b41", [], []],
#     "tVERSION": ["9a60f330", [], []],
#     "totalSupply": ["18160ddd", [], []],
#     "tradeInBST": ["d8785767", ["uint64"], []],
#     "transfer": ["a9059cbb", ["address","uint256"], []],
#     "transferFrom": ["23b872dd", ["address","address","uint256"], []],
#     "transferOwnership": ["f2fde38b", ["address"], []]
# }