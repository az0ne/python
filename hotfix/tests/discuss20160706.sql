ALTER TABLE mz_common_newdiscuss
ADD COLUMN object_content  VARCHAR(20) DEFAULT NULL,
ADD COLUMN object_name  VARCHAR(50) DEFAULT NULL,
ADD COLUMN object_location  VARCHAR(50) DEFAULT NULL,
ADD COLUMN group_name varchar(20) DEFAULT NULL,
ADD COLUMN problem_id int(11) NOT NULL DEFAULT 0,
ADD COLUMN weight int(2) NOT NULL DEFAULT 0,
ADD COLUMN last_answer_datetime datetime,
ADD COLUMN last_answer_id int(11),
ADD COLUMN answer_nick_name varchar(50) DEFAULT NULL,
ADD COLUMN answer_user_id int(11) DEFAULT NULL,
ADD COLUMN discuss_count int(11) NOT NULL DEFAULT 0,
ADD COLUMN user_praise_count int(11) NOT NULL DEFAULT 0,
ADD KEY `mz_common_newdiscuss_last_answer_id` (`last_answer_id`);

DROP TABLE IF EXISTS `mz_common_newdiscussmaterial`;
CREATE TABLE `mz_common_newdiscussmaterial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `new_discuss_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `material` varchar(200) NOT NULL,
  `small_material` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `new_discuss_id` (`new_discuss_id`) USING BTREE,
  CONSTRAINT `mz_common_newdiscussmaterial_new_discuss_id_111` FOREIGN KEY (`new_discuss_id`) REFERENCES `mz_common_newdiscuss` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `mz_common_newdiscussuserpraise`;
CREATE TABLE `mz_common_newdiscussuserpraise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `new_discuss_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mz_common_newdiscussuserpraise_new_discuss_id_user_id` (`user_id`,`new_discuss_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `new_discuss_id` (`new_discuss_id`) USING BTREE,
  CONSTRAINT `mz_common_newdiscussuserpraise_new_discuss_id` FOREIGN KEY (`new_discuss_id`) REFERENCES `mz_common_newdiscuss` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `mz_common_newdiscussuserstatus`;
CREATE TABLE `mz_common_newdiscussuserstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(3) NOT NULL DEFAULT '1',
  `user_id` int(11) NOT NULL,
  `new_discuss_id` int(11) NOT NULL,
  group_name varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `new_discuss_id_user_id` (`user_id`,`new_discuss_id`) USING BTREE,
  KEY `new_discuss_id` (`new_discuss_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `mz_common_newdiscussuserstatus_ibfk_1` FOREIGN KEY (`new_discuss_id`) REFERENCES `mz_common_newdiscuss` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE mz_course_careercourse ADD ad VARCHAR(100) DEFAULT NULL;