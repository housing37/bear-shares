DELIMITER $$
-- #================================================================# --
--		SUPPORT FUNCTIONS
-- #================================================================# --
DELIMITER $$
drop FUNCTION if exists valid_tg_user_admin; -- setup
CREATE FUNCTION `valid_tg_user_admin`(
		p_tg_user_id VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM users WHERE tg_user_id = p_tg_user_id AND is_admin = TRUE INTO @v_cnt;
	IF @v_cnt > 0 THEN
		RETURN TRUE; 
	ELSE
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_tg_user; -- setup
CREATE FUNCTION `valid_tg_user`(
		p_tg_user_id VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM users WHERE tg_user_id = p_tg_user_id INTO @v_cnt;
	IF @v_cnt > 0 THEN
		RETURN TRUE; 
	ELSE
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists tw_conf_exists; -- setup
CREATE FUNCTION `tw_conf_exists`(
		p_tw_conf_url VARCHAR(1024)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	set @v_exp_days = 7;
	SELECT COUNT(*) FROM users WHERE tw_conf_url = p_tw_conf_url INTO @v_cnt_fnd;
	IF @v_cnt_fnd > 0 THEN
		RETURN TRUE; 
	ELSE
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists exp_tw_conf; -- setup
CREATE FUNCTION `exp_tw_conf`(
		p_tg_user_id VARCHAR(40)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	set @v_exp_days = 7;
	SELECT COUNT(*) FROM users
		WHERE tg_user_id = p_tg_user_id
			AND DATEDIFF(NOW(), dt_last_tw_conf) > @v_exp_days into @v_exp_fnd;
	IF @v_exp_fnd > 0 THEN
		RETURN TRUE; 
	ELSE
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_tg_user_tw_conf; -- setup
CREATE FUNCTION `valid_tg_user_tw_conf`(
		p_tg_user_id VARCHAR(40)) 
		RETURNS VARCHAR(1024)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	IF NOT valid_tg_user(p_tg_user_id) THEN
		RETURN 'user not found';
	END IF;
	IF exp_tw_conf(p_tg_user_id) THEN
		RETURN 'user conf expired';
	END IF;

	RETURN 'valid user';
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_new_shill; -- setup
CREATE FUNCTION `valid_new_shill`(
		p_post_url VARCHAR(1024)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM shills
		WHERE post_url = p_post_url
		INTO @v_cnt;
	IF @v_cnt > 0 THEN
		RETURN FALSE; -- not new
	ELSE
		RETURN TRUE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists add_default_user_earns; -- setup
CREATE FUNCTION `add_default_user_earns`(
		p_user_id VARCHAR(1024)) 
		RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	INSERT INTO user_earns (
			fk_user_id
		) VALUES (
			p_user_id
		);
	SELECT LAST_INSERT_ID() into @new_earns_id;
	RETURN @new_earns_id;
END 
$$ DELIMITER ;

$$ DELIMITER
drop FUNCTION if exists get_usr_pay_rate; -- setup
CREATE FUNCTION `get_usr_pay_rate`(
		p_user_id INT(11),
		p_plat VARCHAR(40),
		p_type VARCHAR(40))
		RETURNS FLOAT
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT pay_usd FROM user_shill_rates 
		WHERE fk_user_id = p_user_id
			AND platform = p_plat
			AND type_descr = p_type
		ORDER BY id DESC LIMIT 1 
		INTO @v_pay_usd;
	RETURN @v_pay_usd;
END 
$$ DELIMITER ;

-- $$ DELIMITER
-- drop FUNCTION if exists add_shill_plat; -- setup
-- CREATE FUNCTION `add_shill_plat`(
-- 		p_platform VARCHAR(40))
-- 		RETURNS BOOLEAN
--     READS SQL DATA
--     DETERMINISTIC
-- BEGIN
-- 	INSERT INTO valid_shill_plats (
-- 		platform
-- 	) VALUES (
-- 		p_platform
-- 	);
-- 	SELECT LAST_INSERT_ID() into @new_id;
-- 	RETURN @new_id as new_shill_plat_id;
-- END 
-- $$ DELIMITER ;

-- $$ DELIMITER
-- drop FUNCTION if exists add_shill_type; -- setup
-- CREATE FUNCTION `add_shill_type`(
-- 		p_descr VARCHAR(40))
-- 		RETURNS BOOLEAN
--     READS SQL DATA
--     DETERMINISTIC
-- BEGIN
-- 	INSERT INTO valid_shill_types (
-- 		descr
-- 	) VALUES (
-- 		p_descr
-- 	);
-- 	SELECT LAST_INSERT_ID() into @new_id;
-- 	RETURN @new_id as new_shill_type_id;
-- END 
-- $$ DELIMITER ;

-- $$ DELIMITER
-- drop FUNCTION if exists add_user_shill_rate; -- setup
-- CREATE FUNCTION `add_user_shill_rate`(
-- 		p_user_id INT(11),
-- 		p_shill_plat_id INT(11),
-- 		p_shill_type_id INT(11),
-- 		p_pay_usd FLOAT)
-- 		RETURNS BOOLEAN
--     READS SQL DATA
--     DETERMINISTIC
-- BEGIN
-- 	INSERT INTO user_shill_rates (
-- 		fk_user_id,
-- 		fk_shill_plat_id,
-- 		fk_shill_type_id,
-- 		pay_usd
-- 	) VALUES (
-- 		p_user_id,
-- 		p_shill_plat_id,
-- 		p_shill_type_id,
-- 		p_pay_usd
-- 	);
-- 	SELECT LAST_INSERT_ID() into @new_rate_id;
-- 	RETURN @new_rate_id;

-- END 
-- $$ DELIMITER ;

-- #================================================================# --
--		STORED PROCEDURES
-- #================================================================# --
-- # '/register_as_shiller'
DELIMITER $$
DROP PROCEDURE IF EXISTS ADD_NEW_TG_USER;
CREATE PROCEDURE `ADD_NEW_TG_USER`(
    IN p_tg_user_id VARCHAR(40), -- -1000342
	IN p_tg_user_at VARCHAR(1024), -- @whatever
	IN p_tg_user_handle VARCHAR(1024), -- my handle
    IN p_wallet_address VARCHAR(255),
    IN p_tw_conf_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
	-- LST_KEYS_REG_SHILLER = ['user_id', 'wallet_address', 'tweet_url']
	-- DB_PROC_ADD_NEW_USER = 'ADD_NEW_USER'
	--     # validate 'p_tw_conf_url' contains texts '@BearSharesNFT' & 'trinity'

	-- vaidate user does NOT exists (only)
	IF valid_tg_user(p_tg_user_id) THEN
		SELECT id, tg_user_id, tg_user_at, tg_user_handle, is_admin
				'failed' as `status`, 
				'user already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
			FROM users 
			where tg_user_id = p_tg_user_id;

	-- vaidate p_tw_conf_url has not been used yet
	ELSE IF tw_conf_exists(p_tw_conf_url) THEN
		SELECT id, tg_user_id, tg_user_at, tg_user_handle, is_admin, tw_conf_url, dt_last_tw_conf,
				'failed' as `status`, 
				'tw conf url already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tw_conf_url as tw_conf_url_inp
			FROM users 
			where tg_user_id = p_tg_user_id;
	ELSE
		-- add to users table
		INSERT INTO users (
				tg_user_id,
				tg_user_at,
				tg_user_handle,
				wallet_address,
				tw_conf_url,
				dt_last_tw_conf
			) VALUES (
				p_tg_user_id,
				p_tg_user_at,
				p_tg_user_handle,
				p_wallet_address,
				p_tw_conf_url,
				NOW()
			);

		-- get new user id
		SELECT LAST_INSERT_ID() into @new_usr_id;

		-- set default earnings for new user
		SELECT add_default_user_earns(@new_usr_id);

		-- set default rates for new user
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'htag', 0.005); -- tw, hashtag, .5c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'short_txt', 0.01); -- tw, short_txt, 1c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'long_txt', 0.05); -- tw, long_txt, 5c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'img_meme', 0.25); -- tw, meme/img, 25c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'short_vid', 0.50); -- tw, short_vid, 50c
		SELECT add_user_shill_rate(@new_usr_id, 'twitter', 'long_vid', 1.00); -- tw, long_vid, 100c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 0, 0.005); -- tw, hashtag, .5c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 1, 0.01); -- tw, short_txt, 1c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 2, 0.05); -- tw, long_txt, 5c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 3, 0.25); -- tw, meme/img, 25c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 4, 0.50); -- tw, short_vid, 50c
		-- SELECT add_user_shill_rate(@new_usr_id, 0, 5, 1.00); -- tw, long_vid, 100c

		-- return
		SELECT u.dt_updated, u.tg_user_id, tg_user_at, tg_user_handle, u.is_admin,
				r.platform, r.type, r.pay_usd,
					'success' as `status`,
					'added new user' as info,
					@new_usr_id as new_users_id,
					p_tg_user_id as tg_user_id_inp
			FROM users u
			INNER JOIN user_shill_rates r
				ON u.id = r.fk_user_id
			WHERE u.id = @new_usr_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/confirm_twitter'
