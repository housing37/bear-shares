__fname = '_abi'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
cStrDivider_1 = '#----------------------------------------------------------------#'

BST_FUNC_MAP_READ = {
    # read functions
    "KEEPER()": ["862a179e", [], ['address']],
    "KEEPER_collectiveStableBalances(bool,uint256)": ["cf0c8683", ['bool','uint256'], ['uint64','uint64','uint64','int64']],
    "ACCT_USD_BALANCES(address)": ["c67483dc", ["address"], ['uint64']],
    "ACCT_USD_PAYOUTS(address,uint256)": ["8b47da26", ["address","uint256"], ['address', 'uint64', 'uint64', 'uint64', 'uint64', 'uint64', 'uint64', 'uint256', 'address']],

    "USD_STABLE_DECIMALS(address)": ["7f8754f4", ["address"], ['uint8']],
    # "USD_BST_PATHS(address,uint256)": ["85783459", ["address","uint256"], ['address']],
    "USWAP_V2_ROUTERS(uint256)": ["ee80b054", ["uint256"], ['address']],
    
    "balanceOf(address)": ["70a08231", ["address"], ['uint256']],
    "decimals()": ["313ce567", [], ['uint8']],
    "getAccounts()": ["8a48ac03", [], ['address[]']],
    "getAccountPayouts(address)": ["d08e6c88", ["address"], ['address', 'uint64', 'uint64', 'uint64', 'uint64', 'uint64', 'uint256', 'address']],

    "getDexOptions()": ["3685f08b", [], ['bool','bool','bool']],
    "getPayoutPercs()": ["2edef8a4", [], ['uint32','uint32','uint32','uint32']],
    
    "getUsdStablesHistory()": ["d4155f07", [], ['address[]']],
    "getWhitelistStables()": ["00f403e8", [], ['address[]']],
    "getDexRouters()": ["ba41debb", [], ['address[]']],
    "getSwapDelegateInfo()": ["4bae2eef", [], ['address','uint8','address']],
    "getUsdBstPath(address)": ["260e5df9", ['address'], ['address[]']],

    "TOK_WPLS()": ["fa4a9870", [], ['address']],
    "BURN_ADDR()": ["783028a9", [], ['address']],

    "name()": ["06fdde03", [], ['string']],
    "owner()": ["8da5cb5b", [], ['address']],
    "symbol()": ["95d89b41", [], ['string']],
    "tVERSION()": ["9a60f330", [], ['string']],
    "totalSupply()": ["18160ddd", [], ['uint256']],
}
BST_FUNC_MAP_WRITE = {
    # write functions
    "KEEPER_maintenance(uint64,address)": ["3015d747", ["uint64","address"], []], # gas used: 62,434
    "KEEPER_setKeeper(address)": ["11851737", ["address"], []], 
    "KEEPER_setKeeperCheck(uint256)": ["9d7c9834", ["uint256"], []],
    "KEEPER_setSwapDelegate(address)": ["c1533a53", ["address"], []],
	"KEEPER_setSwapDelegateUser(address)": ["126d4301", ['address'], []],

    "KEEPER_editDexRouters(address,bool)": ["bceeba33", ["address","bool"], []], # gas used: 36,601 (rem), 55,723 (add)
    "KEEPER_editWhitelistStables(address,uint8,bool)": ["b290b9bf", ["address","uint8","bool"], []],
    "KEEPER_setUsdBstPath(address,address[])": ["4f51d029", ['address','address[]'], []], # gas used: 38,852
    "KEEPER_enableDexOptions(bool,bool,bool)": ["ffc9f2fd", ["bool","bool","bool"], []], # gas used: 7.731

    "KEEPER_setPayoutPercs(uint32,uint32,uint32)": ["c0e202fa", ["uint32","uint32","uint32"], []], # gas used: 30,082
    "KEEPER_setBuyBackFeePerc(uint32)": ["57e8a5a5", ["uint32"], []], # gas used: 28,887

    "payOutBST(uint64,address,address)": ["09f5c380", ["uint64","address","address"], []], # gas used: 700,000+
    "tradeInBST(uint64)": ["d8785767", ["uint64"], []], # gas used: 126,956+

    "burn(uint64)": ["9dbead42", ["uint64"], []], 
    "allowance(address,address)": ["dd62ed3e", ["address","address"], []],
    "approve(address,uint256)": ["095ea7b3", ["address","uint256"], []],
    "transfer(address,uint256)": ["a9059cbb", ["address","uint256"], []],
    "transferFrom(address,address,uint256)": ["23b872dd", ["address","address","uint256"], []],
    "renounceOwnership()": ["715018a6", [], []],
    "transferOwnership(address)": ["f2fde38b", ["address"], []],
}

