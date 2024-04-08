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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_tw_conf_urls`
--

LOCK TABLES `log_tw_conf_urls` WRITE;
/*!40000 ALTER TABLE `log_tw_conf_urls` DISABLE KEYS */;
INSERT INTO `log_tw_conf_urls` VALUES (2,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,'2','chucknorrisprc','','https://x.com/chucknorrisprc/status/1768392990609809777?s=20','1768392990609809777'),(4,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,'4','fricardooo','','https://x.com/fricardooo/status/1769660430861897989?s=20','1769660430861897989'),(6,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,'6','housing37','','https://x.com/housing37/status/1770550133387915683?s=20','1770550133387915683'),(7,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,'7','richardslongg','','https://twitter.com/richardslongg/status/1770916148755726654?s=19','1770916148755726654'),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,'9','FuckWorldCoin','','https://x.com/FuckWorldCoin/status/1770934680252031387?s=20','1770934680252031387'),(10,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,'10','TheSimonBurnett','','https://x.com/TheSimonBurnett/status/1775968345164001614?s=20','1775968345164001614'),(11,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,'11','cryptonomad6','','https://x.com/cryptonomad6/status/1776006518002868572?s=46','1776006518002868572'),(12,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,'12','midpointTO','','https://twitter.com/midpointTO/status/1775989944437064120?t=NrAJP03BDR5f07Aw03K20w&s=19','1775989944437064120'),(13,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,'13','Defi_SB','','https://x.com/Defi_SB/status/1776752662832411124?t=2__f-g2CVJW_nUeEqD-4PQ&s=35','1776752662832411124'),(14,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,'14','diamond_grip','','https://x.com/diamond_grip/status/1776779488476688875?s=46&t=pfYAtlj9U_iyDuit5cTn-g','1776779488476688875'),(15,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,'15','goran44840523','','https://x.com/goran44840523/status/1776865384588620198?s=46&t=RjSxNI4Z5ftQMT3Jj2CMHQ','1776865384588620198');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shills`
--