DELIMITER $$
DROP PROCEDURE IF EXISTS UPDATE_TWITTER_CONF;
CREATE PROCEDURE `UPDATE_TWITTER_CONF`(
    IN p_tg_user_id VARCHAR(40), -- ex: '-1000342'
    IN p_tw_conf_url VARCHAR(1024))
BEGIN
	-- vaidate user exists (only)
	IF NOT valid_tg_user(p_tg_user_id) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_tw_conf_url as tw_conf_url_inp;
	ELSE
		UPDATE TABLE users
			SET dt_updated = NOW(),
				dt_last_tw_conf = NOW(),
				tw_conf_url = p_tw_conf_url
			WHERE tg_user_id = p_tg_user_id;
		SELECT id, dt_created, dt_updated, tg_user_id, tg_user_at, tg_user_handle, is_admin, tw_conf_url,
				'success' as `status`,
				'set new exp' as info,
				p_tg_user_id as tg_user_id_inp
			FROM users
			WHERE tg_user_id = p_tg_user_id;
	END IF;
END
$$ DELIMITER ;

-- # '/submit_shill_link'
DELIMITER $$
DROP PROCEDURE IF EXISTS ADD_USER_SHILL_TW;
CREATE PROCEDURE `ADD_USER_SHILL_TW`(
    IN p_tg_user_id VARCHAR(40),
    IN p_post_url VARCHAR(1024))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
	-- LST_KEYS_SUBMIT_SHILL = ['user_id', 'post_url']
	-- DB_PROC_ADD_SHILL = 'ADD_USER_SHILL'
	-- 	   # check number of pending shills (is_apporved=False), return rate-limit info
	--	   #	perhaps set a max USD per day that people can earn?

	-- vaidate user exists & tw conf not expired
	set @v_valid = valid_tg_user_tw_conf(p_tg_user_id);
	IF NOT @v_valid = 'valid user' THEN
		SELECT 'failed' as `status`, 
				@v_valid as info, 
				p_tg_user_id as tg_user_id_inp;

	-- validate 'post_url' is not in 'shills' table yet
	ELSE IF NOT valid_new_shill(p_post_url) THEN
		SELECT 'failed' as `status`, 
				'shill already exists' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_post_url as post_url;
	ELSE
		-- insert into 'shills' (...) values (...) for user_id
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		INSERT INTO shills
			SET (
				fk_user_id,
				post_url,
				shill_plat
			) VALUES (
				@v_user_id,
				p_post_url,
				'twitter'
			);
		-- get new shill id
		SELECT LAST_INSERT_ID() into @new_shill_id;
		
		-- return
		SELECT s.id as s_id, s.dt_created as s_dt_created, s.post_url, s.shill_plat, s.shill_type, s.is_apporved,
				u.id as u_id, u.tw_conf_url as u_tw_conf_url, u.tg_user_id, u.tg_user_at, u.tg_user_handle,
				'success' as `status`,
				'added new shill' as info,
				p_tg_user_id as tg_user_id_inp
			FROM shills s
			INNER JOIN users u
				ON s.fk_user_id = u.id
			WHERE s.id = @new_shill_id;
	END IF;
