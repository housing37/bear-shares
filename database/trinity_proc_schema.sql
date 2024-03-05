DELIMITER $$
-- ADD_NEW_USER Procedure
DROP PROCEDURE IF EXISTS ADD_NEW_USER;
CREATE PROCEDURE `ADD_NEW_USER`(
    IN p_user_id VARCHAR(40),
    IN p_wallet_address VARCHAR(1024),
    IN p_tweet_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_REG_SHILLER = ['user_id', 'wallet_address', 'tweet_url']
-- DB_PROC_ADD_NEW_USER = 'ADD_NEW_USER'
--     # validate 'tweet_url' contains texts '@BearSharesNFT' & 'trinity'
--     # insert into 'users' (...) values (...)
END 
$$ DELIMITER ;

DELIMITER $$
-- ADD_USER_SHILL Procedure
DROP PROCEDURE IF EXISTS ADD_USER_SHILL;
CREATE PROCEDURE `ADD_USER_SHILL`(
    IN p_user_id VARCHAR(40),
    IN p_post_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_SUBMIT_SHILL = ['user_id', 'post_url']
-- DB_PROC_ADD_SHILL = 'ADD_USER_SHILL'
--     # validate 'post_url' is not in 'shills' table yet
--     # insert into 'shills' (...) values (...) for user_id
-- 	   # check number of pending shills (is_apporved=False), return rate-limit info
--	   #	perhaps set a max USD per day that people can earn?
END 
$$ DELIMITER ;

DELIMITER $$
-- GET_USER_RATES Procedure
DROP PROCEDURE IF EXISTS GET_USER_RATES;
CREATE PROCEDURE `GET_USER_RATES`(
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_SHOW_RATES = ['user_id']
-- DB_PROC_GET_USR_RATES = 'GET_USER_RATES'
--     # select * from 'user_shill_rates' for user_id (order by id desc limit 1)
END 
$$ DELIMITER ;

DELIMITER $$
-- GET_USER_EARNINGS Procedure
DROP PROCEDURE IF EXISTS GET_USER_EARNINGS;
CREATE PROCEDURE `GET_USER_EARNINGS`(
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_SHOW_EARNINGS = ['user_id']
-- DB_PROC_GET_USR_EARNINGS = 'GET_USER_EARNINGS'
--     # select * from 'user_earns' where 'user_earns.fk_user_id=user_id'
END 
$$ DELIMITER ;

DELIMITER $$
-- WITHDRAW_USER_EARNINGS Procedure
DROP PROCEDURE IF EXISTS WITHDRAW_USER_EARNINGS;
CREATE PROCEDURE `WITHDRAW_USER_EARNINGS`(
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_WITHDRAW_EARNINGS = ['user_id']
-- DB_PROC_WITHDRAW_EARNS = 'WITHDRAW_USER_EARNINGS'
--     # select 'user_earns.usd_owed' for user_id (req: usd_owed >= <some-min-amnt>)
--     # select 'users.wallet_address' for user_id
--     # use solidity 'transfer' to send 'usd_owed' amount to 'wallet_address'
--     # update 'user_earns.withdraw_request' where 'user_earns.usd_owed > 0' for user_id
END 
$$ DELIMITER ;

DELIMITER $$
-- GET_USER_SHILLS_ALL Procedure
DROP PROCEDURE IF EXISTS GET_USER_SHILLS_ALL;
CREATE PROCEDURE `GET_USER_SHILLS_ALL`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40),
    IN p_pending BOOLEAN,
    IN p_removed BOOLEAN)
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_USR_SHILLS = ['admin_id','user_id','pending','removed']
-- DB_PROC_GET_USR_SHILLS_ALL = 'GET_USER_SHILLS_ALL'
--     # select * from 'shills' where 'shills.is_approved=True|False' and 'shills.is_removed=True|False' for user_id
END 
$$ DELIMITER ;

DELIMITER $$
-- GET_PEND_SHILLS Procedure
DROP PROCEDURE IF EXISTS GET_PEND_SHILLS;
CREATE PROCEDURE `GET_PEND_SHILLS`(
    IN p_admin_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_ALL_PEND_SHILLS = ['admin_id']
-- DB_PROC_GET_PEND_SHILLS = 'GET_PEND_SHILLS' # get where 'is_approved' = False
--     # select * from 'shills' where 'shills.is_approved=False' for all users
END 
$$ DELIMITER ;

DELIMITER $$
-- SET_SHILL_APPROVE_STATUS Procedure
DROP PROCEDURE IF EXISTS SET_SHILL_APPROVE_STATUS;
CREATE PROCEDURE `SET_SHILL_APPROVE_STATUS`(
    IN p_admin_id VARCHAR(40),
    IN p_shill_id VARCHAR(40),
    IN p_shill_url VARCHAR(1024),
    IN p_is_approved BOOLEAN)
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_APPROVE_SHILL = ['admin_id','shill_id','shill_url','is_approved']
-- DB_PROC_APPROVE_SHILL_STATUS = "SET_SHILL_APPROVE_STATUS" 
--     # admin views shill_url on the web
--     # set 'shills.is_approved=True|False' where 'shills.is_removed=False' for 'user_id + shill_id|url' combo
--     # update 'user_earns.usd_total|owed' accordingly (+-) for user_id
END 
$$ DELIMITER ;

DELIMITER $$
-- GET_USER_SHILL Procedure
DROP PROCEDURE IF EXISTS GET_USER_SHILL;
CREATE PROCEDURE `GET_USER_SHILL`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40),
    IN p_shill_id VARCHAR(40),
    IN p_shill_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_VIEW_SHILL = ['admin_id','user_id','shill_id','shill_url']
-- DB_PROC_GET_USR_SHILL = 'GET_USER_SHILL'
--     # select * from 'shills' where 'shills.id|shill_url=shill_id|url' for user_id
END 
$$ DELIMITER ;

DELIMITER $$
-- UPDATED_USER_SHILL_PAID_EARNS Procedure
DROP PROCEDURE IF EXISTS UPDATED_USER_SHILL_PAID_EARNS;
CREATE PROCEDURE `UPDATED_USER_SHILL_PAID_EARNS`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_id']
-- DB_PROC_UPDATE_USR_PAID_EARNS = 'UPDATED_USER_SHILL_PAID_EARNS'
--     # check 'user_earns.withdraw_request=True' for 'user_id'
--     # validate 'user_earns.usd_owed' == 
--     #   total of (select 'shills.pay_usd' where 'shills.is_paid=False' & 'shills.is_approved=True & 'shills.is_removed=False') for user_id
--     # update 'user_earns.usd_owed|paid' where 'user_earns.fk_user_id=user_id'
--     # update 'shills.is_paid=True' for user_id
--     # then perform solidity 'transfer' call on 'users.wallet_address' for user_id
END 
$$ DELIMITER ;

DELIMITER $$
-- SET_USER_SHILL_REMOVED Procedure
DROP PROCEDURE IF EXISTS SET_USER_SHILL_REMOVED;
CREATE PROCEDURE `SET_USER_SHILL_REMOVED`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40),
    IN p_shill_id VARCHAR(40),
    IN p_shill_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_SET_SHILL_REM = ['admin_id','user_id','shill_id','shill_url']
-- DB_PROC_SET_SHILL_REM = 'SET_USER_SHILL_REMOVED'
--     # updated 'shills.is_removed' for 'shills.user_id + shills.shill_id|url' combo
END 
$$ DELIMITER ;

DELIMITER $$
-- CHECK_USR_REM_SHILL Procedure
DROP PROCEDURE IF EXISTS CHECK_USR_REM_SHILL;
CREATE PROCEDURE `CHECK_USR_REM_SHILL`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_CHECK_USR_REM_SHILLS = ['admin_id','user_id']
-- DB_PROC_CHECK_USR_REM_SHILL = DB_PROC_GET_USR_SHILLS_ALL 
--     # select post_url from 'shills' where 'shills.is_removed=False' for user_id
--     # then web scrape those post_urls to see if they are still working / viewable
END 
$$ DELIMITER ;

DELIMITER $$
-- SET_USER_PAY_RATES Procedure
DROP PROCEDURE IF EXISTS SET_USER_PAY_RATES;
CREATE PROCEDURE `SET_USER_PAY_RATES`(
    IN p_admin_id VARCHAR(40),
    IN p_user_id VARCHAR(40))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
-- LST_KEYS_SET_USR_SHILL_PAY_RATES = ['admin_id','user_id']
-- DB_PROC_SET_USR_RATES = 'SET_USER_PAY_RATES'
--     # update 'user_shill_rates' for user_id
END 
$$ DELIMITER ;



-- #================================================================# --
--		LEGACY
-- #================================================================# --

-- DELIMITER $$
-- drop PROCEDURE if exists AVM_GET_CNT_DT_EVT_TYPE; -- setup
-- CREATE PROCEDURE `AVM_GET_CNT_DT_EVT_TYPE`(
-- 	IN p_dt_updated VARCHAR(40),
-- 	IN p_evt_type VARCHAR(10))
-- BEGIN
-- 	SELECT count(*) 
-- 		FROM avm_logs
-- 		INTO @v_count;

-- 	IF @v_count > 0 THEN
-- 		-- 	GET FROM X TIME TO X TIME
-- 		-- SELECT CONCAT(p_dt_updated, " 03:00:00") INTO @v_dt_utc_start;
--         SELECT CONCAT(p_dt_updated, " 05:00:00") INTO @v_dt_utc_start;
-- 		-- SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 4 HOUR) INTO @v_dt_edt_start;
-- 		SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 5 HOUR) INTO @v_dt_edt_start; -- EST
-- 		SELECT DATE_ADD(@v_dt_edt_start, INTERVAL 1 DAY) INTO @v_dt_edt_end;
-- 		SELECT dt_updated, count(*) as 'evt_type count',
-- 				p_evt_type as input_evt_type,
-- 				'success' as `status`,
-- 				'retrieved avm_log count for dt_updated & evt_type' as info,
-- 				p_dt_updated as input_dt_updated
-- 			FROM avm_logs 
-- 			WHERE evt_code = p_evt_type
-- 				AND dt_updated 
-- 					BETWEEN @v_dt_edt_start AND @v_dt_edt_end
-- 				ORDER BY dt_updated DESC;
-- 	ELSE
-- 		SELECT 'failed' as `status`, 
-- 				'no avm_logs found at all' as info, 
-- 				p_dt_updated as input_dt_updated,
-- 				p_evt_type as input_evt_type;
-- 	END IF;
-- END 
-- $$ DELIMITER ;

