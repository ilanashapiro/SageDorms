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

DROP PROCEDURE IF EXISTS InfoIfInMyWishList$$
CREATE PROCEDURE GetMyWishList(
	IN emailID CHAR(8),
	IN dormName VARCHAR(50),
	IN roomNum VARCHAR(10)
)
BEGIN
	SELECT w.dormName, w.dormRoomNum
	FROM WishList AS w
	WHERE w.dormRoomNum = roomNum
		  AND w.dormName = dormName
		  AND w.emailID = emailID;
END $$

DELIMITER ;
