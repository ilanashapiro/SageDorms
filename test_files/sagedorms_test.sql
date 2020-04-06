-- USE Test;

DROP TRIGGER IF EXISTS prospective_suite_group_constraints;
DELIMITER $$
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
DELIMITER ;

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

CREATE TABLE IF NOT EXISTS ClosetType (
  typeName VARCHAR(50) NOT NULL,
  length INT NOT NULL,
  width INT NOT NULL,
  PRIMARY KEY (typeName));

CREATE TABLE IF NOT EXISTS CommonRoom (
  number INT NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  hasStove BIT NOT NULL,
  hasSink BIT NOT NULL,
  hasRefrigerator BIT NOT NULL,
  hasBathroom BIT NOT NULL,
  PRIMARY KEY (number, dormName),
  FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

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

-- INSERT INTO DormRoom VALUES ();
-- INSERT INTO Student VALUES (123456, "Sam", 2019, 100, "10PM", '1', 18, "Norton", null, null);
	INSERT INTO ProspectiveSuiteGroup VALUES (13.5, "10:00AM");
