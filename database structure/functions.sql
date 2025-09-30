DELIMITER //

CREATE FUNCTION calculate_score(score INT, 
								old_user_score INT, 
                                old_score FLOAT(3), 
                                all_watched INT, 
                                calculate_status ENUM('increase', 'decrease', 'update')
                                ) RETURNS FLOAT(3)
                                DETERMINISTIC
                                NO SQL
BEGIN
	DECLARE new_score FLOAT(3);
    
	IF calculate_status = 'increase' THEN
		SET new_score = ((old_score * all_watched) + score) / (all_watched + 1);
	ELSEIF calculate_status = 'decrease' AND all_watched = 0 THEN
		SET new_score = 0;
	ELSEIF calculate_status = 'decrease' THEN
		SET new_score = ((old_score * all_watched) - score) / (all_watched - 1);
	ELSEIF calculate_status = 'update' THEN
		SET new_score = ((old_score * all_watched) - old_user_score + score) / (all_watched);
	END IF;

	IF new_score = NULL THEN
		SET new_score = 0;
	END IF;

	RETURN new_score;
END//

DELIMITER ;