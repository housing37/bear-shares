# bear-shares TBF testing log

## testing results for…
### TBF8.0: 0x105ff2ca3F353B5E3631dFd0906e118768b696F8 -> LP added $200 (100:100 USD)
    PLP8.0: 0x6Cb2e4cb0b9DD947C9f6d683e5d984b3DC5e6CC1 (pulseX v1)
    PLP8.0_v2: 0x9A473d357De5C66b8844819C209f1E88ca54F803 (pulseX v2)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLP8.0
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLP8.0_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
				8 buys total (4 on each LP) @ 10k PLS each
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
			BUYS: 
                after 2nd LP added, lots activity starts to occcur
                    bots seem to respond to my market buys more
                    total liquidity increased to $430 (~$15 profit margin)
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF7.1: 0x5Cbc25C03d241d12ab227f4dE791dAE2d0325eef -> LP added $200 (100:100 USD)
    PLP7.1: 0xa5a73A80EBe03Bd9FE2587032a86B33dE10622c1
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
				x1 market buys w/ 10k PLS
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
			BUYS: 
                None
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF7.0: 0x20c18Fb341C04F83FF9BF0CDF0170e57F35991bc -> LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
            PLP7.0: 0x45F05975BB231363E9A9A1f946d6CDaDeEf3b2A1
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
				None
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
			BUYS: 
				~5 buys w/ 100k each 
                ~2 buys w/ 50k each 
                ~1 buys w/ 15k each 
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
            NOTE: attempted to create LP with new 'BRO' token just launched
                    basically got attached and drained some of my LP connected to WPLS (lost ~$30)
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                NOTE: the following occurred because of pairing v7.0 LP w/ 'BRO' (activity stopped, when LP removed)
                    1 sell w/ ~28.37: due to creting another LP with 7.0 and new 'BRO' token
                        one of my LPs (successfully) called 'transfer' on my other LP
                    1 sell w/ ~3.46: due to creting another LP with 7.0 and new 'BRO' token
                        one of my LPs (successfully) called 'transfer' on my other LP
		observed market activity: …

### TBF6.0: 0x76d0b9953dd7587578562CaCC75ac4A793852F7A -> LP added $200 (100:100 USD) -> LP wiped
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
    (added 'transfer' check for selling 'to' LP; requires whitelisting LP after its created)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
            PLP6.0: 0x5cDA6c079F34510E75dfe03929866CB4e5b933B5
             added ^ to whitelisted LPs in TBF contract
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
				x2 market buys w/ 10k PLS
			SELLS:
                None
		observed market activity … ~21 hrs after LP deploy
			BUYS: 
				None
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF5.0: 0x613E8509aA671FE00164321A91390241722cCF87 -> LP added $200 (100:100 USD) -> LP wiped
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS)
            PLP5.0: 0xF77B949D1A23D2dA7BD58F54D1851cbCDC3701cf
		starting market cap: $1.0k = $1.00 * 1000 TBF
		…
		performed manual market action to show activity
			BUYS: 
				2 buy = + ~$0.70 in LP
			SELLS:
                None
		observed market activity … ~x hrs after LP deploy
			BUYS: 
				3 buys = + ~$2.12 in LP
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                1 sell ... failure: snipe got through  it looks like
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF4.4: 0x5302F41B377862983aaEbab9050184eC95839363 -> LP added $500 (250:250 USD) -> LP wiped
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