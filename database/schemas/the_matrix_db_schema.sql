#===============================================#
# init database 'trinity'
#===============================================#

#===============================================#
# clean
#===============================================#
-- call DeleteAll_IF_EXISTS('client_shops', 'password37', @result);

-- -- 0=unknown, 1=twitter, 2=tiktok, 3=reddit
-- select add_shill_plat('unknown');
-- select add_shill_plat('twitter');
-- select add_shill_plat('tiktok');
-- select add_shill_plat('reddit');

-- -- 0=unknown, 1=hastag, 2=short_text, 3=long_ext, 4=meme, 5=short_video, 6=long_video
-- select add_shill_type('unknown');
-- select add_shill_type('hashtag');
-- select add_shill_type('short_text');
-- select add_shill_type('long_text');
-- select add_shill_type('image_meme');
-- select add_shill_type('short_video');
-- select add_shill_type('long_video');

#===============================================#
# create tables
#===============================================#
drop table if exists users;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `tg_user_id` varchar(40) NOT NULL, -- ex: '581475171'
  `tg_user_at` varchar(1024) default 'nil_at', -- ex: '@whatever'
  `tg_user_handle` varchar(1024) default 'nil_handle', -- ex: 'bob joe'
  `tw_user_at` varchar(1024) default '',
  `tw_user_handle` varchar(1024) default '',
  `tw_conf_url` varchar(1024) default '',
  `dt_last_tw_conf` timestamp NULL DEFAULT NULL,
  `fk_last_shill_id` int(11) default -1, -- for rate-limit
  `wallet_address` varchar(255) default '0x0',
  `is_admin` BOOLEAN DEFAULT FALSE, -- admin required for some stored procs
  `is_admin_pay` BOOLEAN DEFAULT FALSE, -- admin_pay required for some stored procs

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists user_earns;
CREATE TABLE `user_earns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `usd_total` float NOT NULL DEFAULT 0.0,
  `usd_owed` float NOT NULL DEFAULT 0.0,
  `usd_paid` float NOT NULL DEFAULT 0.0,
  `withdraw_requested` BOOLEAN DEFAULT FALSE,

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists shills;
CREATE TABLE `shills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `post_url` varchar(1024) NOT NULL,
  -- `fk_shill_plat_id` int(11) NOT NULL,
  -- `fk_shill_type_id` int(11) DEFAULT -1, -- set by admin
  -- `fk_shill_rate_id` int(11) NOT NULL, -- latest fk_user_id rate: platform, type, & pay_usd
  `pay_usd` FLOAT DEFAULT -1.0, -- set by admin after review
  `shill_plat` VARCHAR(40) DEFAULT 'unknown', -- set by admin after post_url review
  `shill_type` VARCHAR(40) DEFAULT 'unknown', -- set by admin after post_url review
  `is_approved` BOOLEAN DEFAULT FALSE,
  `dt_updated_approve` timestamp NULL DEFAULT NULL,
  `is_paid` BOOLEAN DEFAULT FALSE,
  `is_removed` BOOLEAN DEFAULT FALSE,
  `dt_shill_removed` timestamp NULL DEFAULT NULL,
  `dt_tx_submit` timestamp NULL DEFAULT NULL,
  `dt_tx_status` timestamp NULL DEFAULT NULL,
  `pay_tx_submit` BOOLEAN DEFAULT FALSE,
  `pay_tx_status` VARCHAR(40) DEFAULT 'nil', -- const: baseFee, pending, queued
  `pay_tx_hash` VARCHAR(255) DEFAULT '0x0', 
  `pay_tok_addr` VARCHAR(255) DEFAULT '0x0',
  `pay_tok_symb` VARCHAR(40) DEFAULT 'nil_tok_symb',
  `pay_tok_amnt` FLOAT DEFAULT -1.0,

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists user_shill_rates;
CREATE TABLE `user_shill_rates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `platform` VARCHAR(40) NOT NULL, -- const: unknown, twitter, tiktok, reddit
  `type_descr` VARCHAR(40) NOT NULL, -- const: unknown, htag, short_txt, long_txt, img_meme, short_vid, long_vid
  `pay_usd` float default 0.0, -- dyn: 0.005, 0.01, 0.05, 0.25 0.50, 1.00, etc.

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists user_blacklist_scammers;
CREATE TABLE `user_blacklist_scammers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id_added` int(11) NOT NULL,
  `tg_user_id` varchar(40) NOT NULL, -- ex: '581475171'
  `tg_user_at` varchar(1024) default 'nil_at', -- ex: '@whatever'
  `tg_user_handle` varchar(1024) default 'nil_handle', -- ex: 'bob joe'
  `tg_chat_id_found` varchar(40) NOT NULL, -- ex: '-10493048'
  `is_enabled` BOOLEAN DEFAULT FALSE,

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- #====================================================# --
--    'user_shill_rates' ALTERNATE INTEGRATION            --
-- #====================================================# --
-- drop table if exists user_shill_rates;
-- CREATE TABLE `user_shill_rates` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_deleted` timestamp NULL DEFAULT NULL,
--   `fk_user_id` int(11) NOT NULL,
--   `fk_shill_plat_id` int(11) NOT NULL, -- 0=unknown, 1=twitter, 2=tiktok, 3=reddit
--   `fk_shill_type_id` int(11) NOT NULL, -- 0=unknown, 1=hastag, 2=short_txt, 3=long_txt, 4=img_meme, 5=short_vid, 6=long_vid
--   `pay_usd` float default 0.0 -- (0.01, 0.05, 0.50, 1.0)

--   UNIQUE KEY `ID` (`id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- drop table if exists valid_shill_plats; -- platforms
-- CREATE TABLE `valid_shill_plats` (
--   `id` int(11) NOT NULL AUTO_INCREMENT, -- 0=unknown, 1=twitter, 2=tiktok, 3=reddit
--   `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_deleted` timestamp NULL DEFAULT NULL,
--   `platform` varchar(40) DEFAULT 'nil_loc', -- 0=unknown, 1=twitter, 2=tiktok, 3=reddit

--   UNIQUE KEY `ID` (`id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- drop table if exists valid_shill_types;
-- CREATE TABLE `valid_shill_types` (
--   `id` int(11) NOT NULL AUTO_INCREMENT, -- 0, 1, 2, 3, 4, 5, 6=long_video
--   `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   `dt_deleted` timestamp NULL DEFAULT NULL,
--   `descr` varchar(40), -- 0=unknown, 1=hastag, 2=short_text, 3=long_ext, 4=meme, 5=short_video, 6=long_video

--   UNIQUE KEY `ID` (`id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


#===============================================#
#===============================================#
