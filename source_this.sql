DELIMITER $$

DROP PROCEDURE IF EXISTS AddDorms$$
CREATE PROCEDURE AddDorms()
BEGIN
    INSERT INTO Dorm (name, campusEnd) VALUES ('CLARK-I','NORTH');
    INSERT INTO Dorm (name, campusEnd) VALUES ('CLARK-V', 'NORTH');
    INSERT INTO Dorm (name, campusEnd) VALUES ('LAWRY', 'NORTH');
    INSERT INTO Dorm (name, campusEnd) VALUES ('WALKER', 'NORTH');
    INSERT INTO Dorm (name, campusEnd) VALUES ('SMILEY', 'NORTH');
    INSERT INTO Dorm (name, campusEnd) VALUES ('NORTON-CLARK', 'NORTH');
END $$

DROP PROCEDURE IF EXISTS AddStudents$$
CREATE PROCEDURE AddStudents()
BEGIN
    INSERT INTO STUDENT (emailID, name, year, drawNum, drawGroup) VALUES ('hpaa2018', 'Helen Paulini', 3, 810, 6);
    INSERT INTO STUDENT (emailID, name, year, drawNum, drawGroup) VALUES ('ymac2018', 'Yurie Muramatsu', 2, 635, 7);
    INSERT INTO STUDENT (emailID, name, year, drawNum, drawGroup) VALUES ('ayza2018', 'Alan Zhou', 2, 844, 6);
    INSERT INTO STUDENT (emailID, name, year, drawNum, drawGroup) VALUES ('gpaa2018', 'Gabe Alzate', 3, 150, 1);
END $$

DELIMITER ;
DELIMITER $$

