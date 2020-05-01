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

DROP PROCEDURE IF EXISTS GetDormRoomsSinglesSummary$$
CREATE PROCEDURE GetDormRoomsSinglesSummary()
BEGIN
	SELECT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, Room AS r
	WHERE dr.number = r.number AND dr.dormName = r.dormName AND r.suite IS NULL -- this is for singles/doubles draw, NOT suite draw
	ORDER BY r.dormName, r.number; -- group first by dorm, alphabetically, then group data by number for later processing
END $$

DROP PROCEDURE IF EXISTS GetRoomDetails$$
CREATE PROCEDURE GetRoomDetails(  -- common or dorm
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	SELECT r.dormName, r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum, dr.closetsDescription, dr.bathroomDescription
	FROM DormRoom AS dr, Room AS r
	WHERE r.dormName = dormName AND r.number = roomNum
		  AND dr.dormName = r.dormName AND dr.number = r.number;

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
