-- a SQL script that creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average score for a student. 
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    SELECT AVG(`score`) FROM `corrections`
    WHERE corrections.user_id = user_id INTO @avg_score;

    UPDATE `users` SET `average_score` = @avg_score
    WHERE `id` = user_id;
END$$
DELIMITER ;
