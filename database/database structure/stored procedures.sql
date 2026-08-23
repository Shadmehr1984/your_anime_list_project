DELIMITER //
    -- changing account status
    DROP PROCEDURE IF EXISTS change_account_status //

    CREATE PROCEDURE change_account_status(
                                            status_of_change ENUM('increase', 'decrease'),
                                            status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching'),
                                            account_id INT
                                            )
    BEGIN
        -- increase account new status count 
        IF status_of_change = 'increase' THEN
            IF status = 'completed' THEN
                UPDATE account
                SET account.completed_count = account.completed_count + 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'dropped' THEN
                UPDATE account
                SET account.dropped_count = account.dropped_count + 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'plan to watch' THEN
                UPDATE account
                SET account.plan_to_watch_count = account.plan_to_watch_count + 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'watching' THEN
                UPDATE account
                SET account.watching_count = account.watching_count + 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'on hold' THEN
                UPDATE account
                SET account.on_hold_count = account.on_hold_count + 1
                WHERE account_id = account.account_id;
            END IF;
        -- decrease account old status count
        ELSEIF status_of_change = 'decrease' THEN
            IF status = 'completed' THEN
                UPDATE account
                SET account.completed_count = account.completed_count - 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'dropped' THEN
                UPDATE account
                SET account.dropped_count = account.dropped_count - 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'plan to watch' THEN
                UPDATE account
                SET account.plan_to_watch_count = account.plan_to_watch_count - 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'watching' THEN
                UPDATE account
                SET account.watching_count = account.watching_count - 1
                WHERE account_id = account.account_id;
            ELSEIF status = 'on hold' THEN
                UPDATE account
                SET account.on_hold_count = account.on_hold_count - 1
                WHERE account_id = account.account_id;
            END IF;
        END IF;
    END //
DELIMITER ;