-- DELIMITER $$
-- drop FUNCTION if exists AVM_GET_CNT_DT_EVT; -- setup
-- CREATE FUNCTION `AVM_GET_CNT_DT_EVT`(
-- 		p_dt_updated VARCHAR(40),
-- 		p_cnt_evt_type VARCHAR(10),
-- 		p_get_total_cnt BOOL) RETURNS INT(11)
--     READS SQL DATA
--     DETERMINISTIC
-- BEGIN
-- 	DECLARE v_i INT;
-- 	DECLARE v_lvl FLOAT;
-- 	-- 	GET FROM X TIME TO X TIME
-- 	-- SELECT CONCAT(p_dt_updated, " 03:00:00") INTO @v_dt_utc_start;
--     SELECT CONCAT(p_dt_updated, " 05:00:00") INTO @v_dt_utc_start;
-- 	-- SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 4 HOUR) INTO @v_dt_edt_start;
-- 	SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 5 HOUR) INTO @v_dt_edt_start; -- EST
-- 	SELECT DATE_ADD(@v_dt_edt_start, INTERVAL 1 DAY) INTO @v_dt_edt_end;

-- 	IF p_get_total_cnt = TRUE THEN
-- 		SELECT count(*)
-- 			FROM avm_logs 
-- 			WHERE evt_code = p_cnt_evt_type 
-- 				AND dt_updated 
-- 					BETWEEN @v_dt_edt_start AND @v_dt_edt_end
-- 				INTO v_i;
-- 		return v_i;
-- 	ELSE
-- 		SELECT count(*)
-- 			FROM avm_logs 
-- 			WHERE evt_code = p_cnt_evt_type 
-- 				AND evt_level >= 0.25 -- ignores less than 0.25
-- 				AND dt_updated 
-- 					BETWEEN @v_dt_edt_start AND @v_dt_edt_end
-- 				INTO v_i;
-- 		return v_i;
-- 	END IF;
-- END 
-- $$ DELIMITER ;