# BST_FUNC_MAP = {
#     "KEEPER_setKeeper(address)": ["11851737", ["address"], []],

#     "ACCT_USD_BALANCES(address)": ["c67483dc", ["address"], ['uint64']],

#     "ACCT_USD_PAYOUTS(address,uint256)": ["8b47da26", ["address","uint256"], []],

#     "BUY_BACK_FEE_PERC()": ["aa21f232", [], ['uint8']],

#     "ENABLE_MARKET_BUY()": ["405d2a83", [], []],
#     "ENABLE_MARKET_QUOTE()": ["46538f8c", [], []],

#     "KEEPER()": ["862a179e", [], ['address']],

#     "KEEPER_editDexRouters(address,bool)": ["bceeba33", ["address","bool"], []],
#     "KEEPER_editWhitelistStables(address,uint8,bool)": ["b290b9bf", ["address","uint8","bool"], []],
#     "KEEPER_enableMarketBuy(bool)": ["bc47b906", ["bool"], []],
#     "KEEPER_enableMarketQuote(bool)": ["624b3abe", ["bool"], []],
#     "KEEPER_maintenance(uint64,address)": ["3015d747", ["uint64","address"], []],
#     "KEEPER_setBuyBackFeePerc(uint8)": ["dd8645c2", ["uint8"], []],
#     "KEEPER_setServiceBurnPerc(uint8)": ["66eff5cf", ["uint8"], []],
#     "KEEPER_setServiceFeePerc(uint8)": ["61cad1db", ["uint8"], []],

#     "SERVICE_BURN_PERC()": ["c364daa4", [], ['uint8']],
#     "SERVICE_FEE_PERC()": ["a004d00d", [], ['uint8']],
#     "TOK_WPLS()": ["fa4a9870", [], ['address']],
#     "USD_STABLE_DECIMALS(address)": ["7f8754f4", ["address"], ['uint8']],
#     "USWAP_V2_ROUTERS(uint256)": ["ee80b054", ["uint256"], ['address']],
#     "WHITELIST_USD_STABLES(uint256)": ["593d1bf7", ["uint256"], ['address']],

#     "allowance(address,address)": ["dd62ed3e", ["address","address"], []],
#     "approve(address,uint256)": ["095ea7b3", ["address","uint256"], []],

#     "balanceOf(address)": ["70a08231", ["address"], ['uint256']],
#     "decimals()": ["313ce567", [], ['uint8']],
#     "getSwapRouters()": ["c85ec1e0", [], ['address[]']],
#     "getWhitelistStables()": ["00f403e8", [], ['address[]']],
#     "name()": ["06fdde03", [], ['string']],
#     "owner()": ["8da5cb5b", [], ['address']],

#     "payOutBST(uint64,address)": ["031cc420", ["uint64","address"], []],
#     "renounceOwnership()": ["715018a6", [], []],

#     "symbol()": ["95d89b41", [], ['string']],
#     "tVERSION()": ["9a60f330", [], ['string']],
#     "totalSupply()": ["18160ddd", [], ['uint256']],

#     "tradeInBST(uint64)": ["d8785767", ["uint64"], []],
#     "transfer(address,uint256)": ["a9059cbb", ["address","uint256"], []],
#     "transferFrom(address,address,uint256)": ["23b872dd", ["address","address","uint256"], []],
#     "transferOwnership(address)": ["f2fde38b", ["address"], []]
# }