DELIMITER //
    -- change all anime have been changed
    DROP PROCEDURE IF EXISTS calculate_and_clear_log_list //

    CREATE PROCEDURE calculate_and_clear_log_list()
    BEGIN
        -- drop CTE if exist
        DROP TEMPORARY TABLE IF EXISTS anime_changes;

        -- make a CTE for save anime changes
        CREATE TEMPORARY TABLE anime_changes(
            SELECT DISTINCT anime_id
            FROM log_list
        );

        -- add new column for changes
        ALTER TABLE anime_changes
        ADD COLUMN score_changes INT DEFAULT 0;
        ALTER TABLE anime_changes
        ADD COLUMN plan_to_watch_changes INT DEFAULT 0;
        ALTER TABLE anime_changes
        ADD COLUMN completed_changes INT DEFAULT 0;
        ALTER TABLE anime_changes
        ADD COLUMN dropped_changes INT DEFAULT 0;
        ALTER TABLE anime_changes
        ADD COLUMN on_hold_changes INT DEFAULT 0;
        ALTER TABLE anime_changes
        ADD COLUMN watching_changes INT DEFAULT 0;

        -- save changes in anime_changes table

        -- save insert and update changes
        UPDATE anime_changes
        INNER JOIN log_list
        USING(anime_id)
        SET anime_changes.score_changes = anime_changes.score_changes + (SELECT SUM(new_score) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.log_status IN ('insert', 'update') AND log_list.new_status IN ('completed', 'dropped'))
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.log_status IN ('insert', 'update') 
        AND log_list.new_status IN ('completed', 'dropped');

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes + (SELECT COUNT(new_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.new_status = 'plan to watch' AND log_list.log_status IN ('insert', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'plan to watch' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET completed_changes = completed_changes + (SELECT COUNT(new_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.new_status = 'completed' AND log_list.log_status IN ('insert', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'completed' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET dropped_changes = dropped_changes + (SELECT COUNT(new_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.new_status = 'dropped' AND log_list.log_status IN ('insert', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'dropped' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes + (SELECT COUNT(new_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.new_status = 'on hold' AND log_list.log_status IN ('insert', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'on hold' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET watching_changes = watching_changes + (SELECT COUNT(new_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.new_status = 'watching' AND log_list.log_status IN ('insert', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'watching' AND log_list.log_status IN ('insert', 'update'));

        -- save delete and update changes
        UPDATE anime_changes
        INNER JOIN log_list
        USING(anime_id)
        SET anime_changes.score_changes = anime_changes.score_changes - (SELECT SUM(new_score) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.log_status IN ('delete', 'update') AND log_list.old_status IN ('completed', 'dropped'))
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.log_status IN ('delete', 'update') 
        AND log_list.old_status IN ('completed', 'dropped');

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes - (SELECT COUNT(old_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.old_status = 'plan to watch' AND log_list.log_status IN ('delete', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'plan to watch' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET completed_changes = completed_changes - (SELECT COUNT(old_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.old_status = 'completed' AND log_list.log_status IN ('delete', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'completed' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET dropped_changes = dropped_changes - (SELECT COUNT(old_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.old_status = 'dropped' AND log_list.log_status IN ('delete', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'dropped' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes - (SELECT COUNT(old_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.old_status = 'on hold' AND log_list.log_status IN ('delete', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'on hold' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET watching_changes = watching_changes - (SELECT COUNT(old_status) FROM log_list WHERE anime_changes.anime_id = log_list.anime_id AND log_list.old_status = 'watching' AND log_list.log_status IN ('delete', 'update'))
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'watching' AND log_list.log_status IN ('delete', 'update'));

        -- update animes changes

        -- set new score
        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.score =
        ((anime.score * (anime.completed_count + anime.dropped_count)) + anime_changes.score_changes) / (anime.completed_count + anime_changes.completed_changes + anime.dropped_count + anime_changes.dropped_changes)
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.score_changes != 0;

        -- set new status count
        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.plan_to_watch_count = anime.plan_to_watch_count + anime_changes.plan_to_watch_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.plan_to_watch_changes != 0;

        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.completed_count = anime.completed_count + anime_changes.completed_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.completed_changes != 0;

        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.dropped_count = anime.dropped_count + anime_changes.dropped_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.dropped_changes != 0;

        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.on_hold_count = anime.on_hold_count + anime_changes.on_hold_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.on_hold_changes != 0;

        UPDATE anime
        INNER JOIN anime_changes
        USING(anime_id)
        SET anime.watching_count = anime.watching_count + anime_changes.watching_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.watching_changes != 0;

        -- clear log_list table
        TRUNCATE log_list;
    END //
DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS strictest_users_report //

CREATE PROCEDURE strictest_users_report()
BEGIN
    SELECT user_name, avg_score, completed_count + dropped_count AS rating_count
    FROM account
    ORDER BY avg_score ASC
    LIMIT 3;
END //

DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS active_studios_report //

CREATE PROCEDURE active_studios_report()
BEGIN
    SELECT studio_name, product_numbers
    FROM studio
    ORDER BY product_numbers DESC
    LIMIT 10;
END //

DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS top_studios_by_average_score_report //

CREATE PROCEDURE top_studios_by_average_score_report()
BEGIN
	SELECT studio.studio_name, ROUND(AVG(anime.score), 2) AS avg_score, COUNT(anime.anime_id) AS products
	FROM anime_production_studio
	LEFT JOIN studio
	USING(studio_id)
	LEFT JOIN anime
	USING(anime_id)
	GROUP BY studio.studio_id
	HAVING avg_score > 0
	ORDER BY avg_score DESC
	LIMIT 10;
END //
DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS top_genres_by_anime_count_report //

CREATE PROCEDURE top_genres_by_anime_count_report()
BEGIN
	SELECT genre_name, anime_numbers
	FROM genre
	ORDER BY anime_numbers DESC
	LIMIT 10;
END//

DELIMITER ;


DELIMITER //

DROP PROCEDURE IF EXISTS genre_average_scores //

CREATE PROCEDURE genre_average_scores()
BEGIN
	SELECT genre.genre_name, ROUND(AVG(anime.score), 2) AS avg_score, genre.anime_numbers
	FROM anime_genres
	LEFT JOIN genre
	USING(genre_id)
	LEFT JOIN anime
	USING(anime_id)
	GROUP BY genre.genre_id
	HAVING avg_score > 0
	ORDER BY avg_score DESC
	LIMIT 10;
END//

DELIMITER ;