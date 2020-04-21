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

DELIMITER ;
