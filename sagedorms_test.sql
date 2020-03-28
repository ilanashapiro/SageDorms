CREATE TABLE IF NOT EXISTS ClosetType (
  typeName VARCHAR(50) NOT NULL,
  length INT NOT NULL,
  width INT NOT NULL,
  PRIMARY KEY (typeName));

CREATE TABLE IF NOT EXISTS WindowType (
  typeName VARCHAR(50) NOT NULL,
  directionFacing ENUM('NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTHEAST', 'NORTHWEST',
                       'SOUTHEAST', 'SOUTHWEST'),
  viewDescription VARCHAR(100) NOT NULL,
  PRIMARY KEY (typeName));
  
CREATE TABLE IF NOT EXISTS Dorm (
  name VARCHAR(50) NOT NULL,
  location VARCHAR(50) NOT NULL,
  otherDescription VARCHAR(100),
  PRIMARY KEY (name));
  
CREATE TABLE IF NOT EXISTS ProspectiveSuiteGroup (
  avgDrawNum DOUBLE NOT NULL,
  avgDrawTime DATETIME NOT NULL,
  PRIMARY KEY (avgDrawNum));

CREATE TABLE IF NOT EXISTS Suite (
	suiteID VARCHAR(50) NOT NULL,
	isSubFree BOOL NOT NULL,
	numRooms INT NOT NULL,
	numPeople INT NOT NULL,
	dormName VARCHAR(50) NOT NULL,
	otherDescription VARCHAR(100),
	FOREIGN KEY (dormName) REFERENCES Dorm(name),
	PRIMARY KEY (suiteID));

CREATE TABLE IF NOT EXISTS Room (
	number INT NOT NULL,
	dormName VARCHAR(50) NOT NULL,
	floorNum INT NOT NULL,
	lengthDescription VARCHAR(50) NOT NULL,
	widthDescription VARCHAR(50) NOT NULL,
	squareFeet DOUBLE NOT NULL,
	isSubFree BOOL NOT NULL,
	isReservedForSponsorGroup BOOL NOT NULL,
	windowType VARCHAR(50) NOT NULL,
	suite VARCHAR(50) NOT NULL,
	otherDescription VARCHAR(100),
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (dormName) REFERENCES Dorm(name),
	FOREIGN KEY (windowType) REFERENCES WindowType(typeName),
	FOREIGN KEY (suite) REFERENCES Suite(suiteID));

