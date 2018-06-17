-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.7-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for tw
DROP DATABASE IF EXISTS `tw`;
CREATE DATABASE IF NOT EXISTS `tw` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tw`;

-- Dumping structure for table tw.feedback
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
  `feedback_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `transaction_id` int(20) unsigned NOT NULL,
  `user_id` int(20) unsigned NOT NULL,
  `rating` int(20) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` varchar(8192) NOT NULL,
  PRIMARY KEY (`feedback_id`),
  KEY `FK_feedback_user` (`user_id`),
  KEY `FK_feedback_transaction` (`transaction_id`),
  CONSTRAINT `FK_feedback_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`transaction_id`),
  CONSTRAINT `FK_feedback_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.images
DROP TABLE IF EXISTS `images`;
CREATE TABLE IF NOT EXISTS `images` (
  `image_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `product_data_id` int(20) unsigned NOT NULL,
  `image` mediumtext DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `FK_images_productdata` (`product_data_id`),
  CONSTRAINT `FK_images_productdata` FOREIGN KEY (`product_data_id`) REFERENCES `productdata` (`product_data_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.notice
DROP TABLE IF EXISTS `notice`;
CREATE TABLE IF NOT EXISTS `notice` (
  `notice_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `for_user_id` int(20) unsigned NOT NULL,
  `from_user_id` int(20) unsigned NOT NULL,
  `count` int(20) unsigned NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` varchar(9192) NOT NULL,
  PRIMARY KEY (`notice_id`),
  KEY `FK_notice_user` (`for_user_id`),
  KEY `FK_notice_user_2` (`from_user_id`),
  CONSTRAINT `FK_notice_user` FOREIGN KEY (`for_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `FK_notice_user_2` FOREIGN KEY (`from_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.productdata
DROP TABLE IF EXISTS `productdata`;
CREATE TABLE IF NOT EXISTS `productdata` (
  `product_data_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(20) unsigned NOT NULL,
  `title` varchar(512) DEFAULT NULL,
  `description` varchar(9192) DEFAULT NULL,
  `conditie` int(11) DEFAULT NULL,
  `country` varchar(64) DEFAULT NULL,
  `state` varchar(128) DEFAULT NULL,
  `city` varchar(64) DEFAULT NULL,
  `is_auction` bit(1) DEFAULT NULL,
  `price` int(20) unsigned DEFAULT NULL,
  `currency` varchar(50) DEFAULT NULL,
  `shipping_type` varchar(128) DEFAULT NULL,
  `shipping_price` int(20) unsigned DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `date_expires` datetime DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `subcategory` varchar(50) DEFAULT NULL,
  `views` int(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`product_data_id`),
  KEY `FK_productdata_user` (`user_id`),
  FULLTEXT KEY `title_description_category_subcategory` (`title`,`description`,`category`,`subcategory`),
  CONSTRAINT `FK_productdata_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.question
DROP TABLE IF EXISTS `question`;
CREATE TABLE IF NOT EXISTS `question` (
  `question_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(20) unsigned NOT NULL,
  `user_id` int(20) unsigned NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` varchar(9192) NOT NULL,
  PRIMARY KEY (`question_id`),
  KEY `FK_question_user` (`user_id`),
  KEY `FK_question_product` (`product_id`),
  CONSTRAINT `FK_question_product` FOREIGN KEY (`product_id`) REFERENCES `productdata` (`product_data_id`),
  CONSTRAINT `FK_question_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.report
DROP TABLE IF EXISTS `report`;
CREATE TABLE IF NOT EXISTS `report` (
  `report_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `from_uid` int(20) unsigned NOT NULL,
  `to_uid` int(20) unsigned NOT NULL,
  `product_id` int(20) unsigned NOT NULL,
  `reason` int(20) unsigned NOT NULL,
  `details` varchar(1024) NOT NULL,
  `resolved` bit(1) NOT NULL DEFAULT b'0',
  `date_resolved` datetime NOT NULL,
  `is_valid` bit(1) NOT NULL,
  PRIMARY KEY (`report_id`),
  KEY `FK_report_user` (`from_uid`),
  KEY `FK_report_user_2` (`to_uid`),
  KEY `FK_report_product` (`product_id`),
  CONSTRAINT `FK_report_product` FOREIGN KEY (`product_id`) REFERENCES `productdata` (`product_data_id`),
  CONSTRAINT `FK_report_user` FOREIGN KEY (`from_uid`) REFERENCES `user` (`user_id`),
  CONSTRAINT `FK_report_user_2` FOREIGN KEY (`to_uid`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.response
DROP TABLE IF EXISTS `response`;
CREATE TABLE IF NOT EXISTS `response` (
  `response_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(20) unsigned NOT NULL,
  `user_id` int(20) unsigned NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` varchar(9192) NOT NULL,
  PRIMARY KEY (`response_id`),
  KEY `FK_response_user` (`user_id`),
  KEY `FK_response_product` (`product_id`),
  CONSTRAINT `FK_response_product` FOREIGN KEY (`product_id`) REFERENCES `productdata` (`product_data_id`),
  CONSTRAINT `FK_response_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.sessions
DROP TABLE IF EXISTS `sessions`;
CREATE TABLE IF NOT EXISTS `sessions` (
  `session_key` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` varchar(60) NOT NULL,
  `user_id` int(20) unsigned DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `last_connected` datetime DEFAULT NULL,
  `device` varchar(256) DEFAULT NULL,
  `ip` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`session_key`),
  KEY `FK_sessions_user` (`user_id`),
  CONSTRAINT `FK_sessions_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.testare
DROP TABLE IF EXISTS `testare`;
CREATE TABLE IF NOT EXISTS `testare` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ceva` int(11) NOT NULL DEFAULT 0,
  `ceva2` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.transaction
DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `transaction_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `seller_user_id` int(20) unsigned NOT NULL,
  `buyer_user_id` int(20) unsigned NOT NULL,
  `product_id` int(20) unsigned NOT NULL,
  `has_ended` varchar(50) NOT NULL,
  `date_initiated` datetime NOT NULL,
  `date_ended` datetime NOT NULL,
  `seller_confirm` bit(1) NOT NULL DEFAULT b'0',
  `buyer_confirm` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`transaction_id`),
  KEY `FK_transaction_user` (`seller_user_id`),
  KEY `FK_transaction_user_2` (`buyer_user_id`),
  KEY `FK_transaction_product` (`product_id`),
  CONSTRAINT `FK_transaction_product` FOREIGN KEY (`product_id`) REFERENCES `productdata` (`product_data_id`),
  CONSTRAINT `FK_transaction_user` FOREIGN KEY (`seller_user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `FK_transaction_user_2` FOREIGN KEY (`buyer_user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(64) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `email` varchar(32) NOT NULL,
  `country` varchar(64) NOT NULL,
  `state` varchar(64) NOT NULL,
  `city` varchar(64) NOT NULL,
  `adress_1` varchar(256) DEFAULT NULL,
  `adress_2` varchar(256) NOT NULL,
  `zip_code` varchar(64) NOT NULL,
  `contact_info` varchar(64) DEFAULT NULL,
  `cell_number` varchar(32) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'active',
  `salt` tinyblob DEFAULT NULL,
  `is_admin` bit(1) DEFAULT b'0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_username` (`user_id`,`username`),
  FULLTEXT KEY `username` (`username`),
  FULLTEXT KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table tw.userbid
DROP TABLE IF EXISTS `userbid`;
CREATE TABLE IF NOT EXISTS `userbid` (
  `current_bid_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(20) unsigned NOT NULL,
  `product_id` int(20) unsigned NOT NULL,
  `status` varchar(50) DEFAULT 'ongoing',
  `value` int(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`current_bid_id`),
  KEY `FK_userbid_user` (`user_id`),
  KEY `FK_userbid_product` (`product_id`),
  CONSTRAINT `FK_userbid_product` FOREIGN KEY (`product_id`) REFERENCES `productdata` (`product_data_id`),
  CONSTRAINT `FK_userbid_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
