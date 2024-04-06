-- NOTE: this migration only works for migrating old data 
--  to a new table schemas with 'additional' columns only
-- NOTE: all queries only include the OG db schema columns
--  and then the 'source ./' file includes the updated db schema
-- *WARNING* -> make sure you backup the data before migrating


-- creat temp db w/ new updated schema structure
CREATE DATABASE the_matrix_2;
USE the_matrix_2;
source ./the_matrix_db_schema.sql;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.users (id, dt_created, dt_updated, dt_deleted, tg_user_id, tg_user_at, tg_user_handle, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id, dt_last_tw_conf, fk_last_shill_id, wallet_address, is_admin, is_admin_pay)
SELECT id, dt_created, dt_updated, dt_deleted, tg_user_id, tg_user_at, tg_user_handle, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id, dt_last_tw_conf, fk_last_shill_id, wallet_address, is_admin, is_admin_pay
FROM the_matrix.users;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.log_tg_user_at_changes (id, dt_created, dt_updated, dt_deleted, fk_user_id, tg_user_id_const, tg_user_at_prev, tg_user_at_new)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, tg_user_id_const, tg_user_at_prev, tg_user_at_new
FROM the_matrix.log_tg_user_at_changes;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.log_tw_conf_urls (id, dt_created, dt_updated, dt_deleted, fk_user_id, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id
FROM the_matrix.log_tw_conf_urls;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.user_earns (id, dt_created, dt_updated, dt_deleted, fk_user_id, usd_total, usd_owed, usd_paid, withdraw_requested)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, usd_total, usd_owed, usd_paid, withdraw_requested
FROM the_matrix.user_earns;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.shills (id, dt_created, dt_updated, dt_deleted, fk_user_id, post_url, post_id, post_uname, pay_usd, shill_plat, shill_type, is_approved, dt_updated_approve, is_paid, is_removed, dt_shill_removed, dt_tx_submit, dt_tx_status, pay_tx_submit, pay_tx_hash, pay_tok_addr, pay_tok_symb)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, post_url, post_id, post_uname, pay_usd, shill_plat, shill_type, is_approved, dt_updated_approve, is_paid, is_removed, dt_shill_removed, dt_tx_submit, dt_tx_status, pay_tx_submit, pay_tx_hash, pay_tok_addr, pay_tok_symb
FROM the_matrix.shills;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.user_shill_rates (id, dt_created, dt_updated, dt_deleted, fk_user_id, platform, type_descr, pay_usd)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, platform, type_descr, pay_usd
FROM the_matrix.user_shill_rates;

-- Copy Old table Data to the Temporary Table
INSERT INTO the_matrix_2.user_blacklist_scammers (id, dt_created, dt_updated, dt_deleted, fk_user_id_added, tg_user_id, tg_user_at, tg_user_handle, tg_chat_id_found, is_enabled)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id_added, tg_user_id, tg_user_at, tg_user_handle, tg_chat_id_found, is_enabled
FROM the_matrix.user_blacklist_scammers;

-- switch to use old databse & recreate it using updated schema
USE the_matrix;
source ./the_matrix_db_schema.sql;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.users (id, dt_created, dt_updated, dt_deleted, tg_user_id, tg_user_at, tg_user_handle, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id, dt_last_tw_conf, fk_last_shill_id, wallet_address, is_admin, is_admin_pay)
SELECT id, dt_created, dt_updated, dt_deleted, tg_user_id, tg_user_at, tg_user_handle, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id, dt_last_tw_conf, fk_last_shill_id, wallet_address, is_admin, is_admin_pay
FROM the_matrix_2.users;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.log_tg_user_at_changes (id, dt_created, dt_updated, dt_deleted, fk_user_id, tg_user_id_const, tg_user_at_prev, tg_user_at_new)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, tg_user_id_const, tg_user_at_prev, tg_user_at_new
FROM the_matrix_2.log_tg_user_at_changes;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.log_tw_conf_urls (id, dt_created, dt_updated, dt_deleted, fk_user_id, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, tw_user_at, tw_user_handle, tw_conf_url, tw_conf_id
FROM the_matrix_2.log_tw_conf_urls;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.user_earns (id, dt_created, dt_updated, dt_deleted, fk_user_id, usd_total, usd_owed, usd_paid, withdraw_requested)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, usd_total, usd_owed, usd_paid, withdraw_requested
FROM the_matrix_2.user_earns;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.shills (id, dt_created, dt_updated, dt_deleted, fk_user_id, post_url, post_id, post_uname, pay_usd, shill_plat, shill_type, is_approved, dt_updated_approve, is_paid, is_removed, dt_shill_removed, dt_tx_submit, dt_tx_status, pay_tx_submit, pay_tx_status, pay_tx_hash, pay_tok_addr, pay_tok_symb)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, post_url, post_id, post_uname, pay_usd, shill_plat, shill_type, is_approved, dt_updated_approve, is_paid, is_removed, dt_shill_removed, dt_tx_submit, dt_tx_status, pay_tx_submit, pay_tx_status, pay_tx_hash, pay_tok_addr, pay_tok_symb
FROM the_matrix_2.shills;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.user_shill_rates (id, dt_created, dt_updated, dt_deleted, fk_user_id, platform, type_descr, pay_usd)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id, platform, type_descr, pay_usd
FROM the_matrix_2.user_shill_rates;

-- Copy old table Data back into recreated table with new schema
INSERT INTO the_matrix.user_blacklist_scammers (id, dt_created, dt_updated, dt_deleted, fk_user_id_added, tg_user_id, tg_user_at, tg_user_handle, tg_chat_id_found, is_enabled)
SELECT id, dt_created, dt_updated, dt_deleted, fk_user_id_added, tg_user_id, tg_user_at, tg_user_handle, tg_chat_id_found, is_enabled
FROM the_matrix_2.user_blacklist_scammers;

-- drop temp database
DROP DATABASE the_matrix_2;