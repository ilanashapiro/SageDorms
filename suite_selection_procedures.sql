DELIMITER $$

DROP PROCEDURE IF EXISTS GetMySuiteRooms$$
CREATE PROCEDURE GetMySuiteRooms(
	IN emailID CHAR(8)
)
BEGIN
	SELECT sr.suiteID, sr.isSubFree, sr.numRooms, sr.dormName, sr.otherDescription,
		   sr.number, sr.squareFeet, sr.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, (SELECT * FROM Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID) AS sr, SuiteGroup AS sg
	WHERE dr.number = sr.number AND dr.dormName = sr.dormName
		  AND cr.number = sr.number AND cr.dormName = sr.dormName
		  AND sg.emailID = emailID AND sg.suiteID IS NOT NULL -- select only the rooms in the suite the student is in. If the student doesn't have a suite, nothing gets returned
	ORDER BY sr.dormName, sr.suiteID, sr.number; -- group first by dorm, alphabetically, then group data by suite for later processing, then finally by room number, for later processing
END $$

DROP PROCEDURE IF EXISTS GetAllSuitesSummary$$
CREATE PROCEDURE GetAllSuitesSummary()
BEGIN
	SELECT sr.suiteID, sr.isSubFree, sr.numRooms, sr.dormName, sr.otherDescription,
		   sr.number, sr.squareFeet, sr.otherDescription,
		   dr.numOccupants, dr.connectingRoomNum,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM DormRoom AS dr, CommonRoom AS cr, (SELECT * FROM Room AS r LEFT JOIN Suite AS s ON r.suiteID = s.suiteID) AS sr
	WHERE dr.number = sr.number AND dr.dormName = sr.dormName
		  AND cr.number = sr.number AND cr.dormName = sr.dormName
	ORDER BY sr.dormName, sr.suiteID, sr.number; -- group first by dorm, alphabetically, then group data by suite for later processing, then finally by room number, for later processing
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

DROP PROCEDURE IF EXISTS GetRoomsSummaryForSuite$$
CREATE PROCEDURE GetRoomsSummaryForSuite(
	IN suiteID VARCHAR(50)
)
BEGIN
	-- dorm room info
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   dr.numOccupants, dr.connectingRoomNum
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
	UPDATE SuiteGroup AS sg -- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	SET sg.avgDrawNum = (SELECT avg(s.drawNum)
						FROM Student AS s
						WHERE s.emailID != emailID
							  AND s.emailID IN (SELECT s.emailID
										  FROM SuiteGroup AS sg
										  WHERE sg.avgDrawNum IN
				   							    (SELECT sg.avgDrawNum
				   				  			    FROM SuiteGroup AS sg
				   						  	    WHERE sg.emailID = emailID)));

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
	INSERT INTO SuiteGroup (emailID) VALUES (emailID);

	-- recompute average draw num for all members of group (including your newly added self).
	UPDATE SuiteGroup AS sg
	SET sg.avgDrawNum = (SELECT avg(s.drawNum)
						FROM Student AS s
						WHERE s.emailID = emailID
							  OR s.emailID IN (SELECT s.emailID
										  FROM SuiteGroup AS sg
										  WHERE sg.avgDrawNum IN
				   							    (SELECT sg.avgDrawNum
				   				  			    FROM SuiteGroup AS sg
				   						  	    WHERE sg.emailID = emailIDInSG)));

		-- If someone else was originally the SG rep and now you are, update this
		IF isNewSuiteRep AND emailIDInSG IN (SELECT sg.emailID
										     FROM SuiteGroup AS sg
										     WHERE sg.avgDrawNum IN (SELECT avgDrawNum
											   					  FROM SuiteGroup AS sg1
																  WHERE sg1.emailID = emailIDInSG)
												   AND sg.isSuiteRepresentative = TRUE) THEN
			UPDATE SuiteGroup AS sg
			SET sg.isSuiteRepresentative = TRUE WHERE sg.emailID = emailID;

            UPDATE SuiteGroup AS sg
			SET sg.isSuiteRepresentative = FALSE WHERE sg.emailID IN (SELECT sg.emailID
																     FROM SuiteGroup AS sg
																     WHERE sg.avgDrawNum IN (SELECT avgDrawNum
																	   					  FROM SuiteGroup AS sg1
																						  WHERE sg1.emailID = emailIDInSG)
																		   AND sg.isSuiteRepresentative = TRUE);
		END IF;

	DELETE
	FROM SuiteGroup AS sg
	WHERE sg.emailID = emailID; -- delete the student from the suite group. This can be done anythime (including during suite draw) before their suite draw time is reached
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
	UPDATE SuiteGroup AS sg
	SET sg.suiteID = suiteID
	WHERE s.emailID IN (SELECT s.emailID
						FROM SuiteGroup AS sg
						WHERE sg.avgDrawNum IN
							  (SELECT sg.avgDrawNum
							  FROM SuiteGroup AS sg
							  WHERE sg.emailID = emailIDSuiteRep));
END $$

DELIMITER ;
