-- #================================================================# --
-- #STORED PROCEDURES
-- #================================================================# --
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS ADD_NEW_QUIZ_LOG;
-- CREATE PROCEDURE `ADD_NEW_QUIZ_LOG`(
-- 	IN p_user_id INT(11),
--     IN p_tg_bot_id VARCHAR(40), -- '581475171'
-- 	IN p_tg_bot_at VARCHAR(1024), -- '@bs_trinity_bot'
--     IN p_question TEXT)
-- BEGIN
-- 	-- add to users table
-- 	INSERT INTO log_bot_quiz (
-- 			p_user_id,
-- 			p_tg_bot_id,
-- 			p_tg_bot_at,
-- 			p_question
-- 		) VALUES (
-- 			fk_user_id_created,
-- 			tg_bot_id,
-- 			tg_bot_at,
-- 			question
-- 		);

-- 	-- get new user id
-- 	SELECT LAST_INSERT_ID() into @new_usr_id;
-- END 
-- $$ DELIMITER ;

-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS ADD_NEW_DATA_LOG;
-- CREATE PROCEDURE `ADD_NEW_DATA_LOG`(
--     IN p_tg_user_id VARCHAR(40), -- '581475171'
-- 	IN p_tg_user_at VARCHAR(1024), -- '@whatever'
-- 	IN p_tg_user_handle VARCHAR(1024), -- 'my handle'
--     IN p_wallet_address VARCHAR(255),
--     IN p_tw_conf_url VARCHAR(1024),
-- 	IN p_tw_conf_id VARCHAR(40),
-- 	IN p_tw_user_at VARCHAR(255))
-- BEGIN
-- END 
-- $$ DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS GET_TG_USER_ID_WEB;
CREATE PROCEDURE `GET_TG_USER_ID_WEB`(
	IN p_tg_user_at VARCHAR(40))
