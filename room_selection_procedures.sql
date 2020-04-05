-- THIS CODE IS NOT CORRECT. THIS IS A BOILERPLATE THAT WILL BE REBUILT DYNAMICALLY IN THE PYTHON FILE TO HANDLE NULL VALUES
DELIMITER $$

CREATE PROCEDURE SelectRooms(
	IN dormNum INT,
	IN dormName VARCHAR(50),
	IN numOccupants INT,
	IN hasPrivateBathroom BOOL,
	IN numDoors INT,
	IN closetType VARCHAR(50),
	IN connectingRoomNum INT,
	IN floorNum INT,
	IN lengthDescription VARCHAR(50),
	IN widthDescription VARCHAR(50),
	IN squareFeet DOUBLE,
	IN isSubFree BOOL,
	IN isReservedForSponsorGroup BOOL,
	IN windowType VARCHAR(50),
	IN suite VARCHAR(50),
	IN otherDescription VARCHAR(100)
)
BEGIN
	SET myParam = IFNULL(myParam, 0);
	SELECT *
	FROM DormRoom AS dr, Room AS r
	WHERE dr.dormName LIKE dormName
			  AND dr.number LIKE dormNum
			  AND dr.dormName LIKE r.dormName
			  AND dr.number LIKE r.number
        AND dr.numOccupants LIKE numOccupants
        AND dr.hasPrivateBathroom LIKE hasPrivateBathroom
        AND dr.numDoors LIKE numDoors
        AND dr.closetType LIKE closetType
        AND dr.connectingRoomNum LIKE connectingRoom
        AND r.floorNum LIKE floorNum
        AND r.lengthDescription LIKE lengthDescription
        AND r.widthDescription LIKE widthDescription
        AND r.squareFeet LIKE squareFeet
        AND r.isSubFree LIKE isSubFree
        AND r.isReservedForSponsorGroup LIKE isReservedForSponsorGroup
				AND r.windowType LIKE windowType
				AND r.suite LIKE suite
				AND r.otherDescription LIKE otherDescription;
END $$

DELIMITER ;
