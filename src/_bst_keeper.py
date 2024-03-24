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
from ethereum.abi import encode_abi, decode_abi # pip install ethereum

LST_CONTR_ABI_BIN = [
    "../bin/contracts/BearSharesTrinity",
]

W3_ = None
ABI_FILE = None
BIN_FILE = None
CONTRACT = None
CONTRACT_ABI = None
BST_ADDRESS = None
FUNC_SIGN_SEL = None
LST_FUNC_SIGN_PARAMS = []
BST_FUNC_MAP = {}
IS_WRITE = False

# def init_web3():
#     global W3_, ABI_FILE, BIN_FILE, CONTRACT
#     # init W3_, user select abi to deploy, generate contract & deploy
#     W3_ = _web3.myWEB3().init_inp()
#     # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
#     # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
#     # CONTRACT = W3_.add_contract_deploy(ABI_FILE, BIN_FILE)

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

def write_with_hash(_contr_addr, _func_hash, _lst_param_types, _lst_params, _lst_ret_types):
    global W3_

    print('preparing function signature w/ func hash & params lists ...')
    func_sign = _func_hash
    if len(_lst_param_types) > 0:
        func_sign = _func_hash + encode_abi(_lst_param_types, _lst_params).hex()

    print('building tx_data w/ _contr_addr & func_sign ...')
    tx_data = {
        "to": _contr_addr,
        "data": func_sign,
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

    print(f'signing and sending tx w/ NONCE: {tx_nonce} ... {get_time_now()}')
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
    print("\nTransaction mined!")

    return_value = decode_abi(['address'], bytes.fromhex(tx_receipt['output'][2:]))[0]
    print(f'function call return_value: {return_value}')

def read_with_hash(_contr_addr, _func_hash, _lst_param_types, _lst_params, _lst_ret_types):
    global W3_

    print('preparing function signature params ...')
    func_sign = _func_hash
    if len(_lst_param_types) > 0:
        func_sign = _func_hash + encode_abi(_lst_param_types, _lst_params).hex()

    print(f'building tx_data w/ ...\n _contr_addr: {_contr_addr}\n _func_hash: {_func_hash}')
    tx_data = {
        "to": _contr_addr,
        "data": func_sign,
    }

    # Call contract function to retrieve the value of the KEEPER state variable
    print(f'calling contract function _ {get_time_now()}')
    return_val = W3_.W3.eth.call(tx_data)
    print(f'calling contract function _ {get_time_now()} ... DONE')
    print('\nparsing & printing response ...')
    print(f'return_val: {return_val}')
    print(f'return_val.hex(): {return_val.hex()}')
    decoded_value_return = decode_abi(_lst_ret_types, return_val)
    print(f'decoded_value_return: {decoded_value_return}')
    # hex_bytes = HexBytes('0x745472696e6974795f39')
    hex_bytes = decoded_value_return[0]
    decoded_string = hex_bytes
    if isinstance(hex_bytes, bytes):
        bytes_value = bytes(hex_bytes) # Convert hex bytes to bytes
        decoded_string = bytes_value.decode('utf-8') # Decode bytes to string
    print(f'decoded_string: {decoded_string}')
    return decoded_string

def go_user_inputs(_set_gas=True):
    global W3_, CONTRACT_ABI # REQUIRED (using assignment)
    W3_ = _web3.myWEB3().init_inp(_set_gas)
    # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
    # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
    # CONTRACT_ABI = _abi.BST_ABI
    # print(' using CONTRACT_ABI = _abi.BST_ABI')

def go_enter_bst_addr():
    global BST_ADDRESS
    while BST_ADDRESS == None or BST_ADDRESS == '':
        BST_ADDRESS = input('\n Enter BST contract address:\n  > ')
    print(f'  using BST_ADDRESS: {BST_ADDRESS}')

def go_select_func():
    global FUNC_SIGN_SEL, BST_FUNC_MAP, IS_WRITE
    print(f'\n Select function to invoke ... (IS_WRITE={IS_WRITE})')
    lst_keys = list(BST_FUNC_MAP.keys())
    for i,k in enumerate(lst_keys):
        print(f'  {i} = {k}')
    ans_idx = input('  > ')
    assert ans_idx.isdigit() and int(ans_idx) >= 0 and int(ans_idx) < len(lst_keys), f'failed ... invalid input {ans_idx}'
    FUNC_SIGN_SEL = list(BST_FUNC_MAP.keys())[int(ans_idx)]
    ans = input(f'\n  Confirm func [y/n]: {FUNC_SIGN_SEL}\n  > ')
    if str(ans).lower() != 'y' and str(ans).lower() != 'yes': go_select_func()

def go_enter_func_params():
    global FUNC_SIGN_SEL, LST_FUNC_SIGN_PARAMS
    ans = input(f'\n  Enter params for: "{FUNC_SIGN_SEL}"\n  > ')
    for v in list(ans.split()):
        if v.lower() == 'true': LST_FUNC_SIGN_PARAMS.append(True)
        elif v.lower() == 'false': LST_FUNC_SIGN_PARAMS.append(False)
        elif v.isdigit(): LST_FUNC_SIGN_PARAMS.append(int(v))
        else: LST_FUNC_SIGN_PARAMS.append(v)

    print(f'  executing "{FUNC_SIGN_SEL}" w/ params: {LST_FUNC_SIGN_PARAMS} ...\n')

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        invoke BST contract functions
         utilizes function hashes instead of contract ABI

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
        # read requests: _set_gas=False
        ans = input("Start 'write' or 'read' request?\n 0 = write\n 1 = read\n > ")
        IS_WRITE = ans=='0'
        BST_FUNC_MAP = _abi.BST_FUNC_MAP_WRITE if IS_WRITE else _abi.BST_FUNC_MAP_READ
        print(f' ans: "{ans}"; IS_WRITE={IS_WRITE}')
        go_user_inputs(_set_gas=IS_WRITE)
        go_enter_bst_addr()
        
        ans = input(f'\n Run Mode...(for IS_WRITE={IS_WRITE})\n  0 = traverse all functions\n  1 = function select loop\n  > ')
        func_sel = ans == '1'
        if func_sel:
            # continue function selection progression until killed
            while func_sel:
                print('', cStrDivider_1, "here we go!", sep='\n')
                go_select_func()
                go_enter_func_params()

                assert input('\n (^) proceed? [y/n]\n  > ') == 'y', f"aborted... _ {get_time_now()}\n"
                print('\n')

                lst_params = BST_FUNC_MAP[FUNC_SIGN_SEL]
                lst_params.insert(2, LST_FUNC_SIGN_PARAMS)
                tup_params = (BST_ADDRESS,lst_params[0],lst_params[1],lst_params[2],lst_params[3])
                if not IS_WRITE:
                    read_with_hash(*tup_params)
                else:
                    write_with_hash(*tup_params)
                print(f'\nBST_ADDRESS: {BST_ADDRESS}\nFUNC_SIGN_SEL: {FUNC_SIGN_SEL}')
        else:
            # loop through all functions in BST_FUNC_MAP
            dict_returns = {}
            for key in list(BST_FUNC_MAP.keys()):
                FUNC_SIGN_SEL = key
                print('', cStrDivider_1, f"time for {FUNC_SIGN_SEL}", sep='\n')
                go_enter_func_params()
                lst_params = BST_FUNC_MAP[FUNC_SIGN_SEL]
                lst_params.insert(2, LST_FUNC_SIGN_PARAMS)
                tup_params = (BST_ADDRESS,lst_params[0],lst_params[1],lst_params[2],lst_params[3])
                if not IS_WRITE:
                    decoded_string = read_with_hash(*tup_params)
                    dict_returns[FUNC_SIGN_SEL] = decoded_string
                else:
                    write_with_hash(*tup_params)
                print(f'\nBST_ADDRESS: {BST_ADDRESS}\nFUNC_SIGN_SEL: {FUNC_SIGN_SEL}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}')
            return_print = pprint.PrettyPrinter().pformat(dict_returns)
            print('all returns...')
            print(return_print)

        # LEFT OFF HERE ... can't get return working...
        #   for 'mapping(address => ACCT_PAYOUT[]) public ACCT_USD_PAYOUTS;'
        # tuple_ = 'tuple(address,uint64,uint64,uint64,uint64,uint64,uint64)[]'
        # read_with_hash(BST_ADDRESS, "8b47da26", ['address'], [W3_.SENDER_ADDRESS], ['address',tuple_]) # "ACCT_USD_PAYOUTS(address,uint256)": "8b47da26",


        # write requests: _set_gas=True
        # go_user_inputs(_set_gas=True)
        # # # // weUSDT
        # usdStable = '0x0Cb6F5a34ad42ec934882A05265A7d5F59b51A2f' 
        # amnt = int(0.012155 * 10**6)
        # write_with_hash(BST_ADDRESS, "3015d747", ['uint64','address'], [amnt,usdStable], []) # "KEEPER_maintenance(uint64,address)": "3015d747",

    except Exception as e:
        print_except(e, debugLvl=0)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')


# tBST9: 0x528F9F50Ea0179aF66D0AC99cdc4E45E55120D92
# tBST1: 0xc679C6FeDc13Aae0CEC1754a9688768Ade3f0443