BEGIN
	-- fail: if tg_user_at doesn't exist
	IF NOT valid_tg_user_at(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user does not exists' as info, 
				p_tg_user_at as tg_user_at_inp;
	ELSE
		-- get support requirements
		SELECT id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_user_id;
		SELECT tg_user_id FROM users WHERE id = @v_user_id INTO @v_tg_user_id;
		SELECT 'success' as `status`, 
				'found user id for user at' as info, 
				@v_user_id as user_id,
				@v_tg_user_id as tg_user_id,
				p_tg_user_at as tg_user_at_inp;
	END IF;
END 
$$ DELIMITER ;

-- # '/set_wallet'
-- LST_KEYS_SET_WALLET = ['user_id','user_at','wallet_address']
-- DB_PROC_SET_WALLET = 'SET_WALLET_ADDR'
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_WALLET_ADDR;
CREATE PROCEDURE `SET_WALLET_ADDR`(
    IN p_tg_user_id VARCHAR(40), -- ex: '-1000342'
	IN p_tg_user_at VARCHAR(40),
    IN p_wallet_address VARCHAR(255))
BEGIN
	-- get support requirements
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;

	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	IF NOT valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp;
	ELSE
		UPDATE users 
			SET wallet_address = p_wallet_address,
				dt_updated = NOW()
			WHERE id = @v_user_id;
		SELECT wallet_address, dt_updated,
				'success' as `status`,
				'set new wallet address' as info,
				@v_user_id as user_id,
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp,
				p_wallet_address as wallet_address_inp
			FROM users
			WHERE tg_user_id = p_tg_user_id;
	END IF;
END 
$$ DELIMITER ;

-- aux cmd: /register & /submit
DELIMITER $$
DROP PROCEDURE IF EXISTS TW_URL_IS_USED;
CREATE PROCEDURE `TW_URL_IS_USED`(
    IN p_tweet_url VARCHAR(1024),
	IN p_tweet_id VARCHAR(40),
	IN p_tw_user_at VARCHAR(255))
BEGIN
	-- checks url used for shill | conf
	SELECT valid_new_tw_conf(p_tweet_url, p_tweet_id) INTO @v_new_tweet;
	SET @v_is_used = NOT @v_new_tweet;
	SELECT 'success' as `status`, 
			'tweet url used' as info, 
			@v_is_used as is_used,
			p_tweet_url as tweet_url_inp,
			p_tweet_id as tweet_id_inp;
END
$$ DELIMITER ;

-- # '/register_as_shiller'
-- LST_KEYS_REG_SHILLER = ['user_id','user_at','user_handle','wallet_address','trinity_tw_url']
-- DB_PROC_ADD_NEW_USER = 'ADD_NEW_TG_USER'
-- # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesX' & 'trinity' & 'register'
DELIMITER $$
DROP PROCEDURE IF EXISTS ADD_NEW_TG_USER;
CREATE PROCEDURE `ADD_NEW_TG_USER`(
    IN p_tg_user_id VARCHAR(40), -- '581475171'
	IN p_tg_user_at VARCHAR(1024), -- '@whatever'
	IN p_tg_user_handle VARCHAR(1024), -- 'my handle'
    IN p_wallet_address VARCHAR(255),
    IN p_tw_conf_url VARCHAR(1024),
	IN p_tw_conf_id VARCHAR(40),
	IN p_tw_user_at VARCHAR(255))
BEGIN
	-- setup
	SELECT COUNT(*) FROM users WHERE tw_user_at = p_tw_user_at INTO @v_tw_at_found;

	-- fail: if tg_user_at is taken
	IF valid_tg_user_at(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user already exists; contact support' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp;
	
	-- fail: if p_tw_user_at is already registerd
	ELSEIF @v_tw_at_found > 0 THEN
		SELECT 'failed' as `status`,
				'twitter user already exists' as info,
				p_tw_user_at as tw_user_at_inp,
				p_tw_conf_url as tw_conf_url_inp;

	-- fail: if tg_user_id is indeed taken (updates 'users.tg_user_at' if needed)
	ELSEIF valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		SELECT id, tg_user_id, tg_user_at, tg_user_handle, is_admin,
				'failed' as `status`, 
				'telegram user already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp
			FROM users 
			WHERE tg_user_id = p_tg_user_id;

	-- fail: if p_tw_conf_url has already been used
	ELSEIF NOT valid_new_tw_conf(p_tw_conf_url, p_tw_conf_id) THEN -- checks url used for shill | conf
		SELECT u.id as user_id_OG, u.tg_user_id as tg_user_id_OG, 
				u.tw_conf_url as tw_conf_url_OG, u.dt_last_tw_conf as dt_last_tw_conf_OG,
				l.tw_conf_url as tw_conf_url_LOG,
				'failed' as `status`, 
				'tw conf url already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp,
				p_tg_user_handle as tg_user_handle_inp,
				p_wallet_address as wallet_address_inp,
				p_tw_conf_url as tw_conf_url_inp,
				p_tw_user_at as tw_user_at_inp
			FROM users u
			INNER JOIN log_tw_conf_urls l
				ON u.id = l.fk_user_id
			WHERE l.tw_conf_url = p_tw_conf_url;
	ELSE
		-- add to users table
		INSERT INTO users (
				tg_user_id,
				tg_user_at,
				tg_user_handle,
				wallet_address,
				tw_conf_url,
				dt_last_tw_conf,
				tw_conf_id,
				tw_user_at
			) VALUES (
				p_tg_user_id,
				p_tg_user_at,
				p_tg_user_handle,
				p_wallet_address,
				p_tw_conf_url,
				NOW(),
				p_tw_conf_id,
				p_tw_user_at
			);

		-- get new user id
		SELECT LAST_INSERT_ID() into @new_usr_id;

		-- log conf url used (so it can't be used again)
		SELECT add_tw_conf_url_log(@new_usr_id, p_tw_conf_url, p_tw_conf_id, p_tw_user_at) INTO @new_log_url_id;

		-- set default earnings for new user
		SELECT add_default_user_earns(@new_usr_id) INTO @new_earns_id;

		-- set default rates for new user
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_0', 0.5) INTO @v_rate_id; -- tw, hashtag, .5c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_1', 1.00) INTO @v_rate_id; -- tw, short_txt, 1c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_2', 2.00) INTO @v_rate_id; -- tw, long_txt, 5c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_3', 5.00) INTO @v_rate_id; -- tw, meme/img, 25c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_4', 10.00) INTO @v_rate_id; -- tw, short_vid, 50c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'level_5', 25.00) INTO @v_rate_id; -- tw, long_vid, 100c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 0, 0.005); -- tw, hashtag, .5c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 1, 0.01); -- tw, short_txt, 1c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 2, 0.05); -- tw, long_txt, 5c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 3, 0.25); -- tw, meme/img, 25c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 4, 0.50); -- tw, short_vid, 50c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 5, 1.00); -- tw, long_vid, 100c

		-- return
		SELECT u.dt_updated, u.tg_user_id, u.tg_user_at, u.tg_user_handle, u.is_admin, 
				u.tw_conf_url, u.tw_conf_id, u.dt_last_tw_conf, u.tw_user_at, 
				r.platform, r.type_descr, r.pay_usd,
				'success' as `status`,
				'added new user' as info,
				@new_usr_id as new_users_id,
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp,
				p_tg_user_handle as tg_user_handle_inp,
				p_wallet_address as wallet_address_inp,
				p_tw_conf_url as tw_conf_url_inp,
				p_tw_user_at as tw_user_at_inp
			FROM users u			
			INNER JOIN user_shill_rates r
				ON u.id = r.fk_user_id
			WHERE u.id = @new_usr_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/confirm_twitter'
-- LST_KEYS_TW_CONF = ['user_id','user_at','trinity_tw_url']
-- DB_PROC_RENEW_TW_CONFRIM = 'UPDATE_TWITTER_CONF'
-- # PRE-DB: validate 'trinity_tw_url' contains texts '@BearSharesX' & 'trinity' & 'register
DELIMITER $$
DROP PROCEDURE IF EXISTS UPDATE_TWITTER_CONF;
CREATE PROCEDURE `UPDATE_TWITTER_CONF`(
    IN p_tg_user_id VARCHAR(40), -- ex: '-1000342'
	IN p_tg_user_at VARCHAR(40),
    IN p_tw_conf_url VARCHAR(1024),
	IN p_tw_conf_id VARCHAR(255),
	IN p_tw_user_at VARCHAR(40))
BEGIN
	-- get support requirements
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
	SELECT tw_user_at FROM users WHERE id = @v_user_id INTO @v_tw_user_at;

	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	IF NOT valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tw_conf_url as tw_conf_url_inp;

	-- fail: if current twitter user does not match twitter user for new confirmation
	ELSEIF @v_tw_user_at != p_tw_user_at THEN
		SELECT 'failed' as `status`,
				'twitter user cannot be changed' as info,
				@v_tw_user_at as tw_user_at,
				p_tw_user_at as tw_user_at_inp,
				p_tw_conf_url as tw_conf_url_inp;

	-- vaidate p_tw_conf_url has not been used yet
	ELSEIF NOT valid_new_tw_conf(p_tw_conf_url, p_tw_conf_id) THEN -- checks url used for shill | conf
		SELECT u.id as user_id_OG, u.tg_user_id as tg_user_id_OG, 
				u.tw_conf_url as tw_conf_url_OG, u.dt_last_tw_conf as dt_last_tw_conf_OG,
				l.tw_conf_url as tw_conf_url_LOG,
				'failed' as `status`, 
				'tw conf url already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tw_conf_url as tw_conf_url_inp,
				p_tw_conf_id as tw_conf_id_inp,
				p_tw_user_at as tw_user_at_inp
			FROM users u
			INNER JOIN log_tw_conf_urls l
				ON u.id = l.fk_user_id
			WHERE l.tw_conf_url = p_tw_conf_url;

	ELSE	
		-- update conf url for this user
		UPDATE users
			SET dt_updated = NOW(),
				dt_last_tw_conf = NOW(),
				tw_conf_url = p_tw_conf_url,
				tw_conf_id = p_tw_conf_id,
				tw_user_at = p_tw_user_at
			WHERE id = @v_user_id;

		-- log conf url used (so it can't be used again)
		-- SELECT add_tw_conf_url_log(@v_user_id, p_tw_conf_url) INTO @new_log_url_id;
		SELECT add_tw_conf_url_log(@v_user_id, p_tw_conf_url, p_tw_conf_id, p_tw_user_at) INTO @new_log_url_id;

		SELECT id, dt_created, dt_updated, tg_user_id, tg_user_at, tg_user_handle, is_admin, tw_conf_url, dt_last_tw_conf,
				'success' as `status`,
				'set new exp' as info,
				p_tg_user_id as tg_user_id_inp
			FROM users
			WHERE tg_user_id = p_tg_user_id;
	END IF;
END
$$ DELIMITER ;

-- # '/submit_shill'
-- LST_KEYS_SUBMIT_SHILL = ['user_id','user_at','post_url']
-- DB_PROC_ADD_SHILL = 'ADD_USER_SHILL_TW'
DELIMITER $$
DROP PROCEDURE IF EXISTS ADD_USER_SHILL_TW;
CREATE PROCEDURE `ADD_USER_SHILL_TW`(
    IN p_tg_user_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
    IN p_post_url VARCHAR(1024),
	IN p_post_id VARCHAR(255),
	IN p_post_uname VARCHAR(255))
BEGIN
	-- get support requirements
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
	SELECT tw_user_at FROM users WHERE id = @v_user_id INTO @v_tw_user_at;

	-- vaidate user exists & tw conf not expired
	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	set @v_valid = valid_tg_user_tw_conf(p_tg_user_id, p_tg_user_at); -- invokes 'valid_tg_user'
	IF NOT @v_valid = 'valid user' THEN
		SELECT 'failed' as `status`, 
				@v_valid as info, 
				p_tg_user_id as tg_user_id_inp;

	-- fail: if TG user's tw_user_at does not match incoming new shill p_post_uname
	ELSEIF @v_tw_user_at != p_post_uname THEN
		SELECT 'failed' as `status`,
				'invalid twitter account for this user' as info,
				@v_tw_user_at as tw_user_at,
				p_post_uname as post_uname_inp,
				p_post_url as post_url_inp;

	-- validate 'post_url' is not in 'shills' table yet (or log_tw_conf_urls)
	ELSEIF NOT valid_new_shill(p_post_url, p_post_id) THEN -- checks url used for shill | conf
		SELECT 'failed' as `status`,
				'shill already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_post_url as post_url;
	ELSE
		-- insert into 'shills' (...) values (...) for user_id
		INSERT INTO shills (
				fk_user_id,
				post_url,
				post_id,
				post_uname,
				shill_plat
			) VALUES (
				@v_user_id,
				p_post_url,
				p_post_id,
				p_post_uname,
				'twitter'
			);
		-- get new shill id
		SELECT LAST_INSERT_ID() into @new_shill_id;
		
		-- return
		SELECT s.id as shill_id, s.dt_created as dt_created_s, s.post_url, s.post_id, s.post_uname, s.shill_plat, s.shill_type, s.is_approved,
				u.id as user_id, u.tw_conf_url as tw_conf_url_u, u.tg_user_id, u.tg_user_at, u.tg_user_handle, u.tw_user_at,
				'success' as `status`,
				'added new shill' as info,
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp,
				p_post_uname as post_uname_inp,
				p_post_url as post_url_inp,
				p_post_id as post_id_inp
			FROM shills s
			INNER JOIN users u
				ON s.fk_user_id = u.id
			WHERE s.id = @new_shill_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/request_cashout'
-- LST_KEYS_REQUEST_CASHOUT = ['user_id','user_at']
-- DB_PROC_REQUEST_CASHOUT = 'SET_USER_WITHDRAW_REQUESTED'
-- # POST-DB: python TG notify admin_pay to process
-- # POST-DB: python TG notify p_tg_user_id that request has been submit (w/ user_earns.usd_owed)
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_USER_WITHDRAW_REQUESTED;
CREATE PROCEDURE `SET_USER_WITHDRAW_REQUESTED`(
    IN p_tg_user_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40))
BEGIN
	-- vaidate user exists & tw conf not expired
	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	set @v_valid = valid_tg_user_tw_conf(p_tg_user_id, p_tg_user_at); -- invokes 'valid_tg_user'
	IF NOT @v_valid = 'valid user' THEN
		SELECT 'failed' as `status`, 
				@v_valid as info, 
				p_tg_user_id as tg_user_id_inp;

	ELSEIF NOT valid_wallet_set(p_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'no wallet address set' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tg_user_at as tg_user_at_inp;
				
	ELSE
		SET @v_usd_min = 1.00;
		-- SET @v_usd_min = 0.25;
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT usd_owed FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_usd_owed;

		-- fail: if owed amount is at least equal to min withdraw amount
		IF NOT @v_usd_owed >= @v_usd_min THEN
			SELECT 'failed' as `status`, 
					'owed balance too low' as info,
					@v_user_id as user_id,
					@v_usd_owed as usd_owed,
					CAST(@v_usd_min AS FLOAT) as usd_withdraw_min,
					p_tg_user_id as tg_user_id_inp;
		ELSE
			-- set withdraw requested
			UPDATE user_earns
				SET withdraw_requested = TRUE
				WHERE fk_user_id = @v_user_id;
			
			-- return request confirmation + admin contact info to notify
			SELECT is_admin FROM users WHERE id = @v_user_id INTO @v_is_admin;
			SELECT is_admin_pay FROM users WHERE id = @v_user_id INTO @v_is_admin_pay;

			--	NOTE: if withdraw request user is indeed an admin, then no need for UNION
			IF @v_is_admin = TRUE OR @v_is_admin_pay = TRUE THEN
				SELECT tg_user_id, tg_user_at, is_admin, is_admin_pay,
						tg_user_handle, tw_user_at, wallet_address, 
						'success' as `status`,
						'set withdraw requested' as info,
						@v_user_id as user_id,
						@v_usd_owed as usd_owed,
						CAST(@v_usd_min AS FLOAT) as usd_withdraw_min,
						p_tg_user_id as tg_user_id_inp
					FROM users
					WHERE id = @v_user_id;

			--	NOTE: if withdraw request user is not an admin, 
			--		then use UNION to ensure admins are returned as well
			ELSE
				SELECT tg_user_id, tg_user_at, is_admin, is_admin_pay,
						tg_user_handle, tw_user_at, wallet_address, 
						'success' as `status`,
						'set withdraw requested' as info,
						@v_user_id as user_id,
						@v_usd_owed as usd_owed,
						CAST(@v_usd_min AS FLOAT) as usd_withdraw_min,
						p_tg_user_id as tg_user_id_inp
					FROM users
					WHERE id = @v_user_id
				UNION
				SELECT tg_user_id, tg_user_at, is_admin, is_admin_pay, 
						NULL as tg_user_handle, NULL as tw_user_at, NULL as wallet_address,
						'ADMIN' as `status`,
						NULL as info,
						NULL as user_id,
						NULL as usd_owed,
						NULL as usd_withdraw_min,
						NULL as tg_user_id_inp
					FROM users
					WHERE is_admin = TRUE 
						OR is_admin_pay = TRUE;
			END IF;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/show_my_rates'
-- LST_KEYS_SHOW_RATES = ['user_id','user_at','platform'] # const: unknown, twitter, tiktok, reddit
-- DB_PROC_GET_USR_RATES = 'GET_USER_PAY_RATES'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_PAY_RATES;
CREATE PROCEDURE `GET_USER_PAY_RATES`(
    IN p_tg_user_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
	IN p_platform VARCHAR(40)) -- const: unknown, twitter, tiktok, reddit
BEGIN
	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	IF NOT valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_platform as platform_inp;
	ELSE
		-- get latest 'p_platform' rates for tg_user_id (note: 'ORDER BY id DESC LIMIT 1')
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_0') INTO @v_pay_usd_htag;		
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_1') INTO @v_pay_usd_stxt;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_2') INTO @v_pay_usd_ltxt;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_3') INTO @v_pay_usd_img;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_4') INTO @v_pay_usd_svid;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'level_5') INTO @v_pay_usd_lvid;
		SELECT 'success' as `status`,
				'get user rates' as info,
				@v_user_id as user_id,
				@v_pay_usd_htag as pay_usd_hashtag,
				@v_pay_usd_stxt as pay_usd_short_text,
				@v_pay_usd_ltxt as pay_usd_long_text,
				@v_pay_usd_img as pay_usd_img_meme,
				@v_pay_usd_svid as pay_usd_short_vid,
				@v_pay_usd_lvid as pay_usd_long_vid,
				p_tg_user_id as tg_user_id_inp,
				p_platform as platform_inp;
	END IF;
