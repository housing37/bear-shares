__fname = '_bst_keeper'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
cStrDivider_1 = '#----------------------------------------------------------------#'

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os, traceback, time, pprint, json
from datetime import datetime

# from web3 import Web3, HTTPProvider
# from web3.middleware import construct_sign_and_send_raw_middleware
# from web3.gas_strategies.time_based import fast_gas_price_strategy
# import env
import pprint
from attributedict.collections import AttributeDict # tx_receipt requirement
import _web3 # from web3 import Account, Web3, HTTPProvider
import _abi

LST_CONTR_ABI_BIN = [
    "../bin/contracts/BearSharesTrinity",
]

W3_ = None
ABI_FILE = None
BIN_FILE = None
CONTRACT = None
CONTRACT_ABI = None
BST_ADDRESS = None

def init_web3():
    global W3_, ABI_FILE, BIN_FILE, CONTRACT
    # init W3_, user select abi to deploy, generate contract & deploy
    W3_ = _web3.myWEB3().init_inp()
    # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
    # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
    # CONTRACT = W3_.add_contract_deploy(ABI_FILE, BIN_FILE)

def estimate_gas(contract, contract_args=[]):
    global W3_, ABI_FILE, BIN_FILE, CONTRACT
    # Replace with your contract's ABI and bytecode
    # contract_abi = CONTR_ABI
    # contract_bytecode = CONTR_BYTES
    
    # Replace with your wallet's private key
    private_key = W3_.SENDER_SECRET

    # Create a web3.py contract object
    # contract = W3_.W3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    # Set the sender's address from the private key
    sender_address = W3_.W3.eth.account.from_key(private_key).address

    # Estimate gas for contract deployment
    # gas_estimate = contract.constructor().estimateGas({'from': sender_address})
    gas_estimate = contract.constructor(*contract_args).estimate_gas({'from': sender_address})

    print(f"\nEstimated gas cost _ 0: {gas_estimate}")

    import statistics
    block = W3_.W3.eth.get_block("latest", full_transactions=True)
    gas_estimate = int(statistics.median(t.gas for t in block.transactions))
    gas_price = W3_.W3.eth.gas_price
    gas_price_eth = W3_.W3.from_wei(gas_price, 'ether')
    print(f"Estimated gas cost _ 1: {gas_estimate}")
    print(f" Current gas price: {gas_price_eth} ether (PLS) == {gas_price} wei")
    # Optionally, you can also estimate the gas price (in Gwei) using a gas price strategy
    # Replace 'fast' with other strategies like 'medium' or 'slow' as needed
    #gas_price = W3.eth.generateGasPrice(fast_gas_price_strategy)
    #print(f"Estimated gas price (Gwei): {W3.fromWei(gas_price, 'gwei')}")
    
    return input('\n (3) procced? [y/n]\n  > ') == 'y'

# note: params checked/set in priority order; 'def|max_params' uses 'mpf_ratio'
#   if all params == False, falls back to 'min_params=True' (ie. just use 'gas_limit')
def get_gas_params_lst(rpc_url, min_params=False, max_params=False, def_params=True):
    global W3_
    # Estimate the gas cost for the transaction
    #gas_estimate = buy_tx.estimate_gas()
    gas_limit = W3_.GAS_LIMIT # max gas units to use for tx (required)
    gas_price = W3_.GAS_PRICE # price to pay for each unit of gas (optional?)
    max_fee = W3_.MAX_FEE # max fee per gas unit to pay (optional?)
    max_prior_fee = W3_.MAX_PRIOR_FEE # max fee per gas unit to pay for priority (faster) (optional)
    #max_priority_fee = W3.to_wei('0.000000003', 'ether')

    if min_params:
        return [{'gas':gas_limit}]
    elif max_params:
        #return [{'gas':gas_limit}, {'gasPrice': gas_price}, {'maxFeePerGas': max_fee}, {'maxPriorityFeePerGas': max_prior_fee}]
        return [{'gas':gas_limit}, {'maxFeePerGas': max_fee}, {'maxPriorityFeePerGas': max_prior_fee}]
    elif def_params:
        return [{'gas':gas_limit}, {'maxPriorityFeePerGas': max_prior_fee}]
    else:
        return [{'gas':gas_limit}]

def generate_contructor():
    constr_args = []
    print()
    while True:
        arg = input(' Add constructor arg (use -1 to end):\n  > ')
        if arg == '-1': break
        if arg.isdigit(): arg = int(arg)
        constr_args.append(arg)
    return constr_args