CREATE TABLE IF NOT EXISTS DormRoom (
	number INT NOT NULL,
	dormName VARCHAR(50) NOT NULL,
	numOccupants INT NOT NULL,
	hasPrivateBathroom BOOL NOT NULL,
	numDoors INT NOT NULL,
	closetType VARCHAR(50) NOT NULL,
	connectingRoomNum INT,
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (connectingRoomNum, dormName) REFERENCES DormRoom(number, dormName),
	FOREIGN KEY (closetType) REFERENCES ClosetType(typeName),
	FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

CREATE TABLE IF NOT EXISTS Student (
	SID INT NOT NULL,
	name VARCHAR(50) NOT NULL,
	year INT NOT NULL,
	drawNum INT NOT NULL, 
	drawTime DATETIME, -- Students not living on campus don't get a draw time
	drawGroup ENUM('1', '2', '3', '4', '5', '6', '7', '8', '9') NOT NULL,
	isDrawing BOOL NOT NULL DEFAULT 1,
	dormRoomNum INT, -- Students not living on campus don't draw for a room
	dormName VARCHAR(50),
	isSuiteRepresentative BOOL,
	avgSuiteGroupDrawNum DOUBLE,
    suiteDrawTime DATETIME,
	PRIMARY KEY (SID),
	FOREIGN KEY (avgSuiteGroupDrawNum) REFERENCES ProspectiveSuiteGroup(avgDrawNum),
	FOREIGN KEY (dormRoomNum, dormName) REFERENCES DormRoom(number, dormName));

CREATE TABLE IF NOT EXISTS DrawsUp (
  higherStudent INT NOT NULL,
  lowerStudent INT NOT NULL,
  PRIMARY KEY (higherStudent),
  FOREIGN KEY (higherStudent) REFERENCES Student(SID),
  FOREIGN KEY (lowerStudent) REFERENCES Student(SID));

CREATE TABLE IF NOT EXISTS Wishes (
  SID INT NOT NULL,
  dormRoomNum INT NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  PRIMARY KEY (SID),
  FOREIGN KEY (SID) REFERENCES Student(SID),
  FOREIGN KEY (dormRoomNum, dormName) REFERENCES DormRoom(number, dormName));

CREATE TABLE IF NOT EXISTS CommonRoom (
  number INT NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  hasStove BOOL NOT NULL,
  hasSink BOOL NOT NULL,
  hasRefrigerator BOOL NOT NULL,
  hasBathroom BOOL NOT NULL,
  PRIMARY KEY (number, dormName),
  FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

DELIMITER $$

DROP TRIGGER IF EXISTS prospective_suite_group_constraints$$
CREATE TRIGGER prospective_suite_group_constraints AFTER INSERT ON ProspectiveSuiteGroup
	FOR EACH ROW BEGIN
		IF EXISTS (
		    SELECT *
		    FROM ProspectiveSuiteGroup AS p
		    WHERE p.avgDrawNum NOT IN
    		    (SELECT DISTINCT s.avgSuiteGroupDrawNum
    		    FROM Student AS s, ProspectiveSuiteGroup AS p
    		    WHERE p.avgDrawNum = s.avgSuiteGroupDrawNum) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ProspectiveSuiteGroup does not satisfy constraints!';
		END IF;
    END$$
    
DROP TRIGGER IF EXISTS closet_type_constraints$$
CREATE TRIGGER closet_type_constraints AFTER INSERT ON ClosetType
	FOR EACH ROW BEGIN 
		IF EXISTS (
			SELECT *
			FROM ClosetType AS c
			WHERE c.typeName NOT IN
				(SELECT c.typeName
				FROM ClosetType AS c, DormRoom AS dm
				WHERE c.typeName = dm.closetType) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ClosetType does not satisfy constraints!';
		END IF;
	END$$

DROP TRIGGER IF EXISTS window_type_constraints$$
CREATE TRIGGER window_type_constraints AFTER INSERT ON WindowType
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM WindowType AS w
			WHERE w.typeName NOT IN
				(SELECT w.typeName
				FROM WindowType AS w, Room AS r
				WHERE w.typeName = r.windowType) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
		END IF;
	END$$
 
 
DROP TRIGGER IF EXISTS suite_constraints$$
CREATE TRIGGER suite_constraints AFTER INSERT ON Suite
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM Suite AS s
			WHERE s.suiteID NOT IN
				(SELECT s.suiteID
				FROM Suite AS s, Room AS r
				WHERE s.suiteID = r.suite) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
		END IF;
	END$$

DROP TRIGGER IF EXISTS draws_up_constraints$$
CREATE TRIGGER draws_up_constraints AFTER INSERT ON DrawsUp
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM DrawsUp as du1, DrawsUp as du2
			WHERE du1.higherStudent = du2.lowerStudent ) -- a student drawing someone up cannot be drawn up, and a student being drawn up cannot draw someone else up
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'DrawsUp does not satisfy constraints!';
		END IF;
	END$$
        
DROP TRIGGER IF EXISTS student_constraints$$
CREATE TRIGGER student_constraints AFTER INSERT ON Student
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM Student
			WHERE isDrawing IS TRUE
				  AND drawTime IS NULL)
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'All drawing students need a draw time -- Student does not satisfy constraints!';
		END IF;
	END$$

    
-- used to check after the draw if all students living on campus (isDrawing = true) have drawn rooms
DROP FUNCTION IF EXISTS checkStudentsChooseRooms$$
CREATE FUNCTION checkStudentsChooseRooms()
RETURNS BOOL
DETERMINISTIC
BEGIN
		RETURN NOT EXISTS (
			    SELECT *
			    FROM Student as s
			    WHERE s.isDrawing IS TRUE
					  AND s.dormRoomNum IS NULL
                      AND s.dormName IS NULL );  -- the dorm of the connecting room must be the same as that of the dorm room
END $$

DROP FUNCTION IF EXISTS checkSuiteHasRepresentative$$
CREATE FUNCTION checkSuiteHasRepresentative()
RETURNS BOOL
DETERMINISTIC
BEGIN
		RETURN NOT EXISTS (
			SELECT *   
             FROM  
				(SELECT avgSuiteGroupDrawNum, max(isSuiteRep) AS containsSuiteREP
                FROM Student 
                WHERE avgSuiteGroupDrawNum IS NOT NULL 
                GROUP BY avgSuiteGroupDrawNum)
                AS
                suiteGroups
			WHERE suiteGroups.containsSuiteRep IS FALSE ); 
END $$

DELIMITER ;
