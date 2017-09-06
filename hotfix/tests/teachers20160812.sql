DROP TABLE IF EXISTS `mz_lps_classteachers`;
CREATE TABLE `mz_lps_classteachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `teacher_class_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `mz_lps_classteacher_teacher_class_id_teacher_id` (`teacher_id`,`teacher_class_id`) USING BTREE,
  KEY `mz_lps_classteacher_teacher_id` (`teacher_id`) USING BTREE,
  KEY `mz_lps_classteacher_teacher_class_id` (`teacher_class_id`) USING BTREE,
  CONSTRAINT `mz_lps_classteachers_ibfk_2` FOREIGN KEY (`teacher_class_id`) REFERENCES `mz_lps_class` (`id`),
  CONSTRAINT `mz_lps_classteachers_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `mz_user_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8;


INSERT INTO mz_lps_classteachers (teacher_class_id,teacher_id) SELECT id,teacher_id FROM mz_lps_class WHERE teacher_id!='Null';

Alter table mz_lps_class DROP FOREIGN KEY mz_lps_cla_teacher_id_1299bc11dc5fbd13_fk_mz_user_userprofile_id;
Alter table mz_lps_class DROP INDEX mz_lps_class_d9614d40;
Alter table mz_lps_class drop column teacher_id;