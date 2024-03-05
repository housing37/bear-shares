#===============================================#
# init database 'trinity'
#===============================================#

#===============================================#
# clean
#===============================================#
-- call DeleteAll_IF_EXISTS('client_shops', 'password37', @result);

#===============================================#
# create tables
#===============================================#
drop table if exists users;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `tg_user_id` varchar(40) NOT NULL, -- ex: -10493048
  `tg_user_at` varchar(1024) default '', -- ex: @whatever
  `tg_user_handle` varchar(1024) default '', -- ex: bob joe
  `tw_user_at` varchar(1024) default '',
  `tw_user_handle` varchar(1024) default '',
  `tw_conf_url` varchar(1024) default '',
  `dt_last_tw_conf` timestamp NULL DEFAULT NULL,
  `fk_last_shill_id` int(11) default -1, -- for rate-limit
  `is_admin` BOOLEAN DEFAULT FALSE, -- admin required for some stored procs

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists user_earns;
CREATE TABLE `user_earns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `user_total` float NOT NULL DEFAULT 0.0,
  `user_owed` float NOT NULL DEFAULT 0.0,
  `user_paid` float NOT NULL DEFAULT 0.0,
  `withdraw_requested` BOOLEAN DEFAULT FALSE,

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists shill_types;
CREATE TABLE `shill_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `post_loc` varchar(40) DEFAULT 'nil_loc', -- (Twitter, tiktok, Reddit)
  `descr` varchar(40), -- (simple hastag, simple text, full text, meme, video)

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

drop table if exists user_shill_rates;
CREATE TABLE `user_shill_rates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `fk_shill_type_id` int(11) NOT NULL,
  `pay_usd` float default 0.0 -- (0.01, 0.05, 0.50, 1.0)

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


drop table if exists shills;
CREATE TABLE `shills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_shill_type_id` int(11) NOT NULL,
  `fk_shill_rate_id` int(11) NOT NULL,
  `pay_usd` float default 0.0 -- (0.01, 0.05, 0.50, 1.0)
  `post_url` varchar(1024) default '',
  `is_approved` BOOLEAN DEFAULT FALSE,
  `is_paid` BOOLEAN DEFAULT FALSE,
  `is_removed` BOOLEAN DEFAULT FALSE,
  `dt_shill_removed` timestamp NULL DEFAULT NULL,

  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



#===============================================#
#===============================================#
