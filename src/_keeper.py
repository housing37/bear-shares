__fname = '_keeper'
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
from _env import env
import pprint
from attributedict.collections import AttributeDict # tx_receipt requirement
import _web3 # from web3 import Account, Web3, HTTPProvider
import _abi, _gen_pls_key
from ethereum.abi import encode_abi, decode_abi # pip install ethereum
# from _constants import *

DEBUG_LEVEL = 0
LST_CONTR_ABI_BIN = [
    "../bin/contracts/BearSharesTrinity",
]

W3_ = None
ABI_FILE = None
BIN_FILE = None
CONTRACT = None
CONTRACT_ABI = None
BST_ADDRESS = None
BST_FUNC_MAP = {}
IS_WRITE = False
USE_TBF = False # TBFckr contract
USE_ROUTER = False # uniswap v2 router type contract
USE_FLR = False # balancer Flash Loan Recipient contract

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
def get_gas_params_lst(rpc_url, min_params=False, max_params=False, def_params=True, _w3:_web3.myWEB3=None):
    global W3_
    if _w3 == None: _w3 = W3_
    # Estimate the gas cost for the transaction
    #gas_estimate = buy_tx.estimate_gas()
    gas_limit = _w3.GAS_LIMIT # max gas units to use for tx (required)
    gas_price = _w3.GAS_PRICE # price to pay for each unit of gas (optional?)
    max_fee = _w3.MAX_FEE # max fee per gas unit to pay (optional?)
    max_prior_fee = _w3.MAX_PRIOR_FEE # max fee per gas unit to pay for priority (faster) (optional)
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

def write_with_hash(_contr_addr, _func_hash, _lst_param_types, _lst_params, _lst_ret_types, _value_in_wei=0, _w3:_web3.myWEB3=None, _tx_wait_sec=300):
    global W3_
    if _w3 == None: _w3 = W3_

    print('preparing function signature w/ func hash & params lists ...')
    func_sign = _func_hash
    if len(_lst_param_types) > 0:
        func_sign = _func_hash + encode_abi(_lst_param_types, _lst_params).hex()

    print(f'building tx_data w/ ...\n _contr_addr: {_contr_addr}\n _func_hash: 0x{_func_hash}\n _lst_params: {_lst_params}')
    tx_data = {
        "to": _contr_addr,
        "data": func_sign,
        "value":_value_in_wei,
    }

    print('setting tx_params ...')
    tx_nonce = _w3.W3.eth.get_transaction_count(_w3.SENDER_ADDRESS)
    tx_params = {
        'chainId': _w3.CHAIN_ID,
        'nonce': tx_nonce,
    }
    print('setting gas params in tx_params ...')
    lst_gas_params = get_gas_params_lst(_w3.RPC_URL, min_params=False, max_params=True, def_params=True, _w3=_w3)
    for d in lst_gas_params: tx_params.update(d) # append gas params

    print('update tx_data w/ tx_params')
    tx_data.update(tx_params)

    print(f'signing and sending tx w/ NONCE: {tx_nonce} ... {get_time_now()}')
    tx_signed = _w3.W3.eth.account.sign_transaction(tx_data, private_key=_w3.SENDER_SECRET)
    tx_hash = _w3.W3.eth.send_raw_transaction(tx_signed.rawTransaction)

    print(cStrDivider_1, f'waiting for receipt ... {get_time_now()}', sep='\n')
    print(f'    tx_hash: {tx_hash.hex()}')

    # Wait for the transaction to be mined
    # wait_time = 300 # sec
    wait_time = _tx_wait_sec # sec
    try:
        tx_receipt = _w3.W3.eth.wait_for_transaction_receipt(tx_hash, timeout=wait_time)
        print("Transaction confirmed in block:", tx_receipt.blockNumber, f' ... {get_time_now()}')
    except Exception as e:
        print(f"\n{get_time_now()}\n Transaction not confirmed within the specified timeout... wait_time: {wait_time}")
        print_except(e, debugLvl=DEBUG_LEVEL)
        return -1, tx_hash.hex(), {}
        # exit(1)

    # print incoming tx receipt (requires pprint & AttributeDict)
    tx_receipt = AttributeDict(tx_receipt) # import required
    tx_rc_print = pprint.PrettyPrinter().pformat(tx_receipt)
    print(cStrDivider_1, f'RECEIPT:\n {tx_rc_print}', sep='\n')
    print("\nTransaction mined!")
    print(f" return status={tx_receipt['status']}")
    # tx_status = tx_receipt['status']
    # tx_hash = tx_receipt['logs'][0]['transactionHash']
    
    # Get the logs from the transaction receipt
    d_ret_log = parse_logs_for_func_hash(tx_receipt, _func_hash, _w3)
    print('returning from "write_with_hash"')
    return tx_receipt, tx_hash.hex(), d_ret_log

