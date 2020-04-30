CREATE TABLE IF NOT EXISTS Dorm (
    name VARCHAR(50) NOT NULL,
    campusEnd ENUM('NORTH', 'SOUTH') NOT NULL,
    locationDescription VARCHAR(50),
    otherDescription VARCHAR(100),
    PRIMARY KEY (name));

 CREATE TABLE IF NOT EXISTS Suite (
  	suiteID VARCHAR(50) NOT NULL,
  	isSubFree BOOLEAN NOT NULL,
  	numRooms INT NOT NULL,
  	numPeople INT NOT NULL,
  	dormName VARCHAR(50) NOT NULL,
  	otherDescription VARCHAR(100),
  	FOREIGN KEY (dormName) REFERENCES Dorm(name),
  	PRIMARY KEY (suiteID));

CREATE TABLE IF NOT EXISTS SuiteGroup (
    emailID CHAR(8) NOT NULL,
    avgDrawNum DOUBLE NOT NULL, -- students with the same avgDrawNum are in the same group
    avgDrawTime DATETIME,
    isSuiteRepresentative BOOLEAN NOT NULL,
    suiteID VARCHAR(50) NULL,
    FOREIGN KEY (emailID) REFERENCES Student(emailID),
    FOREIGN KEY (suiteID) REFERENCES Suite(suiteID),
    PRIMARY KEY (emailID)); -- a student can't be part of multiple prospective suite groups

CREATE TABLE IF NOT EXISTS Room (
	dormName VARCHAR(50) NOT NULL,
	number VARCHAR(10) NOT NULL,
	dimensionsDescription VARCHAR(250) NOT NULL,
	squareFeet DOUBLE NOT NULL,
	isSubFree BOOLEAN NOT NULL DEFAULT FALSE,
	isReservedForSponsorGroup BOOLEAN NOT NULL DEFAULT FALSE,
	windowsDescription VARCHAR(250) NOT NULL,
	suite VARCHAR(50),
	otherDescription VARCHAR(250),
	PRIMARY KEY (number, dormName),
	FOREIGN KEY (dormName) REFERENCES Dorm(name),
	-- FOREIGN KEY (windowType) REFERENCES WindowType(typeName),
	FOREIGN KEY (suite) REFERENCES Suite(suiteID));

CREATE TABLE IF NOT EXISTS DormRoom (
    dormName VARCHAR(50) NOT NULL,
	number VARCHAR(10) NOT NULL,
	numOccupants INT NOT NULL,
	hasPrivateBathroom BOOLEAN NOT NULL DEFAULT FALSE,
	numDoors INT NOT NULL DEFAULT 1,
	closetsDescription VARCHAR(250) NOT NULL,
    bathroomDescription VARCHAR(250),
	connectingRoomNum VARCHAR(10),
	PRIMARY KEY (dormName, number),
	FOREIGN KEY (connectingRoomNum, dormName) REFERENCES DormRoom(number, dormName),
	FOREIGN KEY (dormName, number) REFERENCES Room(dormName, number));

CREATE TABLE IF NOT EXISTS Student (
	emailID CHAR(8) NOT NULL,
	name VARCHAR(50) NOT NULL,
	year ENUM('1','2','3') NOT NULL,
	drawNum INT NOT NULL,
	drawTime DATETIME, -- Students not living on campus don't get a draw time
	drawGroup ENUM('1', '2', '3', '4', '5', '6', '7', '8', '9') NOT NULL,
	isDrawing BOOLEAN NOT NULL DEFAULT TRUE,
	dormRoomNum VARCHAR(10), -- Students not living on campus don't draw for a room
	dormName VARCHAR(50),
    roommateEID CHAR(8) NOT NULL,
    PRIMARY KEY (emailID),
	FOREIGN KEY (dormRoomNum, dormName) REFERENCES DormRoom(number, dormName));

CREATE TABLE IF NOT EXISTS WishList (
  emailID CHAR(8) NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  dormRoomNum VARCHAR(10) NOT NULL,
  PRIMARY KEY (emailID, dormName, dormRoomNum),
  FOREIGN KEY (emailID) REFERENCES Student(emailID),
  FOREIGN KEY (dormName, dormRoomNum) REFERENCES DormRoom(dormName, number));

CREATE TABLE IF NOT EXISTS CommonRoom (
  number VARCHAR(10) NOT NULL,
  dormName VARCHAR(50) NOT NULL,
  hasStove BOOLEAN NOT NULL,
  hasSink BOOLEAN NOT NULL,
  hasRefrigerator BOOLEAN NOT NULL,
  hasBathroom BOOLEAN NOT NULL,
  PRIMARY KEY (number, dormName),
  FOREIGN KEY (number, dormName) REFERENCES Room(number, dormName));