END 
$$ DELIMITER ;

-- # '/show_my_rates'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_PAY_RATES;
CREATE PROCEDURE `GET_USER_PAY_RATES`(
    IN p_tg_user_id VARCHAR(40)
	IN p_platform VARCHAR(40)) -- const: unknown, twitter, tiktok, reddit
BEGIN
	-- vaidate user exists
	IF NOT valid_tg_user(p_tg_user_id) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp,
				p_platform as platform_inp
	ELSE
		-- get latest 'p_platform' rates for tg_user_id (note: 'ORDER BY id DESC LIMIT 1')
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'htag') INTO @v_pay_usd_htag;		
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'short_txt') INTO @v_pay_usd_stxt;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'long_txt') INTO @v_pay_usd_ltxt;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'img_meme') INTO @v_pay_usd_img;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'short_vid') INTO @v_pay_usd_svid;
		SELECT get_usr_pay_rate(@v_user_id, p_platform, 'long_vid') INTO @v_pay_usd_lvid;
		SELECT @v_pay_usd_htag as pay_usd_hashtag,
				@v_pay_usd_stxt as pay_usd_short_text,
				@v_pay_usd_ltxt as pay_usd_long_text,
				@v_pay_usd_img as pay_usd_img_meme,
				@v_pay_usd_svid as pay_usd_short_vid,
				@v_pay_usd_lvid as pay_usd_long_vid,
				'success' as `status`,
				'get user rates' as info,
				@v_user_id as user_id,
				p_tg_user_id as tg_user_id_inp,
				p_platform as platform_inp
	END IF;
