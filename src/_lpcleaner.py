__fname = '_lpcleaner' # -> 051522: copy of _keeper.py
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
cStrDivider_1 = '#----------------------------------------------------------------#'

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os, traceback, time, pprint, json
from datetime import datetime
from _env import env
import pprint
from attributedict.collections import AttributeDict # tx_receipt requirement
import _web3 # from web3 import Account, Web3, HTTPProvider
import _abi, _gen_pls_key
from ethereum.abi import encode_abi, decode_abi # pip install ethereum
from _constants import FACTORY_pulsex_router_02_v2 as PULSEX_V2_FACTORY

DEBUG_LEVEL = 0
LST_CONTR_ABI_BIN = [
    "../bin/contracts/BearSharesTrinity",
]

W3_ = None
ABI_FILE = None
BIN_FILE = None
CONTRACT = None
CONTRACT_ABI = None

# note: params checked/set in priority order; 'def|max_params' uses 'mpf_ratio'
#   if all params == False, falls back to 'min_params=True' (ie. just use 'gas_limit')
def get_gas_params_lst(rpc_url, min_params=False, max_params=False, def_params=True, _w3:_web3.myWEB3=None):
    global W3_
    if _w3 == None: _w3 = W3_
    # Estimate the gas cost for the transaction
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

    if DEBUG_LEVEL > 1: print('preparing function signature params ...')
    func_sign = _func_hash
    if len(_lst_param_types) > 0:
        func_sign = _func_hash + encode_abi(_lst_param_types, _lst_params).hex()

    if DEBUG_LEVEL > 1: print(f'building tx_data w/ ...\n _contr_addr: {_contr_addr}\n _func_hash: 0x{_func_hash}')
    tx_data = {
        "to": _contr_addr,
        "data": func_sign,
        "from": W3_.SENDER_ADDRESS,
    }

    # Call contract function to retrieve the value of the KEEPER state variable
    if DEBUG_LEVEL > 1: print(f'calling contract function _ {get_time_now()}')
    return_val = W3_.W3.eth.call(tx_data)
    if DEBUG_LEVEL > 1: print(f'calling contract function _ {get_time_now()} ... DONE')
    if DEBUG_LEVEL > 1: print('\nparsing & printing response ...')
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
    
    if DEBUG_LEVEL > 0: print(f'pretty print... cnt: {len(decoded_value_return)}')
    for i in range(len(decoded_value_return)):
        # if isinstance(decoded_value_return[i], str):
        if isinstance(decoded_value_return[i], int):
            # f_val = float(decoded_value_return[i]) / 10 ** 6
            f_val = float(decoded_value_return[i]) / 10 ** 18
            if DEBUG_LEVEL > 1: print(f' {f_val:,.3f}')
        elif isinstance(decoded_value_return[i], list):
            if DEBUG_LEVEL > 1: print(json.dumps(list(decoded_value_return[i]), indent=4))
        else:
            if DEBUG_LEVEL > 1: print(decoded_value_return[i])
    
    if isinstance(decoded_value_return, list) and isinstance(decoded_value_return[0], list) :
        if DEBUG_LEVEL > 0: print(f'pretty print... cnt[0]: {len(decoded_value_return[0])}')

    # print(f'decoded_value_return', *decoded_value_return, sep='\n ')
    # return decoded_string
    return decoded_value_return

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
            print(" receiver:", payout[0])
            print(" usdAmntDebit:", float(payout[1]) / 10 ** 6)
            print(" usdPayout:", float(payout[2]) / 10 ** 6)
            print(" bstPayout:", float(payout[3]) / 10 ** 6)
            print(" usdFeeVal:", float(payout[4]) / 10 ** 6)
            print(" usdBurnValTot:", float(payout[5]) / 10 ** 6)
            print(" usdBurnVal:", float(payout[6]) / 10 ** 6)
            print(" auxUsdBurnVal:", float(payout[7]) / 10 ** 6)
            print(" auxTok:", payout[8])
            print()
        return payouts

def go_user_inputs(_set_gas=True):
    global W3_, CONTRACT_ABI # REQUIRED (using assignment)
    W3_ = _web3.myWEB3().init_inp(_set_gas)
    
    # ABI_FILE, BIN_FILE = W3_.inp_sel_abi_bin(LST_CONTR_ABI_BIN) # returns .abi|bin
    # CONTRACT_ABI = W3_.read_abi_file(ABI_FILE)
    # CONTRACT_ABI = _abi.BST_ABI
    # print(' using CONTRACT_ABI = _abi.BST_ABI')

