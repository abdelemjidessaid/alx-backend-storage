-- Script that create a PROCEDURE named AddBonus
-- That procedure adds new correction for a student

DROP PROCEDURE IF EXISTS `AddBonus`;

DELIMITER $$
CREATE PROCEDURE `AddBonus` (IN user_id INT, IN project_name VARCHAR(255), IN score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;
    -- count the projects name
    SELECT COUNT(id) INTO project_count
    FROM projects
    WHERE name = project_name;
    -- if the count of projects is equal to 0 insert it
    IF project_count = 0 THEN INSERT INTO projects(name) VALUES (project_name);
    END IF;
    -- select all projects with name
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;
    -- insert all in corrections table
    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);
END $$
DELIMITER ;