LOCK TABLES `shills` WRITE;
/*!40000 ALTER TABLE `shills` DISABLE KEYS */;
INSERT INTO `shills` VALUES (2,'2024-03-15 18:18:11','2024-03-15 18:19:33',NULL,2,'https://x.com/chucknorrisprc/status/1768702864132657632?s=20','1768702864132657632','chucknorrisprc',0.05,'twitter','long_txt',1,'2024-03-15 18:19:33',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(3,'2024-03-18 18:05:21','2024-03-18 18:28:02',NULL,4,'https://x.com/fricardooo/status/1769661736645247034?s=20','1769661736645247034','fricardooo',0.25,'twitter','img_meme',1,'2024-03-18 18:28:02',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(4,'2024-03-18 18:49:05','2024-03-21 03:48:13',NULL,2,'https://x.com/chucknorrisprc/status/1769796625117888698?s=20','1769796625117888698','chucknorrisprc',0.05,'twitter','long_txt',1,'2024-03-21 03:48:13',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(5,'2024-03-21 03:46:13','2024-03-21 03:46:13',NULL,6,'https://x.com/housing37/status/1770557256196591668?s=20','1770557256196591668','housing37',-1,'twitter','unknown',0,NULL,0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(6,'2024-04-04 22:41:21','2024-04-04 22:41:21',NULL,11,'https://x.com/cryptonomad6/status/1776015656539787276?s=46','1776015656539787276','cryptonomad6',-1,'twitter','unknown',0,NULL,0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(7,'2024-04-05 10:47:27','2024-04-07 03:41:50',NULL,11,'https://x.com/cryptonomad6/status/1776199815400935577?s=46','1776199815400935577','cryptonomad6',0.005,'twitter','htag',1,'2024-04-07 03:41:50',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(8,'2024-04-05 22:56:51','2024-04-07 03:41:44',NULL,11,'https://x.com/cryptonomad6/status/1776161195587670169?s=46','1776161195587670169','cryptonomad6',0.005,'twitter','htag',1,'2024-04-07 03:41:44',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(9,'2024-04-06 23:52:36','2024-04-06 23:56:44',NULL,13,'https://x.com/Defi_SB/status/1776759830184898908?t=11wWyjdt-8cNY9PHJiu2UQ&s=35','1776759830184898908','Defi_SB',0.01,'twitter','short_txt',1,'2024-04-06 23:56:44',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(10,'2024-04-07 00:10:25','2024-04-07 01:32:43',NULL,11,'https://x.com/cryptonomad6/status/1776764263253631086?s=46','1776764263253631086','cryptonomad6',0.05,'twitter','long_txt',1,'2024-04-07 01:32:43',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(11,'2024-04-07 01:57:04','2024-04-07 01:57:04',NULL,14,'https://x.com/Diamond_Grip/status/1776787426138280440?s=20','1776787426138280440','Diamond_Grip',-1,'twitter','unknown',0,NULL,0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(12,'2024-04-07 02:02:08','2024-04-07 03:42:58',NULL,14,'https://twitter.com/Diamond_Grip/status/1776792338721112254?s=20','1776792338721112254','Diamond_Grip',0.05,'twitter','long_txt',1,'2024-04-07 03:42:58',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(13,'2024-04-07 03:26:09','2024-04-07 03:39:23',NULL,14,'https://twitter.com/Diamond_Grip/status/1776813429141172485?s=20','1776813429141172485','Diamond_Grip',0.25,'twitter','img_meme',1,'2024-04-07 03:39:23',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(14,'2024-04-07 03:38:09','2024-04-07 03:40:07',NULL,14,'https://twitter.com/Diamond_Grip/status/1776814645606830229?s=20','1776814645606830229','Diamond_Grip',0.25,'twitter','img_meme',1,'2024-04-07 03:40:07',0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1),(15,'2024-04-07 04:15:22','2024-04-07 04:15:22',NULL,13,'https://x.com/Defi_SB/status/1776825932080427475?t=xhNTrMNhvJFMD_DOIqQhnQ&s=35','1776825932080427475','Defi_SB',-1,'twitter','unknown',0,NULL,0,0,NULL,NULL,NULL,0,'nil','0x0','0x0','nil_tok_symb',-1);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_earns`
--

LOCK TABLES `user_earns` WRITE;
/*!40000 ALTER TABLE `user_earns` DISABLE KEYS */;
INSERT INTO `user_earns` VALUES (1,'2024-03-14 20:47:32','2024-03-14 21:13:34',NULL,1,0.5,0.5,0,0),(2,'2024-03-14 21:45:54','2024-03-21 03:48:13',NULL,2,0.1,0.1,0,0),(3,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,0,0,0,0),(4,'2024-03-18 18:05:06','2024-03-18 18:28:02',NULL,4,0.25,0.25,0,0),(5,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,0,0,0,0),(6,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,0,0,0,0),(7,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,0,0,0,0),(8,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,0,0,0,0),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,0,0,0,0),(10,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,0,0,0,0),(11,'2024-04-04 22:00:03','2024-04-07 03:41:50',NULL,11,0.06,0.06,0,0),(12,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,0,0,0,0),(13,'2024-04-06 23:24:08','2024-04-06 23:56:44',NULL,13,0.01,0.01,0,0),(14,'2024-04-07 01:10:48','2024-04-07 03:42:58',NULL,14,0.55,0.55,0,0),(15,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,0,0,0,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_shill_rates`
--

LOCK TABLES `user_shill_rates` WRITE;
/*!40000 ALTER TABLE `user_shill_rates` DISABLE KEYS */;
INSERT INTO `user_shill_rates` VALUES (1,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','htag',0.005),(2,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','short_txt',0.01),(3,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','long_txt',0.05),(4,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','img_meme',0.25),(5,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','short_vid',0.5),(6,'2024-03-14 20:47:32','2024-03-14 20:47:32',NULL,1,'twitter','long_vid',1),(7,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','htag',0.005),(8,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','short_txt',0.01),(9,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','long_txt',0.05),(10,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','img_meme',0.25),(11,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','short_vid',0.5),(12,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,2,'twitter','long_vid',1),(13,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','htag',0.005),(14,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','short_txt',0.01),(15,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','long_txt',0.05),(16,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','img_meme',0.25),(17,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','short_vid',0.5),(18,'2024-03-17 21:51:13','2024-03-17 21:51:13',NULL,3,'twitter','long_vid',1),(19,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','htag',0.005),(20,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','short_txt',0.01),(21,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','long_txt',0.05),(22,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','img_meme',0.25),(23,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','short_vid',0.5),(24,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,4,'twitter','long_vid',1),(25,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','htag',0.005),(26,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','short_txt',0.01),(27,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','long_txt',0.05),(28,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','img_meme',0.25),(29,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','short_vid',0.5),(30,'2024-03-20 00:59:29','2024-03-20 00:59:29',NULL,5,'twitter','long_vid',1),(31,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','htag',0.005),(32,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','short_txt',0.01),(33,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','long_txt',0.05),(34,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','img_meme',0.25),(35,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','short_vid',0.5),(36,'2024-03-21 03:45:02','2024-03-21 03:45:02',NULL,6,'twitter','long_vid',1),(37,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','htag',0.005),(38,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','short_txt',0.01),(39,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','long_txt',0.05),(40,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','img_meme',0.25),(41,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','short_vid',0.5),(42,'2024-03-21 20:52:40','2024-03-21 20:52:40',NULL,7,'twitter','long_vid',1),(43,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','htag',0.005),(44,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','short_txt',0.01),(45,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','long_txt',0.05),(46,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','img_meme',0.25),(47,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','short_vid',0.5),(48,'2024-03-21 21:43:35','2024-03-21 21:43:35',NULL,8,'twitter','long_vid',1),(49,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','htag',0.005),(50,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','short_txt',0.01),(51,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','long_txt',0.05),(52,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','img_meme',0.25),(53,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','short_vid',0.5),(54,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,9,'twitter','long_vid',1),(55,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','htag',0.005),(56,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','short_txt',0.01),(57,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','long_txt',0.05),(58,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','img_meme',0.25),(59,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','short_vid',0.5),(60,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,10,'twitter','long_vid',1),(61,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','htag',0.005),(62,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','short_txt',0.01),(63,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','long_txt',0.05),(64,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','img_meme',0.25),(65,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','short_vid',0.5),(66,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,11,'twitter','long_vid',1),(67,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','htag',0.005),(68,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','short_txt',0.01),(69,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','long_txt',0.05),(70,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','img_meme',0.25),(71,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','short_vid',0.5),(72,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,12,'twitter','long_vid',1),(73,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','htag',0.005),(74,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','short_txt',0.01),(75,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','long_txt',0.05),(76,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','img_meme',0.25),(77,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','short_vid',0.5),(78,'2024-04-06 23:24:08','2024-04-06 23:24:08',NULL,13,'twitter','long_vid',1),(79,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','htag',0.005),(80,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','short_txt',0.01),(81,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','long_txt',0.05),(82,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','img_meme',0.25),(83,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','short_vid',0.5),(84,'2024-04-07 01:10:48','2024-04-07 01:10:48',NULL,14,'twitter','long_vid',1),(85,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','htag',0.005),(86,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','short_txt',0.01),(87,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','long_txt',0.05),(88,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','img_meme',0.25),(89,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','short_vid',0.5),(90,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,15,'twitter','long_vid',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'2024-03-14 21:45:54','2024-03-14 21:45:54',NULL,'1770298859','tir_fly','Tir','chucknorrisprc','','https://x.com/chucknorrisprc/status/1768392990609809777?s=20','1768392990609809777','2024-03-14 21:45:54',-1,'0xCF7251372b0c023e7BF46427c55D6B40E356510d',0,0),(4,'2024-03-18 18:05:06','2024-03-18 18:05:06',NULL,'6919802491','fricardooo','nil_handle_disabled','fricardooo','','https://x.com/fricardooo/status/1769660430861897989?s=20','1769660430861897989','2024-03-18 18:05:06',-1,'0x8F1F9653C056b41dF1Ca4d521Fd1d16Ff8A8A00d',0,0),(6,'2024-03-21 03:45:02','2024-03-21 19:39:56',NULL,'581475171','housing37','nil_handle_disabled','housing37','','https://x.com/housing37/status/1770550133387915683?s=20','1770550133387915683','2024-03-21 03:45:02',-1,'0x037',1,0),(7,'2024-03-21 20:52:40','2024-03-21 20:58:40',NULL,'1693021537','LukeDuke5555','nil_disabled','richardslongg','','https://twitter.com/richardslongg/status/1770916148755726654?s=19','1770916148755726654','2024-03-21 20:52:40',-1,'0x488B3Ae9B55bac6622D6cB60871e97979F404DC9',0,0),(9,'2024-03-21 22:05:34','2024-03-21 22:05:34',NULL,'1019220630','WhiteRabbit0x0','nil_disabled','FuckWorldCoin','','https://x.com/FuckWorldCoin/status/1770934680252031387?s=20','1770934680252031387','2024-03-21 22:05:34',-1,'0x0',0,0),(10,'2024-04-04 19:27:31','2024-04-04 19:27:31',NULL,'5138838422','psi931','nil_disabled','TheSimonBurnett','','https://x.com/TheSimonBurnett/status/1775968345164001614?s=20','1775968345164001614','2024-04-04 19:27:31',-1,'0x0',0,0),(11,'2024-04-04 22:00:03','2024-04-04 22:00:03',NULL,'1255644269','jay_555','nil_disabled','cryptonomad6','','https://x.com/cryptonomad6/status/1776006518002868572?s=46','1776006518002868572','2024-04-04 22:00:03',-1,'0x0',0,0),(12,'2024-04-04 22:13:32','2024-04-04 22:13:32',NULL,'6900972647','AlbertoBundy','nil_disabled','midpointTO','','https://twitter.com/midpointTO/status/1775989944437064120?t=NrAJP03BDR5f07Aw03K20w&s=19','1775989944437064120','2024-04-04 22:13:32',-1,'0x0',0,0),(13,'2024-04-06 23:24:08','2024-04-07 01:43:04',NULL,'2102645538','sb_defi','nil_disabled','Defi_SB','','https://x.com/Defi_SB/status/1776752662832411124?t=2__f-g2CVJW_nUeEqD-4PQ&s=35','1776752662832411124','2024-04-06 23:24:08',-1,'0xEtc',0,0),(14,'2024-04-07 01:10:48','2024-04-07 01:16:04',NULL,'1924983670','InfinityIntruder','nil_disabled','diamond_grip','','https://x.com/diamond_grip/status/1776779488476688875?s=46&t=pfYAtlj9U_iyDuit5cTn-g','1776779488476688875','2024-04-07 01:10:48',-1,'<0x4DB77F9331E1a4A8837369e255E7f435a4024A79>',0,0),(15,'2024-04-07 06:52:31','2024-04-07 06:52:31',NULL,'1680936626','None','nil_disabled','goran44840523','','https://x.com/goran44840523/status/1776865384588620198?s=46&t=RjSxNI4Z5ftQMT3Jj2CMHQ','1776865384588620198','2024-04-07 06:52:31',-1,'0x0',0,0);
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

-- Dump completed on 2024-04-07  6:58:44