def main(_contr_addr, _contr_abi):
    global W3_, ABI_FILE, BIN_FILE, CONTRACT, CONTRACT_ABI
    # init_web3()
    # print(f'\nUSING bytecode: {BIN_FILE}')
    # print(f'USING abi: {ABI_FILE}')
    # assert input('\n (1) proceed? [y/n]\n  > ') == 'y', "aborted...\n"

    # Connect to a local Ethereum node
    # web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

    # Add middleware for handling Proof of Authority networks
    # W3_.W3.middleware_onion.inject(W3_.W3.geth_poa_middleware, layer=0)

    # Contract address (you'll need to replace this with your actual contract address)
    # contract_address = _contr_addr


    print('preparing function signature params ...')
    # Function hash & Parameters for the function call
    function_hash = "3015d747" 
    # "KEEPER_maintenance(uint64,address)": "3015d747",
    # // weUSDT
    usdStable = '0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f' 
    decimals_ = 6
    amnt = 0.012155
    param1 = int(amnt * 10**decimals_)
    param2 = usdStable

    print('preparing function signature ...')
    # Encode function call data
    # function_signature = function_hash + Web3.toHex(Web3.toBytes(text="uint64"))[2:] + Web3.toHex(Web3.toBytes(hexstr=param1))[2:] + Web3.toHex(Web3.toBytes(text="address"))[2:] + Web3.toHex(Web3.toBytes(hexstr=param2))[2:]
    # function_signature = function_hash + W3_.Web3.to_hex(W3_.Web3.to_bytes(text="uint64"))[2:] + W3_.Web3.to_hex(W3_.Web3.to_bytes(hexstr=param1))[2:] + W3_.Web3.to_hex(W3_.Web3.to_bytes(text="address"))[2:] + W3_.Web3.to_hex(W3_.Web3.to_bytes(hexstr=param2))[2:]
    # function_signature = function_hash + W3_.W3.toHex(W3_.W3.toBytes(text="uint64"))[2:] + W3_.W3.toHex(W3_.W3.toBytes(hexstr=param1))[2:] + W3_.W3.toHex(W3_.W3.toBytes(text="address"))[2:] + W3_.W3.toHex(W3_.W3.toBytes(hexstr=param2))[2:]
    # concat_0 = W3_.Web3.to_hex(W3_.Web3.to_bytes(text="uint64"))[2:]
    # print(concat_0)
    # concat_1 = W3_.Web3.to_hex(W3_.Web3.to_bytes(hexstr=param1))[2:]
    # print(concat_1)
    # concat_2 = W3_.Web3.to_hex(W3_.Web3.to_bytes(text="address"))[2:]
    # print(concat_2)
    # concat_3 = W3_.Web3.to_hex(W3_.Web3.to_bytes(hexstr=param2))[2:]
    # print(concat_3)
    # lst_concat = [concat_0, concat_1, concat_2, concat_3]
    # print(function_hash)
    # print(*lst_concat)
    # function_signature = function_hash + concat_0 + concat_1 + concat_2 + concat_3

    # Get contract instance
    contract = W3_.W3.eth.contract(address=_contr_addr, abi=_contr_abi)

    # Generate function signature using the function hash and parameters
    function_signature = contract.encodeABI(
        fn_name="KEEPER_maintenance",
        args=[param1, param2]
    )
    # Construct transaction data
    # transaction_data = {
    #     'to': contract_address,
    #     'data': function_signature,
    #     'gas': 2000000,  # Adjust gas limit accordingly
    # }
    print('building tx_data w/ function signature ...')
    # func_hex = "0x467c4e68" # BOND
    tx_data = {
        # "nonce": W3_.W3.eth.getTransactionCount(W3_.SENDER_ADDRESS),
        "to": _contr_addr,
        "data": function_signature,
        # "gas": 1_00_000,  # Adjust the gas limit as needed
        # "gasPrice": W3_.W3.toWei("300000", "gwei"),  # Adjust the gas price as needed
        # "gasPrice": W3_.W3.to_wei(300_000, "gwei"),  # Adjust the gas price as needed
        #"value": w3.toWei(1, "ether"),  # Specify the value you want to send with the transaction
        # "chainId": 369 # 369 = pulsechain Mainnet... required for replay-protection (EIP-155)
    }

    print('setting tx_params ...')
    tx_nonce = W3_.W3.eth.get_transaction_count(W3_.SENDER_ADDRESS)
    tx_params = {
        'chainId': W3_.CHAIN_ID,
        'nonce': tx_nonce,
    }
    print(' setting gas params in tx_params ...')
    lst_gas_params = get_gas_params_lst(W3_.RPC_URL, min_params=False, max_params=True, def_params=True)
    for d in lst_gas_params: tx_params.update(d) # append gas params

    print('update tx_data w/ tx_params')
    tx_data.update(tx_params)

    # print(f'building tx w/ NONCE: {tx_nonce} ...')
    # # constructor_tx = CONTRACT.constructor().build_transaction(tx_params)
    # constructor_tx = CONTRACT.constructor(*constr_args).build_transaction(tx_params)

    print(f'signing and sending tx w/ NONE: {tx_nonce} ... {get_time_now()}')
    # Sign and send the transaction # Deploy the contract
    # tx_signed = W3_.W3.eth.account.sign_transaction(constructor_tx, private_key=W3_.SENDER_SECRET)
    tx_signed = W3_.W3.eth.account.sign_transaction(tx_data, private_key=W3_.SENDER_SECRET)
    tx_hash = W3_.W3.eth.send_raw_transaction(tx_signed.rawTransaction)

    print(cStrDivider_1, f'waiting for receipt ... {get_time_now()}', sep='\n')
    print(f'    tx_hash: {tx_hash.hex()}')

    # Wait for the transaction to be mined
    wait_time = 300 # sec
    try:
        tx_receipt = W3_.W3.eth.wait_for_transaction_receipt(tx_hash, timeout=wait_time)
        print("Transaction confirmed in block:", tx_receipt.blockNumber, f' ... {get_time_now()}')
    except Exception as e:
        print(f"\n{get_time_now()}\n Transaction not confirmed within the specified timeout... wait_time: {wait_time}")
        print_except(e)
        exit(1)

    # print incoming tx receipt (requires pprint & AttributeDict)
    tx_receipt = AttributeDict(tx_receipt) # import required
    tx_rc_print = pprint.PrettyPrinter().pformat(tx_receipt)
    print(cStrDivider_1, f'RECEIPT:\n {tx_rc_print}', sep='\n')
    # print(cStrDivider_1, f"\n\n Contract deployed at address: {tx_receipt['contractAddress']}\n\n", sep='\n')
    print("Transaction mined!")





    
    # # Send transaction
    # tx_hash = W3_.W3.eth.sendTransaction(transaction_data)

    # # Wait for the transaction to be mined
    # W3_.W3.eth.waitForTransactionReceipt(tx_hash)

    # print("Transaction mined!")

    # # Create contract instance
    # # contract = W3_.W3.eth.contract(address=contract_address, abi=contract_abi)
    # # contr_abi, contr_bytes  = self.read_abi_bytecode(_abi_file, _bin_file)
    
    # # contract, contract_addr = W3_.init_contract(_contr_addr, CONTRACT_ABI, W3_)

    # # Parameters for the function call
    # param1 = 123
    # param2 = "0x456def..."

    # # Function hash
    # function_hash = "3015d747" # "KEEPER_maintenance(uint64,address)": "3015d747",

    # # Encode function call data
    # function_signature = function_hash + W3_.W3.toHex(W3_.W3.toBytes(text="uint64"))[2:] + W3_.W3.toHex(W3_.W3.toBytes(hexstr=param1))[2:] + W3_.W3.toHex(W3_.W3.toBytes(text="address"))[2:] + W3_.W3.toHex(W3_.W3.toBytes(hexstr=param2))[2:]

    # # Construct transaction data
    # transaction_data = {
    #     'to': contract_address,
    #     'data': function_signature,
    #     'gas': 2000000,  # Adjust gas limit accordingly
    # }

    # # Send transaction
    # tx_hash = web3.eth.sendTransaction(transaction_data)

    # # Wait for the transaction to be mined
    # web3.eth.waitForTransactionReceipt(tx_hash)

    # print("Transaction mined!")


    # constr_args = generate_contructor() # 0x78b48b71C8BaBd02589e3bAe82238EC78966290c
    # print(f'  using "constructor({", ".join(map(str, constr_args))})"')
    # assert input('\n (2) procced? [y/n]\n  > ') == 'y', "aborted...\n"

    # # proceed = estimate_gas(CONTRACT, constr_args) # (3) proceed? [y/n]
    # # assert proceed, "\ndeployment canceled after gas estimate\n"

    # print('\ncalculating gas ...')
    # tx_nonce = W3_.W3.eth.get_transaction_count(W3_.SENDER_ADDRESS)
    # tx_params = {
    #     'chainId': W3_.CHAIN_ID,
    #     'nonce': tx_nonce,
    # }
    # lst_gas_params = get_gas_params_lst(W3_.RPC_URL, min_params=False, max_params=True, def_params=True)
    # for d in lst_gas_params: tx_params.update(d) # append gas params

    # print(f'building tx w/ NONCE: {tx_nonce} ...')
    # # constructor_tx = CONTRACT.constructor().build_transaction(tx_params)
    # constructor_tx = CONTRACT.constructor(*constr_args).build_transaction(tx_params)

    # print(f'signing and sending tx ... {get_time_now()}')
    # # Sign and send the transaction # Deploy the contract
    # tx_signed = W3_.W3.eth.account.sign_transaction(constructor_tx, private_key=W3_.SENDER_SECRET)
    # tx_hash = W3_.W3.eth.send_raw_transaction(tx_signed.rawTransaction)

    # print(cStrDivider_1, f'waiting for receipt ... {get_time_now()}', sep='\n')
    # print(f'    tx_hash: {tx_hash.hex()}')

    # # Wait for the transaction to be mined
    # wait_time = 300 # sec
    # try:
    #     tx_receipt = W3_.W3.eth.wait_for_transaction_receipt(tx_hash, timeout=wait_time)
    #     print("Transaction confirmed in block:", tx_receipt.blockNumber, f' ... {get_time_now()}')
    # # except W3_.W3.exceptions.TransactionNotFound:    
    # #     print(f"Transaction not found within the specified timeout... wait_time: {wait_time}", f' ... {get_time_now()}')
    # # except W3_.W3.exceptions.TimeExhausted:
    # #     print(f"Transaction not confirmed within the specified timeout... wait_time: {wait_time}", f' ... {get_time_now()}')
    # except Exception as e:
    #     print(f"\n{get_time_now()}\n Transaction not confirmed within the specified timeout... wait_time: {wait_time}")
    #     print_except(e)
    #     exit(1)

    # # print incoming tx receipt (requires pprint & AttributeDict)
    # tx_receipt = AttributeDict(tx_receipt) # import required
    # tx_rc_print = pprint.PrettyPrinter().pformat(tx_receipt)
    # print(cStrDivider_1, f'RECEIPT:\n {tx_rc_print}', sep='\n')
    # print(cStrDivider_1, f"\n\n Contract deployed at address: {tx_receipt['contractAddress']}\n\n", sep='\n')

