/*

	Nmappah Pah Rappah seequel sheet musak!

*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `environment`
-- ----------------------------
DROP TABLE IF EXISTS `environment`;
CREATE TABLE `environment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `last_scanned` timestamp NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `region` varchar(255) NOT NULL DEFAULT '',
  `avaliability` varchar(255) NOT NULL DEFAULT 'public',
  `type` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`name`,`region`,`avaliability`,`type`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for `host`
-- ----------------------------
DROP TABLE IF EXISTS `host`;
CREATE TABLE `host` (
  `ip_address` varchar(64) NOT NULL,
  `hostname` varchar(256) DEFAULT NULL,
  `os` varchar(1024) DEFAULT NULL,
  `state` varchar(64) DEFAULT NULL,
  `environment_id` int(11) unsigned NOT NULL,
  `aws_security_group` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY (`ip_address`,`environment_id`),
  KEY `Env ID FK` (`environment_id`),
  KEY `ip_address` (`ip_address`),
  CONSTRAINT `Env ID FK` FOREIGN KEY (`environment_id`) REFERENCES `environment` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `port`
-- ----------------------------
DROP TABLE IF EXISTS `port`;
CREATE TABLE `port` (
  `host_ip` varchar(64) NOT NULL DEFAULT '',
  `protocol` varchar(32) NOT NULL,
  `number` int(32) NOT NULL,
  `state` varchar(64) DEFAULT NULL,
  `reason` varchar(64) DEFAULT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`host_ip`,`protocol`,`number`),
  CONSTRAINT `Host IP FK` FOREIGN KEY (`host_ip`) REFERENCES `host` (`ip_address`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `target`
-- ----------------------------
DROP TABLE IF EXISTS `target`;
CREATE TABLE `target` (
  `ip_address` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`ip_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
