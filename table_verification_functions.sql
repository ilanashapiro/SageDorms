-- used to check after the draw if all students living on campus (isDrawing = true) have drawn rooms
DELIMITER $$
DROP FUNCTION IF EXISTS CheckStudentsChooseRooms$$
CREATE FUNCTION CheckStudentsChooseRooms()
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN NOT EXISTS (
		SELECT *
		FROM Student as s
		WHERE s.isDrawing IS TRUE
			AND s.dormRoomNum IS NULL
			AND s.dormName IS NULL );  -- the dorm of the connecting room must be the same as that of the dorm room
END $$

DROP FUNCTION IF EXISTS CheckSuiteHasRepresentative$$
CREATE FUNCTION CheckSuiteHasRepresentative()
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN NOT EXISTS (
		SELECT *
		FROM
			(SELECT avgSuiteGroupDrawNum, max(isSuiteRep) AS containsSuiteRep
			FROM Student
			WHERE avgSuiteGroupDrawNum IS NOT NULL
			GROUP BY avgSuiteGroupDrawNum)
			AS
			suiteGroups
		WHERE suiteGroups.containsSuiteRep IS FALSE );
END $$

DROP FUNCTION IF EXISTS CheckIfStudentHasRoom$$
CREATE FUNCTION CheckIfStudentHasRoom(
	emailID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM Student AS s
		WHERE s.emailID = emailID AND s.roomNum IS NOT NULL);
END $$

DROP FUNCTION IF EXISTS CheckIfStudentHasSuite$$
CREATE FUNCTION CheckIfStudentHasSuite(
	emailID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM SuiteGroup AS sg
		WHERE sg.emailID = emailID AND sg.suiteID IS NOT NULL);
END $$

DROP FUNCTION IF EXISTS CheckIfNewSuiteRepIsInGroup$$
CREATE FUNCTION CheckIfNewSuiteRepIsInGroup(
	emailID VARCHAR(8),
	newSuiteRepID VARCHAR(8)
)
RETURNS BOOL
DETERMINISTIC
BEGIN
	RETURN EXISTS (
		SELECT *
		FROM SuiteGroup AS sg
		WHERE sg.newSuiteRepID IN (SELECT s.emailID
								   FROM SuiteGroup AS sg
								   WHERE sg.avgDrawNum IN
									     (SELECT sg.avgDrawNum
									     FROM SuiteGroup AS sg
									     WHERE sg.emailID = emailID)));
END $$
DELIMITER ;
