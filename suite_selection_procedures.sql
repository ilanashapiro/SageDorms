DELIMITER $$

-- a true summary, informational only. This is just for informational purposes and displays ALL data, even rooms and suites that have been selected.
DROP PROCEDURE IF EXISTS GetSuitesForDorm$$
CREATE PROCEDURE GetSuitesForDorm(
	IN dormName VARCHAR(50)
)
BEGIN
-- suite info
	SELECT s.suiteID
	FROM Suite AS s
	WHERE s.dormName = dormName;
END $$

DROP PROCEDURE IF EXISTS GetMySuiteDetails$$
CREATE PROCEDURE GetMySuiteDetails(
	IN emailID CHAR(8)
)
BEGIN
	-- suite info
	SELECT s.suiteID, s.dormName, s.isSubFree, s.numRooms, s.numPeople, s.otherDescription
	FROM Suite AS s, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND s.suiteID = sg.suiteID;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
	ORDER BY cast(r.number as unsigned);

	-- common room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, r.otherDescription,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr, SuiteGroup AS sg
	WHERE sg.emailID = emailID AND r.suite = sg.suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY cast(r.number as unsigned);
END $$

DROP PROCEDURE IF EXISTS GetSuiteSummaryForSuite$$
CREATE PROCEDURE GetSuiteSummaryForSuite(
	IN suiteID VARCHAR(50)
)
BEGIN
	-- suite info
	SELECT *
	FROM Suite AS s
	WHERE s.suiteID = suiteID AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where sg.suiteID = s.suiteID); --  we only want suites that are still free;

	-- dorm room info
	SELECT DISTINCT r.dormName, r.number, r.squareFeet, dr.numOccupants, dr.connectingRoomNum, r.otherDescription
	FROM DormRoom AS dr, Room AS r, Suite AS s
	WHERE r.suite = suiteID
		  AND dr.dormName = r.dormName AND dr.number = r.number
		  AND NOT EXISTS (SELECT * FROM Student AS st where st.dormName = dr.dormName AND st.dormRoomNum = dr.number) --  we only want rooms that are still free
		  AND s.suiteID = suiteID
		  AND NOT EXISTS (SELECT * FROM SuiteGroup AS sg where sg.suiteID = s.suiteID)
	ORDER BY cast(r.number as unsigned);

	-- common room info
	SELECT DISTINCT r.number, r.squareFeet, r.otherDescription, r.isSubFree,
		   cr.hasStove, cr.hasSink, cr.hasRefrigerator, cr.hasBathroom
	FROM Room AS r, CommonRoom AS cr
	WHERE r.suite = suiteID
		  AND cr.dormName = r.dormName AND cr.number = r.number
	ORDER BY cast(r.number as unsigned);
END $$