END 
$$ DELIMITER ;

-- # '/show_my_earnings'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_EARNINGS;
CREATE PROCEDURE `GET_USER_EARNINGS`(
    IN p_tg_user_id VARCHAR(40))
BEGIN
	-- vaidate user exists
	IF NOT valid_tg_user(p_tg_user_id) THEN
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

-- # '/withdraw_my_earnings'
DELIMITER $$
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

-- # '/admin_show_user_shills' | # '/admin_scan_web_for_removed_shills'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_SHILLS_ALL;
CREATE PROCEDURE `GET_USER_SHILLS_ALL`(
    IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_id VARCHAR(40),
    IN p_approved BOOLEAN,
    IN p_removed BOOLEAN)
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSE IF NOT valid_tg_user(p_tg_user_id) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp;
	ELSE
		-- return all 'p_tg_user_id' data from 'user_earns' table
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT *, 
				'success' as `status`,
				'get user shills all' as info,
				@v_user_id as user_id,
				p_tg_user_id as tg_user_id_inp,
				p_approved as is_approved_inp,
				p_removed as is_removed_inp
			FROM shills
			WHERE fk_user_id = @v_user_id
				AND is_apporved = p_approved,
				AND is_removed = p_removed
			ORDER BY id desc;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_list_all_pend_shills'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_PEND_SHILLS_ALL;
CREATE PROCEDURE `GET_PEND_SHILLS_ALL`(
    IN p_tg_admin_id VARCHAR(40)
	IN p_removed BOOLEAN)
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;
	ELSE
		-- return all 'is_approved=FALSE' from shills table
		SELECT *, 
				'success' as `status`,
				'get all pending shills' as info,
				@v_user_id as user_id,
				p_tg_user_id as tg_user_id_inp,
				p_removed as is_removed_inp
			FROM shills
			WHERE is_apporved = FALSE, -- FALSE = 'pending'
				AND is_removed = p_removed
			ORDER BY id desc;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_approve_pend_shill'