DROP PROCEDURE IF EXISTS SetStudentRoom$$
CREATE PROCEDURE SetStudentRoom(
	IN emailID CHAR(8),
	IN roommateEID CHAR(8),
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	UPDATE Student AS s
	SET s.dormName = dormName, s.dormRoomNum = roomNum
	WHERE s.emailID = emailID OR s.emailID = roommateEID;

	UPDATE Student AS s
	SET s.roommateEID = roommateEID
	WHERE s.emailID = emailID;

	UPDATE Student AS s
	SET s.roommateEID = emailID
	WHERE s.emailID = roommateEID;
END $$

-- gets the summary if the room hasn't been selected yet. Used for the search results in Search Rooms
DROP PROCEDURE IF EXISTS GetSummaryForDormRoom$$
CREATE PROCEDURE GetSummaryForDormRoom(
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, dr.numOccupants, r.isSubFree, dr.hasPrivateBathroom, dr.bathroomDescription,
		   r.windowsDescription, dr.closetsDescription, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.number = roomNum AND r.dormName = dormName
		  AND dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL -- this is for singles/doubles draw, NOT suite draw
		  AND NOT EXISTS (SELECT * FROM Student AS s where s.dormName = dr.dormName AND s.dormRoomNum = dr.number); --  we only want rooms that are still free
END $$

-- generic: gets summary even if room has been selected. This is used for the informational summary of rooms on the "View Dorms" page
-- (NOT used for Search Rooms -- that is updated based on rooms that have been selected, as this is where students actually select rooms)
DROP PROCEDURE IF EXISTS GetSummaryForDormRoomGeneric$$
CREATE PROCEDURE GetSummaryForDormRoomGeneric(
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, dr.numOccupants, r.isSubFree, dr.hasPrivateBathroom, dr.bathroomDescription,
		   r.windowsDescription, dr.closetsDescription, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.number = roomNum AND r.dormName = dormName
		  AND dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL; -- this is for singles/doubles draw, NOT suite draw
END $$

-- a true summary, informational only. This is just for informational purposes and displays ALL data, even rooms and suites that have been selected.
DROP PROCEDURE IF EXISTS GetDormRoomSummaryForDorm$$
CREATE PROCEDURE GetDormRoomSummaryForDorm(
	IN dormName VARCHAR(50)
)
BEGIN
	-- dorm room info
	SELECT DISTINCT r.dormName, r.number
	FROM DormRoom AS dr, Room AS r
	WHERE r.dormName = dormName
		  AND dr.dormName = r.dormName AND dr.number = r.number AND r.suite IS NULL
		  AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where r.suite = sg.suiteID) -- the room is not part of a suite
	ORDER BY cast(r.number as unsigned);
END $$

DROP PROCEDURE IF EXISTS GetMyRoomDetails$$
CREATE PROCEDURE GetMyRoomDetails(
	IN emailID CHAR(8)
)
BEGIN
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, dr.numOccupants, r.isSubFree, dr.hasPrivateBathroom, dr.bathroomDescription,
		   r.windowsDescription, dr.closetsDescription, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, Student AS s
	WHERE dr.dormName = r.dormName
		  AND dr.number = r.number
		  AND r.dormName = s.dormName
		  AND r.number = s.dormRoomNum
		  AND s.emailID = emailID;
END $$

DROP PROCEDURE IF EXISTS GetMyRoommateInfo$$
CREATE PROCEDURE GetMyRoommateInfo(
	IN emailID CHAR(8)
)
BEGIN
	SELECT roommate.name, roommate.emailID
	FROM Student AS myself, Student AS roommate
	WHERE myself.emailID = emailID
		  AND myself.roommateEID = roommate.emailID;
END $$

DELIMITER ;
DELIMITER $$

-- a true summary, informational only. This is just for informational purposes and displays ALL data, even rooms and suites that have been selected.
DROP PROCEDURE IF EXISTS GetSuitesForDorm$$
CREATE PROCEDURE GetSuitesForDorm(
	IN dormName VARCHAR(50)
)
BEGIN
-- suite info
	SELECT s.suiteID
	FROM Suite AS s
	WHERE s.dormName = dormName;
END $$

DROP PROCEDURE IF EXISTS GetMySuiteDetails$$
CREATE PROCEDURE GetMySuiteDetails(
	IN emailID CHAR(8)
)
BEGIN
	-- suite info
	SELECT s.suiteID, s.dormName, s.isSubFree, s.numRooms, s.numPeople, s.otherDescription
	FROM Suite AS s, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND s.suiteID = sg.suiteID;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY cast(r.number as unsigned);

	-- common room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, r.otherDescription,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY cast(r.number as unsigned);
END $$

DROP PROCEDURE IF EXISTS GetSuiteSummaryForSuite$$
CREATE PROCEDURE GetSuiteSummaryForSuite(
	IN suiteID VARCHAR(50)
)
BEGIN
	-- suite info
	SELECT *
	FROM Suite AS s
	WHERE s.suiteID = suiteID AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where sg.suiteID = s.suiteID); --  we only want suites that are still free;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, Suite AS s
	WHERE r.suite = suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
		  AND s.suiteID = suiteID
		  AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where sg.suiteID = s.suiteID) -- not part of a suite that has been selected already (i.e still free)
	ORDER BY cast(r.number as unsigned);

	-- common room info
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr, Suite AS s
	WHERE r.suite = suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
		  AND s.suiteID = suiteID
		  AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where sg.suiteID = s.suiteID) -- not part of a suite that has been selected already (i.e still free)
	ORDER BY cast(r.number as unsigned);
END $$

-- generic: gets summary even if suite has been selected. This is used for the informational summary of suites on the "View Dorms" page
-- (NOT used for Search Suites -- that is updated based on rooms that have been selected, as this is where students actually select suites)
DROP PROCEDURE IF EXISTS GetSuiteSummaryForSuiteGeneric$$
CREATE PROCEDURE GetSuiteSummaryForSuiteGeneric(
	IN suiteID VARCHAR(50)
)
BEGIN
	-- suite info
	SELECT *
	FROM Suite AS s
	WHERE s.suiteID = suiteID;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, Suite AS s
	WHERE r.suite = suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
		  AND s.suiteID = suiteID
	ORDER BY cast(r.number as unsigned);

	-- common room info
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr
	WHERE r.suite = suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY cast(r.number as unsigned);
END $$

