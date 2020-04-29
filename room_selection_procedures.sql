DELIMITER $$

CREATE PROCEDURE SetStudentRoom(
	IN emailID VARCHAR(8),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE Student AS s
	SET s.dormName = dormName, s.dormRoomNum = roomNum
	WHERE s.emailID = emailID;
END $$

CREATE PROCEDURE AddToWishlist(
	IN emailID VARCHAR(8),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	UPDATE WishList AS q
	SET w.dormName = dormName, w.dormRoomNum = roomNum
	WHERE s.emailID = emailID;
END $$

CREATE PROCEDURE DeleteFromWishList(
	IN emailID VARCHAR(8),
	IN dormName INT,
	IN roomNum INT
)
BEGIN
	DELETE
	FROM WishList AS w
	WHERE w.dormRoomNum = roomNum
		  AND w.dormName = dormName
		  AND w.emailID = emailID;
END $$

CREATE PROCEDURE GetMySuiteGroup(
	IN emailID VARCHAR(8)
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

CREATE PROCEDURE RemoveMyselfFromSuiteGroup(
	IN emailID VARCHAR(8),
	IN newSuiteRepID VARCHAR(8)
)
BEGIN
	UPDATE SuiteGroup AS sg -- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	SET sg.avgDrawNum = SELECT avg(s.drawNum)
						FROM Student AS s
						WHERE s.emailID!= emailID
							  AND s.emailID IN (SELECT s.emailID
										  FROM SuiteGroup AS sg
										  WHERE sg.avgDrawNum IN
				   							    (SELECT sg.avgDrawNum
				   				  			    FROM SuiteGroup AS sg
				   						  	    WHERE sg.emailID = emailID)),

		SET sg.isSuiteRepresentative = TRUE
			WHERE newSuiteRepID IS NOT NULL AND sg.emailID = newSuiteRepID
		END IF;

	DELETE
	FROM SuiteGroup AS sg
	WHERE sg.emailID = emailID; -- delete the student from the suite group. This can be done anythime (including during suite draw) before their suite draw time is reached
END $$

CREATE PROCEDURE AddMyselfToSuiteGroup(
	IN emailID VARCHAR(8),
	IN newSuiteRepID VARCHAR(8)
)
BEGIN
	UPDATE SuiteGroup AS sg -- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	SET sg.avgDrawNum = SELECT avg(s.drawNum)
						FROM Student AS s
						WHERE s.emailID!= emailID
							  AND s.emailID IN (SELECT s.emailID
										  FROM SuiteGroup AS sg
										  WHERE sg.avgDrawNum IN
				   							    (SELECT sg.avgDrawNum
				   				  			    FROM SuiteGroup AS sg
				   						  	    WHERE sg.emailID = emailID)),

		SET sg.isSuiteRepresentative = TRUE
			WHERE newSuiteRepID IS NOT NULL AND sg.emailID = newSuiteRepID
		END IF;

	DELETE
	FROM SuiteGroup AS sg
	WHERE sg.emailID = emailID; -- delete the student from the suite group. This can be done anythime (including during suite draw) before their suite draw time is reached
END $$

CREATE PROCEDURE GetAllDormRoomsSummary(
	IN emailID
)
BEGIN
	SELECT r.number, r.squareFeet, r.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum
	FROM DormRoom AS dr, CommonRoom AS cr, Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID
	WHERE r.number = roomNum AND r.dormName = dormName
		  AND dr.dormRoomNum = r.number AND dr.dormName = r.dormName
	ORDER BY r.dormName, r.roomNum; -- group first by dorm, alphabetically, then group data by suite for later processing
END $$

CREATE PROCEDURE GetRoomDetails(  -- common or dorm
	IN roomNum INT,
	IN dormName VARCHAR(50)
)
BEGIN
	SELECT r.number, r.squareFeet, r.dimensionsDescription, r.otherDescription, r.windowsDescription,
		   dr.numOccupants, dr.connectingRoomNum, dr.closetsDescription, dr.bathroomDescription,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, Room AS r
	WHERE r.number = roomNum AND r.dormName = dormName
		  AND dr.dormRoomNum = r.number AND dr.dormName = r.dormName
		  AND cr.number = r.number AND cr.dormName = sr.dormName;
END $$

CREATE PROCEDURE GetAllSuitesSummary()
BEGIN
	SELECT sr.suiteID, sr.isSubFree, sr.numRooms, sr.dormName, sr.otherDescription
		   sr.number, sr.squareFeet, sr.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, (SELECT * FROM Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID) AS sr
	WHERE dr.dormRoomNum = sr.number AND dr.dormName = sr.dormName
		  AND cr.number = sr.number AND cr.dormName = sr.dormName
	ORDER BY sr.dormName, sr.suiteID, sr.number; -- group first by dorm, alphabetically, then group data by suite for later processing, then finally by room number, for later processing
END $$

CREATE PROCEDURE GetMySuiteRooms(
	IN emailID VARCHAR(8)
)
BEGIN
	SELECT sr.suiteID, sr.isSubFree, sr.numRooms, sr.dormName, sr.otherDescription
		   sr.number, sr.squareFeet, sr.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, (SELECT * FROM Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID) AS sr, SuiteGroup AS sg
	WHERE dr.dormRoomNum = sr.number AND dr.dormName = sr.dormName
		  AND cr.number = sr.number AND cr.dormName = sr.dormName
		  AND sg.emailID = emailID AND sg.suiteID IS NOT NULL -- select only the rooms in the suite the student is in. If the student doesn't have a suite, nothing gets returned
	ORDER BY sr.dormName, sr.suiteID, sr.number; -- group first by dorm, alphabetically, then group data by suite for later processing, then finally by room number, for later processing
END $$