DELIMITER $$
DROP PROCEDURE IF EXISTS UPDATE_USER_SHILL_APPR_EARNS;
CREATE PROCEDURE `UPDATE_USER_SHILL_APPR_EARNS`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_id VARCHAR(40),
    IN p_shill_id VARCHAR(40),
	IN p_shill_plat VARCHAR(40), -- const: unknown, twitter, tiktok, reddit
	IN p_shill_type VARCHAR(40), -- const: unknown, htag, short_txt, long_txt, img_meme, short_vid, long_vid
	IN p_pay_usd VARCHAR(40), -- dyn: 0.005, 0.01, 0.05, 0.25 0.50, 1.00, etc.
    IN p_approved BOOLEAN)
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
	-- LST_KEYS_APPROVE_SHILL = ['admin_id','user_id', 'shill_id','shill_plat','shill_type','pay_usd','approved']
	-- DB_PROC_APPROVE_SHILL_STATUS = "UPDATE_USER_SHILL_APPR_EARNS" 
	--     # admin views / inspects shill_url on the web (determines: plat, type, pay, approve)

	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	ELSE
		-- get shill counts & user earngs counts for 'p_tg_user_id' (w/ additional vars needed)
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT COUNT(*) FROM shills WHERE id = p_shill_id AND fk_user_id = @v_user_id INTO @v_cnt_ids;
		SELECT COUNT(*) FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_cnt_earns;
		SELECT is_removed FROM shills WHERE id = p_shill_id INTO @v_shill_removed;
		SELECT post_url FROM shills WHERE id = p_shill_id INTO @v_post_url;

		-- check shill_id exists
		IF @v_cnt_ids = 0 THEN
			SELECT 'failed' as `status`, 
					'shill id not found' as info, 
					p_tg_user_id as tg_user_id_inp,
					p_shill_id as shill_id_inp,
					p_approved as approved_inp;

		-- validate shill post_url is still active  (is_removed not set to True)
		ELSE IF @v_shill_removed = TRUE THEN
			SELECT post_url,
					'failed' as `status`, 
					'dead shill post url' as info, 
					p_tg_user_id as tg_user_id_inp,
					p_shill_id as shill_id_inp,
					p_approved as approved_inp
				FROM shills 
				WHERE id = p_shill_id;
		ELSE
			-- update shill plat, type, and pay with admin data (prev. reviewed & selected)
			-- 	NOTE: is_removed gauranteed 'FALSE' for p_shill_id, due to prev. check w/ @v_shill_removed
			UPDATE shills 
				SET dt_updated = NOW(),
					shill_plat = p_shill_plat,
					shill_type = p_shill_type,
					pay_usd = p_pay_usd,
					is_approved = p_approved 
				WHERE id = p_shill_id
					AND fk_user_id = @v_user_id
					AND is_removed = FALSE; 

			-- if user_id has no user_earns entry yet, then create it (safety check)
			--	NOTE: this should have already been created in 'ADD_NEW_TG_USER' (cmd: /register_as_shillter) 
			IF @v_cnt_earns = 0 THEN
				SELECT add_default_user_earns(@v_user_id) INTO @v_earns_id;
			END IF;

			-- calc & update user_earns for this user_id
			SELECT user_total FROM user_earns WHERE fk_user_id = @v_user_id INTO @u_total;
			SELECT user_owed FROM user_earns WHERE fk_user_id = @v_user_id INTO @u_owed;
			SET @v_tot = @u_total + p_pay_usd;
			SET @v_owe = @u_owed + p_pay_usd;
			UPDATE user_earns
				SET dt_updated = NOW(),
					user_total = @v_tot,
					user_owed = @v_owe,
					is_apporved = TRUE
				WHERE fk_user_id = @v_user_id;

			-- return
			SELECT *, 
					'success' as `status`,
					'updated user earns' as info,
					@v_user_id as user_id,
					@v_post_url as shill_url,
					p_tg_user_id as tg_user_id_inp,
					p_shill_id as shill_id_inp,
					p_shill_plat_inp as shill_id_plat_inp,
					p_shill_type_inp as shill_id_type_inp,
					p_pay_usd as pay_usd_inp,
					p_approved as approved_inp
				FROM user_earns
				WHERE fk_user_id = @v_user_id;
				ORDER BY id desc;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_view_shill_status'
DELIMITER $$
DROP PROCEDURE IF EXISTS GET_USER_SHILL;
CREATE PROCEDURE `GET_USER_SHILL`(
    IN p_tg_admin_id VARCHAR(40),
    IN p_tg_user_id VARCHAR(40),
    IN p_shill_id INT(11),
    IN p_shill_url VARCHAR(1024))