-- DELIMITER $$
-- drop PROCEDURE if exists AVM_GET_EVENT_LOG_2; -- setup
-- CREATE PROCEDURE `AVM_GET_EVENT_LOG_2`(
-- 	IN p_dt_updated VARCHAR(40),
-- 	IN p_cnt_evt_type VARCHAR(10),
-- 	IN p_get_all BOOL)
-- BEGIN
-- 	SELECT count(*) 
-- 		FROM avm_logs
-- 		INTO @v_count;

-- 	-- get counts just once (total & specific) to return as vars in select statements
-- 	SELECT AVM_GET_CNT_DT_EVT(p_dt_updated, p_cnt_evt_type, TRUE) INTO @evt_type_cnt_tot;
-- 	SELECT AVM_GET_CNT_DT_EVT(p_dt_updated, p_cnt_evt_type, FALSE) INTO @evt_type_cnt;

-- 	IF @v_count > 0 THEN
-- 		-- compensate 4hr EDT diff (JS client side will calc from UTC to EDT)
-- 		-- 	GET FROM X TIME TO X TIME
-- 		SELECT CONCAT(p_dt_updated, " 05:00:00") INTO @v_dt_utc_start;
-- 		SELECT DATE_ADD(@v_dt_utc_start, INTERVAL 5 HOUR) INTO @v_dt_edt_start; -- EST
-- 		SELECT NOW() INTO @v_dt_edt_end;
-- 		SELECT *, 
-- -- 		SELECT
-- 				p_cnt_evt_type as input_cnt_evt_type,
-- 				@evt_type_cnt_tot as 'evt_type_cnt_tot',
-- 				@evt_type_cnt as 'evt_type_cnt',																	
				