DROP PROCEDURE IF EXISTS RemoveMyselfFromSuiteGroup$$
CREATE PROCEDURE RemoveMyselfFromSuiteGroup(
	IN emailID CHAR(8)
)
BEGIN
	-- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	-- business logic ensures the suite rep cannot remove themself, unless they are the last person remaining in the group and are thus dissolving the group
	UPDATE /*+ NO_MERGE(average)*/ SuiteGroup AS sg,
		(SELECT avg(DISTINCT s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID != emailID
			  AND s.emailID IN (SELECT s.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailID))) AS average
	SET sg.avgDrawNum = average.avgDrawNum
	WHERE sg.emailID != emailID
		  AND sg.emailID IN (SELECT * FROM (SELECT sg.emailID
	  												FROM SuiteGroup AS sg
	  												WHERE sg.avgDrawNum IN
	  													  (SELECT sg.avgDrawNum
	  													  FROM SuiteGroup AS sg
	  													  WHERE sg.emailID = emailID)) AS mySG);

	DELETE
	FROM SuiteGroup AS sg
	WHERE sg.emailID = emailID; -- delete the student from the suite group. This can be done anythime (including during suite draw) before their suite draw time is reached
END $$

DROP PROCEDURE IF EXISTS AddMyselfToSuiteGroup$$
CREATE PROCEDURE AddMyselfToSuiteGroup(
	IN emailID CHAR(8),
	IN emailIDInSG CHAR(8),
	IN isNewSuiteRep BOOLEAN
)
BEGIN
	INSERT INTO SuiteGroup (emailID, avgDrawNum, isSuiteRepresentative) VALUES (emailID, 0.0, 0);

	-- recompute average draw num for all members of group (including your newly added self).
	UPDATE /*+ NO_MERGE(average) */ SuiteGroup AS sg,
		(SELECT avg(DISTINCT s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID = emailID
			  OR s.emailID IN (SELECT sg.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailIDInSG))) AS average
	SET sg.avgDrawNum = average.avgDrawNum
	WHERE sg.emailID = emailID OR sg.emailID IN (SELECT * FROM (SELECT sg.emailID
										FROM SuiteGroup AS sg
										WHERE sg.avgDrawNum IN
											  (SELECT sg.avgDrawNum
											  FROM SuiteGroup AS sg
											  WHERE sg.emailID = emailIDInSG)) AS mySG);

		-- If someone else was originally the SG rep and now you are, update this
		IF isNewSuiteRep AND emailIDInSG IN (SELECT sg.emailID
										     FROM SuiteGroup AS sg
										     WHERE sg.avgDrawNum IN (SELECT avgDrawNum
											   					  FROM SuiteGroup AS sg
																  WHERE sg.emailID = emailIDInSG)
											   AND sg.isSuiteRepresentative = TRUE) THEN
		   -- they are no longer suite rep
           UPDATE /*+ NO_MERGE(oldSuiteRep) */ SuiteGroup AS sg,
				(SELECT sg.emailID
				 FROM SuiteGroup AS sg
				 WHERE sg.avgDrawNum IN (SELECT avgDrawNum
									  FROM SuiteGroup AS sg
									  WHERE sg.emailID = emailIDInSG)
					   AND sg.isSuiteRepresentative = TRUE) AS oldSuiteRep
			SET sg.isSuiteRepresentative = FALSE WHERE sg.emailID = oldSuiteRep.emailID;

			-- you become new suite rep
			UPDATE SuiteGroup AS sg
			SET sg.isSuiteRepresentative = TRUE WHERE sg.emailID = emailID;
		END IF;
	END $$

DROP PROCEDURE IF EXISTS GetMySuiteGroup$$
CREATE PROCEDURE GetMySuiteGroup(
	IN emailID CHAR(8)
)
BEGIN
	SELECT DISTINCT s.name, s.emailID, sg.isSuiteRepresentative, sg.avgDrawNum
	FROM Student AS s, SuiteGroup AS sg
	WHERE s.emailID IN (SELECT sg.emailID
		  				  FROM SuiteGroup AS sg
					  	  WHERE sg.avgDrawNum IN
							    (SELECT sg.avgDrawNum
				  			    FROM SuiteGroup AS sg
						  	    WHERE sg.emailID = emailID))
		  AND sg.emailID = s.emailID;
END $$