END 
$$ DELIMITER ;

-- # '/show_my_earnings'
-- LST_KEYS_SHOW_EARNINGS = ['user_id','user_at']
-- DB_PROC_GET_USR_EARNS = 'GET_USER_EARNINGS'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_EARNINGS;
CREATE PROCEDURE `GET_USER_EARNINGS`(
    IN p_tg_user_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40))
BEGIN
	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	IF NOT valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp;
	ELSE
		-- return all 'p_tg_user_id' data from 'user_earns' table
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT ue.*, u.tg_user_id, u.tg_user_at, u.tg_user_handle, u.tw_conf_url, u.dt_last_tw_conf, u.wallet_address,
				'success' as `status`,
				'get user earnings' as info,
				@v_user_id as user_id,
				p_tg_user_id as tg_user_id_inp
			FROM user_earns ue
			INNER JOIN users u
				ON ue.fk_user_id = u.id
			WHERE ue.fk_user_id = @v_user_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_show_user_rates'
-- LST_KEYS_SHOW_RATES_ADMIN = ['admin_id','user_id','platform'] # const: unknown, twitter, tiktok, reddit
-- DB_PROC_GET_USR_RATES_ADMIN = 'GET_USER_PAY_RATES_ADMIN'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_PAY_RATES_ADMIN;
CREATE PROCEDURE `GET_USER_PAY_RATES_ADMIN`(
	IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_at VARCHAR(40),
	IN p_platform VARCHAR(40)) -- const: unknown, twitter, tiktok, reddit
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;
	ELSE
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
		CALL GET_USER_PAY_RATES(@v_tg_user_id, p_tg_user_at, p_platform);
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_show_user_earnings'
-- LST_KEYS_SHOW_EARNS_ADMIN = ['admin_id','user_id']
-- DB_PROC_GET_USR_EARNS_ADMIN = 'GET_USER_EARNINGS'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_EARNINGS_ADMIN;
CREATE PROCEDURE `GET_USER_EARNINGS_ADMIN`(
	IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40))
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;
	ELSE
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
		CALL GET_USER_EARNINGS(@v_tg_user_id, p_tg_user_at);
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_show_user_shills' | # '/admin_scan_web_for_removed_shills'
-- # '/admin_show_user_shills'
-- LST_KEYS_USR_SHILLS = ['admin_id','user_id','approved','removed']
-- DB_PROC_GET_USR_SHILLS_ALL = 'GET_USER_SHILLS_ALL'
-- # '/admin_scan_web_for_removed_shills'
-- LST_KEYS_CHECK_USR_REM_SHILLS = ['admin_id','user_id','approved','removed']
-- DB_PROC_CHECK_USR_REM_SHILL = 'GET_USER_SHILLS_ALL'
-- # POST-DB: web scrape those post_urls to see if they are still working / viewable
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_SHILLS_ALL;
CREATE PROCEDURE `GET_USER_SHILLS_ALL`(
    IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_at VARCHAR(40),
    IN p_approved BOOLEAN,
    IN p_removed BOOLEAN)
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;
	ELSE
		-- setup
		SELECT id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_user_id;
		SELECT tg_user_id FROM users WHERE id = @v_user_id INTO @v_tg_user_id; -- for return only
		SELECT COUNT(*) FROM shills WHERE fk_user_id = @v_user_id AND is_approved = p_approved AND is_removed = p_removed INTO @v_shill_cnt;

		-- fail: if no shills exist for this query
		IF @v_shill_cnt = 0 THEN
			SELECT 'failed' as `status`, 
					'no shills found' as info, 
					@v_user_id as user_id,
					@v_tg_user_id as tg_user_id,
					p_tg_user_at as tg_user_at_inp,
					p_approved as is_approved_inp,
					p_removed as is_removed_inp;
		ELSE
			SELECT *, id as shill_id, -- return all 'p_tg_user_at' data from 'shills' table
					'success' as `status`,
					'get user shills all' as info,
					@v_user_id as user_id,
					@v_tg_user_id as tg_user_id,
					p_tg_user_at as tg_user_at_inp,
					p_approved as is_approved_inp,
					p_removed as is_removed_inp
				FROM shills
				WHERE fk_user_id = @v_user_id
					AND is_approved = p_approved
					AND is_removed = p_removed
				ORDER BY id desc;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_list_all_pend_shills'