-- 				-- client side bar-graph support: log x-axis true event level 
-- -- 				case when (evt_code='S') then evt_level else NULL end as 'seizure',
-- 				case when (evt_code='S') and evt_level >= 0.009 then evt_level else NULL end as 'seizure',
-- -- 				case when (evt_code='P') then evt_level else NULL end as 'pain',
-- 				case when (evt_code='R') then 1 else NULL end as 'rest_hour',
-- 				case when (evt_code='T') then evt_level else NULL end as 'tizanidine_2mg',
-- 				case when (evt_code='X') then evt_level else NULL end as 'xanax_1mg',
-- 				case when (evt_code='V') and (DATE(dt_updated) >= '2023-01-22') then evt_level else NULL end as 'ativan_2mg',
-- --                 case when (evt_code='J') and (DATE(dt_updated) < '2022-12-04') then evt_level else NULL end as 'arjuna_powd_500mg',
--                 case when (evt_code='J') and (DATE(dt_updated) >= '2022-12-04') then evt_level else NULL end as 'arjuna_extr_500mg',	
-- 				-- case when (evt_code='W') then evt_level else NULL end as 'workout_100cnt',
-- 				-- client side bar-graph support: log x-axis blank space
-- -- 				case when (evt_code='A') then 0 else NULL end as 'anxiety',
-- -- 				case when (evt_code='F') then 0 else NULL end as 'food', 
-- -- 				case when (evt_code='O') then 0 else NULL end as 'other',
-- -- 				case when (evt_code='K') then 0 else NULL end as 'keppra_1000mg',

                
-- 				'success' as `status`,
-- 				'retrieved avm_logs for dt_updated' as info,
-- 				p_dt_updated as input_dt_updated,
-- 				p_cnt_evt_type as input_cnt_evt_type,
-- 				p_get_all as get_all
-- 			FROM avm_logs
-- 			WHERE dt_updated
-- 				BETWEEN @v_dt_edt_start AND @v_dt_edt_end
-- 			ORDER BY dt_updated DESC;
-- 	ELSE
-- 		SELECT 'failed' as `status`, 
-- 				'no avm_logs found at all' as info, 
-- 				p_dt_updated as input_dt_updated,
-- 				p_get_all as get_all;
-- 	END IF;
-- END 
-- $$ DELIMITER ;

