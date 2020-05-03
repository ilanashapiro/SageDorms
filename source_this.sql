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
END $$

DROP PROCEDURE IF EXISTS GetDormRoomSinglesSummary$$
CREATE PROCEDURE GetDormRoomSinglesSummary()
BEGIN
	SELECT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r
	WHERE dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL -- this is for singles/doubles draw, NOT suite draw
	ORDER BY r.dormName, r.number; -- group first by dorm, alphabetically, then group data by number for later processing
END $$

DROP PROCEDURE IF EXISTS GetDormRoomAndSuiteSummaryForDorm$$
CREATE PROCEDURE GetDormRoomAndSuiteSummaryForDorm(
	IN dormName VARCHAR(50)
)
BEGIN
	-- dorm room info
	SELECT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r
	WHERE r.dormName = dormName
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY r.number;

	-- suite info
	SELECT s.suiteID, s.numPeople, s.isSubFree
	FROM Room AS r, Suite AS s
	WHERE r.dormName = dormName AND r.suite = s.suiteID
	ORDER BY s.suiteID;

	-- common room info
	SELECT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr
	WHERE r.dormName = dormName
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY r.number;
END $$

DROP PROCEDURE IF EXISTS GetSummaryForDormRoom$$
CREATE PROCEDURE GetSummaryForDormRoom(
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	SELECT r.dormName, r.number, r.squareFeet, dr.numOccupants, r.isSubFree, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.number = roomNum AND r.dormName = dormName
		  AND dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL; -- this is for singles/doubles draw, NOT suite draw
END $$

DROP PROCEDURE IF EXISTS GetRoomDetails$$
CREATE PROCEDURE GetRoomDetails(  -- common or dorm
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	-- dorm room info
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum, dr.closetsDescription, dr.bathroomDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.dormName = dormName AND r.number = roomNum
		  AND dr.dormName = r.dormName AND dr.number = r.number;

	-- common room info
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription,
  		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
  	FROM Room AS r, CommonRoom AS cr
  	WHERE r.dormName = dormName AND r.number = roomNum
  		  AND cr.number = r.number AND cr.dormName = r.dormName;
END $$

DROP PROCEDURE IF EXISTS GetMyRoomDetails$$
CREATE PROCEDURE GetMyRoomDetails(
	IN emailID CHAR(8)
)
BEGIN
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum, dr.closetsDescription, dr.bathroomDescription
	FROM DormRoom AS dr, Room AS r, Student AS s, Student AS roommate
	WHERE dr.dormName = r.dormName
		  AND dr.number = r.number
		  AND r.dormName = s.dormName
		  AND r.number = s.dormRoomNum
		  AND s.emailID = emailID;
END $$

DELIMITER ;
DELIMITER $$

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
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, r.otherDescription,
					dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY r.number;

	-- common room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, r.otherDescription,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY r.number;
END $$

DROP PROCEDURE IF EXISTS GetAllSuitesSummary$$
CREATE PROCEDURE GetAllSuitesSummary()
BEGIN
	-- suite info
	SELECT *
	FROM Suite AS s;

	-- dorm room info
	SELECT DISTINCT r.suite, r.number, r.squareFeet, r.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r
	WHERE r.suite IS NOT NULL
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY r.suite;

	-- common room info
	SELECT DISTINCT r.suite, r.number, r.squareFeet, r.otherDescription,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr
	WHERE r.suite IS NOT NULL
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY r.suite;
END $$

DROP PROCEDURE IF EXISTS GetSuiteSummaryForSuite$$
CREATE PROCEDURE GetSuiteSummaryForSuite(
	IN suiteID VARCHAR(50)
)
BEGIN
	-- suite info
	SELECT *
	FROM Suite AS s
	WHERE s.suiteID = suiteID;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.suite = suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY r.number;

	-- common room info
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr
	WHERE r.suite = suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY r.number;
END $$

DROP PROCEDURE IF EXISTS RemoveMyselfFromSuiteGroup$$
CREATE PROCEDURE RemoveMyselfFromSuiteGroup(
	IN emailID CHAR(8),
	IN newSuiteRepID CHAR(8)
)
BEGIN
	-- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	UPDATE /*+ NO_MERGE(average) */ SuiteGroup AS sg,
		(SELECT avg(s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID != emailID
			  AND s.emailID IN (SELECT s.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailID))) AS average
	SET sg.avgDrawNum = average.avgDrawNum;

	-- If you are the suite group rep and you are leaving, you must specify a new representative
	IF emailID IN (SELECT sg.emailID
				   FROM SuiteGroup AS sg
				   WHERE sg.avgDrawNum IN (SELECT avgDrawNum
					   					FROM SuiteGroup AS sg1
										WHERE sg1.emailID = emailID)
						 AND sg.isSuiteRepresentative = TRUE) THEN
		UPDATE SuiteGroup AS sg
		SET sg.isSuiteRepresentative = TRUE
			WHERE sg.emailID = newSuiteRepID;
	END IF;

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
		(SELECT avg(s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID = emailID
			  OR s.emailID IN (SELECT s.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailIDInSG))) AS average
	SET sg.avgDrawNum = average.avgDrawNum;

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
	SELECT s.name, s.emailID
	FROM Student AS s
	WHERE s.emailID != emailID -- exclude the current student, we just want to see the other ppl in the group
		  AND s.emailID IN (SELECT sg.emailID
		  				  FROM SuiteGroup AS sg
					  	  WHERE sg.avgDrawNum IN
							    (SELECT sg.avgDrawNum
				  			    FROM SuiteGroup AS sg
						  	    WHERE sg.emailID = emailID));
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
-- used to check after the draw if all students living on campus (isDrawing = true) have drawn rooms
DELIMITER $$
DROP FUNCTION IF EXISTS CheckStudentsChooseRooms$$
CREATE FUNCTION CheckStudentsChooseRooms()
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

DROP FUNCTION IF EXISTS CheckSuiteHasRepresentative$$
CREATE FUNCTION CheckSuiteHasRepresentative()
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN NOT EXISTS (
		SELECT *
		FROM
			(SELECT avgSuiteGroupDrawNum, max(isSuiteRep) AS containsSuiteRep
			FROM Student
			WHERE avgSuiteGroupDrawNum IS NOT NULL
			GROUP BY avgSuiteGroupDrawNum)
			AS
			suiteGroups
		WHERE suiteGroups.containsSuiteRep IS FALSE );
END $$

DROP FUNCTION IF EXISTS CheckIfStudentHasRoom$$
CREATE FUNCTION CheckIfStudentHasRoom(
	emailID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM Student AS s
		WHERE s.emailID = emailID AND s.roomNum IS NOT NULL);
END $$

DROP FUNCTION IF EXISTS CheckIfStudentHasSuite$$
CREATE FUNCTION CheckIfStudentHasSuite(
	emailID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM SuiteGroup AS sg
		WHERE sg.emailID = emailID AND sg.suiteID IS NOT NULL);
END $$

DROP FUNCTION IF EXISTS CheckIfNewSuiteRepIsInGroup$$
CREATE FUNCTION CheckIfNewSuiteRepIsInGroup(
	emailID VARCHAR(8),
	newSuiteRepID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM SuiteGroup AS sg
		WHERE sg.newSuiteRepID IN (SELECT s.emailID
								   FROM SuiteGroup AS sg
								   WHERE sg.avgDrawNum IN
									     (SELECT sg.avgDrawNum
									     FROM SuiteGroup AS sg
									     WHERE sg.emailID = emailID)));
END $$
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
	closetsDescription VARCHAR(250) NOT NULL,
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
-- DELIMITER $$
--
-- DROP TRIGGER IF EXISTS closet_type_constraints$$
-- CREATE TRIGGER closet_type_constraints AFTER INSERT ON ClosetType
-- 	FOR EACH ROW BEGIN
-- 		IF EXISTS (
-- 			SELECT *
-- 			FROM ClosetType AS c
-- 			WHERE c.typeName NOT IN
-- 				(SELECT c.typeName
-- 				FROM ClosetType AS c, DormRoom AS dm
-- 				WHERE c.typeName = dm.closetType) )
-- 		THEN
-- 			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ClosetType does not satisfy constraints!';
-- 		END IF;
-- 	END$$
-- 
-- DROP TRIGGER IF EXISTS window_type_constraints$$
-- CREATE TRIGGER window_type_constraints AFTER INSERT ON WindowType
-- 	FOR EACH ROW BEGIN
-- 		IF EXISTS (
-- 			SELECT *
-- 			FROM WindowType AS w
-- 			WHERE w.typeName NOT IN
-- 				(SELECT w.typeName
-- 				FROM WindowType AS w, Room AS r
-- 				WHERE w.typeName = r.windowType) )
-- 		THEN
-- 			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
-- 		END IF;
-- 	END$$


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
