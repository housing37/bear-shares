-- MariaDB dump 10.19  Distrib 10.6.16-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: the_matrix
-- ------------------------------------------------------
-- Server version	10.6.16-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `the_matrix`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `the_matrix` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `the_matrix`;

--
-- Table structure for table `log_tg_user_at_changes`
--

DROP TABLE IF EXISTS `log_tg_user_at_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_tg_user_at_changes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` varchar(40) NOT NULL,
  `tg_user_id_const` varchar(40) NOT NULL,
  `tg_user_at_prev` varchar(40) NOT NULL,
  `tg_user_at_new` varchar(40) NOT NULL,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tg_user_at_changes`
--

LOCK TABLES `log_tg_user_at_changes` WRITE;
/*!40000 ALTER TABLE `log_tg_user_at_changes` DISABLE KEYS */;
/*!40000 ALTER TABLE `log_tg_user_at_changes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_tw_conf_urls`
--

DROP TABLE IF EXISTS `log_tw_conf_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_tw_conf_urls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` varchar(40) NOT NULL,
  `tw_user_at` varchar(1024) DEFAULT '',
  `tw_user_handle` varchar(1024) DEFAULT '',
  `tw_conf_url` varchar(1024) DEFAULT '',
  `tw_conf_id` varchar(40) DEFAULT '',
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tw_conf_urls`
--