def go_input_contr_addr(_symb='nil_symb', _contr_addr=None):
    while _contr_addr == None or _contr_addr == '':
        _contr_addr = input(f'\n Enter {_symb} contract address:\n > ')

    _contr_addr = W3_.W3.to_checksum_address(_contr_addr)
    if DEBUG_LEVEL > 1: print(f'  using {_symb}_ADDRESS: {_contr_addr}')
    return _contr_addr

def go_select_func(_bst_func_map=None):
    print(f'\n Select function to invoke ...')
    lst_keys = list(_bst_func_map.keys())
    for i,k in enumerate(lst_keys):
        print(f'  {i} = {k}')
    ans_idx = input('  > ')
    assert ans_idx.isdigit() and int(ans_idx) >= 0 and int(ans_idx) < len(lst_keys), f'failed ... invalid input {ans_idx}'
    func_select = list(_bst_func_map.keys())[int(ans_idx)]
    ans = input(f'\n  Confirm func [y/n]: {func_select}\n  > ')
    lst_ans_go = ['y','yes','']
    if str(ans).lower() not in lst_ans_go: func_select = go_select_func()
    return func_select

# NOTE: ex _ans = '0xc629e65d4d 0 true false [0x149b277ee166f9f,0x146e1a240ae32]'
def go_enter_func_params(_contr_address, _func_select, _lst_abi_params=None, _str_inp_params=None):
    lst_func_params = []
    value_in_wei = 0
    if _str_inp_params == None:
        _str_inp_params = input(f'\n  Enter params for: "{_func_select}"\n  > ')
    for v in list(_str_inp_params.split()):
        if v.lower() == 'true': lst_func_params.append(True)
        elif v.lower() == 'false': lst_func_params.append(False)
        elif v.isdigit(): lst_func_params.append(int(v))
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

    if DEBUG_LEVEL > 1: print(f'  executing "{_func_select}" w/ params: {lst_func_params} ...\n')
    # return lst_func_params, value_in_wei

    # update _lst_hash_params with everything and return tuple ready for 'read|write_with_hash'
    _lst_abi_params.insert(2, lst_func_params)
    tup_params = (_contr_address,_lst_abi_params[0],_lst_abi_params[1],_lst_abi_params[2],_lst_abi_params[3])
    return tup_params

def go_select_contract(_autofill=False, _is_write=False):
    is_write = _is_write
    if _autofill:
        symb = 'UniswapFlashQuery'
        contr_func_map = _abi.UniswapFlashQuery_FUNC_MAP_WRITE if is_write else _abi.UniswapFlashQuery_FUNC_MAP_READ
        opt_sel_str = f"use_flashquery={True}"
        print(f' auto-ans: "{symb}"; {opt_sel_str}, reset contr_func_map')
        return symb, contr_func_map, opt_sel_str
    
    # check for using TBF or uniswap v2 ROUTER contract
    ans = input("\nSelect contract func list to use ...\n 0 = 'BST'\n 1 = 'TBF (or standard ERC20)'\n 2 = 'UswapV2Router'\n 3 = 'FLR (FlashLoanRecipient)'\n 4 = 'UswapV2Pair'\n 5 = 'LPCleaner'\n 6 = 'UniswapFlashQuery'\n > ")
    opt_sel_str = 'nil_sel_str'
    symb = 'nil_symb_init'
    use_bst = ans == '0' or True # True = default to BST
    use_tbf = ans == '1' # TBFckr contract
    use_router = ans == '2' # uniswap v2 router type contract
    use_flr = ans == '3' # balancer Flash Loan Recipient contract
    use_pair = ans == '4'
    use_lpcleaner = ans == '5'
    use_flashquery = ans == '6'

    if use_bst: # NOTE: first check required to act as default
        symb = 'BST'
        contr_func_map = _abi.BST_FUNC_MAP_WRITE if is_write else _abi.BST_FUNC_MAP_READ
        opt_sel_str = f"use_bst={use_bst}"
    if use_tbf:
        symb = 'TBF|ERC20'
        contr_func_map = _abi.TBF_FUNC_MAP_WRITE if is_write else _abi.TBF_FUNC_MAP_READ
        opt_sel_str = f"use_tbf={use_tbf}"
    if use_router:
        symb = 'ROUTER|USWAPv2'
        contr_func_map = _abi.ROUTERv2_FUNC_MAP_WRITE if is_write else _abi.USWAPv2_ROUTER_FUNC_MAP_READ
        opt_sel_str = f"use_router={use_router}"
    if use_flr:
        symb = 'FLR'
        contr_func_map = _abi.BALANCER_FLR_FUNC_MAP_WRITE if is_write else _abi.BALANCER_FLR_FUNC_MAP_READ
        opt_sel_str = f"use_flr={use_flr}"
    if use_pair:
        symb = 'PAIR|USWAPv2'
        contr_func_map = _abi.USWAPv2_PAIR_FUNC_MAP_WRITE if is_write else _abi.USWAPv2_PAIR_FUNC_MAP_READ
        opt_sel_str = f"use_pair={use_pair}"
    if use_lpcleaner:
        symb = 'LPCleaner'
        contr_func_map = _abi.LPCleaner_FUNC_MAP_WRITE if is_write else _abi.LPCleaner_FUNC_MAP_READ
        opt_sel_str = f"use_lpcleaner={use_lpcleaner}"
    if use_flashquery:
        symb = 'UniswapFlashQuery'
        contr_func_map = _abi.UniswapFlashQuery_FUNC_MAP_WRITE if is_write else _abi.UniswapFlashQuery_FUNC_MAP_READ
        opt_sel_str = f"use_flashquery={use_flashquery}"
    print(f' ans: "{ans}"; {opt_sel_str}, reset contr_func_map')
    return symb, contr_func_map, opt_sel_str

