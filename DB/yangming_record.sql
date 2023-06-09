-- MySQL dump 10.13  Distrib 8.0.32, for Linux (aarch64)
--
-- Host: localhost    Database: yangming
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `patient_info`
--

DROP TABLE IF EXISTS `patient_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_info` (
  `class` int DEFAULT NULL,
  `barcode` varchar(20) DEFAULT NULL,
  `info` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_info`
--

LOCK TABLES `patient_info` WRITE;
/*!40000 ALTER TABLE `patient_info` DISABLE KEYS */;
INSERT INTO `patient_info` VALUES (4,'1234567890ABC','陳志明(男) 出生年月日：52/9/27 病例號：11481701 身分證字號：A125152001');
/*!40000 ALTER TABLE `patient_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record` (
  `class` int DEFAULT NULL,
  `id` varchar(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `1_barcode` varchar(20) DEFAULT NULL,
  `1_select` varchar(5) DEFAULT NULL,
  `1_correctness` int DEFAULT NULL,
  `2_check` varchar(5) DEFAULT NULL,
  `2_Dilatrend` int DEFAULT NULL,
  `2_Dilantin` int DEFAULT NULL,
  `2_correctness` int DEFAULT NULL,
  `2_reason` varchar(200) DEFAULT NULL,
  `3_check` varchar(5) DEFAULT NULL,
  `3_Requip` int DEFAULT NULL,
  `3_Requip1` int DEFAULT NULL,
  `3_correctness` int DEFAULT NULL,
  `3_reason` varchar(200) DEFAULT NULL,
  `4_check` varchar(5) DEFAULT NULL,
  `4_correctness` int DEFAULT NULL,
  `4_reason` varchar(200) DEFAULT NULL,
  `5_check` varchar(5) DEFAULT NULL,
  `5_Repaglinide` int DEFAULT NULL,
  `5_correctness` int DEFAULT NULL,
  `5_reason` varchar(200) DEFAULT NULL,
  `6_check` varchar(5) DEFAULT NULL,
  `6_Transamin` int DEFAULT NULL,
  `6_correctness` int DEFAULT NULL,
  `6_reason` varchar(200) DEFAULT NULL,
  `7_check` varchar(5) DEFAULT NULL,
  `7_correctness` int DEFAULT NULL,
  `7_reason` varchar(200) DEFAULT NULL,
  `8_check` varchar(5) DEFAULT NULL,
  `8_Bokey` int DEFAULT NULL,
  `8_correctness` int DEFAULT NULL,
  `8_reason` varchar(200) DEFAULT NULL,
  `9_check` varchar(5) DEFAULT NULL,
  `9_Zocor` int DEFAULT NULL,
  `9_correctness` int DEFAULT NULL,
  `9_reason` varchar(200) DEFAULT NULL,
  `10_check` varchar(5) DEFAULT NULL,
  `10_FLU` int DEFAULT NULL,
  `10_correctness` int DEFAULT NULL,
  `10_reason` varchar(200) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `uid` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (4,'ff','fF','_____________','no',1,'True',1,0,0,' 1','True',0,0,0,' 2','False',2,NULL,'False',0,1,' 3','False',0,1,' 44','False',2,NULL,'False',0,0,' 5','False',1,0,' 6','False',0,1,' 77','2023_02_21_16_58_53',NULL),(4,'gg','hh','_____________','no',1,'True',1,0,0,' 1','True',0,0,0,' 2','False',2,NULL,'False',0,1,' 3','False',0,1,' 44','False',2,NULL,'False',0,0,' 5','False',1,0,' 6','False',0,1,' 77','2023_02_21_18_39_48',NULL),(4,'310832007','343DF','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_17_18','473r95695'),(4,'310832007','111','_____________','yes',0,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_17_39','d91c74nslk'),(4,'310832007','111','_____________','yes',0,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_17_42','d91c74nslk'),(4,'310832007','ttt','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_18_11','2ew5xe0ytd'),(4,'310832007','ttt','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_18_20','2ew5xe0ytd'),(4,'310832007','ttt','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_18_40','2ew5xe0ytd'),(4,'310832007','ttt','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_05_23_33_09','2ew5xe0ytd'),(4,'310832007','eere','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'True',-1,1,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_01_02_37','u61jj4u72'),(4,'310832007','dd','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_12_21_13','zwpk9kixie'),(4,'310832007','24241','_____________','no',1,'False',-1,-1,1,' ','True',-1,-1,0,' ','True',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_12_39_20','bznnouxhk'),(4,'5','5','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_12_42_24','010vqj8tx'),(4,'310832008','Fritingo','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_12_44_02','qtkc580jk'),(4,'4','4','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_13_14_53','5rrux2rue'),(4,'310832007','Fritingo','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'True',-1,1,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_13_15_23','pzyri9s7b'),(4,'310832007','asdf','_____________','no',1,'True',-1,-1,0,' ','True',-1,-1,0,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_13_27_16','go5vptm66j'),(4,'310832007','我','4711279510010','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_13_28_48','cmpqm24vs'),(4,'03062023','雯','_____________','yes',0,'True',-1,-1,0,' ','True',-1,-1,0,' ','True',2,NULL,'True',-1,0,' ','True',-1,0,' ','True',2,NULL,'True',-1,1,' ','True',-1,1,' ','True',-1,1,' ','2023_03_06_16_37_04','jncha4mqi'),(4,'222','惠','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023_03_06_16_47_42','2egeeahxf'),(4,'1','1','_____________','yes',0,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'True',-1,1,' ','False',-1,0,' ','False',-1,1,' ','2023_03_09_21_53_07','l722k8oy1m'),(4,'1','1','_____________','no',1,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023-03-10-20-39-57','oo7ujvatsq'),(4,'','','_____________','null',0,'False',-1,-1,1,' 1','False',-1,-1,1,' 2','False',2,NULL,'False',-1,1,' 3','False',-1,1,' 4','False',2,NULL,'False',-1,0,' 5','False',-1,0,' 6','False',-1,1,' 7','2023-03-15-02-45-49','ki13ehpvu'),(4,'','','_____________','null',0,'False',-1,-1,1,' 1','False',-1,-1,1,' 2','False',2,NULL,'False',-1,1,' 3','False',-1,1,' 4','False',2,NULL,'False',-1,0,' 5','False',-1,0,' 6','False',-1,1,' 7','2023-03-15-02-46-23','r4pw5flst'),(4,'1','1','_____________','null',0,'False',-1,-1,1,' 1','False',-1,-1,1,' 2','False',2,NULL,'False',-1,1,' 3','False',-1,1,' 4','False',2,NULL,'False',-1,0,' 5','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-47-20','johnktsvbi'),(4,'1','1','_____________','null',0,'False',-1,-1,1,' 1','True',-1,-1,1,' 2','False',2,NULL,'True',-1,1,' 3','False',-1,1,' 4','False',2,NULL,'False',-1,0,' 5','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-47-59','johnktsvbi'),(4,'3','3','_____________','null',0,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-50-49','lp0s7x0kmb'),(4,'','','_____________','null',0,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' ','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-51-52','9575cbyvr'),(4,'','','_____________','null',0,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' 3','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-53-36','iill936nh'),(4,'','','_____________','null',0,'False',-1,-1,1,' ','False',-1,-1,1,' ','False',2,NULL,'False',-1,1,' 5','False',-1,1,' ','False',2,NULL,'False',-1,0,' ','False',-1,0,' ','False',-1,1,' ','2023-03-15-02-54-24','yle93ya0um'),(4,'','','_____________','null',0,'False',-1,-1,1,' 2','False',-1,-1,1,' 2','False',2,NULL,'False',-1,1,' 2','False',-1,1,' 2','False',2,NULL,'False',-1,0,' 2','False',-1,0,' 2','False',-1,1,' 2','2023-03-19-17-30-07','ylxu6n3kk'),(4,'','','_____________','null',0,'False',0,0,1,' 1','False',0,0,1,' 1','False',2,NULL,'False',0,1,' 1','False',0,1,' 1','False',2,NULL,'False',0,0,' 1','False',0,0,' 1','False',0,1,' 1','2023-03-19-18-09-45','fxzp5t0zbc'),(4,'３','２','_____________','no',1,'True',1,1,0,' ㄉˇ','False',0,0,1,' ㄉ','False',2,NULL,'False',0,1,' ˇ','False',0,1,' ˇ','False',2,NULL,'False',0,0,' ㄅ','False',1,0,' ㄅ','False',1,1,' ㄅ','2023-03-19-18-39-40','n3md1foeyd'),(4,'3','3','_____________','null',0,'False',1,1,0,' q','False',0,0,1,' q','False',2,NULL,'False',0,1,' qq','False',0,1,' q','False',2,NULL,'False',0,0,' q','False',1,0,' q','False',1,1,' q','2023-03-22-03-29-16','64tucscg4i'),(4,'2','2','_____________','null',0,'False',1,1,0,' 1','False',0,0,1,' 1','False',2,NULL,'False',0,1,' 1','False',0,1,' 1','False',2,NULL,'False',0,0,' 1','False',1,0,' 1','False',1,1,' 11','2023-03-22-03-31-17','f7oa3vnjxk'),(4,'33','3','_____________','null',0,'False',1,1,0,' 1','False',0,0,1,' 1','False',2,NULL,'False',0,1,' 1','False',0,1,' 1','False',2,NULL,'False',0,0,' 1','False',1,0,' 1','False',1,1,' 1','2023-03-22-03-53-03','00pqnc2cni'),(4,'1','1','_____________','null',0,'False',1,1,0,' 1','False',0,0,1,' 1','False',2,NULL,'False',0,1,' 1','False',0,1,' 1','False',2,NULL,'False',0,0,' 1','False',1,0,' 1','False',1,1,' 1','2023-03-22-03-54-58','rvbwp40h5'),(4,'33','3','_____________','null',0,'False',1,1,0,' 3','False',0,0,1,' 3','False',2,NULL,'False',0,1,' 3','False',0,1,' 3','False',2,NULL,'False',0,0,' 33','False',1,0,' 3','False',1,1,' 3','2023-03-22-03-57-45','8ex0uf92'),(4,'3','3','_____________','null',0,'False',1,1,0,' 3','False',0,0,1,' 3','False',2,NULL,'False',0,1,' 3','False',0,1,' 3','False',2,NULL,'False',0,0,' 3','False',1,0,' 3','False',1,1,' 3','2023-03-22-04-04-52','5v8yeuyuk'),(4,'','','_____________','null',0,'False',1,1,0,' ㄎ','False',0,0,1,' ㄎㄎ','False',2,NULL,'False',0,1,' 2','False',0,1,' 3','False',2,NULL,'False',0,0,' 4','False',1,0,' 5','False',1,1,' 3','2023-03-22-14-05-54','iqsigqbdj6'),(4,'','','_____________','null',0,'False',0,0,1,' ㄎ','False',0,0,1,' ㄎㄎ','False',2,NULL,'False',0,1,' 2','False',0,1,' 3','False',2,NULL,'False',0,0,' 4','False',0,0,' 5','False',0,1,' 3','2023-03-22-14-06-52','iqsigqbdj6'),(4,'','','_____________','null',0,'False',1,1,0,' e','False',0,0,1,' e','False',0,NULL,'False',0,1,' e','False',0,1,' e','False',2,NULL,'False',0,0,' e','False',0,0,' e','False',1,1,' e','2023-03-22-14-46-59','2yu38prz'),(4,'','','_____________','null',0,'False',1,1,0,' 3','False',0,0,1,' 3','False',0,NULL,'False',0,1,' 3','False',0,1,' 3','False',0,NULL,'False',0,0,' 3','False',0,0,' 3','False',1,0,' 3','2023-03-22-15-04-25','r457n7obm'),(4,'','','_____________','null',0,'False',1,1,0,' 0','False',0,0,1,' 9','False',0,NULL,'False',0,1,' 8','False',0,1,' 7','False',0,NULL,'False',0,0,' 6','False',0,0,' 5','False',1,0,' 4','2023-03-22-15-15-11','w8rxn0dtg'),(4,'','','_____________','null',0,'False',1,1,0,' 4','False',0,0,1,' 5','True',0,NULL,'False',0,1,' 6','True',0,0,' 2','False',0,NULL,'True',0,0,' 3','False',0,0,' 8','False',1,0,' 9','2023-03-22-15-40-04','eztafrunn'),(4,'310832007','莊東昇','_____________','no',1,'False',1,1,0,' 2','False',0,0,1,' 3','False',1,' 4','False',0,1,' 5','False',0,1,' 6','False',1,' 7','True',0,0,' ㄅ','True',0,0,' 1','False',1,0,' 8','2023-03-22-16-45-50','t5n5gfcdtp'),(4,'310832007','莊東昇','1234567890ABC','no',1,'False',1,1,0,' 3','False',0,0,1,' 4','False',0,' 5','False',0,1,' 6','False',0,1,' 7','False',0,' 8','True',0,0,' 1','True',0,0,' 2','False',1,0,' 9','2023-03-22-18-00-59','uy67mt8i2'),(4,'3','4','4711279510072','no',1,'False',1,1,0,' F','False',0,0,1,' F','False',0,' G','False',0,1,' F','False',0,1,' F','False',0,' G','True',0,0,' Q','True',0,0,' T','False',1,0,' H','2023-03-22-19-35-23','30r3lxb8zi'),(4,'109201001','尤珉晨','1234567890ABC','no',1,'False',0,0,1,'藥物名稱錯誤','False',0,0,1,' 劑量錯誤','True',0,' stat藥物','False',0,1,' 給藥時間錯誤','True',1,0,' 給藥時間到','False',0,'藥物過敏','True',1,1,'給藥時間到','True',1,1,' 給藥時間到','True',1,1,'  給藥時間到','2023-03-23-13-21-55','5uabngr6pfi');
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `id` int DEFAULT NULL,
  `tname` varchar(100) DEFAULT NULL,
  `info` varchar(20) DEFAULT NULL,
  `day` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (1,'bird','123','1999-02-24'),(3,'tiger','456','1342-03-04');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-29 21:43:32