LOCK TABLES `log_tw_conf_urls` WRITE;
/*!40000 ALTER TABLE `log_tw_conf_urls` DISABLE KEYS */;
INSERT INTO `log_tw_conf_urls` VALUES (2,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,'2','chucknorrisprc','','https://x.com/chucknorrisprc/status/1768392990609809777?s=20','1768392990609809777'),(4,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,'4','fricardooo','','https://x.com/fricardooo/status/1769660430861897989?s=20','1769660430861897989'),(6,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,'6','housing37','','https://x.com/housing37/status/1770550133387915683?s=20','1770550133387915683'),(7,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,'7','richardslongg','','https://twitter.com/richardslongg/status/1770916148755726654?s=19','1770916148755726654'),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,'9','FuckWorldCoin','','https://x.com/FuckWorldCoin/status/1770934680252031387?s=20','1770934680252031387');
/*!40000 ALTER TABLE `log_tw_conf_urls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shills`
--

DROP TABLE IF EXISTS `shills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `post_url` varchar(1024) NOT NULL,
  `post_id` varchar(1024) DEFAULT '<nil_post_id>',
  `post_uname` varchar(255) DEFAULT '<nil_post_uname>',
  `pay_usd` float DEFAULT -1,
  `shill_plat` varchar(40) DEFAULT 'unknown',
  `shill_type` varchar(40) DEFAULT 'unknown',
  `is_approved` tinyint(1) DEFAULT 0,
  `dt_updated_approve` timestamp NULL DEFAULT NULL,
  `is_paid` tinyint(1) DEFAULT 0,
  `is_removed` tinyint(1) DEFAULT 0,
  `dt_shill_removed` timestamp NULL DEFAULT NULL,
  `dt_tx_submit` timestamp NULL DEFAULT NULL,
  `dt_tx_status` timestamp NULL DEFAULT NULL,
  `pay_tx_submit` tinyint(1) DEFAULT 0,
  `pay_tx_status` varchar(40) DEFAULT 'nil',
  `pay_tx_hash` varchar(255) DEFAULT '0x0',
  `pay_tok_addr` varchar(255) DEFAULT '0x0',
  `pay_tok_symb` varchar(40) DEFAULT 'nil_tok_symb',
  `pay_tok_amnt` float DEFAULT -1,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shills`
--

LOCK TABLES `shills` WRITE;
/*!40000 ALTER TABLE `shills` DISABLE KEYS */;
INSERT INTO `shills` VALUES (2,'2024-03-15 18:18:11','2024-03-15 18:19:33',NULL,2,'https://x.com/chucknorrisprc/status/1768702864132657632?s=20','1768702864132657632','chucknorrisprc',0.05,'twitter','long_txt',1,'2024-03-15 18:19:33',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(3,'2024-03-18 18:05:21','2024-03-18 18:28:02',NULL,4,'https://x.com/fricardooo/status/1769661736645247034?s=20','1769661736645247034','fricardooo',0.25,'twitter','img_meme',1,'2024-03-18 18:28:02',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(4,'2024-03-18 18:49:05','2024-03-21 03:48:13',NULL,2,'https://x.com/chucknorrisprc/status/1769796625117888698?s=20','1769796625117888698','chucknorrisprc',0.05,'twitter','long_txt',1,'2024-03-21 03:48:13',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(5,'2024-03-21 03:46:13','2024-03-21 03:46:13',NULL,6,'https://x.com/housing37/status/1770557256196591668?s=20','1770557256196591668','housing37',-1,'twitter','unknown',0,NULL,0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1);
/*!40000 ALTER TABLE `shills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_blacklist_scammers`
--

DROP TABLE IF EXISTS `user_blacklist_scammers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_blacklist_scammers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id_added` int(11) NOT NULL,
  `tg_user_id` varchar(40) NOT NULL,
  `tg_user_at` varchar(1024) DEFAULT 'nil_at',
  `tg_user_handle` varchar(1024) DEFAULT 'nil_handle',
  `tg_chat_id_found` varchar(40) NOT NULL,
  `is_enabled` tinyint(1) DEFAULT 0,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_blacklist_scammers`
--

LOCK TABLES `user_blacklist_scammers` WRITE;
/*!40000 ALTER TABLE `user_blacklist_scammers` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_blacklist_scammers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_earns`
--

DROP TABLE IF EXISTS `user_earns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_earns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `usd_total` float NOT NULL DEFAULT 0,
  `usd_owed` float NOT NULL DEFAULT 0,
  `usd_paid` float NOT NULL DEFAULT 0,
  `withdraw_requested` tinyint(1) DEFAULT 0,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_earns`
--

LOCK TABLES `user_earns` WRITE;
/*!40000 ALTER TABLE `user_earns` DISABLE KEYS */;
INSERT INTO `user_earns` VALUES (1,'2024-03-14 20:47:32','2024-03-14 21:13:34',NULL,1,0.5,0.5,0,0),(2,'2024-03-14 21:45:54','2024-03-21 03:48:13',NULL,2,0.1,0.1,0,0),(3,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,0,0,0,0),(4,'2024-03-18 18:05:06','2024-03-18 18:28:02',NULL,4,0.25,0.25,0,0),(5,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,0,0,0,0),(6,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,0,0,0,0),(7,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,0,0,0,0),(8,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,0,0,0,0),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,0,0,0,0);
/*!40000 ALTER TABLE `user_earns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_shill_rates`
--

DROP TABLE IF EXISTS `user_shill_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_shill_rates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `fk_user_id` int(11) NOT NULL,
  `platform` varchar(40) NOT NULL,
  `type_descr` varchar(40) NOT NULL,
  `pay_usd` float DEFAULT 0,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_shill_rates`
--

LOCK TABLES `user_shill_rates` WRITE;
/*!40000 ALTER TABLE `user_shill_rates` DISABLE KEYS */;
INSERT INTO `user_shill_rates` VALUES (1,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','htag',0.005),(2,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','short_txt',0.01),(3,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','long_txt',0.05),(4,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','img_meme',0.25),(5,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','short_vid',0.5),(6,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','long_vid',1),(7,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','htag',0.005),(8,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','short_txt',0.01),(9,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','long_txt',0.05),(10,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','img_meme',0.25),(11,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','short_vid',0.5),(12,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','long_vid',1),(13,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','htag',0.005),(14,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','short_txt',0.01),(15,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','long_txt',0.05),(16,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','img_meme',0.25),(17,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','short_vid',0.5),(18,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','long_vid',1),(19,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','htag',0.005),(20,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','short_txt',0.01),(21,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','long_txt',0.05),(22,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','img_meme',0.25),(23,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','short_vid',0.5),(24,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','long_vid',1),(25,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','htag',0.005),(26,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','short_txt',0.01),(27,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','long_txt',0.05),(28,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','img_meme',0.25),(29,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','short_vid',0.5),(30,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','long_vid',1),(31,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','htag',0.005),(32,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','short_txt',0.01),(33,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','long_txt',0.05),(34,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','img_meme',0.25),(35,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','short_vid',0.5),(36,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','long_vid',1),(37,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','htag',0.005),(38,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','short_txt',0.01),(39,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','long_txt',0.05),(40,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','img_meme',0.25),(41,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','short_vid',0.5),(42,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','long_vid',1),(43,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','htag',0.005),(44,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','short_txt',0.01),(45,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','long_txt',0.05),(46,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','img_meme',0.25),(47,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','short_vid',0.5),(48,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','long_vid',1),(49,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','htag',0.005),(50,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','short_txt',0.01),(51,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','long_txt',0.05),(52,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','img_meme',0.25),(53,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','short_vid',0.5),(54,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','long_vid',1);
/*!40000 ALTER TABLE `user_shill_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_updated` timestamp NOT NULL DEFAULT current_timestamp(),
  `dt_deleted` timestamp NULL DEFAULT NULL,
  `tg_user_id` varchar(40) NOT NULL,
  `tg_user_at` varchar(1024) DEFAULT 'nil_at',
  `tg_user_handle` varchar(1024) DEFAULT 'nil_handle',
  `tw_user_at` varchar(255) DEFAULT '',
  `tw_user_handle` varchar(1024) DEFAULT '',
  `tw_conf_url` varchar(1024) DEFAULT '',
  `tw_conf_id` varchar(40) DEFAULT '',
  `dt_last_tw_conf` timestamp NULL DEFAULT NULL,
  `fk_last_shill_id` int(11) DEFAULT -1,
  `wallet_address` varchar(255) DEFAULT '0x0',
  `is_admin` tinyint(1) DEFAULT 0,
  `is_admin_pay` tinyint(1) DEFAULT 0,
  UNIQUE KEY `ID` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,'1770298859','tir_fly','Tir','chucknorrisprc','','https://x.com/chucknorrisprc/status/1768392990609809777?s=20','1768392990609809777','2024-03-14 21:45:54',-1,'0xCF7251372b0c023e7BF46427c55D6B40E356510d',0,0),(4,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,'6919802491','fricardooo','nil_handle_disabled','fricardooo','','https://x.com/fricardooo/status/1769660430861897989?s=20','1769660430861897989','2024-03-18 18:05:06',-1,'0x8F1F9653C056b41dF1Ca4d521Fd1d16Ff8A8A00d',0,0),(6,'2024-03-21 03:45:02','2024-03-21 19:39:56',NULL,'581475171','housing37','nil_handle_disabled','housing37','','https://x.com/housing37/status/1770550133387915683?s=20','1770550133387915683','2024-03-21 03:45:02',-1,'0x037',1,0),(7,'2024-03-21 20:52:40','2024-03-21 20:58:40',NULL,'1693021537','LukeDuke5555','nil_disabled','richardslongg','','https://twitter.com/richardslongg/status/1770916148755726654?s=19','1770916148755726654','2024-03-21 20:52:40',-1,'0x488B3Ae9B55bac6622D6cB60871e97979F404DC9',0,0),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,'1019220630','WhiteRabbit0x0','nil_disabled','FuckWorldCoin','','https://x.com/FuckWorldCoin/status/1770934680252031387?s=20','1770934680252031387','2024-03-21 22:05:34',-1,'0x0',0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-03  7:03:37