def parse_logs_for_func_hash(_tx_receipt, _func_hash, _w3:_web3.myWEB3=None):
    # Get the logs from the transaction receipt
    logs = _tx_receipt['logs']
    d_ret_log = {'err':'no logs found'}
    if _w3 == None: return d_ret_log
    print(f' event logs (for func_hash: 0x{_func_hash}) ...')
    if _func_hash == _abi.BST_FUNC_MAP_WRITE[_abi.BST_PAYOUT_FUNC_SIGN][0]:
        # Define & filter logs based on the event signature
        # event PayOutProcessed(address _from, address _to, uint64 _usdAmnt, uint64 _usdAmntPaid, uint64 _bstPayout, uint64 _usdFee, uint64 _usdBurnValTot, uint64 _usdBurnVal, uint64 _usdAuxBurnVal, address _auxToken, uint32 _ratioBstPay, uint256 _blockNumber);
        # event_signature = _w3.W3.keccak(text="PayOutProcessed(address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,address,uint32,uint256)").hex()
        # pay_out_logs = [log for log in logs if log['topics'][0].hex() == event_signature]

        evt_sign_0 = _w3.W3.keccak(text="PayOutProcessed(address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,address,uint32,uint256)").hex()
        evt_sign_1 = _w3.W3.keccak(text="BuyAndBurnExecuted(address,uint256)").hex()
        pay_out_logs = [log for log in logs if log['topics'][0].hex() in evt_sign_0]
        
        d_ret_log = {}
        # Parse the event logs
        for log in pay_out_logs:
            lst_evt_params = ['address','address','uint64','uint64','uint64','uint64','uint64','uint64','uint64','address','uint32','uint256']
            decoded_data = decode_abi(lst_evt_params, log['data'])
            d_ret_log.update({'_from':decoded_data[0],
                         '_to':decoded_data[1],
                         '_usdAmnt':decoded_data[2],
                         '_usdAmntPaid':decoded_data[3],
                         '_bstPayout':decoded_data[4],
                         '_usdFee':decoded_data[5],
                         '_usdBurnValTot':decoded_data[6],
                         '_usdBurnVal':decoded_data[7],
                         '_usdAuxBurnVal':decoded_data[8],
                         '_auxToken':decoded_data[9],
                         '_ratioBstPay':decoded_data[10],
                         '_blockNumber':decoded_data[11]})
        
            # [print(f'   {key}: {val}') for key,val in d_ret_log.items()]
            # print()
        
        pay_out_logs = [log for log in logs if log['topics'][0].hex() in evt_sign_1]
        # Parse the event logs
        for log in pay_out_logs:
            lst_evt_params = ['address','uint256']
            decoded_data = decode_abi(lst_evt_params, log['data'])
            d_ret_log.update({'_burnTok':decoded_data[0],
                            '_burnAmnt':decoded_data[1]})
        [print(f'   {key}: {val}') for key,val in d_ret_log.items()]
        print()
        print(decoded_data)

    if _func_hash == _abi.BST_FUNC_MAP_WRITE[_abi.BST_TRADEIN_FUNC_SIGN][0]:
        # Define & filter logs based on the event signature
        # event TradeInProcessed(address _trader, uint64 _bstAmnt, uint64 _usdTradeVal, uint64 _usdBuyBackVal, uint32 _ratioUsdPay, uint256 _blockNumber);
        event_signature = _w3.W3.keccak(text="TradeInProcessed(address,uint64,uint64,uint64,uint32,uint256)").hex()
        pay_out_logs = [log for log in logs if log['topics'][0].hex() == event_signature]
        
        # Parse the event logs
        for log in pay_out_logs:
            lst_evt_params = ['address', 'uint64', 'uint64', 'uint64', 'uint32','uint256']
            evt_data = log['data']
            decoded_data = decode_abi(lst_evt_params, evt_data)
            d_ret_log = {'_trader':decoded_data[0],
                         '_bstAmnt':decoded_data[1],
                         '_usdTradeVal':decoded_data[2],
                         '_usdBuyBackVal':decoded_data[3],
                         '_ratioBstTrade':decoded_data[4],
                         '_blockNumber':decoded_data[5]}
        
            [print(f'   {key}: {val}') for key,val in d_ret_log.items()]
            print()

    if _func_hash == _abi.ROUTERv2_FUNC_MAP_WRITE[_abi.ROUTERv2_FUNC_ADD_LIQ_ETH][0]:
        # Define & filter logs based on the event signature
        # PairCreated(address indexed token0, address indexed token1, address pair, uint256)
        event_signature = _w3.W3.keccak(text="PairCreated(address,address,address,uint256)").hex()
        pay_out_logs = [log for log in logs if log['topics'][0].hex() == event_signature]
        
        # Parse the event logs
        for log in pay_out_logs:
            lst_evt_params = ['address', 'address', 'address','uint256']
            evt_data = log['data']
            decoded_data = decode_abi(lst_evt_params, evt_data)
            d_ret_log = {'_token0':decoded_data[0],
                         '_token1':decoded_data[1],
                         '_pair':decoded_data[2],
                         '_param_3':decoded_data[3]}
        
            [print(f'   {key}: {val}') for key,val in d_ret_log.items()]
            print()
            
    return d_ret_log
            
