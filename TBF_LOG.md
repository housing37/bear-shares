# bear-shares TBF testing log

## testing results for…
### TBF5.0:  -> LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
		starting market cap: $1.0k = $1.00 * 1000 TBF
		…
		performed manual market action to show activity
			BUYS: 
				NONE
			SELLS:
                None
		observed market activity … ~x hrs after LP deploy
			BUYS: 
				None
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF4.4: 0x5302F41B377862983aaEbab9050184eC95839363 -> LP added $500 (250:250 USD)
	(ignoring successful sell w/ OPEN_SELL==false, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 20 to 25 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
		added ~$500 LP @ 1:1 USD (250 TBF : $250 in PLS)
		starting market cap: $1.0k = $1.00 * 1000 TBF
		….
		performed manual market action to show activity
			BUYS: 
				8 buys = + ~$80.00 in LP
			SELLS:
                None
		observed market activity … ~18+ hrs after LP deploy
			BUYS: 
				None
			SELLS (slipped through w/ OPEN_SELL=false):
				1 sell = - ~18.00 in LP ('skim' fault from sending TBF4.4 to LP contract address)
                1 sell = - ~9.00 in LP (slipped through via 'front-running' a $36 buy of mine)
		new market cap: ~$1.4k
		changed options to: …
		observed market activity: …

### TBF4.3: 0x5f9fa75803a5695437d77066E6678fE56ab124F1 -> LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 20 to 25 wallets: 750 TBF
		starting with OPEN_BUY|SELL = true|false
		added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
		starting market cap: $1.0k = $1.00 * 1000 TBF
		performed manual market action to show activity
			BUYS: 
				4 buys = + ~$8.00 in LP
			SELLS:
				NONE
		observed market activity … ~6hrs after LP deploy
			BUYS: 
				~30 buys = +$200 in LP
			SELLS (slipped through w/ OPEN_SELL=false):
				5 sells @ < -$0.10 each
				1 sell @ -$3.02
		new market cap: $4.4k = $4.40 * 1000 TBF
		changed options to: … none
		observed market activity: … none
        __ PULLED LIQUIDITY

### TBF4.2: 0x3c3aFF046d75000ceA3a8776C6cf430fFFD25EE5 -> LP added
	reverted back tTBF3.0
	(ignoring successful sell w/ OPEN_SELL==false, for now, continue testing settings below)
		init supply: 250 TBF
		mixing supply amount 10 to 15 wallets: 125 TBF
		starting with open buy,sell = true, false
		add ~$100 LP @ 1:1 USD (50 TBF : $50 in PLS)
		performed a bit of manual market buy & sell to show activity
		observed buy action: … initial random/first buy from EOA that’s not me
		 changed options to: …
		observed buy action: …


### TBF4.2: 0x3c3aFF046d75000ceA3a8776C6cf430fFFD25EE5 -> LP added
	reverted back tTBF3.0
	(ignoring successful sell w/ OPEN_SELL==false, for now, continue testing settings below)
		init supply: 250 TBF
		mixing supply amount 10 to 15 wallets: 125 TBF
		starting with open buy,sell = true, false
		add ~$100 LP @ 1:1 USD (50 TBF : $50 in PLS)
		performed a bit of manual market buy & sell to show activity
		observed buy action: … initial random/first buy from EOA that’s not me
		 changed options to: …
		observed buy action: …


### TBF4.0: 0xFfaD853F74D71925196dc772c991f4f23803B560
		init supply: 250 TBF
		mixing supply amount 10 to 15 wallets: 125 TBF
		starting with open buy,sell = true, false
		add ~$100 LP @ 1:1 USD (50 TBF : $50 in PLS)
		a little bit of manual market buy & sell to show activity
		ERROR: could not create buy order with options open buy true
		observed buy action: …
		 changed options to: …
		observed buy action: …

### tTBF3.0: 0x8fd10330363C85F6a2bE61EbDeCB66894f545Be7
		init supply: 500 TBF
		mixing supply amount 10 to 15 wallets
		starting with open buy,sell = true, false
		add ~$100 LP @ 1:1 USD (50 TBF : $50 in PLS)
		a little bit of manual market buy & sell to show activity
		buy action: started $0.42 & $0.15 test buys from open market
		 set options to: “true, true”
		over night action: multiple buy/sell activity w/ $15+ buys
		 yielded price increase: +500%
		 set options to: “true, false” (to stop the sells)
     - found failure w/ successful sell from non-whitelist account
		  options set: yes open buy, no open sell
          tx hash: 0x36409ccc2c693b02ee7c75158f51c321ef11664aa6ac40b6b42a34afc2f67cdb
             used: 'transfer' w/ 'to' = PLP3.0 (0x41e191f8E957c5CfCA6706F54455e1428943B480)