-- CREATE TABLE IF NOT EXISTS ClosetType (
--     typeName VARCHAR(50) NOT NULL,
--     otherDescription VARCHAR(50)
--     PRIMARY KEY (typeName));
--
-- CREATE TABLE IF NOT EXISTS WindowType (
--     typeName VARCHAR(50) NOT NULL,
--     directionFacing ENUM('NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTHEAST', 'NORTHWEST',
--                        'SOUTHEAST', 'SOUTHWEST'),
--     viewDescription VARCHAR(100) NOT NULL,
--     PRIMARY KEY (typeName));

CREATE TABLE IF NOT EXISTS Dorm (
    name VARCHAR(50) NOT NULL,
    campusEnd ENUM('NORTH', 'SOUTH'),
    locationDescription VARCHAR(50) NOT NULL,
    otherDescription VARCHAR(100),
    PRIMARY KEY (name));

 CREATE TABLE IF NOT EXISTS Suite (
  	suiteID VARCHAR(50) NOT NULL,
  	isSubFree BOOL NOT NULL,
  	numRooms INT NOT NULL,
  	numPeople INT NOT NULL,
  	dormName VARCHAR(50) NOT NULL,
  	otherDescription VARCHAR(100),
  	FOREIGN KEY (dormName) REFERENCES Dorm(name),
  	PRIMARY KEY (suiteID));

CREATE TABLE IF NOT EXISTS SuiteGroup (
    emailID VARCHAR(8) NOT NULL,
    avgDrawNum DOUBLE NOT NULL, -- students with the same avgDrawNum are in the same group
    avgDrawTime DATETIME,
    isSuiteRepresentative BOOL NOT NULL,
    suiteID VARCHAR(50) NULL,
    FOREIGN KEY (emailID) REFERENCES Student(emailID),
    FOREIGN KEY (suiteID) REFERENCES Suite(suiteID),
    PRIMARY KEY (emailID)); -- a student can't be part of multiple prospective suite groups

CREATE TABLE IF NOT EXISTS Room (
	number INT NOT NULL,
	dormName VARCHAR(50) NOT NULL,
	floorNum INT NOT NULL,
	lengthDescription VARCHAR(50) NOT NULL,
	widthDescription VARCHAR(50) NOT NULL,
	squareFeet DOUBLE NOT NULL,
	isSubFree BOOL NOT NULL,
	isReservedForSponsorGroup BOOL NOT NULL,
	windowsDescription VARCHAR(100) NOT NULL,
	suite VARCHAR(50),
	otherDescription VARCHAR(100),
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (dormName) REFERENCES Dorm(name),
	-- FOREIGN KEY (windowType) REFERENCES WindowType(typeName),
	FOREIGN KEY (suite) REFERENCES Suite(suiteID));

CREATE TABLE IF NOT EXISTS DormRoom (
	number INT NOT NULL,
	dormName VARCHAR(50) NOT NULL,
	numOccupants INT NOT NULL,
	hasPrivateBathroom BOOL NOT NULL,
	numDoors INT NOT NULL,
	closetsDescription VARCHAR(100),
    bathroomDescription VARCHAR(100),
	connectingRoomNum INT,
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (connectingRoomNum, dormName) REFERENCES DormRoom(number, dormName),
	-- FOREIGN KEY (closetType) REFERENCES ClosetType(typeName),
	FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));

CREATE TABLE IF NOT EXISTS Student (
	emailID VARCHAR(8) NOT NULL,
	name VARCHAR(50) NOT NULL,
	year INT NOT NULL,
	drawNum INT NOT NULL,
	drawTime DATETIME, -- Students not living on campus don't get a draw time
	drawGroup ENUM('1', '2', '3', '4', '5', '6', '7', '8', '9') NOT NULL,
	isDrawing BOOL NOT NULL DEFAULT 1,
	dormRoomNum INT, -- Students not living on campus don't draw for a room
	dormName VARCHAR(50),
    PRIMARY KEY (emailID),
	FOREIGN KEY (dormRoomNum, dormName) REFERENCES DormRoom(number, dormName));

-- CREATE TABLE IF NOT EXISTS DrawsUp (
--   higherStudent VARCHAR(26) NOT NULL,
--   lowerStudent VARCHAR(26) NOT NULL,
--   PRIMARY KEY (higherStudent),
--   FOREIGN KEY (higherStudent) REFERENCES Student(emailID),
--   FOREIGN KEY (lowerStudent) REFERENCES Student(emailID));

CREATE TABLE IF NOT EXISTS Wishes (
  emailID VARCHAR(8) NOT NULL,
  dormRoomNum INT NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  PRIMARY KEY (emailID, dormRoomNum, dormName),
  FOREIGN KEY (emailID) REFERENCES Student(emailID),
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