DROP PROCEDURE IF EXISTS SetSuite$$
CREATE PROCEDURE SetSuite(
	IN suiteID VARCHAR(50),
	IN emailIDSuiteRep CHAR(8)
)
BEGIN
	UPDATE /*+ NO_MERGE(mygroup) */ SuiteGroup AS sg,
		(SELECT sg.emailID
		FROM SuiteGroup AS sg
		WHERE sg.avgDrawNum IN
			  (SELECT sg.avgDrawNum
			  FROM SuiteGroup AS sg
			  WHERE sg.emailID = emailIDSuiteRep)) AS mygroup
	SET sg.suiteID = suiteID
	WHERE sg.emailID = mygroup.emailID;
END $$

DROP PROCEDURE IF EXISTS SetSuiteRepresentative$$
CREATE PROCEDURE SetSuiteRepresentative(
	IN emailID CHAR(8)
)
BEGIN
	-- old suite rep is no longer suite rep
   	UPDATE /*+ NO_MERGE(oldSuiteRep) */ SuiteGroup AS sg,
   		(SELECT sg.emailID
   		 FROM SuiteGroup AS sg
   		 WHERE sg.avgDrawNum IN (SELECT avgDrawNum
   							  FROM SuiteGroup AS sg
   							  WHERE sg.emailID = emailID)
   			   AND sg.isSuiteRepresentative = TRUE) AS oldSuiteRep
   	SET sg.isSuiteRepresentative = FALSE WHERE sg.emailID = oldSuiteRep.emailID AND sg.emailID != emailID;

	-- you become new suite rep
	UPDATE SuiteGroup AS sg
	SET sg.isSuiteRepresentative = TRUE WHERE sg.emailID = emailID;
END $$

DELIMITER ;
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
	PRIMARY KEY (dormName, number),
	FOREIGN KEY (dormName) REFERENCES Dorm(name),
	FOREIGN KEY (suite) REFERENCES Suite(suiteID));

CREATE TABLE IF NOT EXISTS DormRoom (
    dormName VARCHAR(50) NOT NULL,
	number VARCHAR(10) NOT NULL,
	numOccupants INT NOT NULL,
	hasPrivateBathroom BOOLEAN NOT NULL DEFAULT FALSE,
	numDoors INT NOT NULL DEFAULT 1,
	closetsDescription VARCHAR(250),
    bathroomDescription VARCHAR(250),
	connectingRoomNum VARCHAR(10),
	PRIMARY KEY (dormName, number),
	FOREIGN KEY (dormName, connectingRoomNum) REFERENCES DormRoom(dormName, number),
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
    roommateEID CHAR(8) NULL,
    PRIMARY KEY (emailID),
	FOREIGN KEY (dormName, dormRoomNum) REFERENCES DormRoom(dormName, number));

CREATE TABLE IF NOT EXISTS SuiteGroup (
    emailID CHAR(8) NOT NULL,
    avgDrawNum DOUBLE NOT NULL, -- students with the same avgDrawNum are in the same group
    avgDrawTime DATETIME,
    isSuiteRepresentative BOOLEAN NOT NULL,
    suiteID VARCHAR(50) NULL,
    FOREIGN KEY (emailID) REFERENCES Student(emailID),
    FOREIGN KEY (suiteID) REFERENCES Suite(suiteID),
    PRIMARY KEY (emailID)); -- a student can't be part of multiple prospective suite groups

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
  PRIMARY KEY (dormName, number),
  FOREIGN KEY (dormName, number) REFERENCES Room(dormName, number));
DELIMITER $$

DROP PROCEDURE IF EXISTS AddToWishlist$$
CREATE PROCEDURE AddToWishlist(
	IN emailID CHAR(8),
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	INSERT INTO WishList (emailID, dormName, dormRoomNum) VALUES (emailID, dormName, roomNum);
END $$

DROP PROCEDURE IF EXISTS DeleteFromWishList$$
CREATE PROCEDURE DeleteFromWishList(
	IN emailID CHAR(8),
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	DELETE
	FROM WishList AS w
	WHERE w.dormRoomNum = roomNum
		  AND w.dormName = dormName
		  AND w.emailID = emailID;
END $$

DROP PROCEDURE IF EXISTS GetMyWishList$$
CREATE PROCEDURE GetMyWishList(
	IN emailID CHAR(8)
)
BEGIN
	SELECT w.dormName, w.dormRoomNum
	FROM WishList AS w
	WHERE w.emailID = emailID;
END $$

DELIMITER ;
