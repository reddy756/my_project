-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: invigi
-- ------------------------------------------------------
-- Server version	8.0.36

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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `absentee_records`
--

LOCK TABLES `absentee_records` WRITE;
/*!40000 ALTER TABLE `absentee_records` DISABLE KEYS */;
INSERT INTO `absentee_records` VALUES (1,41,2,'Health issues'),(2,42,1,'Family emergency'),(3,43,0,NULL),(4,44,3,'Sudden illness of family member'),(5,45,0,NULL),(6,46,1,'Doctor appointment'),(7,47,2,'Unforeseen travel'),(8,48,0,NULL),(9,49,1,'Personal reasons'),(10,50,0,NULL),(11,51,2,'Sudden illness'),(12,52,0,NULL),(13,53,1,'Family emergency'),(14,54,0,NULL),(15,55,2,'Sudden travel plan'),(16,56,1,'Doctor appointment'),(17,57,0,NULL),(18,58,1,'Meeting with advisor'),(19,59,0,NULL),(20,60,2,'Sudden illness');
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjustment_requests`
--

LOCK TABLES `adjustment_requests` WRITE;
/*!40000 ALTER TABLE `adjustment_requests` DISABLE KEYS */;
INSERT INTO `adjustment_requests` VALUES (21,41,21,22,'Need to attend an emergency meeting','accepted'),(22,42,22,23,'Health issue, need to swap schedules','pending'),(23,43,23,24,'Personal reasons, need to reschedule','pending'),(24,44,24,25,'Sudden family commitment','pending'),(25,45,25,26,'Unexpected travel plan','pending'),(26,46,26,27,'Appointment with doctor','pending'),(27,47,27,28,'Need to attend a conference','pending'),(28,48,28,29,'Family emergency','pending'),(29,49,29,30,'Unexpected situation at home','pending'),(30,50,30,31,'Last-minute unavoidable commitment','pending'),(31,51,31,32,'Sudden illness','pending'),(32,52,32,33,'Family emergency','pending'),(33,53,33,34,'Personal reasons','pending'),(34,54,34,35,'Need to attend a workshop','pending'),(35,55,35,36,'Sudden travel plan','pending'),(36,56,36,37,'Doctor appointment','pending'),(37,57,37,38,'Meeting with advisor','pending'),(38,58,38,39,'Family gathering','pending'),(39,59,39,40,'Sudden illness','pending'),(40,60,40,21,'Personal reasons','accepted');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Introduction to Programming',1),(2,'Circuit Analysis',2),(3,'Thermodynamics',3),(4,'Classical Mechanics',4),(5,'Organic Chemistry',5),(6,'Cell Biology',6),(7,'Calculus',7),(8,'World Literature',8),(9,'World History',9),(10,'Art History',10),(11,'Physical Geography',11),(12,'Microeconomics',12),(13,'Introduction to Psychology',13),(14,'Sociology of Culture',14),(15,'Philosophy of Mind',15),(16,'Music Theory',16),(17,'Contemporary Dance',17),(18,'Theater Production',18),(19,'Film Analysis',19),(20,'Digital Photography',20);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Computer Science',2),(2,'Electrical Engineering',3),(3,'Mechanical Engineering',4),(4,'Physics',5),(5,'Chemistry',6),(6,'Biology',7),(7,'Mathematics',8),(8,'Literature',9),(9,'History',10),(10,'Art',11),(11,'Geography',12),(12,'Economics',13),(13,'Psychology',14),(14,'Sociology',15),(15,'Philosophy',16),(16,'Music',17),(17,'Dance',18),(18,'Theater',19),(19,'Film Studies',20),(20,'Photography',21);
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (21,3,1,1,1,30),(22,4,2,1,2,30),(23,5,3,1,3,30),(24,6,4,1,4,30),(25,7,5,1,5,30),(26,8,6,1,6,30),(27,9,7,1,7,30),(28,10,8,1,8,30),(29,11,9,1,9,30),(30,12,10,1,10,30),(31,13,11,1,11,30),(32,14,12,1,12,30),(33,15,13,1,13,30),(34,16,14,1,14,30),(35,17,15,1,15,30),(36,18,16,1,16,30),(37,19,17,1,17,30),(38,20,18,1,18,30),(39,21,19,1,19,30),(40,22,20,1,20,30);
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
INSERT INTO `feedback` VALUES (1,21,'Great job on the invigilation!','2024-04-06 10:29:44'),(2,22,'Could be more vigilant during the exam','2024-04-06 10:29:44'),(3,23,'Very professional conduct during invigilation','2024-04-06 10:29:44'),(4,24,'Good communication with students','2024-04-06 10:29:44'),(5,25,'Clear instructions provided','2024-04-06 10:29:44'),(6,26,'Friendly demeanor, approachable','2024-04-06 10:29:44'),(7,27,'Excellent handling of exam situation','2024-04-06 10:29:44'),(8,28,'Need to be more organized during exams','2024-04-06 10:29:44'),(9,29,'Knowledgeable and helpful','2024-04-06 10:29:44'),(10,30,'Effective management of exam environment','2024-04-06 10:29:44'),(11,31,'Need to improve punctuality','2024-04-06 10:29:44'),(12,32,'Could explain concepts more clearly','2024-04-06 10:29:44'),(13,33,'Engage more with students','2024-04-06 10:29:44'),(14,34,'Encourage participation in class discussions','2024-04-06 10:29:44'),(15,35,'Provide more constructive feedback','2024-04-06 10:29:44'),(16,36,'Improve coordination with other faculty members','2024-04-06 10:29:44'),(17,37,'Enhance classroom management skills','2024-04-06 10:29:44'),(18,38,'Encourage creativity and exploration in assignments','2024-04-06 10:29:44'),(19,39,'Great job on the invigilation!','2024-04-06 10:29:44'),(20,40,'Could be more vigilant during the exam','2024-04-06 10:29:44');
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
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invigilation_schedule`
--

