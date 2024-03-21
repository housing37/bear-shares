-- #================================================================# --
-- # SUPPORT FUNCTIONS
-- #================================================================# --
DELIMITER $$
drop FUNCTION if exists _clear_all_tables; -- setup
CREATE FUNCTION `_clear_all_tables`() RETURNS VARCHAR(2)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	delete from users;
	delete from user_shill_rates;
	delete from user_earns;
	delete from shills;
	delete from log_tw_conf_urls;
	delete from log_tg_user_at_changes;
	RETURN "QQ";
END 
$$ DELIMITER ;

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
drop FUNCTION if exists valid_tg_user_at; -- setup
CREATE FUNCTION `valid_tg_user_at`(
		p_tg_user_at VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- check if user_id exits yet
	SELECT COUNT(*) FROM users WHERE tg_user_at = p_tg_user_at INTO @v_cnt;
	IF @v_cnt > 0 THEN -- yes exists
		RETURN TRUE; 
	ELSE -- does not exist
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_wallet_set; -- setup
CREATE FUNCTION `valid_wallet_set`(
		p_tg_user_id VARCHAR(40),
		p_tg_user_at VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM users WHERE tg_user_id = p_tg_user_id INTO @v_cnt;
	IF @v_cnt = 0 THEN
		RETURN FALSE;
	ELSE
		SELECT wallet_address FROM users WHERE tg_user_id = p_tg_user_id INTO @v_wa; 
		IF @v_wa = '0x0' THEN
			RETURN FALSE;
		ELSE
			RETURN TRUE;
		END IF;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_tg_user; -- setup
CREATE FUNCTION `valid_tg_user`(
		p_tg_user_id VARCHAR(40),
		p_tg_user_at VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- check if user_id exits yet
	SELECT COUNT(*) FROM users WHERE tg_user_id = p_tg_user_id INTO @v_cnt;
	IF @v_cnt > 0 THEN -- yes exists
		-- check if user_id / user_at comnbo exists
		--	if not, update user_at for this user_id
		SELECT COUNT(*) 
			FROM users 
			WHERE tg_user_at = p_tg_user_at 
				AND tg_user_id = p_tg_user_id 
			INTO @v_found_match;
		IF @v_found_match = 0 THEN -- combo w/ user_at NOT found
			-- get support variables
			SELECT id FROM users where tg_user_id = p_tg_user_id INTO @v_user_id;
			SELECT tg_user_at FROM users where id = @v_user_id INTO @v_prev_tg_user_at;
			
			-- update existing user with new p_tg_user_at
			UPDATE users 
				SET tg_user_at = p_tg_user_at,
					dt_updated = NOW()
				WHERE tg_user_id = p_tg_user_id;

			-- log tg_user_at change in log_tg_user_at_changes
			INSERT INTO log_tg_user_at_changes (
					fk_user_id,
					tg_user_id_const,
					tg_user_at_prev,
					tg_user_at_new
				) VALUES (
					@v_user_id,
					p_tg_user_id,
					@v_prev_tg_user_at,
					p_tg_user_at
				);
		END IF;
		RETURN TRUE; 
	ELSE -- does not exist
		RETURN FALSE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists admin_valid_tg_user; -- setup
CREATE FUNCTION `admin_valid_tg_user`(
		p_tg_user_at VARCHAR(40)) RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT valid_tg_user_at(p_tg_user_at) INTO @v_ret_bool;
	RETURN @v_ret_bool;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists add_tw_conf_url_log; -- setup
CREATE FUNCTION `add_tw_conf_url_log`(
		p_user_id INT(11),
		p_tw_conf_url VARCHAR(1024),
		p_tw_conf_id VARCHAR(40),
		p_tw_user_at VARCHAR(255)) 
		RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	INSERT INTO log_tw_conf_urls (
		fk_user_id,
		tw_conf_url,
		tw_conf_id,
		tw_user_at
	) VALUES (
		p_user_id,
		p_tw_conf_url,
		p_tw_conf_id,
		p_tw_user_at
	);
	SELECT LAST_INSERT_ID() INTO @new_conf_id;
	RETURN @new_conf_id;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists tw_conf_exists; -- setup
CREATE FUNCTION `tw_conf_exists`(
		p_tw_conf_url VARCHAR(1024),
		p_tw_conf_id VARCHAR(255)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- SELECT COUNT(*) FROM log_tw_conf_urls WHERE tw_conf_url = p_tw_conf_url INTO @v_cnt_fnd; -- legacy
	SELECT COUNT(*) FROM log_tw_conf_urls WHERE tw_conf_id = p_tw_conf_id INTO @v_cnt_fnd;
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
		p_tg_user_id VARCHAR(40),
		p_tg_user_at VARCHAR(40)) 
		RETURNS VARCHAR(1024)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- fail: if tg_user_id is not taken (updates 'users.tg_user_at' if needed)
	IF NOT valid_tg_user(p_tg_user_id, p_tg_user_at) THEN
		RETURN 'user not found';
	END IF;
	IF exp_tw_conf(p_tg_user_id) THEN
		RETURN 'user conf expired';
	END IF;

	RETURN 'valid user';
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_new_tw_conf; -- setup
CREATE FUNCTION `valid_new_tw_conf`(
		p_post_url VARCHAR(1024),
		p_post_id VARCHAR(255)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM shills
		-- WHERE post_url = p_post_url
		WHERE post_id = p_post_id
		INTO @v_cnt;
	SELECT tw_conf_exists(p_post_url, p_post_id) INTO @v_exists;
	IF @v_cnt > 0 THEN
		RETURN FALSE; -- not valid: found as shill
	ELSEIF @v_exists = TRUE THEN
		RETURN FALSE; -- not valid: found as conf
	ELSE
		RETURN TRUE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_new_shill; -- setup
CREATE FUNCTION `valid_new_shill`(
		p_post_url VARCHAR(1024),
		p_post_id VARCHAR(255)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT COUNT(*) FROM shills
		WHERE post_url = p_post_url
		INTO @v_cnt;
	SELECT tw_conf_exists(p_post_url, p_post_id) INTO @v_exists;
	IF @v_cnt > 0 THEN
		RETURN FALSE; -- not valid: found as shill
	ELSEIF @v_exists = TRUE THEN
		RETURN FALSE; -- not valid: found as conf
	ELSE
		RETURN TRUE;
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists valid_shill_for_user; -- setup
CREATE FUNCTION `valid_shill_for_user`(
		p_tg_user_id VARCHAR(40),
		p_shill_id INT(11)) 
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
	SELECT COUNT(*) FROM shills
		WHERE id = p_shill_id
			AND fk_user_id = @v_user_id
		INTO @v_cnt;
	IF @v_cnt > 0 THEN
		RETURN TRUE; -- yes exists
	ELSE
		RETURN FALSE; -- does not exist
	END IF;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists add_default_user_earns; -- setup
CREATE FUNCTION `add_default_user_earns`(
		p_user_id INT(11)) 
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

DELIMITER $$
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

DELIMITER $$
drop FUNCTION if exists add_user_shill_rate; -- setup
CREATE FUNCTION `add_user_shill_rate`(
		p_user_id INT(11),
		p_shill_plat VARCHAR(40),
		p_shill_type VARCHAR(40),
		p_pay_usd FLOAT)
		RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	INSERT INTO user_shill_rates (
		fk_user_id,
		platform,
		type_descr,
		pay_usd
	) VALUES (
		p_user_id,
		p_shill_plat,
		p_shill_type,
		p_pay_usd
	);
	SELECT LAST_INSERT_ID() into @new_rate_id;
	RETURN @new_rate_id;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists usr_withdraw_requested; -- setup
CREATE FUNCTION `usr_withdraw_requested`(
		p_tg_user_id VARCHAR(40))
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- get id from users table
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;

	-- check if user_earns entry exists for this user id (if not, create it)
	SELECT COUNT(*) FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_cnt;
	IF @v_cnt = 0 THEN
		SELECT add_default_user_earns(@v_user_id) INTO @v_earn_id;
	END IF;

	-- return boolean for 'withdraw_requested'
	SELECT withdraw_requested FROM user_earns WHERE fk_user_id = @v_user_id INTO @v_requested;
	RETURN @v_requested;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists get_usr_pay_usd_appr_sum; -- setup
CREATE FUNCTION `get_usr_pay_usd_appr_sum`(
		p_tg_user_id VARCHAR(40),
		p_is_paid BOOLEAN)
		RETURNS FLOAT
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- get id for p_tg_user_id in users table
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;

	-- get sum of all pay_usd in shills table
	--	where approved, not removed, not pending, p_is_paid
	SELECT SUM(pay_usd)
		FROM shills 
		WHERE fk_user_id = @v_user_id
			AND is_approved = TRUE
			AND is_removed = FALSE
			AND pay_tx_submit = FALSE
			AND is_paid = p_is_paid
		INTO @v_tot_amnt;

	-- return -37 is no entries for p_tg_user_id in shills table
	IF @v_tot_amnt IS NULL THEN
		SET @v_tot_amnt = -37.0; 
	END IF;

	-- return
	RETURN @v_tot_amnt;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists set_usr_pay_usd_tx_submit; -- setup
CREATE FUNCTION `set_usr_pay_usd_tx_submit`(
		p_tg_user_id VARCHAR(40))
		RETURNS BOOLEAN
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- get id for p_tg_user_id in users table
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;

	-- set tx submit to TRUE for all approved shills and not tx sumbit yet
	--	for user_id where approved, not removed, not paid
	UPDATE shills
		SET pay_tx_submit = TRUE,
			dt_tx_submit = NOW()
		WHERE id 
			IN (SELECT id
					FROM shills 
					WHERE fk_user_id = @v_user_id
						AND is_approved = TRUE
						AND is_removed = FALSE
						AND pay_tx_submit = FALSE
						AND is_paid = FALSE);
	RETURN TRUE;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists set_usr_pay_usd_tx_status; -- setup
CREATE FUNCTION `set_usr_pay_usd_tx_status`(
		p_tg_user_id VARCHAR(40),
		p_pay_tx_hash VARCHAR(255),
		p_pay_tx_status VARCHAR(40), -- const: baseFee, pending, queued
		p_pay_tok_addr VARCHAR(255),
		p_pay_tok_symb VARCHAR(40),
		p_pay_tok_amnt FLOAT)
		RETURNS VARCHAR(40)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- get id for p_tg_user_id in users table
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;

	-- set various tx data & paid to TRUE for all approved shills and tx submitted
	--	for user_id where approved, not removed, not paid
	UPDATE shills
		SET pay_tx_status = p_pay_tx_status,
			dt_tx_status = NOW(),
			pay_tx_hash = p_pay_tx_hash,
			pay_tx_status = p_pay_tx_status,
			pay_tok_addr = p_pay_tok_addr,
			pay_tok_symb = p_pay_tok_symb,
			pay_tok_amnt = p_pay_tok_amnt,
			is_paid = TRUE
		WHERE id 
			IN (SELECT id
					FROM shills 
					WHERE fk_user_id = @v_user_id
						AND pay_tx_submit = TRUE
						AND is_approved = TRUE
						AND is_removed = FALSE
						AND is_paid = FALSE);
	RETURN p_pay_tx_status;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists add_blacklist_usr; -- setup
CREATE FUNCTION `add_blacklist_usr`(
		p_user_id INT(11),
    	p_tg_bl_user_id VARCHAR(40),
		p_tg_bl_user_at VARCHAR(40),
		p_tg_bl_user_handle VARCHAR(40),
		p_tg_chan_id VARCHAR(40),
		p_enabled BOOLEAN)
		RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	INSERT INTO user_blacklist_scammers (
			fk_user_id_added,
			tg_user_id,
			tg_user_at,
			tg_user_handle,
			tg_chat_id_found,
			is_enabled
		) VALUES (
			p_user_id,
			p_tg_bl_user_id,
			p_tg_bl_user_at,
			p_tg_bl_user_handle,
			p_tg_chan_id,
			p_enabled
		);
	SELECT LAST_INSERT_ID() into @new_bl_id;
	RETURN @new_bl_id;
END 
$$ DELIMITER ;

DELIMITER $$
drop FUNCTION if exists usr_shill_limit_reached; -- setup
CREATE FUNCTION `usr_shill_limit_reached`(
    	p_tg_user_id VARCHAR(40))
		RETURNS INT(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
	-- NOTE_030724: current integration checks 3 posts per day max
	--	potential update: check for max pay_usd total per day 
	SET @max_shills_per_day = 3;
	SELECT id FROM users WHERE tg_user_id = p_tg_user_id INTO @v_user_id;
	SELECT COUNT(*) FROM shills 
		WHERE fk_user_id = @v_user_id
			AND is_approved = TRUE
			AND dt_updated_approve >= DATE_SUB(NOW(), INTERVAL 1 DAY) -- within the last day or 24 hours
			-- note: includes is_removed=TRUE|FALSE (limit earns to those removing shills)
		INTO @v_approve_cnt;
	RETURN @v_approve_cnt >= @max_shills_per_day;
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
