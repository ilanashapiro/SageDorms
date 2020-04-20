DELIMITER $$

CREATE PROCEDURE SetStudentRoom(
	IN email VARCHAR(26),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE Student AS s
	SET s.dormName = dormName, s.dormRoomNum = roomNum
	WHERE s.email = email;
END $$

CREATE PROCEDURE AddToWishlist(
	IN email VARCHAR(26),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE Wishes AS q
	SET w.dormName = dormName, w.dormRoomNum = roomNum
	WHERE s.email = email;
END $$

CREATE PROCEDURE DeleteFromWishList(
	IN email VARCHAR(26),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	DELETE
	FROM Wishes AS w
	WHERE w.dormRoomNum = roomNum
		  AND w.dormName = dormName
		  AND w.email = email;
END $$

-- CREATE PROCEDURE DisplayAllSuitesSummary()
-- BEGIN
-- 	SELECT r.number, s.isSubFree, s.numPeople, s.dormName
-- 	FROM Room AS r, Suite AS s
-- 	WHERE r.suiteID IS NOT NULL
-- 		  AND s.suiteID = r.suiteID
-- 	ORDER BY suiteID ASC
-- END $$
--
-- CREATE PROCEDURE DisplaySuiteDetails(
-- 	IN suiteID VARCHAR(50)
-- )
-- BEGIN
-- 	SELECT
-- 		s.suite isSubFree BOOL NOT NULL,
-- 	  	numRooms INT NOT NULL,
-- 	  	numPeople INT NOT NULL,
-- 	  	dormName VARCHAR(50) NOT NULL,
-- 	  	otherDescription VARCHAR(100),,
-- 		r.number,
-- 		r.dormName,
-- 	FROM Room AS r, Suite AS s
-- 	WHERE r.suiteID = suiteID
-- 		  AND s.suiteID = r.suiteID
-- 	ORDER BY suiteID ASC
-- END $$
--
CREATE PROCEDURE DisplayAllSuitesSummary(
	IN roomNum
	IN dormName
)
BEGIN
	SELECT s.suiteID, s.isSubFree, s.numRooms, s.dormName, s.otherDescription
		   r.number, r.squareFeet, r.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID
	WHERE dr.dormRoomNum = r.roomNum AND dr.dormName = r.dormName
		  AND cr.number = r.number AND cr.dormName = r.dormName
	GROUP BY r.dormName, s.suiteID -- group first by dorm, alphabetically, then group data by suite for later processing
END $$
