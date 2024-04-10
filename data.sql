-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: invigila
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `absentee_records`
--

DROP TABLE IF EXISTS `absentee_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `absentee_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `schedule_id` int NOT NULL,
  `absentee_count` int DEFAULT '0',
  `reason` text,
  PRIMARY KEY (`record_id`),
  KEY `schedule_id` (`schedule_id`),
  CONSTRAINT `absentee_records_ibfk_1` FOREIGN KEY (`schedule_id`) REFERENCES `invigilation_schedule` (`schedule_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `absentee_records`
--

LOCK TABLES `absentee_records` WRITE;
/*!40000 ALTER TABLE `absentee_records` DISABLE KEYS */;
INSERT INTO `absentee_records` VALUES (23,67,60,'hey');
/*!40000 ALTER TABLE `absentee_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adjustment_requests`
--

DROP TABLE IF EXISTS `adjustment_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adjustment_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `original_schedule_id` int DEFAULT NULL,
  `requested_by` int DEFAULT NULL,
  `requested_to` int DEFAULT NULL,
  `reason` text,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  PRIMARY KEY (`request_id`),
  KEY `original_schedule_id` (`original_schedule_id`),
  KEY `requested_by` (`requested_by`),
  KEY `requested_to` (`requested_to`),
  CONSTRAINT `adjustment_requests_ibfk_1` FOREIGN KEY (`original_schedule_id`) REFERENCES `invigilation_schedule` (`schedule_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `adjustment_requests_ibfk_2` FOREIGN KEY (`requested_by`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `adjustment_requests_ibfk_3` FOREIGN KEY (`requested_to`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjustment_requests`
--

LOCK TABLES `adjustment_requests` WRITE;
/*!40000 ALTER TABLE `adjustment_requests` DISABLE KEYS */;
INSERT INTO `adjustment_requests` VALUES (42,67,45,43,'I am unable to attend the duty','accepted'),(43,67,45,41,'unable to attend the duty','pending');
/*!40000 ALTER TABLE `adjustment_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `department_id` int DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (12,'Microeconomics',12),(13,'Introduction to Psychology',13),(14,'Sociology of Culture',14),(15,'Philosophy of Mind',15),(22,'Introduction to Programmings',21);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(255) NOT NULL,
  `incharge_user_id` int DEFAULT NULL,
  PRIMARY KEY (`department_id`),
  KEY `incharge_user_id` (`incharge_user_id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`incharge_user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (12,'Economics',NULL),(13,'Psychology',25),(14,'Sociology',NULL),(15,'Philosophy',NULL),(21,'Datascience',27);
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `department_id` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  `course_id` int DEFAULT NULL,
  `max_duties` int DEFAULT '30',
  PRIMARY KEY (`faculty_id`),
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `faculty_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `faculty_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (41,23,21,1,22,30),(42,25,13,NULL,13,30),(43,26,21,1,22,30),(44,27,21,1,22,30),(45,28,12,1,12,30),(46,29,13,1,13,30);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int DEFAULT NULL,
  `feedback` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invigilation_schedule`
--

DROP TABLE IF EXISTS `invigilation_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invigilation_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `room_id` int DEFAULT NULL,
  `date` date NOT NULL,
  `time_slot` varchar(255) NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `faculty_id` (`faculty_id`),
  KEY `course_id` (`course_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `invigilation_schedule_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `invigilation_schedule_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `invigilation_schedule_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invigilation_schedule`
--

LOCK TABLES `invigilation_schedule` WRITE;
/*!40000 ALTER TABLE `invigilation_schedule` DISABLE KEYS */;
INSERT INTO `invigilation_schedule` VALUES (63,41,12,11,'2024-04-10','9:30-12:00'),(66,42,12,1,'2024-04-08','9:30-12:00'),(67,45,12,1,'2024-04-08','9:30-12:00'),(68,45,14,1,'2024-04-11','1:00-4:00'),(69,45,15,11,'2024-04-10','9:30-12:00'),(70,46,14,13,'2024-04-10','1:00-4:00'),(71,46,13,14,'2024-04-11','9.30-10:30');
/*!40000 ALTER TABLE `invigilation_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `room_number` varchar(255) NOT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,'101',1),(10,'110',1),(11,'111',1),(13,'113',1),(14,'114',1),(17,'117',1);
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('Admin','Department Incharge','Faculty') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'Jane Smith','jane@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Department Incharge'),(23,'Bhaskar','bhaskerdareddy75@gmail.com','pbkdf2:sha256:600000$MDxTV5mPpHexOuHN$d6b7639bf41de9da75f61d143af8fbee1114be496f4389d40bbba79bbbf69382','Faculty'),(24,'Bhaskar','dbsreddy3@gmail.com','pbkdf2:sha256:600000$2DLuZe0H4N1c3KkX$f742423950bfbb36fa2a33442f49424073451fd3c7ef440f68b1b1f26a239a66','Admin'),(25,'Lohith','lohithillumalla24@gmail.com','pbkdf2:sha256:600000$OBvMU5NerBIf3lFJ$88ca0e018e761dce36319c0fae7401f9972502ac8e87f4948335da919e334ab3','Department Incharge'),(26,'chandu','chandugangavarapu510@gmail.com','pbkdf2:sha256:600000$xjuf0sDhHSReoGuu$b2157277983ba8d9933b3d4adaa1b4684f88eb32608baa66d33355d402a303d9','Faculty'),(27,'Vinod','20jk1a0517@gmail.com','pbkdf2:sha256:600000$GidCr5lwrumBAopB$e957337a59f187fc6cc0f3f71b232dd7fe96307dc3b77ddb7f8b2b17c132cde8','Department Incharge'),(28,'Teja12','20jk1a0508@gmail.com','pbkdf2:sha256:600000$9gVkJV5MZDEx9DV7$ceafbe68dfed41cb927ede1643b650ff2b22196cb68f72ec04e685620224a000','Faculty'),(29,'Ramesh','vinodillumalla@gmail.com','pbkdf2:sha256:600000$nIGt4ukjmCX568W5$d1915d5f21306ada71054ccffdc3d2f15dcac089571e63422099dd91637980c0','Faculty');
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

-- Dump completed on 2024-04-08 16:39:32
