DELIMITER $$

CREATE PROCEDURE SetStudentRoom(
	IN SID INT,
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE Student AS s
	SET s.dormName = dormName, s.dormRoomNum = roomNum
	WHERE s.SID = SID;
END $$

CREATE PROCEDURE AddStudentToProspectiveSuiteGroup(
	IN SID INT,
)
BEGIN
	UPDATE Student AS s
	SET s.dormName = dormName, s.dormRoomNum = roomNum
	WHERE s.SID = SID;
END $$

CREATE PROCEDURE AddToWishlist(
	IN SID INT,
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE Wishes AS q
	SET w.dormName = dormName, w.dormRoomNum = roomNum
	WHERE s.SID = SID;
END $$

CREATE PROCEDURE DeleteFromWishList(
	IN SID INT,
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	DELETE
	FROM Wishes AS w
	WHERE w.dormRoomNum = roomNum
		  AND w.dormName = dormName
		  AND w.SID = SID;
END $$

-- THIS CODE IS NOT CORRECT. THIS IS A BOILERPLATE THAT WILL BE REBUILT DYNAMICALLY IN THE PYTHON FILE TO HANDLE NULL VALUES
CREATE PROCEDURE SelectRooms(
	IN dormNum INT,
	IN dormName VARCHAR(50),
	IN numOccupants INT,
	IN hasPrivateBathroom BOOL,
	IN numDoors INT,
	IN closetType VARCHAR(50),
	IN hasConnectingRoom BOOL,
	IN floorNum INT,
	IN squareFeet DOUBLE,
	IN isSubFree BOOL,
	IN windowType VARCHAR(50),
	IN suite VARCHAR(50),
)
BEGIN
	SELECT *
	FROM DormRoom AS dr, Room AS r
	WHERE dr.dormName = dormName
		  AND dr.number = dormNum
		  AND dr.dormName = r.dormName
		  AND dr.number = r.number
          AND dr.numOccupants = numOccupants
          AND dr.hasPrivateBathroom = hasPrivateBathroom
          AND dr.numDoors = numDoors
          AND dr.closetType = closetType
          AND dr.connectingRoomNum IS NOT NULL
          AND r.floorNum = floorNum
          AND r.squareFeet = squareFeet
          AND r.isSubFree = isSubFree
          AND r.isReservedForSponsorGroup = FALSE
		  AND r.windowType = windowType
		  AND r.suite = suite
END $$

DELIMITER ;