def go_select_read_write():
    # read requests: _set_gas=False
    ans = input("Start 'write' or 'read' request?\n 0 = write\n 1 = read\n > ")
    is_write = ans=='0'
    print(f' ans: "{ans}"; is_write={is_write}')
    return is_write

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        invoke any contract functions
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
        # list holders for algo support values
        #  to use in whiteboarded algo's 1 & 2
        lst_lp_trio_algo_1 = []
        lst_lp_trio_algo_2 = []

        # 'UniswapFlashQuery' support
        go_user_inputs(_set_gas=False) # select chain, sender, _set_gas=False (read request)
        symb, contr_func_map, opt_sel_str = go_select_contract(_autofill=True, _is_write=False) # _autofill is 'UniswapFlashQuery' w/ read
        contr_addr = go_input_contr_addr(symb, _contr_addr=None) # 'UniswapFlashQuery'

        # get tuple ready for 'read|write_with_hash'
        func_sign = "getPairsByIndexRange_OG(address,uint256,uint256)" # 'UniswapFlashQuery'
        inp_params = f"{PULSEX_V2_FACTORY} 0 5"
        tup_params = go_enter_func_params(contr_addr, func_sign, list(contr_func_map[func_sign]), inp_params)

        try:
            print(f'\nGETTING LIST OF LPs FROM UniswapFlashQuery _ {get_time_now()}')
            lst_return = read_with_hash(*tup_params)
            lst_lps = lst_return[0] # get list of LPs (each LP = list of addresses)
            # print(json.dumps(list(lst_lps), indent=2))
            print(f'GETTING LIST OF LPs FROM UniswapFlashQuery _ {get_time_now()} _ DONE')
            print(f'\nSEARCHING LPs FOR CANDIDATE PAIRS _ {get_time_now()}\n (ie. traversing {len(lst_lps)} LPs recieved from on-chain) ...\n')
            lst_connected_lps = []
            for x in range(0, len(lst_lps)):
                tokx_0, tokx_1, tokx_p = lst_lps[x][0], lst_lps[x][1], lst_lps[x][2]
                if DEBUG_LEVEL > 0: print(cStrDivider_1, f'[{x}] checking {tokx_0, tokx_1} ...', cStrDivider_1, sep='\n')
                for y in range(x+1, len(lst_lps)):
                    toky_0, toky_1, toky_p = lst_lps[y][0], lst_lps[y][1], lst_lps[y][2]
                    if DEBUG_LEVEL > 0:
                        print(f'[{x}.{y}] checking {tokx_0, tokx_1}')
                        print(f'          -> {toky_0, toky_1}')
                        print('           ...')

                    # search x & y pairs for matching tokens
                    #   if found, add the non-matching tokens to lst_cand_pair
                    lst_cand_pair = [toky_1 if x==toky_0 else toky_0 for x in [tokx_0, tokx_1] if x in [toky_0, toky_1]]
                    lst_cand_pair.extend([tokx_1 if y==tokx_0 else tokx_0 for y in [toky_0, toky_1] if y in [tokx_0, tokx_1]])

                    if DEBUG_LEVEL > 0: print(f'    lst_cand_pair: {lst_cand_pair}\n')
                    if len(lst_cand_pair) == 2:
                        if DEBUG_LEVEL > 0: 
                            print('found a candidate pair ...')
                            print(f'  -> {tokx_0, tokx_1}\n  -> {toky_0, toky_1}')
                            print('\nsearching candidate pair adddress ...')
                        # get tuple ready for 'read|write_with_hash'
                        #   need pair from this candidate token combo)
                        #    (use 'getPair' from factory)
                        symb_1 = 'pulsexv2factory' # 'UniswapV2Factory'
                        contr_addr_1 = go_input_contr_addr(symb_1, _contr_addr=PULSEX_V2_FACTORY) # 'UniswapV2Factory'
                        func_sign_1 = "getPair(address,address)" # 'UniswapV2Factory'
                        inp_params_1 = f"{lst_cand_pair[0]} {lst_cand_pair[1]}"
                        tup_params_1 = go_enter_func_params(contr_addr_1, func_sign_1, list(contr_func_map[func_sign_1]), inp_params_1)
                        try:
                            lst_return = read_with_hash(*tup_params_1)
                            lp_cand_addr = lst_return[0]
                            if DEBUG_LEVEL > 0: print(f'\n found candidate pair LP address: {lp_cand_addr}\n')
                            if len(lst_return) > 1: print(f'\n\n **WARNING**\n  func returned more than 1 cand pair address: {lst_return}\n\n')

                            # at this point ... we found an LP trio to work with 
                            #   (ie. we foud 3 tokens, all paired with each other)
                            lp_trio = [[tokx_0, tokx_1, tokx_p], [toky_0, toky_1, toky_p], [lst_cand_pair[0], lst_cand_pair[1], lp_cand_addr]]

                            # now we need to get reserves for this LP trio
                            symb_2 = symb # 'UniswapFlashQuery'
                            contr_addr_2 = go_input_contr_addr(symb_2, _contr_addr=contr_addr) # 'UniswapFlashQuery'
                            func_sign_2 = "getReservesByPairs(address[])" # 'UniswapFlashQuery'
                            inp_params_2 = f"[{lp_trio[0][2]},{lp_trio[1][2]},{lp_trio[2][2]}]"
                            tup_params_2 = go_enter_func_params(contr_addr_2, func_sign_2, list(contr_func_map[func_sign_2]), inp_params_2)
                            try:
                                lst_return = read_with_hash(*tup_params_2)
                                lst_reserves = lst_return[0]
                                if DEBUG_LEVEL > 0: print(f'\n found current reserves ...')
                                if DEBUG_LEVEL > 0: print(json.dumps(lst_reserves, indent=2))
                                for i in range(0,len(lp_trio)): lp_trio[i].extend(lst_reserves[i])
                            except Exception as e:
                                print_except(e, debugLvl=DEBUG_LEVEL)
                            if DEBUG_LEVEL > 0: print(f'\n{symb_2}_ADDRESS: {contr_addr_2}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_sign_2}')
                            
                            # add generated trio to algo 1 & 2 lists
                            #   ex: lp_trio = [
                            #                 "0x95b303987a60c71504d99aa1b13b4da07b0790ab", # token0
                            #                 "0xa1077a294dde1b09bb078844df40758a5d0f9a27", # token1
                            #                 "0x149b2c629e652f2e89e11cd57e5d4d77ee166f9f", # pair
                            #                 28704539784100611350783440879, # token0 reserves
                            #                 12187118246744722302468490448, # token1 reserves
                            #                 1715891735 # reserves timestamp
                            #             ]
                            lst_lp_trio_algo_1.append(lp_trio)
                            lst_lp_trio_algo_2.append(lp_trio)

                        except Exception as e:
                            print_except(e, debugLvl=DEBUG_LEVEL)
                        if DEBUG_LEVEL > 0: print(f'\n{symb_1}_ADDRESS: {contr_addr_1}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_sign_1}')
        except Exception as e:
            print_except(e, debugLvl=DEBUG_LEVEL)

        print(f'\nFOUND {len(lst_lp_trio_algo_1)} LP trio candidates for algo 1 _ {get_time_now()}')
        print('lst_lp_trio_algo_1', json.dumps(lst_lp_trio_algo_1, indent=2), 'lst_lp_trio_algo_1', sep='\n')
        print(f'FOUND {len(lst_lp_trio_algo_1)} LP trio candidates for algo 1 _ {get_time_now()} _ DONE')

        print(f'\n{symb_2}_ADDRESS: {contr_addr_2}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_sign_2}')
        print(f'\n{symb_1}_ADDRESS: {contr_addr_1}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_sign_1}')
        print(f'\n{symb}_ADDRESS: {contr_addr}\nSENDER_ADDRESS: {W3_.SENDER_ADDRESS}\n func_select: {func_sign}')
        
    except Exception as e:
        print_except(e, debugLvl=DEBUG_LEVEL)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')