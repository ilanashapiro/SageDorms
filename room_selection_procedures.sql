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

DROP PROCEDURE IF EXISTS GetDormRoomSinglesSummary$$
CREATE PROCEDURE GetDormRoomSinglesSummary()
BEGIN
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r
	WHERE dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL -- this is for singles/doubles draw, NOT suite draw
		  AND NOT EXISTS (SELECT * FROM Student AS s WHERE s.dormName = dr.dormName AND s.dormRoomNum = dr.number) --  we only want rooms that are still free
	ORDER BY r.dormName, r.number; -- group first by dorm, alphabetically, then group data by number for later processing
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
		  AND dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL -- this is for singles/doubles draw, NOT suite draw
		  AND NOT EXISTS (SELECT * FROM Student AS s where s.dormName = dr.dormName AND s.dormRoomNum = dr.number); --  we only want rooms that are still free
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
	ORDER BY r.number;
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
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, r.isSubFree, dr.connectingRoomNum, r.otherDescription
	-- the old version when we thought we could support more detail. May bring this back in the future
	 -- r.dormName, r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription, r.isSubFree, dr.numOccupants, dr.connectingRoomNum, dr.closetsDescription, dr.bathroomDescription
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