-- LST_KEYS_ALL_PEND_SHILLS = ['admin_id','removed']
-- DB_PROC_GET_PEND_SHILLS = 'GET_PEND_SHILLS_ALL' # get where 'is_approved' = False
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_PEND_SHILLS_ALL;
CREATE PROCEDURE `GET_PEND_SHILLS_ALL`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_removed BOOLEAN)
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;
	ELSE
		-- setup
		-- SELECT id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_user_id;
		-- SELECT tg_user_id FROM users WHERE id = @v_user_id INTO @v_tg_user_id; -- for return only
		SELECT COUNT(*) FROM shills WHERE is_approved = FALSE AND is_removed = p_removed INTO @v_shill_cnt;

		-- fail: if no shills exist for this query
		IF @v_shill_cnt = 0 THEN
			SELECT 'failed' as `status`, 
					'no pending shills found' as info, 
					p_tg_admin_id as tg_admin_id_inp,
					p_removed as is_removed_inp;
		ELSE
			-- return all 'is_approved=FALSE' from shills table
			SELECT s.*, s.id as shill_id,
					u.id as user_id, u.tg_user_at,
					'success' as `status`,
					'get all pending shills' as info,
					p_tg_admin_id as tg_admin_id_inp,
					p_removed as is_removed_inp
				FROM shills s
					INNER JOIN users u
					ON s.fk_user_id = u.id
				WHERE is_approved = FALSE -- FALSE = 'pending'
					AND is_removed = p_removed
				ORDER BY id desc;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_approve_pend_shill'
