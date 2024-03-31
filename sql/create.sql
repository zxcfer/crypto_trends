-- INSERT INTO alembic_version (version_num) VALUES ('d37c7fb77a0b');

CREATE DATABASE botin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `crypto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coin` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `marketcap` decimal(20,2) DEFAULT NULL,
  `epoch` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `crypto_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coin` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `price` decimal(20,2) DEFAULT NULL,
  `epoch` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `feed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(190) NOT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `website_name` varchar(255) DEFAULT NULL,
  `website_url` varchar(255) DEFAULT NULL,
  `epoch` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `feed_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(190) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `feed_id` int(11) DEFAULT NULL,
  `pub_date` datetime DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `summary` text DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `epoch` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  KEY `feed_id` (`feed_id`),
  CONSTRAINT `feed_item_ibfk_1` FOREIGN KEY (`feed_id`) REFERENCES `feed` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