BEGIN
	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	-- vaidate user exists
	ELSE IF NOT valid_tg_user(p_tg_user_id) THEN
		SELECT 'failed' as `status`, 
				'user not found' as info, 
				p_tg_user_id as tg_user_id_inp;
	ELSE
		-- check shill counts by id & url for 'p_tg_user_id'
		SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
		SELECT COUNT(*) FROM shills WHERE id = p_shill_id AND fk_user_id = @v_user_id INTO @v_cnt_ids;
		SELECT COUNT(*) FROM shills WHERE id = p_shill_url AND fk_user_id = @v_user_id INTO @v_cnt_urls;

		-- get shill by url
		IF p_shill_id = -1 THEN
			IF @v_cnt_urls = 0 THEN
				SELECT 'failed' as `status`, 
						'shill url not found' as info, 
						p_tg_user_id as tg_user_id_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as shill_url_inp;
			ELSE
				SELECT *, 
						'success' as `status`,
						'get user shill url' as info,
						@v_user_id as user_id,
						p_tg_user_id as tg_user_id_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as post_url_inp
					FROM shills
					WHERE post_url = p_shill_url,
					ORDER BY id desc;
			END IF;

		-- get shill by id
		ELSE
			IF @v_cnt_ids = 0 THEN
				SELECT 'failed' as `status`, 
						'shill id not found' as info, 
						p_tg_user_id as tg_user_id_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as shill_url_inp;
			ELSE
				SELECT *, 
						'success' as `status`,
						'get user shill id' as info,
						@v_user_id as user_id,
						p_tg_user_id as tg_user_id_inp,
						p_shill_id as shill_id_inp,
						p_shill_url as post_url_inp
					FROM shills
					WHERE id = p_shill_id,
					ORDER BY id desc;
			END IF;
		END IF;
	END IF;
END 
$$ DELIMITER ;

-- # '/admin_pay_shill_rewards'
DELIMITER $$
DROP PROCEDURE IF EXISTS UPDATE_USER_SHILL_PAID_EARNS;
CREATE PROCEDURE `UPDATE_USER_SHILL_PAID_EARNS`(
    IN p_tg_admin_id VARCHAR(40),
	IN p_tg_user_id VARCHAR(40),
    IN p_shill_id VARCHAR(40),
	IN p_pay_tx_hash VARCHAR(255))
BEGIN
    -- Procedure Body
    -- You can add your SQL logic here
	-- LST_KEYS_PAY_SHILL_EARNS = ['admin_id','user_id']
	-- DB_PROC_UPDATE_USR_PAID_EARNS = 'UPDATED_USER_SHILL_PAID_EARNS'
	--     # perform python/solidity 'transfer' call on 'users.wallet_address' for user_id (get pay_tx_hash)
	--     # check 'user_earns.withdraw_request=True' for 'user_id'
	--	   # check 'shills.pay_usd != 0' for shill_id
	--     # validate 'user_earns.usd_owed' == 
	--     #   total of (select 'shills.pay_usd' where 'shills.is_paid=False' & 'shills.is_approved=True' & 'shills.is_removed=False') for user_id
	--     # update 'user_earns.usd_owed|paid' where 'user_earns.fk_user_id=user_id'
	--     # update 'shills.is_paid=True' & 'shills.pay_tx_hash' where all 'shills.is_approved=True' & 'shills.is_removed=False' for user_id
	--     # update 'user_earns.usd_total|owed|paid' accordingly (+-) for user_id

	-- validate admin
	IF NOT valid_tg_user_admin(p_tg_admin_id) THEN
		SELECT 'failed' as `status`, 
				'invalid admin' as info, 
				p_tg_admin_id as tg_admin_id;

	ELSE

	END IF;
END 
$$ DELIMITER ;

-- # '/admin_log_removed_shill'
DELIMITER $$
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

-- # '/admin_scan_web_for_removed_shills'
DELIMITER $$
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

-- # '/admin_set_shiller_rates'
DELIMITER $$
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