-- LST_KEYS_APPROVE_SHILL = ['admin_id','user_at', 'shill_id','shill_plat','shill_type','approved']
-- DB_PROC_APPROVE_SHILL_STATUS = "UPDATE_USER_SHILL_APPR_EARNS" 
-- # POST-DB: python TG notify admin_pay to process
-- # POST-DB: python TG notify p_tg_user_id that request has been submit (w/ user_earns.usd_owed)
DELIMITER $$
DROP PROCEDURE IF EXISTS UPDATE_USER_SHILL_APPR_EARNS;
CREATE PROCEDURE `UPDATE_USER_SHILL_APPR_EARNS`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
    IN p_shill_id VARCHAR(40),
	IN p_shill_plat VARCHAR(40), -- const: unknown, twitter, tiktok, reddit
	IN p_shill_type VARCHAR(40)) -- const: unknown, htag, short_txt, long_txt, img_meme, short_vid, long_vid
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;

	ELSE
		-- get shill counts & user earngs counts for 'p_tg_user_at' (w/ additional vars needed)
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
		SELECT id FROM users WHERE tg_user_id = @v_tg_user_id INTO @v_user_id;
		SELECT COUNT(*) FROM shills WHERE id = p_shill_id AND fk_user_id = @v_user_id INTO @v_cnt_ids;
		SELECT COUNT(*) FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_cnt_earns;
		SELECT is_removed FROM shills WHERE id = p_shill_id INTO @v_shill_removed;
		SELECT is_approved FROM shills WHERE id = p_shill_id INTO @v_shill_approved_curr;
		SELECT post_url FROM shills WHERE id = p_shill_id INTO @v_post_url;

		-- get users current pay rate
		SELECT get_usr_pay_rate(@v_user_id, p_shill_plat, p_shill_type) INTO @v_pay_usd_rate;		

		-- check shill_id exists
		IF @v_cnt_ids = 0 THEN
			SELECT 'failed' as `status`, 
					'shill id not found' as info, 
					@v_tg_user_id as tg_user_id_inp,
					p_tg_user_at as tg_user_at_inp,
					p_shill_id as shill_id_inp;

		-- fail: shill already approved
		ELSEIF @v_shill_approved_curr = TRUE THEN
			SELECT 'failed' as `status`, 
					'shill id already approved' as info, 
					@v_tg_user_id as tg_user_id_inp,
					p_tg_user_at as tg_user_at_inp,
					p_shill_id as shill_id_inp;

		-- validate shill post_url is still active  (is_removed not set to True)
		ELSEIF @v_shill_removed = TRUE THEN
			SELECT post_url,
					'failed' as `status`, 
					'dead shill post url' as info,
					@v_tg_user_id as tg_user_id_inp, 
					p_tg_user_at as tg_user_at_inp,
					p_shill_id as shill_id_inp
				FROM shills 
				WHERE id = p_shill_id;

		-- validate max shills per day for @v_user_id as NOT been met
		-- 	note: includes is_removed=TRUE|FALSE (limit earns to those removing shills)
		ELSEIF usr_shill_limit_reached(@v_tg_user_id) THEN
			SELECT 'failed' as `status`, 
					'daily shill approve limit reached' as info, 
					@v_tg_user_id as tg_user_id_inp,					
					p_tg_user_at as tg_user_at_inp,
					p_shill_id as shill_id_inp;
		ELSE
			-- update shill plat, type, and pay with admin data (prev. reviewed & selected)
			-- 	NOTE: is_removed gauranteed 'FALSE' for p_shill_id, due to prev. check w/ @v_shill_removed
			UPDATE shills 
				SET dt_updated = NOW(),
					shill_plat = p_shill_plat,
					shill_type = p_shill_type,
					pay_usd = @v_pay_usd_rate,
					is_approved = TRUE,
					dt_updated_approve = NOW()
				WHERE id = p_shill_id
					AND fk_user_id = @v_user_id
					AND is_removed = FALSE; 

			-- if user_id has no user_earns entry yet, then create it (safety check)
			--	NOTE: this should have already been created in 'ADD_NEW_TG_USER' (cmd: /register_as_shillter) 
			IF @v_cnt_earns = 0 THEN
				SELECT add_default_user_earns(@v_user_id) INTO @v_earns_id;
			END IF;

			-- calc & update user_earns for this user_id
			SELECT usd_total FROM user_earns WHERE fk_user_id = @v_user_id INTO @u_total;
			SELECT usd_owed FROM user_earns WHERE fk_user_id = @v_user_id INTO @u_owed;
			SET @v_tot = @u_total + @v_pay_usd_rate;
			SET @v_owe = @u_owed + @v_pay_usd_rate;

			UPDATE user_earns
				SET dt_updated = NOW(),
					usd_total = @v_tot,
					usd_owed = @v_owe
				WHERE fk_user_id = @v_user_id;

			-- return
			SELECT *, 
					'success' as `status`,
					'updated user earns' as info,
					@v_user_id as user_id,
					@v_post_url as shill_url,
					@v_tg_user_id as tg_user_id_inp,
					p_tg_user_at as tg_user_at_inp,
					p_shill_id as shill_id_inp,
					p_shill_plat as shill_plat_inp,
					p_shill_type as shill_type_inp,
					@v_pay_usd_rate as pay_usd
				FROM user_earns
				WHERE fk_user_id = @v_user_id
				ORDER BY id desc;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_view_shill_status'
