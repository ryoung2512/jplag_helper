DROP TABLE IF EXISTS `submission_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submission_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_a` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `student_b` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `similarity` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `submission_a` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `submission_b` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