BST_ABI = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_initSupply",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "allowance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientAllowance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "balance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientBalance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "approver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidApprover",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidReceiver",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSpender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "OwnableInvalidOwner",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "OwnableUnauthorizedAccount",
		"type": "error"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "_account",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "_plsDeposit",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint64",
				"name": "_stableConvert",
				"type": "uint64"
			}
		],
		"name": "DepositReceived",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "_prev",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "_new",
				"type": "address"
			}
		],
		"name": "KeeperTransfer",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "bool",
				"name": "_prev",
				"type": "bool"
			},
			{
				"indexed": False,
				"internalType": "bool",
				"name": "_new",
				"type": "bool"
			}
		],
		"name": "MarketBuyEnabled",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "bool",
				"name": "_prev",
				"type": "bool"
			},
			{
				"indexed": False,
				"internalType": "bool",
				"name": "_new",
				"type": "bool"
			}
		],
		"name": "MarketQuoteEnabled",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "_from",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint64",
				"name": "_usdAmnt",
				"type": "uint64"
			}
		],
		"name": "PayOutProcessed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_prev",
				"type": "uint8"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_new",
				"type": "uint8"
			}
		],
		"name": "ServiceBurnUpdate",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_prev",
				"type": "uint8"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_new",
				"type": "uint8"
			}
		],
		"name": "ServiceFeeUpdate",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_prev",
				"type": "uint8"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "_new",
				"type": "uint8"
			}
		],
		"name": "TradeInFeeUpdate",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "_trader",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint64",
				"name": "_bstAmnt",
				"type": "uint64"
			},
			{
				"indexed": False,
				"internalType": "uint64",
				"name": "_usdTradeVal",
				"type": "uint64"
			}
		],
		"name": "TradeInProcessed",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "ACCT_USD_BALANCES",
		"outputs": [
			{
				"internalType": "uint64",
				"name": "",
				"type": "uint64"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "ACCT_USD_PAYOUTS",
		"outputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			},
			{
				"internalType": "uint64",
				"name": "usdAmnt",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "usdFee",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "usdBurn",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "usdPayout",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "bstBurn",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "bstPayout",
				"type": "uint64"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "BUY_BACK_FEE_PERC",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "ENABLE_MARKET_BUY",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "ENABLE_MARKET_QUOTE",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "KEEPER",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_router",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "_add",
				"type": "bool"
			}
		],
		"name": "KEEPER_editDexRouters",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_usdStable",
				"type": "address"
			},
			{
				"internalType": "uint8",
				"name": "_decimals",
				"type": "uint8"
			},
			{
				"internalType": "bool",
				"name": "_add",
				"type": "bool"
			}
		],
		"name": "KEEPER_editWhitelistStables",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "_enable",
				"type": "bool"
			}
		],
		"name": "KEEPER_enableMarketBuy",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "_enable",
				"type": "bool"
			}
		],
		"name": "KEEPER_enableMarketQuote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "_usdAmnt",
				"type": "uint64"
			},
			{
				"internalType": "address",
				"name": "_usdStable",
				"type": "address"
			}
		],
		"name": "KEEPER_maintenance",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint8",
				"name": "_perc",
				"type": "uint8"
			}
		],
		"name": "KEEPER_setBuyBackFeePerc",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_newKeeper",
				"type": "address"
			}
		],
		"name": "KEEPER_setKeeper",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint8",
				"name": "_perc",
				"type": "uint8"
			}
		],
		"name": "KEEPER_setServiceBurnPerc",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint8",
				"name": "_perc",
				"type": "uint8"
			}
		],
		"name": "KEEPER_setServiceFeePerc",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "SERVICE_BURN_PERC",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "SERVICE_FEE_PERC",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "TOK_WPLS",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "USD_STABLE_DECIMALS",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "USWAP_V2_ROUTERS",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "WHITELIST_USD_STABLES",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getSwapRouters",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getWhitelistStables",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "_usdValue",
				"type": "uint64"
			},
			{
				"internalType": "address",
				"name": "_payTo",
				"type": "address"
			}
		],
		"name": "payOutBST",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "tVERSION",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "_bstAmnt",
				"type": "uint64"
			}
		],
		"name": "tradeInBST",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	}
]