-- LST_KEYS_VIEW_SHILL = ['admin_id','user_id','shill_id','shill_url']
-- DB_PROC_GET_USR_SHILL = 'GET_USER_SHILL'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_SHILL;
CREATE PROCEDURE `GET_USER_SHILL`(
    IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_at VARCHAR(40),
    IN p_shill_id INT(11),
    IN p_shill_url VARCHAR(1024))
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;
	ELSE
		-- check shill counts by id & url for 'p_tg_user_at'
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
		SELECT id FROM users WHERE tg_user_id = @v_tg_user_id INTO @v_user_id;
		SELECT COUNT(*) FROM shills WHERE id = p_shill_id AND fk_user_id = @v_user_id INTO @v_cnt_ids;
		SELECT COUNT(*) FROM shills WHERE post_url = p_shill_url AND fk_user_id = @v_user_id INTO @v_cnt_urls;

		-- get shill by url
		IF p_shill_id = -1 THEN
			IF @v_cnt_urls = 0 THEN
				SELECT 'failed' as `status`, 
						'shill url not found' as info, 
						@v_tg_user_id as tg_user_id_inp,
						p_tg_user_at as tg_user_at_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as shill_url_inp;
			ELSE
				SELECT *, id as shill_id,
						'success' as `status`,
						'get user shill url' as info,
						@v_user_id as user_id,
						@v_tg_user_id as tg_user_id_inp,
						p_tg_user_at as tg_user_at_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as post_url_inp
					FROM shills
					WHERE post_url = p_shill_url
					ORDER BY id desc;
			END IF;

		-- get shill by id
		ELSE
			IF @v_cnt_ids = 0 THEN
				SELECT 'failed' as `status`, 
						'shill id not found' as info, 
						@v_tg_user_id as tg_user_id_inp,
						p_tg_user_at as tg_user_at_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as shill_url_inp;
			ELSE
				SELECT *, id as shill_id,
						'success' as `status`,
						'get user shill id' as info,
						@v_user_id as user_id,
						@v_tg_user_id as tg_user_id_inp,
						p_tg_user_at as tg_user_at_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as post_url_inp
					FROM shills
					WHERE id = p_shill_id
					ORDER BY id desc;
			END IF;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_pay_shill_rewards'
-- LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_id']
-- DB_PROC_SET_USR_PAY_SUBMIT = 'SET_USER_PAY_TX_SUBMIT' # -> get_usr_pay_usd_appr_sum, set_usr_pay_usd_tx_submit
-- # POST-DB: perform python/solidity 'transfer(user_earns.usd_owed, wallet_address)' to get tx data for DB_PROC_SET_USR_PAY_CONF
-- #	        get 'wallet_address' from 'GET_USER_EARNINGS(tg_user_id)'
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_USER_PAY_TX_SUBMIT;
CREATE PROCEDURE `SET_USER_PAY_TX_SUBMIT`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
	IN p_aux_tok_burn VARCHAR(255), -- NOT IN USE, requied to settle python side
	IN p_sel_aux_tok_send BOOLEAN)
