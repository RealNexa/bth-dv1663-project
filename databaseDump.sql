CREATE DATABASE  IF NOT EXISTS `computerstore` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `computerstore`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: computerstore
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `Username` varchar(30) NOT NULL,
  `Fname` varchar(20) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `PhoneNumber` varchar(15) NOT NULL,
  `ShippingAddress` varchar(50) NOT NULL,
  `InvoiceAddress` varchar(50) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES ('person1','john','doe','0761382743','addressgatan 1','addressgatan 1'),('person2','jane','doe','0438428812','gatan 2','gatan 2'),('person3','ulf','olsen','0713501134','storgatan 500','enaddress 3'),('person4','tim','persson','0123456789','industrigatan 12','julgatan 67'),('person5','max','eriksson','98765432190','addressen 73','stockholmsgatan 42');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(20) NOT NULL,
  `ComputerID` int NOT NULL,
  `OrderDate` datetime NOT NULL,
  `ShippingDate` date NOT NULL,
  PRIMARY KEY (`OrderID`),
  UNIQUE KEY `OrderID` (`OrderID`),
  KEY `Username` (`Username`),
  KEY `ComputerID` (`ComputerID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `customers` (`Username`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`ComputerID`) REFERENCES `prebuiltcomputers` (`ComputerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'person3',1,'2023-05-18 10:44:47','2023-05-26'),(2,'person4',4,'2023-05-18 10:44:47','2023-05-23'),(3,'person1',2,'2023-05-18 10:44:47','2023-05-24');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`tomcat`@`localhost`*/ /*!50003 TRIGGER `decrementStock` AFTER INSERT ON `orders` FOR EACH ROW BEGIN
        UPDATE PrebuiltComputers SET Stock = Stock - 1 WHERE ComputerID = New.ComputerID;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `parts`
--

DROP TABLE IF EXISTS `parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts` (
  `PartID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) NOT NULL,
  `Type` varchar(20) NOT NULL,
  `Brand` varchar(20) NOT NULL,
  `ReleaseDate` date NOT NULL,
  `Description` text,
  PRIMARY KEY (`PartID`),
  UNIQUE KEY `PartID` (`PartID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parts`
--

LOCK TABLES `parts` WRITE;
/*!40000 ALTER TABLE `parts` DISABLE KEYS */;
INSERT INTO `parts` VALUES (1,'i9-13900K','CPU','Intel','2022-11-23','3 GHz 24-Core Processor'),(2,'Ryzen 5 5600X','CPU','AMD','2021-03-05','3.7 GHz 6-Core Processor'),(3,'Vengeance LPX','RAM','Corsair','2021-04-12','LPX 16 GB (2 x 8 GB) DDR4-3200 CL16'),(4,'Trident Z5 RGB','RAM','G.Skill','2023-02-21','64 GB (2 x 32 GB) DDR5-6400 CL32'),(5,'GeForce RTX 3060','GPU','MSI','2021-07-11','GeForce RTX 3060 12GB 12 GB Video Card'),(6,'RX 6600 XT MECH','GPU','MSI','2021-09-17','RX 6600 XT MECH'),(7,'TUF GAMING X570-PLUS','Motherboard','ASUS','2023-01-04','(WI-FI) ATX AM4 Motherboard'),(8,'A520M-A PRO','Motherboard','MSI','2020-05-03','MSI Micro ATX AM4'),(9,'RM850x','PSU','Corsair','2021-05-02','850 W 80+ Gold Certified Fully Modular ATX'),(10,'Smart BM2','PSU','Thermaltake','2019-04-29','650 W 80+ Bronze Certified Semi-modular ATX');
/*!40000 ALTER TABLE `parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prebuiltcomputers`
--

DROP TABLE IF EXISTS `prebuiltcomputers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prebuiltcomputers` (
  `ComputerID` int NOT NULL AUTO_INCREMENT,
  `ComputerName` varchar(30) DEFAULT NULL,
  `Price` int NOT NULL,
  `Stock` int DEFAULT NULL,
  PRIMARY KEY (`ComputerID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prebuiltcomputers`
--

LOCK TABLES `prebuiltcomputers` WRITE;
/*!40000 ALTER TABLE `prebuiltcomputers` DISABLE KEYS */;
INSERT INTO `prebuiltcomputers` VALUES (1,'Karlskrona Special',64000,2),(2,'Next Gen Gaming Computer',33000,5),(3,'Traditional Work Computer',15000,100),(4,'Low-end Budget Computer',10000,50);
/*!40000 ALTER TABLE `prebuiltcomputers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prebuiltcomputersparts`
--

DROP TABLE IF EXISTS `prebuiltcomputersparts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prebuiltcomputersparts` (
  `PCPID` int NOT NULL AUTO_INCREMENT,
  `ComputerID` int NOT NULL,
  `PartID` int NOT NULL,
  PRIMARY KEY (`PCPID`),
  UNIQUE KEY `PCPID` (`PCPID`),
  KEY `ComputerID` (`ComputerID`),
  KEY `PartID` (`PartID`),
  CONSTRAINT `prebuiltcomputersparts_ibfk_1` FOREIGN KEY (`ComputerID`) REFERENCES `prebuiltcomputers` (`ComputerID`),
  CONSTRAINT `prebuiltcomputersparts_ibfk_2` FOREIGN KEY (`PartID`) REFERENCES `parts` (`PartID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prebuiltcomputersparts`
--

LOCK TABLES `prebuiltcomputersparts` WRITE;
/*!40000 ALTER TABLE `prebuiltcomputersparts` DISABLE KEYS */;
INSERT INTO `prebuiltcomputersparts` VALUES (1,1,1),(2,1,4),(3,1,6),(4,1,7),(5,1,9),(6,2,2),(7,2,4),(8,2,5),(9,2,7),(10,2,10),(11,3,2),(12,3,3),(13,3,5),(14,3,8),(15,3,9),(16,4,1),(17,4,3),(18,4,5),(19,4,7),(20,4,9);
/*!40000 ALTER TABLE `prebuiltcomputersparts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'computerstore'
--

--
-- Dumping routines for database 'computerstore'
--
/*!50003 DROP FUNCTION IF EXISTS `usernameExist` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`tomcat`@`localhost` FUNCTION `usernameExist`(inpUsername TEXT) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
        DECLARE varUsernameExist INT;
        SELECT COUNT(*) FROM CUSTOMERS WHERE Username = inpUsername INTO varUsernameExist;
        IF (varUsernameExist = 1) THEN
            RETURN True;
        ELSE 
            RETURN False;
        END IF;
    
    END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `validUsername` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`tomcat`@`localhost` FUNCTION `validUsername`(inpUsername TEXT) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
        DECLARE duplicate INT;
        SELECT count(username) FROM Customers WHERE username = inpUsername INTO duplicate;
        
        IF (LENGTH(inpUsername) > 30 OR LENGTH(inpUsername) < 3) THEN
            RETURN False;
            
        ELSEIF (duplicate > 0) THEN
            RETURN False;
            
        ELSE
            RETURN True;

        END IF;

    END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-18 10:57:54
