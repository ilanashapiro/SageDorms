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
  avgDrawNum DOUBLE(4, 1) NOT NULL,
  avgDrawTime VARCHAR(50) NOT NULL,
  PRIMARY KEY (avgDrawNum));

CREATE TABLE IF NOT EXISTS Suite (
	suiteID VARCHAR(50) NOT NULL,
	isSubFree BIT NOT NULL,
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
	squareFeet DOUBLE(3, 2) NOT NULL,
	isSubFree BIT NOT NULL,
	isReservedForSponsorGroup BIT NOT NULL,
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
	hasPrivateBathroom BIT NOT NULL,
	numDoors INT NOT NULL,
	closetType VARCHAR(50) NOT NULL,
	connectingRoomNum INT,
	connectingDorm VARCHAR(50),
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (connectingRoomNum, connectingDorm) REFERENCES DormRoom(number, dormName),
	FOREIGN KEY (closetType) REFERENCES ClosetType(typeName),
	FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

CREATE TABLE IF NOT EXISTS Student (
		  SID INT NOT NULL,
		  name VARCHAR(50) NOT NULL,
		  year INT NOT NULL,
		  drawNum INT NOT NULL,
		  drawTime VARCHAR(50) NOT NULL,
		  drawGroup ENUM('1', '2', '3', '4', '5', '6', '7', '8', '9') NOT NULL,
		  dormRoomNum INT NOT NULL,
		  dormName VARCHAR(50) NOT NULL,
		  isSuiteRepresentative BIT,
		  avgSuiteGroupDrawNum DOUBLE(4, 1),
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
  hasStove BIT NOT NULL,
  hasSink BIT NOT NULL,
  hasRefrigerator BIT NOT NULL,
  hasBathroom BIT NOT NULL,
  PRIMARY KEY (number, dormName),
  FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

DELIMITER $$
DROP TRIGGER IF EXISTS prospective_suite_group_constraints$$
CREATE
	TRIGGER prospective_suite_group_constraints AFTER INSERT ON ProspectiveSuiteGroup
	FOR EACH ROW BEGIN
		IF EXISTS (
		    SELECT p.avgDrawNum
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
CREATE
		TRIGGER closet_type_constraints AFTER INSERT ON ClosetType
		FOR EACH ROW BEGIN
			IF EXISTS (
			    SELECT c.typeName
			    FROM ClosetType AS c
			    WHERE c.typeName NOT IN
	    		    (SELECT DISTINCT c.typeName
	    		    FROM ClosetType AS c, DormRoom AS dm
	    		    WHERE c.typeName = dm.closetType) )
			THEN
				SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ClosetType does not satisfy constraints!';
			END IF;
	    END$$

DROP TRIGGER IF EXISTS window_type_constraints$$
CREATE
		TRIGGER window_type_constraints AFTER INSERT ON WindowType
		FOR EACH ROW BEGIN
			IF EXISTS (
			    SELECT w.typeName
			    FROM WindowType AS w
			    WHERE w.typeName NOT IN
	    		    (SELECT DISTINCT w.typeName
	    		    FROM WindowType AS w, Room AS r
	    		    WHERE w.typeName = r.windowType) )
			THEN
				SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ClosetType does not satisfy constraints!';
			END IF;
	    END$$
        
DROP TRIGGER IF EXISTS suite_constraints$$
CREATE
		TRIGGER suite_constraints AFTER INSERT ON Suite
		FOR EACH ROW BEGIN
			IF EXISTS (
			    SELECT s.typeName
			    FROM Suite AS s
			    WHERE s.typeName NOT IN
	    		    (SELECT DISTINCT s.typeName
	    		    FROM Suite AS s, Room AS r
	    		    WHERE w.suiteID = r.suite) )
			THEN
				SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
			END IF;
	    END$$

DROP TRIGGER IF EXISTS draw_up_constraints$$
CREATE
		TRIGGER draw_up_constraints AFTER INSERT ON DrawsUp
		FOR EACH ROW BEGIN
			IF EXISTS (
			    SELECT *
			    FROM DrawsUp as du1, DrawsUp as du2
			    WHERE du1.higherStudent = du2.lowerStudent ) -- a student drawing someone up cannot be drawn up, and a student being drawn up cannot draw someone else up
			THEN
				SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'DrawsUp does not satisfy constraints!';
			END IF;
	    END$$
        
DROP TRIGGER IF EXISTS dorm_room_constraints$$
CREATE
		TRIGGER dorm_room_constraints AFTER INSERT ON DormRoom
		FOR EACH ROW BEGIN
			IF EXISTS (
			    SELECT *
			    FROM DormRoom as dm, DormRoom as cm
			    WHERE dm.connectingRoomNum = cm.number
					  AND dm.connectingDorm = cm.dormName
                      AND dm.dormName != cm.dormName ) -- the dorm of the connecting room must be the same as that of the dorm room
			THEN
				SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'DrawsUp does not satisfy constraints!';
			END IF;
	    END$$
    
DELIMITER ;
-- INSERT INTO DormRoom VALUES ();
-- INSERT INTO Student VALUES (123456, "Sam", 2019, 100, "10PM", '1', 18, "Norton", null, null);
-- INSERT INTO ClosetType VALUES ("crank", 5, 5);
-- INSERT INTO ProspectiveSuiteGroup VALUES (13.5, "10:00AM");
