# bear-shares TBF testing log

## testing results for…
### TBF14.0: 0xed0f5605fCcaeF3797F27C6f1b6e56E4a847dc60 _ -> 
	PulseX v1 -> (pulseX v1 LP added $200 (100:100 USD)
    	PLP_PLS: 0x886E0fCaA55Ab3cC1eF5627824dB0605C49FCFCE 
		PLP_pDAI: 0x2F55D060221e0506E125aE690962C59aA2712415
		PLP_SOLIDX: 0xA5C2D87d8D119965A2be3C6F79f3D4A070D4F09c
    PulseX v2 -> (pulseX v2 LP added $200 (100:100 USD)
		PLP_PLS: 0x0a46548D54caccBd88cd9EF3246a3CD292DC31EB 
		PLP_pDAI: 0x733592b032e378bCA2F404F176E4055c223ceeED
		PLP_SOLIDX: 0x1C1D258327E7591788237ea62bD8b7479b4bBD6c
	NOTE: indeed added ALL PLPs above to whitelisted LPs in contract ("KEEPER_editWhitelistAddressLP(address,bool)")
	NOTE: all same as 13.3, with  few additions...
		added 2nd set of LPs (paired again pDAI)
		and indeed noticed more activity
		still seeing some sells slip through, but that might of been because i didn't whitelist a couple LPs fast enough
		regardless, definitely noticing other acitivty on the positive net return front
	
	*NOTE* -> need to whitelist ALL PLPs created! ASAP! As Soon As They Are Created!

### TBF13.3: 0x47c3E4F3A26a58FE03B97D95ac8931172dEfD706 _ -> 
    PLP13.3_v1: 0xAFB590d7267fdeF2952a9e3455dA2bAe10BfD438 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP13.3_v2: 0x8A3068f18FbD29d63C674E8cFE4ed5e5491Dd5c0 -> (pulseX v2 LP added $200 (100:100 USD)
	NOTE: indeed added PLPs above to whitelisted LPs in contract
			ref: KEEPER_editWhitelistAddressLP(address,bool)
    NOTE: v13.0,1 trying to deny arb attempts between dexes
	NOTE: ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below
    NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault
	NOTE: had to switch to use WPLS instead of PLS during the LP remove proccess (occurred in 13.1,2)
		init supply: 1000 TBF; mixing 50% to 55 wallets
		init settings: OPEN_BUY|SELL = true|false
		starting market cap: $1.0k = $1.00 * 1000 TBF
			added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            a couple initial buys on both LPs 
				slightly different amounts for each, to avoid 'LAST_TRANSFER_AMNT' check
            and then also a couple high volume buys on v2 LP to fish for arb bots (to buy on v1 LP)
                (doesn't look like i'm receiving any immediate attention from arb bots)

		observed market activity … ~1-5 min after LP deploy
			not much activty, maybe a little
		observed market activity … ~20-30 min after LP deploy
			not much activty, maybe a little

### TBF13.2: 0xFb9D5FC22815504819292cef81CB35b6745C06E2 _ -> LP removed
    PLP13.2_v1: 0x4dFd0559598E61935F5b6ed0A55A4D9419C04003 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP13.2_v2: 0x35921610526FdFaa9b597Ec4395F4E1685c23558 -> (pulseX v2 LP added $200 (100:100 USD)
    NOTE: v13.0,1 trying to deny arb attempts between dexes
	NOTE: ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below
    NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault
	NOTE: had to switch to use WPLS instead of PLS during the LP remove proccess (occurred in 13.1,2)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
		added PLPs above to whitelisted LPs in contract
			KEEPER_editWhitelistAddressLP(address,bool)
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            a couple initial buys on both LPs 
				slightly different amounts for each, to avoid 'LAST_TRANSFER_AMNT' check
            and then also a couple high volume buys on v2 LP to fish for arb bots (to buy on v1 LP)
                (doesn't look like i'm receiving any immediate attention from arb bots)

		observed market activity … ~1-5 min after LP deploy
			not much activty, maybe a little
		observed market activity … ~20-30 min after LP deploy
			not much activty, maybe a little

### TBF13.1: 0xdD1A7A1fAb792B18dC41C209aA1c0fab5ea66321 _ -> LP removed
    PLP13.1_v1: 0x5b4743D2A5a4b1E7b0C3422c567372802ac88D89 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP13.1_v2: 0x7Da07008a144344A937C1e11cE58385ED4090cE6 -> (pulseX v2 LP added $200 (100:100 USD)
    NOTE: v13.0,1 trying to deny arb attempts between dexes
	NOTE: ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below
    NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
		added PLPs above to whitelisted LPs in contract
			KEEPER_editWhitelistAddressLP(address,bool)
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            a couple initial buys on both LPs
            and then also a couple high volume buys on v2 LP to fish for arb bots (to buy on v1 LP)
                (doesn't look like i'm receiving any immediate attention from arb bots)

		observed market activity … ~1-5 min after LP deploy
            some wierd activity with LPs i created after the those initial buys
             HOWEVER, they were not buy or sell orders by bots or anything like that
                seems like maybe bots were just testing the waters or checking things out maybe... ?
                ref tx: 0xe38706594b046db9d63f323e7e8bf7b66c3d90f3b2fa3a20b51f53c210c76ade 
                        0x414e94296215dbc4f7a2ef9ddf0385bc7b982b60fbf6993d684737f6d717e02b
		observed market activity … ~20-30 min after LP deploy
			some buys came in on both v1 and v2 LPs, however mostly on v2 LP
				v2 LP shot up to $3.15 in price, with $356.00 in liquidity 
				v1 LP went up to $1.12 in price, with $212.00 in liquidity 

		NEXT: launch v13.2 'exactly' like this one
        

### TBF13.0: 0x8432418A8927a288A63034dC78329B84E80893d0 _ -> LP removed
    PLP13.0_v1: 0x4F4Ba13f188612dc259c6141d61824d7f99bc150 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP13.0_v2: 0x0C69D21dC6F0f95435017E2C9469fB3FDbc07918 -> (pulseX v2 LP added $200 (100:100 USD)
    NOTE: v13.0 trying to deny arb attempts between dexes
	NOTE: ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below
    NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            a couple initial buys
            including to fish for arb bots (high buys one dex)
		observed market activity … ~1-5 min after LP deploy
            got frontrun immediately on 1 dex (w/ 2 txs)
            then got arbed across 2 dexes (w/ 1 tx)
        NOTE: attempt solidity update in v13.1 to detect more arb attempts

		new market cap: …
		changed options to: …
		observed market activity: …

### TBF12.0: 0x1989288D09Ac46819A7E2270892b840999B22daC _ -> reverted back to LEGACY -> LP removed
    PLP12.0_v1: 0xC630B3088dB467Cc0fe5CD96d27896F763361F30 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP12.0_v2: 0x8E999157fE2D87BC1E5131F9D72ec5e8c0E7585a -> (pulseX v2 LP added $200 (100:100 USD)
	NOTE: ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below
    NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            2 init 10k PLS buys (one on each dex)
            1 higher value buy, attracked an arb bot between dexes (and it was successful)
                - have an idea for v13.0 to block them using WHITELISTE_LP_MAP

		observed market activity … ~1-5 min after LP deploy

		new market cap: …
		changed options to: …
		observed market activity: …

### TBF11.0: 0xD2c6E39D820C8d13E78B069A0Ab6a2eB5E3a43Cc _ -> LP removed
    PLP11.0_v1: 0xDd67703991144986cC39e12c866381e9fB3FB185 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP11.0_v2: 0xa890Bf04EF266190792D26003dd256F4B1b18F78 -> (pulseX v2 LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
    (starting over with legacy + v9.0, which is overriding 'balanceOf')
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            changed OPEN_BUY|SELL = true|true (for creating LPs) <---- yes required (but may not before v9.0)
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
            changed back OPEN_BUY|SELL = true|false (for initial start)
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            turns out v9.0 (chaning balanceOf) is NOT a good model
                this causes no buys to go through at all if buy,sell options = true,false
            NOTE: need to start fresh again from legacy simple 'transfer' and 'transferFrom' overrides
		observed market activity … ~1-5 min after LP deploy
            (NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault)

		new market cap: …
		changed options to: …
		observed market activity: …

### TBF10.1: 0xe365658362E46cF9497d022242FCC9a50487320e _ -> LP removed
    PLP10.1_v1: 0xf182bA92B432A3b07D423DAb4c9B6D55a660Da89 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP10.1_v2: 0x851BfFbEACA7b3C7bE370Be3c7d49D4BB7298070 -> (pulseX v2 LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            changed OPEN_BUY|SELL = true|true (for creating LPs)
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
            changed back OPEN_BUY|SELL = true|false (for initial start)
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            nothing seems to work without true,true for buySellOptions
             - removing liquidity immediately 
		observed market activity … ~1-5 min after LP deploy
            (NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault)

		new market cap: …
		changed options to: …
		observed market activity: …

### TBF10.0: 0x5Ba5D9122b6f206Ff3883e0c5477124028e0Da38 _ -> LP removed
    PLP10.0_v1: 0x10a5C8d43F5dd08815531C96013F8d61DD1064fB -> (pulseX v1 LP added $200 (100:100 USD)
    PLP10.0_v2: 0x96A34Ab463229b87A7169ce86006e660A2218C49 -> (pulseX v2 LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
            changed OPEN_BUY|SELL = true|true (for creating LPs)
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
            added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
            changed back OPEN_BUY|SELL = true|false (for initial start)
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
            2 or 3 buys across 2 dexes
                - no one else bought in
                - i think maybe these new changes in v10.0 prevented buys completely
			BUYS: 
                None
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
            (NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault)

		new market cap: …
		changed options to: …
		observed market activity: …


### TBF9.0: 0x9c009EB548F13D31951FE80bc81dDf58D2945409 _ -> LP removed
    PLP9.0_v1: 0xB20105DA3CDBCC105152abfC2339b4fBe84C1a4B -> (pulseX v1 LP added $200 (100:100 USD)
    PLP9.0_v2: 0xA8b94AA5e0f4D0083cDA0539eAe560d8DC87714D -> (pulseX v2 LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
                a few initial buys w/ 10k PLS on each LP above
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
                (NOTE: sells still slip through w/ OPEN_SELL=false -OR- 'skim(…)' fault)
            a few quick arb / snipe buy and sell attempts  
            a couple sells got through, but received net return posotive
                wound up with net return
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF8.1: 0x2D87E134b4986135b8a50E09ff3B73fe415cfF44 _ -> LP removed
    PLP8.1_v1: 0xF97183e35F64C2377eeF56758e567b692c4f8364 -> (pulseX v1 LP added $200 (100:100 USD)
    PLP8.1_v2: 0xa4cD1203cC765e4fDfdBB8722F6730D2aDE69eaa -> (pulseX v2 LP added $200 (100:100 USD)
	(ignoring successful sell w/ OPEN_SELL==false | 'skim(…)' fault, for now, continue testing settings below)
		init supply: 1000 TBF
		mixing supply amount 50 to 55 wallets: 500 TBF
		starting with OPEN_BUY|SELL = true|false
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v1
        added ~$200 LP @ 1:1 USD (100 TBF : $100 in PLS) -> PLPx_v2
		starting market cap: $1.0k = $1.00 * 1000 TBF
        init testing w/ whitelisted vs non-whitelisted accounts seems to work the same
		…
		performed manual market action to show activity
			BUYS: 
                1 initial buy w/ 10k PLS
			SELLS:
                None
		observed market activity … ~1-5 min after LP deploy
			BUYS: 
                1 quick arb / snipe buy and sell before and after
                    launching v9.0 to help stop the sell aspect (but still allow the buy)
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                ^
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF8.0: 0x105ff2ca3F353B5E3631dFd0906e118768b696F8 -> LP added $200 (100:100 USD) _  -> LP removed
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
                after 2nd LP added, lots of activity starts to occcur (more buys than sells)
                    bots seem to respond to my market buys more
                    total liquidity increased to $430 (~$15 profit margin)
			SELLS (slipped through w/ OPEN_SELL=false -OR- 'skim(…)' fault):
                None
		new market cap: …
		changed options to: …
		observed market activity: …

### TBF7.1: 0x5Cbc25C03d241d12ab227f4dE791dAE2d0325eef -> LP added $200 (100:100 USD) -> LP removed
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

### TBF7.0: 0x20c18Fb341C04F83FF9BF0CDF0170e57F35991bc -> LP added $200 (100:100 USD) -> LP removed
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