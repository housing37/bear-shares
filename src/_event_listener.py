__fname = '_event_listener'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
cStrDivider_1 = '#----------------------------------------------------------------#'

''' house_102823
    ref: https://docs.balancer.fi/reference/contracts/apis/vault.html#flashloan
        flashLoan(
            IFlashLoanRecipient recipient,
            IERC20[] tokens,
            uint256[] amounts,
            bytes userData)

        emits FlashLoan(IFlashLoanRecipient indexed recipient,
                        IERC20 indexed token,
                        uint256 amount,
                        uint256 feeAmount)
'''
from web3 import Web3, HTTPProvider
# from web3.contract import ConciseContract
import time
from _env import env
# #------------------------------------------------------------#
# #------------------------------------------------------------#
# #print('getting keys and setting globals ...')
# ### SETTINGS ##
# #abi_file = "../contracts/BalancerFLR.json"
# #bin_file = "../contracts/BalancerFLR.bin"
# #------------------------------------------------------------#
# sel_chain = input('\nSelect chain:\n  0 = ethereum mainnet\n  1 = pulsechain mainnet\n  > ')
# assert 0 <= int(sel_chain) <= 1, 'Invalid entry, abort'
# (RPC_URL, CHAIN_ID) = (env.eth_main, env.eth_main_cid) if int(sel_chain) == 0 else (env.pc_main, env.pc_main_cid)

# sel_send = input(f'\nSelect sender: (_event_listener: n/a)\n  0 = {env.sender_address_3}\n  1 = {env.sender_address_1}\n  > ')
# assert 0 <= int(sel_send) <= 1, 'Invalid entry, abort'
# (SENDER_ADDRESS, SENDER_SECRET) = (env.sender_address_3, env.sender_secret_3) if int(sel_send) == 0 else (env.sender_address_1, env.sender_secret_1)
# #------------------------------------------------------------#
# #LST_CONTR_ARB_ADDR = [
# #    "0x59012124c297757639e4ab9b9e875ec80a5c51da", # deployed eth main 102823_1550
# #    "0x48af7d501bca526171b322ac2d8387a8cf085850", # deployed eth main 102823_2140
# #    "0x0B3f73687A5F78ACbdEccF860cEd0d8A5630F806", # deployed pc main 103023_2128
# #    "0xc2fa6dF341b18AE3c283CE3E7C0f1b4F5F6cabBb", # deployed pc main 110123_1953
# #    "0x42b2dDF6cd1C4c269785a228D40307a1e0441c77", # deployed pc main 110323_1649
# #    "0xF02e6E28E250073583766D77e161f67C21aEe388", # deployed pc main 110323_1715
# #    "0xc3B031914Ef19E32859fbe72b52e1240335B60da", # deployed pc main 110323_1759
# #    "0x4e24f4814306fd8cA4e63f342E8AF1675893c002", # deployed pc main 110323_1902 (TEST)
# #    "0x8cC1fa4FA6aB21D25f07a69f8bBbCbEAE7AD150d", # deployed pc main 110323_1937 (TEST)
# #    "0x5605ca222d290dFf31C4174AbCDFadc7DED90915", # deployed pc main 110323_2301 (TEST)
# #]
# print(f'\nSelect arbitrage contract to use:')
# for i, v in enumerate(LST_CONTR_ARB_ADDR): print(' ',i, '=', v)
# idx = input('  > ')
# assert 0 <= int(idx) < len(LST_CONTR_ARB_ADDR), 'Invalid input, aborting...\n'
# CONTR_ARB_ADDR = str(LST_CONTR_ARB_ADDR[int(idx)])
# #------------------------------------------------------------#
# print(f'''\nINITIALIZING web3 ...
#     RPC: {RPC_URL}
#     ChainID: {CHAIN_ID}
#     SENDER: {SENDER_ADDRESS}
#     ARB CONTRACT: {CONTR_ARB_ADDR}''')
# W3 = Web3(HTTPProvider(RPC_URL))

# print(f'\nreading abi file from contract {CONTR_ARB_ADDR} ...')
# with open("../contracts/BalancerFLR.json", "r") as file: CONTR_ARB_ABI = file.read()
# #------------------------------------------------------------#

# from web3 import Web3, HTTPProvider

# Connect to an Ethereum node
# w3 = Web3(HTTPProvider('http://localhost:8545'))  # Assuming you're running a local Ethereum node

import _web3
W3_ = _web3.myWEB3().init_nat(1, env.sender_addr_trinity, env.sender_secr_trinity, default_gas=True) # 1 = pulsechain
# Event signature
event_signature = W3_.W3.keccak(text="PayOutProcessed(address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,address,uint32,uint256)").hex()

import _bst_keeper

# Function to get event logs
def get_event_logs(tx_hash, event_signature):
    # Get transaction receipt
    tx_receipt = W3_.W3.eth.get_transaction_receipt(tx_hash)
    d_ret_log = _bst_keeper.parse_logs_for_func_hash(tx_receipt, '5c1b4b51', W3_)    
    return d_ret_log
    # Get logs
    # logs = []
    # if tx_receipt:
    #     logs = W3_.W3.eth.get_logs({'address': tx_receipt['contractAddress'], 'topics': [event_signature]})
    
    # return logs

# Example transaction hash
tx_hash = '0xee2d3d10cfc5fd4c1a42f0de2de96a41ddcbb43773248365815eb8d4c62c3fd5'