BEGIN
	SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
	SELECT id FROM users WHERE tg_user_id = @v_tg_user_id INTO @v_user_id;
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;

	-- check withdraw indeed requested by '@v_tg_user_id'
	-- 	note: executes 'add_default_user_earns' (if needed)
	ELSEIF NOT usr_withdraw_requested(@v_tg_user_id) THEN
		SELECT 'failed' as `status`, 
				'withdraw not requested by user' as info, 
				@v_tg_user_id as tg_user_id,
				p_tg_user_at as tg_user_at_inp;

	-- fail: if user has not set a wallet address yet
	ELSEIF NOT valid_wallet_set(@v_tg_user_id, p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'no wallet address set' as info,
				p_tg_user_at as tg_user_at_inp;

	ELSE
		-- calc total pay sum of all approved shills w/ txs non-pending
		--	get total usd_owed for p_tg_user_at (@v_tg_user_id)
		SET @v_is_paid = FALSE;
		SELECT get_usr_pay_usd_appr_sum(@v_tg_user_id, @v_is_paid) INTO @v_tot_pay_usd;
		SELECT usd_owed FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_tot_owed;

		-- validate total pay sum from 'shills' == total usd_owed from 'user_earns'
		IF @v_tot_pay_usd != @v_tot_owed THEN
			SELECT 'failed' as `status`, 
					'total pay_usd != total usd_owed' as info, 
					@v_tot_pay_usd as tot_pend_pay_usd,
					@v_tot_owed as tot_pend_usd_owed,
					@v_tg_user_id as tg_user_id,
					p_tg_user_at as tg_user_at_inp;
		ELSE
			-- set 'pay_tx_submit=TRUE' for all approved shills that are not tx pending yet
			SELECT set_usr_pay_usd_tx_submit(@v_tg_user_id, p_sel_aux_tok_send) INTO @v_success;
			SELECT ue.*, u.wallet_address,
					'success' as `status`,
					'user pay tx submitted' as info,
					@v_user_id as user_id,
					@v_success as tx_pending,
					@v_tot_pay_usd as tot_pay_usd,
					@v_tot_owed as tot_owed,
					@v_tg_user_id as tg_user_id,
					p_tg_user_at as tg_user_at_inp
				FROM user_earns ue
				INNER JOIN users u
					ON u.id = ue.fk_user_id
				WHERE ue.fk_user_id = @v_user_id;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_pay_shill_rewards'
-- LST_KEYS_PAY_SHILL_EARNS_CONF = ['admin_id','user_id','chain_usd_paid','tx_hash','tx_status','tok_addr','tok_symb','tok_amnt']
-- DB_PROC_SET_USR_PAY_CONF = 'SET_USER_PAY_TX_STATUS' # -> set_usr_pay_usd_tx_status
-- # PRE-DB: perform python/solidity 'transfer' to get tx data for DB_PROC_SET_USR_PAY_CONF
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_USER_PAY_TX_STATUS;
CREATE PROCEDURE `SET_USER_PAY_TX_STATUS`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
	IN p_chain_usd_paid FLOAT,
	IN p_pay_tx_hash VARCHAR(255),
	IN p_pay_tx_status INT(11), -- -1|-2 = tx exception, 0 = tx fail, 1 = tx success
	IN p_pay_to_wallet_addr VARCHAR(255),
	IN p_pay_tok_addr VARCHAR(255),
	IN p_pay_tok_symb VARCHAR(40),
	IN p_aux_tok_burn VARCHAR(255))
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;
	
	ELSE
		-- set support variables
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;		
		SELECT id FROM users WHERE tg_user_id = @v_tg_user_id INTO @v_user_id;
		SELECT usd_owed FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_curr_usd_owed;
		SELECT usd_paid FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_curr_usd_paid;

		-- update user_earns entry (change usd_owed|paid accordingly; reset withdraw_requested)
		SET @v_new_usd_paid = @v_curr_usd_paid + @v_curr_usd_owed;
		SET @v_usd_owed_paid_diff = @v_curr_usd_owed - p_chain_usd_paid;

		-- NOTE: do not update user_earns if tx failed (ie. p_chain_usd_paid == -1)
		IF p_chain_usd_paid > 0 THEN
			UPDATE user_earns
				SET dt_updated = NOW(),
					usd_owed = 0.0,
					usd_paid = @v_new_usd_paid,
					withdraw_requested = FALSE
				WHERE fk_user_id = @v_user_id;
		END IF;
		
		-- update tx data (w/ is_paid) for all shills that were submitted by @v_tg_user_id
		SELECT set_usr_pay_usd_tx_status(@v_tg_user_id, p_pay_tx_hash, p_pay_tx_status, p_pay_to_wallet_addr, p_chain_usd_paid, p_pay_tok_addr, p_pay_tok_symb, p_aux_tok_burn) INTO @v_status;

		-- return
		SELECT *, 
				'success' as `status`,
				'user pay tx status updated' as info,
				@v_user_id as user_id,
				@v_status as tx_status_set,
				@v_curr_usd_owed as old_usd_owed,
				p_chain_usd_paid as chain_usd_paid_inp,
				@v_usd_owed_paid_diff as usd_owed_paid_diff,
				@v_new_usd_paid as new_usd_tot_paid,
				p_pay_tx_hash as pay_tx_hash_inp,
				p_pay_tx_status as pay_tx_status_inp,
				p_pay_tok_addr as pay_tok_addr_inp,
				p_pay_tok_symb as pay_tok_symb_inp,
				p_aux_tok_burn as aux_tok_burn_addr,
				p_tg_user_at as tg_user_at_inp,
				@v_tg_user_id as tg_user_id
			FROM user_earns
			WHERE fk_user_id = @v_user_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_log_removed_shill'
-- python execution...
-- LST_KEYS_SET_SHILL_REM = ['admin_id','tg_user_id','shill_id','removed']
-- DB_PROC_SET_SHILL_REM = 'SET_USER_SHILL_REMOVED'
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_USER_SHILL_REMOVED;
CREATE PROCEDURE `SET_USER_SHILL_REMOVED`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_at VARCHAR(40),
    IN p_shill_id INT(11),
	IN p_removed BOOLEAN)
