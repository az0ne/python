
ALTER TABLE mz_course_careercourse
ADD COLUMN enable_free_488  tinyint(1) NOT NULL DEFAULT 0 AFTER try_price;

ALTER TABLE mz_lps3_task
ADD COLUMN type  int(11) NOT NULL DEFAULT 0 AFTER gift_id;

ALTER TABLE mz_course_careercourse
ADD COLUMN jobless_price  int(10) unsigned DEFAULT NULL AFTER net_price;

CREATE TABLE `mz_free_task_desc` (
`id`  int(11) NOT NULL AUTO_INCREMENT,
`task_id`  int(11) NOT NULL ,
`title`  varchar(50) NOT NULL ,
`img1`  varchar(200) NULL ,
`img2`  varchar(200) NULL ,
`img3`  varchar(200) NULL ,
`created_time`  datetime NOT NULL ,
`update_time`  datetime NULL ,
`operator_id`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `index_tftd_task_id` (`task_id`) USING BTREE
)
;

CREATE TABLE `mz_free_task_article` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`task_id`  int(11) NOT NULL ,
`article_title`  varchar(50) NOT NULL ,
`article_url`  varchar(200) NOT NULL ,
`index`  int(11) NOT NULL DEFAULT 1 ,
`type`  int(11) NOT NULL ,
PRIMARY KEY (`id`),
INDEX `index_tfta_task_id` (`task_id`) USING BTREE,
INDEX `index_tfta_type` (`type`) USING BTREE
)
;

CREATE TABLE `mz_free_task_excellent_works` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`task_id`  int(11) NOT NULL ,
`title` varchar(50) NOT NULL ,
`img_url`  varchar(200) NOT NULL ,
`code_url`  varchar(200) NOT NULL ,
`index`  int(11) NOT NULL DEFAULT 1 ,
PRIMARY KEY (`id`),
INDEX `index_tfta_task_id` (`task_id`) USING BTREE,
INDEX `index_tfta_index` (`index`) USING BTREE
)
;

DROP TABLE IF EXISTS `mz_lps3_classmeetingmobilerecord`;
CREATE TABLE `mz_lps3_classmeetingmobilerecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_meeting_id` int(11) NOT NULL,
  `start_3hour_ago` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `class_meeting_id` (`class_meeting_id`) USING BTREE,
  CONSTRAINT `mz_lps3_classmeetingmobilerecord_ibfk_1` FOREIGN KEY (`class_meeting_id`) REFERENCES `mz_lps3_classmeeting` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
