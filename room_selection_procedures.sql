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
-- CREATE PROCEDURE DisplayRoomDetails(
--
-- )