BEGIN
	SELECT id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_user_id;
	SELECT tg_user_id FROM users WHERE id = @v_user_id INTO @v_tg_user_id;
	SELECT is_removed FROM shills WHERE id = p_shill_id INTO @v_is_removed;

	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;

	-- vaidate user / shill combo
	ELSEIF NOT valid_shill_for_user(@v_tg_user_id, p_shill_id) THEN
		SELECT 'failed' as `status`, 
				'user / shill combo not found' as info, 
				@v_tg_user_id as tg_user_id,
				p_shill_id as shill_id_inp;

	-- fail: if shill 'is_removed' would be unchanged
	ELSEIF @v_is_removed = p_removed THEN
		SELECT 'failed' as `status`, 
				'shill remove status resulted in no change' as info, 
				@v_tg_user_id as tg_user_id,
				p_shill_id as shill_id_inp,
				p_removed as removed_inp;
	ELSE
		-- set shill id as removed
		UPDATE shills
			SET is_removed = p_removed
			WHERE id = p_shill_id;

		-- return
		SELECT post_url, fk_user_id, is_removed,
				'success' as `status`,
				'removed shill id' as info,
				#v_tg_user_id as tg_user_id,
				p_tg_user_at as tg_user_at_inp,
				p_shill_id as shill_id_inp,
				p_removed as removed_inp
			FROM shills
			WHERE id = p_shill_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_set_shiller_rate'
-- LST_KEYS_SET_USR_SHILL_PAY_RATES = ['admin_id','user_id','shill_plat','shill_type','pay_usd']
-- DB_PROC_SET_USR_RATES = 'SET_USER_PAY_RATE'
DELIMITER $$
DROP PROCEDURE IF EXISTS SET_USER_PAY_RATE;
CREATE PROCEDURE `SET_USER_PAY_RATE`(
    IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_at VARCHAR(40),
	IN p_shill_plat VARCHAR(40),
	IN p_shill_type VARCHAR(40),
	IN p_pay_usd FLOAT(40))
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSEIF NOT admin_valid_tg_user(p_tg_user_at) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_at as tg_user_at_inp;

	ELSE
		-- add new entry to user_shill_rates table
		SELECT tg_user_id FROM users WHERE tg_user_at = p_tg_user_at INTO @v_tg_user_id;
		SELECT id FROM users WHERE tg_user_id = @v_tg_user_id INTO @v_user_id;
		SELECT add_user_shill_rate(@v_user_id, p_shill_plat, p_shill_type, p_pay_usd) INTO @v_new_rate_id;

		-- return
		SELECT *,
				'success' as `status`,
				'added user shill rate' as info,
				@v_tg_user_id as tg_user_id,
				p_tg_user_at as tg_user_at_inp,
				p_shill_plat as shill_plat_inp,
				p_shill_type as shill_type_inp,
				p_pay_usd as pay_usd_inp
			FROM user_shill_rates
			WHERE id = @v_new_rate_id;
	END IF;
END 
$$ DELIMITER ;

-- _ NOTE_031124 _ : need to consider/fix not having tg_user_id if invoked from non-admin
-- # '/blacklist_user' 
-- LST_KEYS_ADD_BLACKLIST_SCAMMER = ['admin_or_user_id','bl_user_id','bl_user_at','bl_user_handle','tg_chan_id']
-- DB_PROC_ADD_BLACKLIST_SCAMMER = 'ADD_REQUEST_USER_BLACKLIST'
DELIMITER $$
DROP PROCEDURE IF EXISTS ADD_REQUEST_USER_BLACKLIST;
CREATE PROCEDURE `ADD_REQUEST_USER_BLACKLIST`(
    IN p_tg_admin_or_user_id VARCHAR(40),
    IN p_tg_bl_user_id VARCHAR(40),
	IN p_tg_bl_user_at VARCHAR(40),
	IN p_tg_bl_user_handle VARCHAR(40),
	IN p_tg_chan_id VARCHAR(40))
BEGIN
	DECLARE v_new_bl_id INT(11);
	DECLARE v_enabled BOOLEAN;
	-- validate user
	IF NOT admin_valid_tg_user(p_tg_admin_or_user_id) THEN
		SELECT 'failed' as `status`, 
				'request user not found' as info, 
				p_tg_admin_or_user_id as tg_admin_or_user_id;

	-- if admin: add blacklist with is_enabled=TRUE
	ELSEIF valid_tg_user_admin(p_tg_admin_or_user_id) THEN
		SELECT TRUE INTO v_enabled;
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT add_blacklist_usr(@v_user_id, p_tg_bl_user_id, p_tg_bl_user_at, p_tg_bl_user_handle, p_tg_chan_id, v_enabled) INTO v_new_bl_id;

	-- if reg user: add blacklist with is_enabled=FALSE
	ELSE
		SELECT FALSE INTO v_enabled;
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT add_blacklist_usr(@v_user_id, p_tg_bl_user_id, p_tg_bl_user_at, p_tg_bl_user_handle, p_tg_chan_id, v_enabled) INTO v_new_bl_id;
	END IF;

	-- return
	SELECT *,
			'success' as `status`,
			'blacklisted user' as info,
			v_new_bl_id as new_bl_id,
			p_tg_admin_or_user_id as tg_admin_or_user_id_inp,
			p_tg_bl_user_id as tg_bl_user_id_inp,
			p_tg_bl_user_at as tg_bl_user_at_inp,
			p_tg_bl_user_handle as tg_bl_user_handle_inp,
			p_tg_chan_id as tg_chan_id_inp,
			p_pay_usd as pay_usd_inp_inp
		FROM user_blacklist_scammers
		WHERE id = @v_new_bl_id;
END 
$$ DELIMITER ;