def read_with_hash(_contr_addr, _func_hash, _lst_param_types, _lst_params, _lst_ret_types):
    global W3_

    print('preparing function signature params ...')
    func_sign = _func_hash
    if len(_lst_param_types) > 0:
        func_sign = _func_hash + encode_abi(_lst_param_types, _lst_params).hex()

    print(f'building tx_data w/ ...\n _contr_addr: {_contr_addr}\n _func_hash: 0x{_func_hash}')
    tx_data = {
        "to": _contr_addr,
        "data": func_sign,
        "from": W3_.SENDER_ADDRESS,
    }

    # Call contract function to retrieve the value of the KEEPER state variable
    print(f'calling contract function _ {get_time_now()}')
    return_val = W3_.W3.eth.call(tx_data)
    print(f'calling contract function _ {get_time_now()} ... DONE')
    print('\nparsing & printing response ...')
    # print(f'return_val: {return_val}')
    # print(f'return_val.hex(): {return_val.hex()}')

    decoded_value_return = decode_abi(_lst_ret_types, return_val)
    # print(json.dumps(decoded_value_return, indent=4))

    hex_bytes = decoded_value_return[0]
    decoded_string = hex_bytes
    # print(f'decoded_string: {decoded_string}')

    if isinstance(hex_bytes, bytes):
        print('found bytes')
        bytes_value = bytes(hex_bytes) # Convert hex bytes to bytes
        decoded_string = bytes_value.decode('utf-8') # Decode bytes to string
    
    print(f'pretty print... cnt: {len(decoded_value_return)}')
    for i in range(len(decoded_value_return)):
        # if isinstance(decoded_value_return[i], str):
        if isinstance(decoded_value_return[i], int):
            # f_val = float(decoded_value_return[i]) / 10 ** 6
            f_val = float(decoded_value_return[i]) / 10 ** 18
            print(f' {f_val:,.3f}')
        elif isinstance(decoded_value_return[i], list):
            print(json.dumps(list(decoded_value_return[i]), indent=4))
        else:
            print(decoded_value_return[i])
    
    if isinstance(decoded_value_return, list) and isinstance(decoded_value_return[0], list) :
        print(f'pretty print... cnt[0]: {len(decoded_value_return[0])}')

    # print(f'decoded_value_return', *decoded_value_return, sep='\n ')
    return decoded_string

