## mysql db queries

select * from users;
select * from user_shill_rates;
select * from user_earns;
select * from log_tw_conf_urls;
select * from shills;
select * from log_tg_user_at_changes;

-- ************************************** --
-- MANUALLY SET PAYOUT TX SUCCESS - /admin_pay_shill_rewards <tg_user_at>
-- p_tg_admin_id = 581475171 == tg_user_at = housing37, 
-- CALL SET_USER_PAY_TX_STATUS(
-- 			581475171, -- p_tg_admin_id
-- 			
-- 			'sb_defi', -- p_tg_user_at
-- 			5.400000, -- p_chain_usd_paid FLOAT,
-- 			'0xee2d3d10cfc5fd4c1a42f0de2de96a41ddcbb43773248365815eb8d4c62c3fd5', -- p_pay_tx_hash
-- 			1, -- p_pay_tx_status -- -1|-2 = tx exception, 0 = tx fail, 1 = tx success
-- 			'0x9e5De869d2981C413595117c43D5447642e7c454', -- p_pay_to_wallet_addr
-- 			'0x7A580b7Cd9B48Ba729b48B8deb9F4D2cb216aEBC', -- p_pay_tok_addr
-- 			'BST', -- p_pay_tok_symb
-- 			'0x6B175474E89094C44Da98b954EedeAC495271d0F') -- p_aux_tok_burn
-- ************************************** --
-- GET WITHDRAW REQUEST AND AMOUNTS
select ue.*, u.tg_user_at, u.wallet_address from user_earns ue
	inner join users u
		on u.id = ue.fk_user_id 
	where usd_owed > 0
	order by withdraw_requested desc;

-- ************************************** --
-- GET USER EARNINGS REPORT
SELECT SUM(usd_owed) AS tot_owed,
		SUM(usd_paid) as tot_paid,
		SUM(usd_total) as tot_total 
		FROM user_earns;
-- ************************************** --

-- select * from users where tg_user_at ='housing37';
-- select * from shills where is_approved = 0;
-- select * from shills where fk_user_id = 31;
-- select * from shills where post_id = '1778758554574262458';
-- select * from users where tw_user_at = 'Soul88Tireless';
-- select * from user_earns order by withdraw_requested desc;



-- update user_earns set withdraw_requested = 1 
-- 	where id = 
-- select * from user_earns
-- 	where usd_owed > 0
-- 	order by withdraw_requested desc;

-- select * from users;
-- set @v_fk_user_id = 22;
-- select * from user_earns where fk_user_id = @v_fk_user_id;
-- select fk_user_id, id, pay_usd, is_approved, is_paid from shills where fk_user_id = @v_fk_user_id and is_approved = true;

-- set @v_usd_tot = 10.5;
-- update user_earns set usd_total = @v_usd_tot, usd_owed = @v_usd_tot where fk_user_id = @v_fk_user_id;
-- select * from user_earns where fk_user_id = @v_fk_user_id;

-- update user_shill_rates set type_descr = 'level_0', pay_usd = 0.5 where type_descr = 'htag';
-- update user_shill_rates set type_descr = 'level_1', pay_usd = 1.0 where type_descr = 'short_txt';
-- update user_shill_rates set type_descr = 'level_2', pay_usd = 2.0 where type_descr = 'long_txt';
-- update user_shill_rates set type_descr = 'level_3', pay_usd = 5.0 where type_descr = 'img_meme';
-- update user_shill_rates set type_descr = 'level_4', pay_usd = 10.0 where type_descr = 'short_vid';
-- update user_shill_rates set type_descr = 'level_5', pay_usd = 25.0 where type_descr = 'long_vid';

-- update shills set shill_type = 'level_0', pay_usd = 0.5 where shill_type = 'htag';
-- update shills set shill_type = 'level_1', pay_usd = 1.0 where shill_type = 'short_txt';
-- update shills set shill_type = 'level_2', pay_usd = 2.0 where shill_type = 'long_txt';
-- update shills set shill_type = 'level_3', pay_usd = 5.0 where shill_type = 'img_meme';
-- update shills set shill_type = 'level_4', pay_usd = 10.0 where shill_type = 'short_vid';
-- update shills set shill_type = 'level_5', pay_usd = 25.0 where shill_type = 'long_vid';

-- update shills set shill_type = 'level_0'

-- select * from shills where post_id = '1777408984414064833';
-- select fk_user_id, id, dt_created, dt_updated_approve, is_approved from shills where fk_user_id = 14 order by dt_created desc;