# Get event logs
event_logs = get_event_logs(tx_hash, event_signature)

# Print event logs
for log in event_logs:
    print(log)









# import _abi, _web3
# import pprint

# W3_ = _web3.myWEB3().init_inp(_set_gas=False)
# CONTR_ARB_ABI = _abi.BST_ABI
# # CONTR_ARB_ADDR = '0x528F9F50Ea0179aF66D0AC99cdc4E45E55120D92'
# CONTR_ARB_ADDR = input('\n Enter BST contract address ...\n  > ')
# # Create a contract instance
# CONTR_ARB_ADDR = W3_.W3.to_checksum_address(CONTR_ARB_ADDR)
# contract = W3_.W3.eth.contract(address=CONTR_ARB_ADDR, abi=CONTR_ARB_ABI)

# # Event listener
# def event_callback(event):
#     print(f"Event {event['event']} triggered with arguments: {event['args']}")

# # Listen for events
# print(f'\nwaiting for events from contract {CONTR_ARB_ADDR} ...')
# while True:
#     time.sleep(5) # wait 5 sec
#     print('.', end=' ', flush=True)
#     # Start listening for all events
#     for event_abi in CONTR_ARB_ABI:
#         if event_abi['type'] == 'event':
#             event_name = event_abi['name']
#             event_filter = contract.events[event_name].create_filter(fromBlock='latest')
#             event_logs = event_filter.get_all_entries()
#             for event in event_logs:
#                 event_callback(event)









# def handle_event(event):
#     # c = event["args"]["contr"]
#     # s = event["args"]["sender"]
#     # m = event["args"]["message"]
#     bnum = event["blockNumber"]
#     # print(f'\n[EVT] _ b|{bnum} _ ',"Contract: ", c, "Sender: ", s, "Msg: ", m)

#     return_print = pprint.PrettyPrinter().pformat(event)
#     print(f'\n[EVT] _ b|{bnum} _ ',return_print, sep='\n')
# #    print("Event received:")
# #    print("Contract:", event["args"]["contr"])
# #    print("Sender:", event["args"]["sender"])
# #    print("Message:", event["args"]["message"])
# #    print("Block Number:", event["blockNumber"])

# # Set up an event filter
# # event_filter_0 = contract.events.logX.create_filter(fromBlock="latest")
# # event_filter_1 = contract.events.logMFL.create_filter(fromBlock="latest")
# # event_filter_2 = contract.events.logRFL.create_filter(fromBlock="latest")
# # event_filter_0 = contract.events.KeeperTransfer.create_filter(fromBlock="latest")

# # event_filter_1 = contract.events.ServiceFeeUpdate.create_filter(fromBlock="latest")
# # event_filter_2 = contract.events.ServiceBurnUpdate.create_filter(fromBlock="latest")
# # event_filter_3 = contract.events.TradeInFeeUpdate.create_filter(fromBlock="latest")

# # event_filter_4 = contract.events.MarketBuyEnabled.create_filter(fromBlock="latest")
# # event_filter_5 = contract.events.MarketQuoteEnabled.create_filter(fromBlock="latest")
# # event_filter_6 = contract.events.DepositReceived.create_filter(fromBlock="latest")

# # event_filter_7 = contract.events.PayOutProcessed.create_filter(fromBlock="latest")
# # event_filter_8 = contract.events.TradeInProcessed.create_filter(fromBlock="latest")

# # Listen for events
# print(f'\nwaiting for events from contract {CONTR_ARB_ADDR} ...')
# while True:
#     time.sleep(5) # wait 5 sec
#     print('.', end=' ', flush=True)
#     events = contract.events.Transfer().get_logs(fromBlock='latest', toBlock='latest') # toBlock='latest' (default)
#     for i, event in enumerate(events):
#         handle_event(event)

    # for event in event_filter_0.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_1.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_2.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_3.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_4.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_5.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_6.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_7.get_new_entries():
    #     handle_event(event)
    # for event in event_filter_8.get_new_entries():
    #     handle_event(event)
#########

## Replace with the event signature (topic) of the event you want to listen for
#event_signature = W3.keccak(text="FlashLoan(IFlashLoanRecipient,IERC20,uint256,uint256)").hex()
#
## Create a function to handle the event
#def handle_event(event):
#    print("FlashLoan event received:")
#    print("Recipient:", event['args']['recipient'])
#    print("Token:", event['args']['token'])
#    print("Amount:", event['args']['amount'])
#    print("Fee Amount:", event['args']['feeAmount'])
#
## Set up the event filter
#event_filter = W3.eth.filter({'address': CONTR_ARB_ADDR, 'topics': [event_signature]})
#
#print('Started listening for events ... ')
#while True:
#    for event in event_filter.get_new_entries():
#        handle_event(event)


####

## Create a contract object
#contract = W3.eth.contract(address=CONTR_ARB_ADDR, abi=CONTR_ARB_ABI)
#
#def handle_event(event):
#    print("FlashLoan event received:")
#    print("Recipient:", event['args']['recipient'])
#    print("Token:", event['args']['token'])
#    print("Amount:", event['args']['amount'])
#    print("Fee Amount:", event['args']['feeAmount'])
#
## Define the event filter
#event_filter = contract.events.FlashLoan.create_filter(fromBlock="latest")
#
## Start listening for events
#while True:
#    for event in event_filter.get_new_entries():
#        handle_event(event)