def read_with_abi(_contr_addr, _func_hash, _lst_params):
    if _func_hash == _abi.BST_GET_ACCT_PAYOUTS_FUNC_HASH:
        print(f'building contract_abi for func_hash: "{_func_hash}" ...')
        # struct ACCT_PAYOUT {
        #     address receiver;
        #     uint64 usdAmntDebit; // USD total ACCT deduction
        #     uint64 usdPayout; // USD payout value
        #     uint64 bstPayout; // BST payout amount
        #     uint64 usdFeeVal; // USD service fee amount
        #     uint64 usdBurnValTot; // to USD value burned (BST + aux token)
        #     uint64 usdBurnVal; // BST burned in USD value
        #     uint256 auxUsdBurnVal; // aux token burned in USD val during payout
        #     address auxTok; // aux token burned during payout
        #     uint32 ratioBstPay; // rate at which BST was paid (1<:1 USD)
        #     uint256 blockNumber; // current block number of this payout
        # }
        contract_abi = [
            {
                "inputs": [{"internalType": "address", "name": "_account", "type": "address"}],
                "name": "getAccountPayouts",
                "outputs": [{"components": [
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint64", "name": "usdAmntDebit", "type": "uint64"},
                    {"internalType": "uint64", "name": "usdPayout", "type": "uint64"},
                    {"internalType": "uint64", "name": "bstPayout", "type": "uint64"},
                    {"internalType": "uint64", "name": "usdFeeVal", "type": "uint64"},
                    {"internalType": "uint64", "name": "usdBurnValTot", "type": "uint64"},
                    {"internalType": "uint64", "name": "usdBurnVal", "type": "uint64"},
                    {"internalType": "uint256", "name": "auxUsdBurnVal", "type": "uint256"},
                    {"internalType": "address", "name": "auxTok", "type": "address"},
                    {"internalType": "uint32", "name": "ratioBstPay", "type": "uint32"},
                    {"internalType": "uint256", "name": "blockNumber", "type": "uint256"}
                ], "internalType": "struct MyContract.ACCT_PAYOUT[]", "name": "", "type": "tuple[]"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        print(f'building web3 contract w/ abi &\n  _contr_addr: {_contr_addr}')
        contract = W3_.W3.eth.contract(address=_contr_addr, abi=contract_abi)

        print(f'calling contract function _ {get_time_now()}')
        payouts = contract.functions.getAccountPayouts(_lst_params[0]).call()
        print(f'calling contract function _ {get_time_now()} ... DONE')

        print('\nparsing & printing response ...')
        for payout in payouts:
            # print(" Receiver (receiver):", payout[0])
            # print(" USD Amount Debit (usdAmntDebit):", payout[1])
            # print(" USD Payout (usdPayout):", payout[2])
            # print(" BST Payout (bstPayout):", payout[3])
            # print(" USD Fee Value (usdFeeVal):", payout[4])
            # print(" USD Burn Value Total (usdBurnValTot):", payout[5])
            # print(" BST Burned in USD Value (usdBurnVal):", payout[6])
            # print(" Aux Token Burned in USD Value (auxUsdBurnVal):", payout[7])
            # print(" Aux Token (auxTok):", payout[8])
            # f_val = float(payout[0]) / 10 ** 6
            # print(f' {f_val}')

            print(" receiver:", payout[0])
            print(" usdAmntDebit:", float(payout[1]) / 10 ** 6)
            print(" usdPayout:", float(payout[2]) / 10 ** 6)
            print(" bstPayout:", float(payout[3]) / 10 ** 6)
            print(" usdFeeVal:", float(payout[4]) / 10 ** 6)
            print(" usdBurnValTot:", float(payout[5]) / 10 ** 6)
            print(" usdBurnVal:", float(payout[6]) / 10 ** 6)
            print(" auxUsdBurnVal:", float(payout[7]) / 10 ** 6)
            print(" auxTok:", payout[8])

            # print(" receiver:", payout[0])
            # print(" usdAmntDebit:", payout[1])
            # print(" usdPayout:", payout[2])
            # print(" bstPayout:", payout[3])
            # print(" usdFeeVal:", payout[4])
            # print(" usdBurnValTot:", payout[5])
            # print(" usdBurnVal:", payout[6])
            # print(" auxUsdBurnVal:", payout[7])
            # print(" auxTok:", payout[8])
            print()
        return payouts

def go_user_inputs(_set_gas=True):
    global W3_, CONTRACT_ABI # REQUIRED (using assignment)
    W3_ = _web3.myWEB3().init_inp(_set_gas)
    
    # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
    # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
    # CONTRACT_ABI = _abi.BST_ABI
    # print(' using CONTRACT_ABI = _abi.BST_ABI')

def go_enter_bst_addr(_symb='nil_symb'):
    global BST_ADDRESS
    while BST_ADDRESS == None or BST_ADDRESS == '':
        BST_ADDRESS = input(f'\n Enter {_symb} contract address:\n  > ')

    BST_ADDRESS = W3_.W3.to_checksum_address(BST_ADDRESS)
    print(f'  using {_symb}_ADDRESS: {BST_ADDRESS}')

def go_select_func():
    global BST_FUNC_MAP, IS_WRITE
    print(f'\n Select function to invoke ... (IS_WRITE={IS_WRITE})')
    lst_keys = list(BST_FUNC_MAP.keys())
    for i,k in enumerate(lst_keys):
        print(f'  {i} = {k}')
    ans_idx = input('  > ')
    assert ans_idx.isdigit() and int(ans_idx) >= 0 and int(ans_idx) < len(lst_keys), f'failed ... invalid input {ans_idx}'
    func_select = list(BST_FUNC_MAP.keys())[int(ans_idx)]
    ans = input(f'\n  Confirm func [y/n]: {func_select}\n  > ')
    lst_ans_go = ['y','yes','']
    if str(ans).lower() not in lst_ans_go: func_select = go_select_func()
    return func_select

def go_enter_func_params(_func_select):
    lst_func_params = []
    value_in_wei = 0
    ans = input(f'\n  Enter params for: "{_func_select}"\n  > ')
    for v in list(ans.split()):
        if v.lower() == 'true': lst_func_params.append(True)
        elif v.lower() == 'false': lst_func_params.append(False)
        elif v.isdigit(): lst_func_params.append(int(v))
        # elif v.startswith('['): lst_func_params.append([i.strip() for i in v[1:-1].split(',')])
        # elif v.startswith('['): lst_func_params.append([W3_.W3.to_checksum_address(i.strip()) for i in v[1:-1].split(',')])
        elif v.startswith('['):
            lst_str = [i.strip() for i in v[1:-1].split(',')]
            if lst_str[0][1:3] == '0x':
                # appned list of addresses
                lst_func_params.append([W3_.W3.to_checksum_address(i) for i in lst_str])
            elif lst_str[0].isdigit():
                # append list of ints                
                lst_func_params.append([int(i) for i in lst_str])
            else:
                # fall back to appending list of strings
                lst_func_params.append(lst_str)
        else: lst_func_params.append(v)

    # handle edge case: uniswap 'addLiquidityETH'
    if _func_select == _abi.ROUTERv2_FUNC_ADD_LIQ_ETH:
        print(f'\n  found edge case in "{_func_select}"')
        print(f'   inserting & appending additional params to lst_func_params ...\n')
        # lst_func_params[0] = 'token' -> input OG (static idx)
        # lst_func_params[1] = 'amountTokenDesired' -> input OG (static idx)
        # lst_func_params[2] = 'amountETHMin' -> input OG (dynamic idx)
        lst_func_params.insert(2, int(lst_func_params[1])) # insert 'amountTokenMin' into idx #2 (push 'amountETHMin' to #3)
        lst_func_params[3] = W3_.Web3.to_wei(int(float(lst_func_params[3])), 'ether') # update idx #3 'amountETHMin'
        lst_func_params.append(W3_.SENDER_ADDRESS) # append idx #4 -> 'to' 
        lst_func_params.append(int(time.time()) + 3600) # append idx #5 -> 'deadline' == now + 3600 seconds = 1 hour from now

        value_in_wei = lst_func_params[3] # get return value in wei (for write_with_hash)

    print(f'  executing "{_func_select}" w/ params: {lst_func_params} ...\n')
    return lst_func_params, value_in_wei

def gen_random_wallets(_wallet_cnt, _gen_new=True):
    if not _gen_new:
        # return env.RAND_WALLETS, env.RAND_WALLET_CLI_INPUT
        # return env.RAND_WALLETS_20, env.RAND_WALLET_CLI_INPUT_20
        return env.RAND_WALLETS_10, env.RAND_WALLET_CLI_INPUT_10
    else:
        lst_rand_wallets = []
        lst_wallet_addr = []
        for acct_num in range(0,_wallet_cnt): # generate '_wallet_cnt' number of wallets
            d_wallet = _gen_pls_key.gen_pls_key(str("english"), int(256), acct_num, False) # language, entropyStrength, num, _plog
            lst_rand_wallets.append(dict(d_wallet))
            lst_wallet_addr.append(d_wallet['address'])

        # pprint.pprint(lst_rand_wallets)
        file_cnt = len(os.listdir('./_wallets'))
        with open(f"./_wallets/wallets_{file_cnt}_{get_time_now()}.txt", "w") as file:
            pprint.pprint(lst_rand_wallets, stream=file)
            pprint.pprint(lst_rand_wallets)

        # generate formatted string for CLI input
        str_rand_wallet_cli_input = '[' + ','.join(map(str, lst_wallet_addr)) + ']'
        return lst_rand_wallets, str_rand_wallet_cli_input

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
        symb = 'BST'

        # read requests: _set_gas=False
        ans = input("Start 'write' or 'read' request?\n 0 = write\n 1 = read\n > ")
        IS_WRITE = ans=='0'
        BST_FUNC_MAP = _abi.BST_FUNC_MAP_WRITE if IS_WRITE else _abi.BST_FUNC_MAP_READ
        print(f' ans: "{ans}"; IS_WRITE={IS_WRITE}, set BST_FUNC_MAP')

        # check to show or generate new wallets
        ans = input("\nGenerate / show random wallets? [y(1)/n]\n > ")
        gen_addies = ans.lower()=='y' or ans == '1'
        if gen_addies:
            # NOTE: gen/fetch/print CLI input string needed to 
            #   manually feed into 'KEEPER_mixAmntRand' & 'distrAmntRand'
            wallet_cnt = 10
            gen_new = False # False = use _abi.RAND_WALLETS & _abi.RAND_WALLET_CLI_INPUT
            print(f' fetching {wallet_cnt} random wallets (gen_new={gen_new}) ...')
            lst_rand_wallets, str_rand_wallet_cli_input = gen_random_wallets(wallet_cnt, gen_new)
            print(f' fetching {len(lst_rand_wallets)} random wallets (gen_new={gen_new}) ... DONE')
            print(f' ... fetched wallets CLI input ...\n {str_rand_wallet_cli_input}')  # This will print the formatted string    

            ## end ##
            if gen_new:
                print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')
                exit()

        # check for using TBF or uniswap v2 ROUTER contract
        ans = input("\nSelect contract func list to use ...\n 0 = 'BST'\n 1 = 'TBF (or standard ERC20)'\n 2 = 'UswapV2Router'\n 3 = 'FLR (FlashLoanRecipient)'\n 4 = 'UswapV2Pair'\n 5 = 'LPCleaner'\n 6 = 'UniswapFlashQuery'\n > ")
        opt_sel_str = 'nil_sel_str'
        symb = 'nil_symb_init'
        USE_TBF = ans == '1'
        USE_ROUTER = ans == '2'
        USE_FLR = ans == '3'
        use_pair = ans == '4'
        use_lpcleaner = ans == '5'
        use_flashquery = ans == '6'
        
        if USE_TBF:
            symb = 'TBF|ERC20'
            BST_FUNC_MAP = _abi.TBF_FUNC_MAP_WRITE if IS_WRITE else _abi.TBF_FUNC_MAP_READ
            opt_sel_str = f"USE_TBF={USE_TBF}"
            # print(f' ans: "{ans}"; USE_TBF={USE_TBF}, reset BST_FUNC_MAP')
        if USE_ROUTER:
            symb = 'ROUTER|USWAPv2'
            BST_FUNC_MAP = _abi.ROUTERv2_FUNC_MAP_WRITE if IS_WRITE else _abi.USWAPv2_ROUTER_FUNC_MAP_READ
            opt_sel_str = f"USE_ROUTER={USE_ROUTER}"
            # print(f' ans: "{ans}"; USE_ROUTER={USE_ROUTER}, reseting BST_FUNC_MAP')
        if USE_FLR:
            symb = 'FLR'
            BST_FUNC_MAP = _abi.BALANCER_FLR_FUNC_MAP_WRITE if IS_WRITE else _abi.BALANCER_FLR_FUNC_MAP_READ
            opt_sel_str = f"USE_FLR={USE_FLR}"
        if use_pair:
            symb = 'PAIR|USWAPv2'
            BST_FUNC_MAP = _abi.USWAPv2_PAIR_FUNC_MAP_WRITE if IS_WRITE else _abi.USWAPv2_PAIR_FUNC_MAP_READ
            opt_sel_str = f"use_pair={use_pair}"
        if use_lpcleaner:
            symb = 'LPCleaner'
            BST_FUNC_MAP = _abi.LPCleaner_FUNC_MAP_WRITE if IS_WRITE else _abi.LPCleaner_FUNC_MAP_READ
            opt_sel_str = f"use_lpcleaner={use_lpcleaner}"
        if use_flashquery:
            symb = 'UniswapFlashQuery'
            BST_FUNC_MAP = _abi.UniswapFlashQuery_FUNC_MAP_WRITE if IS_WRITE else _abi.UniswapFlashQuery_FUNC_MAP_READ
            opt_sel_str = f"use_flashquery={use_flashquery}"
        
        print(f' ans: "{ans}"; {opt_sel_str}, reseting BST_FUNC_MAP')
        
        go_user_inputs(_set_gas=IS_WRITE)
        go_enter_bst_addr(symb)
        
        ans = input(f'\n Run Mode...(for IS_WRITE={IS_WRITE})\n  0 = traverse all functions\n  1 = function select loop\n  > ')
        func_sel = ans == '1'
        if func_sel:
            # continue function selection progression until killed
            while func_sel:
                print('', cStrDivider_1, f"here we go! _ IS_WRITE={IS_WRITE}", sep='\n')
                func_select = go_select_func()
                lst_func_params, value_in_wei = go_enter_func_params(func_select)
                lst_params = list(BST_FUNC_MAP[func_select])
                lst_params.insert(2, lst_func_params)
                tup_params = (BST_ADDRESS,lst_params[0],lst_params[1],lst_params[2],lst_params[3])
                try:
                    if not IS_WRITE:
                        if lst_params[0] == _abi.BST_GET_ACCT_PAYOUTS_FUNC_HASH:
                            read_with_abi(BST_ADDRESS, lst_params[0], lst_params[2])
                        else:
                            read_with_hash(*tup_params)
                    else:
                        tup_params = tup_params + (value_in_wei,)
                        write_with_hash(*tup_params)
                except Exception as e:
                    print_except(e, debugLvl=DEBUG_LEVEL)
                print(f'\n{symb}_ADDRESS: {BST_ADDRESS}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_select}')
                # assert input('\n (^) proceed? [y/n]\n  > ') == 'y', f"aborted... _ {get_time_now()}\n\n"
        else:
            # loop through all functions in BST_FUNC_MAP
            dict_returns = {}
            for key in list(BST_FUNC_MAP.keys()):
                print('', cStrDivider_1, f"time for {key}", sep='\n')
                func_select = key
                lst_func_params, value_in_wei = go_enter_func_params(func_select)
                lst_params = list(BST_FUNC_MAP[func_select])
                lst_params.insert(2, lst_func_params)
                tup_params = (BST_ADDRESS,lst_params[0],lst_params[1],lst_params[2],lst_params[3])
                try:
                    if not IS_WRITE:
                        if lst_params[0] == _abi.BST_GET_ACCT_PAYOUTS_FUNC_HASH:
                            decoded_string = read_with_abi(BST_ADDRESS, lst_params[0], lst_params[2])
                        else:
                            decoded_string = read_with_hash(*tup_params)
                        dict_returns[func_select] = decoded_string
                    else:
                        write_with_hash(*tup_params)
                except Exception as e:
                    print_except(e, debugLvl=DEBUG_LEVEL)
                print(f'\n{symb}_ADDRESS: {BST_ADDRESS}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_select}')
            return_print = pprint.PrettyPrinter().pformat(dict_returns)
            print(f'all returns... cnt={len(dict_returns.keys())}')
            print(return_print)

    except Exception as e:
        print_except(e, debugLvl=DEBUG_LEVEL)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')
