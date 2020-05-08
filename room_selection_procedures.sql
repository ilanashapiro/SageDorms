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