def go_user_inputs():
    global BST_ADDRESS, W3_, CONTRACT_ABI # REQUIRED (using assignment)
    # rpc_url, chain_id, chain_sel    = _web3.myWEB3().inp_sel_chain()
    # w3, account = _web3.myWEB3().init_web3(empty=True)
    # init_web3()
    W3_ = _web3.myWEB3().init_inp()
    # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
    # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
    

    # print(f'\nUSING bytecode: {BIN_FILE}')
    # print(f'USING abi: {ABI_FILE}')
    

    # ans = input('\n Search address? [y/n]\n  > ')
    # b_ans = ans == 'y' or ans == '1'
    # if b_ans:
    while BST_ADDRESS == None or BST_ADDRESS == '':
        BST_ADDRESS = input('\n Enter BST contract address:\n  > ')
    print(f'\n using BST_ADDRESS: {BST_ADDRESS}')
    CONTRACT_ABI = _abi.BST_ABI
    print(' set CONTRACT_ABI = _abi.BST_ABI')
    assert input('\n (1) proceed? [y/n]\n  > ') == 'y', "aborted...\n"
    print('\n\n')
    # return rpc_url, w3, b_ans

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        deploy contract to chain
         selects .abi & .bin from ../bin/contracts/

    *NOTE* INPUT PARAMS...
        nil
        
    *EXAMPLE EXECUTION*
        $ python3 {__filename} -<nil> <nil>
        $ python3 {__filename}
'''

#ref: https://stackoverflow.com/a/1278740/2298002
def print_except(e, debugLvl=0):
    #print(type(e), e.args, e)
    if debugLvl >= 0:
        print('', cStrDivider, f' Exception Caught _ e: {e}', cStrDivider, sep='\n')
    if debugLvl >= 1:
        print('', cStrDivider, f' Exception Caught _ type(e): {type(e)}', cStrDivider, sep='\n')
    if debugLvl >= 2:
        print('', cStrDivider, f' Exception Caught _ e.args: {e.args}', cStrDivider, sep='\n')
    if debugLvl >= 3:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        strTrace = traceback.format_exc()
        print('', cStrDivider, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDivider, sep='\n')

def wait_sleep(wait_sec : int, b_print=True, bp_one_line=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print and bp_one_line: print(wait_sec-s+1, end=' ', flush=True)
        if b_print and not bp_one_line: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    if bp_one_line and b_print: print() # line break if needed
    print(f'waiting... {wait_sec} sec _ DONE')

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

if __name__ == "__main__":
    ## start ##
    RUN_TIME_START = get_time_now()
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    try:
        go_user_inputs()
        main(BST_ADDRESS, CONTRACT_ABI)
    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')