-- DELIMITER $$
-- drop PROCEDURE if exists AVM_ADD_EVENT_LOG;
-- CREATE PROCEDURE `AVM_ADD_EVENT_LOG`(
-- 	IN p_evt_code VARCHAR(40),
-- 	IN p_evt_level FLOAT,
-- 	IN p_evt_descr VARCHAR(255))
-- BEGIN
-- 	-- add event log
-- 	INSERT INTO avm_logs (
-- 			evt_code,
-- 			evt_level,
-- 			evt_descr
-- 		) VALUES (
-- 			p_evt_code,
-- 			p_evt_level,
-- 			p_evt_descr
-- 		);

-- 	-- s reasons email default support 
-- 	SELECT 'null_r' into @v_reason;
-- 	SELECT -1 into @v_s_cnt;
-- 	SELECT 'nil_email' INTO @v_email_0;
-- 	SELECT 'nil_email' INTO @v_email_1;
-- 	SELECT 'nil_email' INTO @v_email_2;
-- 	SELECT 'nil_email' INTO @v_email_3;

-- 	-- ========================================================== --
-- 	-- comment this block to disbale s reasons email
-- 	-- GET 1 s_reasons if this entry is first for the day
-- 	SELECT COUNT(*) FROM avm_logs WHERE DATE(dt_updated) = CURDATE() INTO @v_entry_cnt;
-- 	IF @v_entry_cnt = 1 THEN
-- 		SELECT COUNT(*) FROM avm_logs 
-- 			WHERE DATE(dt_updated) = CURDATE()-1 AND evt_code = 'S'
-- 			INTO @v_s_cnt;
-- 		SELECT reason FROM avm_reasons ORDER BY RAND() LIMIT 1 into @v_reason;
-- 	END IF;
-- 	-- uncomment these emails wanted to go live with ...
-- 	-- SELECT 'NAME@EMAIL0.com' INTO @v_email_0;
-- 	SELECT 'NAME@EMAIL1.com' INTO @v_email_1;
-- 	SELECT 'NAME@EMAIL2.com' INTO @v_email_2;
-- 	SELECT 'NAME@EMAIL3.com' INTO @v_email_3;
-- 	-- ========================================================== --

-- 	-- RETURN	
-- 	SELECT LAST_INSERT_ID() into @new_evt_id;
-- 	SELECT dt_updated, 
-- 				'success' as `status`,
-- 				'added new avm event log' as info,
-- 				@new_evt_id as new_evt_id,
-- 				p_evt_descr as evt_set,
-- 				@v_s_cnt as s_cnt,
-- 				@v_reason as reason,
-- 				@v_email_0 as e_0,
-- 				@v_email_1 as e_1,
-- 				@v_email_2 as e_2,
-- 				@v_email_3 as e_3
-- 		FROM avm_logs
-- 		WHERE id = @new_evt_id;
-- END $$
-- DELIMITER ;