DROP PROCEDURE IF EXISTS RemoveMyselfFromSuiteGroup$$
CREATE PROCEDURE RemoveMyselfFromSuiteGroup(
	IN emailID CHAR(8)
)
BEGIN
	-- recompute average draw num for all remaining members of group. If the removal happens before the draw, this affects their draw time
	-- business logic ensures the suite rep cannot remove themself, unless they are the last person remaining in the group and are thus dissolving the group
	UPDATE /*+ NO_MERGE(average)*/ SuiteGroup AS sg,
		(SELECT avg(DISTINCT s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID != emailID
			  AND s.emailID IN (SELECT s.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailID))) AS average
	SET sg.avgDrawNum = average.avgDrawNum
	WHERE sg.emailID != emailID
		  AND sg.emailID IN (SELECT * FROM (SELECT sg.emailID
	  												FROM SuiteGroup AS sg
	  												WHERE sg.avgDrawNum IN
	  													  (SELECT sg.avgDrawNum
	  													  FROM SuiteGroup AS sg
	  													  WHERE sg.emailID = emailID)) AS mySG);

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
	INSERT INTO SuiteGroup (emailID, avgDrawNum, isSuiteRepresentative) VALUES (emailID, 0.0, 0);

	-- recompute average draw num for all members of group (including your newly added self).
	UPDATE /*+ NO_MERGE(average) */ SuiteGroup AS sg,
		(SELECT avg(DISTINCT s.drawNum) AS avgDrawNum
		FROM Student AS s
		WHERE s.emailID = emailID
			  OR s.emailID IN (SELECT sg.emailID
						  FROM SuiteGroup AS sg
						  WHERE sg.avgDrawNum IN
								(SELECT sg.avgDrawNum
								FROM SuiteGroup AS sg
								WHERE sg.emailID = emailIDInSG))) AS average
	SET sg.avgDrawNum = average.avgDrawNum
	WHERE sg.emailID = emailID OR sg.emailID IN (SELECT * FROM (SELECT sg.emailID
										FROM SuiteGroup AS sg
										WHERE sg.avgDrawNum IN
											  (SELECT sg.avgDrawNum
											  FROM SuiteGroup AS sg
											  WHERE sg.emailID = emailIDInSG)) AS mySG);

		-- If someone else was originally the SG rep and now you are, update this
		IF isNewSuiteRep AND emailIDInSG IN (SELECT sg.emailID
										     FROM SuiteGroup AS sg
										     WHERE sg.avgDrawNum IN (SELECT avgDrawNum
											   					  FROM SuiteGroup AS sg
																  WHERE sg.emailID = emailIDInSG)
											   AND sg.isSuiteRepresentative = TRUE) THEN
		   -- they are no longer suite rep
           UPDATE /*+ NO_MERGE(oldSuiteRep) */ SuiteGroup AS sg,
				(SELECT sg.emailID
				 FROM SuiteGroup AS sg
				 WHERE sg.avgDrawNum IN (SELECT avgDrawNum
									  FROM SuiteGroup AS sg
									  WHERE sg.emailID = emailIDInSG)
					   AND sg.isSuiteRepresentative = TRUE) AS oldSuiteRep
			SET sg.isSuiteRepresentative = FALSE WHERE sg.emailID = oldSuiteRep.emailID;

			-- you become new suite rep
			UPDATE SuiteGroup AS sg
			SET sg.isSuiteRepresentative = TRUE WHERE sg.emailID = emailID;
		END IF;
	END $$

DROP PROCEDURE IF EXISTS GetMySuiteGroup$$
CREATE PROCEDURE GetMySuiteGroup(
	IN emailID CHAR(8)
)
BEGIN
	SELECT DISTINCT s.name, s.emailID, sg.isSuiteRepresentative, sg.avgDrawNum
	FROM Student AS s, SuiteGroup AS sg
	WHERE s.emailID IN (SELECT sg.emailID
		  				  FROM SuiteGroup AS sg
					  	  WHERE sg.avgDrawNum IN
							    (SELECT sg.avgDrawNum
				  			    FROM SuiteGroup AS sg
						  	    WHERE sg.emailID = emailID))
		  AND sg.emailID = s.emailID;
END $$

DROP PROCEDURE IF EXISTS SetSuite$$
CREATE PROCEDURE SetSuite(
	IN suiteID VARCHAR(50),
	IN emailIDSuiteRep CHAR(8)
)
BEGIN
	UPDATE /*+ NO_MERGE(mygroup) */ SuiteGroup AS sg,
		(SELECT sg.emailID
		FROM SuiteGroup AS sg
		WHERE sg.avgDrawNum IN
			  (SELECT sg.avgDrawNum
			  FROM SuiteGroup AS sg
			  WHERE sg.emailID = emailIDSuiteRep)) AS mygroup
	SET sg.suiteID = suiteID
	WHERE sg.emailID = mygroup.emailID;
END $$

DROP PROCEDURE IF EXISTS SetSuiteRepresentative$$
CREATE PROCEDURE SetSuiteRepresentative(
	IN emailID CHAR(8)
)
BEGIN
	-- old suite rep is no longer suite rep
   	UPDATE /*+ NO_MERGE(oldSuiteRep) */ SuiteGroup AS sg,
   		(SELECT sg.emailID
   		 FROM SuiteGroup AS sg
   		 WHERE sg.avgDrawNum IN (SELECT avgDrawNum
   							  FROM SuiteGroup AS sg
   							  WHERE sg.emailID = emailID)
   			   AND sg.isSuiteRepresentative = TRUE) AS oldSuiteRep
   	SET sg.isSuiteRepresentative = FALSE WHERE sg.emailID = oldSuiteRep.emailID AND sg.emailID != emailID;

	-- you become new suite rep
	UPDATE SuiteGroup AS sg
	SET sg.isSuiteRepresentative = TRUE WHERE sg.emailID = emailID;
END $$

DELIMITER ;