LOCK TABLES `invigilation_schedule` WRITE;
/*!40000 ALTER TABLE `invigilation_schedule` DISABLE KEYS */;
INSERT INTO `invigilation_schedule` VALUES (41,21,1,1,'2024-04-07','09:00-12:00'),(42,22,2,2,'2024-04-08','13:00-16:00'),(43,23,3,3,'2024-04-09','15:00-18:00'),(44,24,4,4,'2024-04-10','10:00-13:00'),(45,25,5,5,'2024-04-11','11:00-14:00'),(46,26,6,6,'2024-04-12','12:00-15:00'),(47,27,7,7,'2024-04-13','09:00-12:00'),(48,28,8,8,'2024-04-14','13:00-16:00'),(49,29,9,9,'2024-04-15','15:00-18:00'),(50,30,10,10,'2024-04-16','10:00-13:00'),(51,31,11,11,'2024-04-17','09:00-12:00'),(52,32,12,12,'2024-04-18','13:00-16:00'),(53,33,13,13,'2024-04-19','15:00-18:00'),(54,34,14,14,'2024-04-20','10:00-13:00'),(55,35,15,15,'2024-04-21','11:00-14:00'),(56,36,16,16,'2024-04-22','12:00-15:00'),(57,37,17,17,'2024-04-23','09:00-12:00'),(58,38,18,18,'2024-04-24','13:00-16:00'),(59,39,19,19,'2024-04-25','15:00-18:00'),(60,40,20,20,'2024-04-26','10:00-13:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (1,'101',1),(2,'102',1),(3,'103',1),(4,'104',1),(5,'105',1),(6,'106',1),(7,'107',1),(8,'108',1),(9,'109',1),(10,'110',1),(11,'111',1),(12,'112',1),(13,'113',1),(14,'114',1),(15,'115',1),(16,'116',1),(17,'117',1),(18,'118',1),(19,'119',1),(20,'120',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John Doe','john@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Admin'),(2,'Jane Smith','jane@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Department Incharge'),(3,'Alice Johnson','alice@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(4,'Bob Brown','bob@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(5,'Emily Davis','emily@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(6,'Michael Wilson','michael@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(7,'Sarah Lee','sarah@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(8,'David Martinez','david@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(9,'Jessica Thompson','jessica@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(10,'Daniel Taylor','daniel@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(11,'Sophia Garcia','sophia@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(12,'James Rodriguez','james@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(13,'Olivia Martinez','olivia@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(14,'Liam Brown','liam@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(15,'Emma Wilson','emma@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(16,'Alexander Johnson','alexander@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(17,'Ava Lee','ava@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(18,'William Smith','william@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(19,'Mia Davis','mia@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(20,'Ethan Taylor','ethan@example.com','hashed_password_20','Faculty'),(21,'Taylor','taylor@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty'),(22,'Jaylor','jaylor@example.com','pbkdf2:sha256:600000$m5W3hrgx4nCce8PW$504bdca5c6074f902bd9df9954a0c031fd0c0c9dac24ccfabc26f82328345bce','Faculty');
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

-- Dump completed on 2024-04-06 14:31:17
