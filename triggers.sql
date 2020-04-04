DELIMITER $$

DROP TRIGGER IF EXISTS prospective_suite_group_constraints$$
CREATE TRIGGER prospective_suite_group_constraints AFTER INSERT ON ProspectiveSuiteGroup
	FOR EACH ROW BEGIN
		IF EXISTS (
		    SELECT *
		    FROM ProspectiveSuiteGroup AS p
		    WHERE p.avgDrawNum NOT IN
    		    (SELECT DISTINCT s.avgSuiteGroupDrawNum
    		    FROM Student AS s, ProspectiveSuiteGroup AS p
    		    WHERE p.avgDrawNum = s.avgSuiteGroupDrawNum) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ProspectiveSuiteGroup does not satisfy constraints!';
		END IF;
    END$$

DROP TRIGGER IF EXISTS closet_type_constraints$$
CREATE TRIGGER closet_type_constraints AFTER INSERT ON ClosetType
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM ClosetType AS c
			WHERE c.typeName NOT IN
				(SELECT c.typeName
				FROM ClosetType AS c, DormRoom AS dm
				WHERE c.typeName = dm.closetType) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'ClosetType does not satisfy constraints!';
		END IF;
	END$$

DROP TRIGGER IF EXISTS window_type_constraints$$
CREATE TRIGGER window_type_constraints AFTER INSERT ON WindowType
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM WindowType AS w
			WHERE w.typeName NOT IN
				(SELECT w.typeName
				FROM WindowType AS w, Room AS r
				WHERE w.typeName = r.windowType) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
		END IF;
	END$$


DROP TRIGGER IF EXISTS suite_constraints$$
CREATE TRIGGER suite_constraints AFTER INSERT ON Suite
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM Suite AS s
			WHERE s.suiteID NOT IN
				(SELECT s.suiteID
				FROM Suite AS s, Room AS r
				WHERE s.suiteID = r.suite) )
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'WindowType does not satisfy constraints!';
		END IF;
	END$$

DROP TRIGGER IF EXISTS draws_up_constraints$$
CREATE TRIGGER draws_up_constraints AFTER INSERT ON DrawsUp
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM DrawsUp as du1, DrawsUp as du2
			WHERE du1.higherStudent = du2.lowerStudent ) -- a student drawing someone up cannot be drawn up, and a student being drawn up cannot draw someone else up
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'DrawsUp does not satisfy constraints!';
		END IF;
	END$$

DROP TRIGGER IF EXISTS student_constraints$$
CREATE TRIGGER student_constraints AFTER INSERT ON Student
	FOR EACH ROW BEGIN
		IF EXISTS (
			SELECT *
			FROM Student
			WHERE isDrawing IS TRUE
				  AND drawTime IS NULL)
		THEN
			SIGNAL SQLSTATE '42927' SET MESSAGE_TEXT = 'All drawing students need a draw time -- Student does not satisfy constraints!';
		END IF;
	END$$
