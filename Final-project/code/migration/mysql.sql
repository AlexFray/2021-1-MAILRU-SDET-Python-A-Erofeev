CREATE DATABASE test;
USE test;
CREATE TABLE `test_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(64) NOT NULL,
  `access` smallint DEFAULT NULL,
  `active` smallint DEFAULT NULL,
  `start_active_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `ix_test_users_username` (`username`)
);
INSERT INTO test_users (username, password, email, access) VALUES ('adminn', 'admin', 'admin@admin.ru', 1);
INSERT INTO test_users (username, password, email, access) VALUES ('userblock', 'userblock', 'userblock@admin.ru', 0);
CREATE USER 'test_qa' IDENTIFIED BY 'qa_test';
GRANT ALL PRIVILEGES ON * . * TO 'test_qa';
FLUSH PRIVILEGES;