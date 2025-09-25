DROP DATABASE IF EXISTS your_anime_list;

CREATE DATABASE IF NOT EXISTS your_anime_list;

USE your_anime_list;

#!tables
DROP TABLE IF EXISTS account;
CREATE TABLE IF NOT EXISTS account(
    account_id INT PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    plan_to_watch_count INT DEFAULT 0,
    completed_count INT DEFAULT 0,
    dropped_count INT DEFAULT 0,
    on_hold_count INT DEFAULT 0,
    watching_count INT DEFAULT 0,
    avg_score FLOAT(4, 2) DEFAULT 0
);

DROP TABLE IF EXISTS anime;
CREATE TABLE IF NOT EXISTS anime(
    anime_id INT PRIMARY KEY,
    anime_name VARCHAR(100) NOT NULL,
    anime_status ENUM('currently_airing', 'not_yet_aired', 'finished_airing') NOT NULL,
    score FLOAT(4, 2) NOT NULL DEFAULT 0,
    CONSTRAINT score_range_anime_table CHECK (score>=0 AND score<=10),
    episodes INT DEFAULT 0,
    year YEAR NOT NULL,
    season ENUM('spring', 'summer', 'fall', 'winter') NOT NULL,
    avg_episodes_time FLOAT(3) NOT NULL,
    plan_to_watch_count INT DEFAULT 0,
    completed_count INT DEFAULT 0,
    dropped_count INT DEFAULT 0,
    on_hold_count INT DEFAULT 0,
    watching_count INT DEFAULT 0
);

DROP TABLE IF EXISTS genre;
CREATE TABLE IF NOT EXISTS genre(
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(30) NOT NULL,
    anime_numbers INT NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS studio;
CREATE TABLE IF NOT EXISTS studio(
    studio_id INT PRIMARY KEY,
    studio_name VARCHAR(30) NOT NULL,
    product_numbers INT DEFAULT 0
);

DROP TABLE IF EXISTS anime_production_studio;
CREATE TABLE IF NOT EXISTS anime_production_studio(
    anime_id INT,
    studio_id INT,
    PRIMARY KEY (anime_id, studio_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(studio_id) REFERENCES studio(studio_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS anime_genres;
CREATE TABLE IF NOT EXISTS anime_genres(
    anime_id INT,
    genre_id INT,
    PRIMARY KEY (anime_id, genre_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS list;
CREATE TABLE IF NOT EXISTS list(
    anime_id INT,
    account_id INT,
    PRIMARY KEY (anime_id, account_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE,
    score INT NOT NULL DEFAULT 0,
    CONSTRAINT score_range_list_table CHECK (score>=0 AND score<=10),
    status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching'),
    episodes_watched INT DEFAULT 0
);

DROP TABLE IF EXISTS log_list;
CREATE TABLE IF NOT EXISTS log_list(
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    log_status ENUM('insert', 'delete', 'update') NOT NULL,
    anime_id INT NOT NULL,
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    new_score INT DEFAULT 0,
    old_score INT DEFAULT 0,
    CONSTRAINT new_score_range_log_list_table CHECK (new_score>=0 AND new_score<=10),
    CONSTRAINT old_score_range_log_list_table CHECK (old_score>=0 AND old_score<=10),
    new_status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching'),
    old_status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching')
);


#!functions


DELIMITER //

CREATE FUNCTION calculate_score(score INT, 
								old_user_score INT, 
                                old_score FLOAT(4, 2), 
                                all_watched INT, 
                                calculate_status ENUM('increase', 'decrease', 'update')
                                ) RETURNS FLOAT(4, 2)
                                DETERMINISTIC
                                NO SQL
BEGIN
	DECLARE new_score FLOAT(4, 2);
    
	IF calculate_status = 'increase' THEN
		SET new_score = ((old_score * all_watched) + score) / (all_watched + 1);
	ELSEIF calculate_status = 'decrease' THEN
		SET new_score = ((old_score * all_watched) - score) / (all_watched - 1);
	ELSEIF calculate_status = 'update' THEN
		SET new_score = ((old_score * all_watched) - old_user_score + score) / (all_watched);
	END IF;

	RETURN new_score;
END//

DELIMITER ;


#!triggers


DELIMITER //
    -- save studio detail change(insert)
    DROP TRIGGER IF EXISTS update_studio_detail_insert //

    CREATE TRIGGER update_studio_detail_insert
    AFTER INSERT ON anime_production_studio
    FOR EACH ROW
    BEGIN
        UPDATE studio
        SET product_numbers = product_numbers + 1
        WHERE studio.studio_id = NEW.studio_id;
    END//
DELIMITER ;


DELIMITER //
    -- save studio detail change(delete)
    DROP TRIGGER IF EXISTS update_studio_detail_delete //

    CREATE TRIGGER update_studio_detail_delete
    AFTER DELETE ON anime_production_studio
    FOR EACH ROW
    BEGIN
        UPDATE studio
        SET product_numbers = product_numbers - 1
        WHERE studio.studio_id = OLD.studio_id;
    END//
DELIMITER ;


DELIMITER //
    -- save studio detail change(update)
    DROP TRIGGER IF EXISTS update_studio_detail_update //

    CREATE TRIGGER update_studio_detail_update
    AFTER UPDATE ON anime_production_studio
    FOR EACH ROW
    BEGIN
        IF NEW.studio_id != OLD.studio_id THEN
            UPDATE studio
            SET product_numbers = product_numbers - 1
            WHERE studio_id = OLD.studio_id;

            UPDATE studio
            SET product_numbers = product_numbers + 1
            WHERE studio_id = NEW.studio_id;
        END IF;
    END//
DELIMITER ;


DELIMITER //
    -- save genres detail change(insert)
    DROP TRIGGER IF EXISTS update_genre_detail_insert //

    CREATE TRIGGER update_genre_detail_insert
    AFTER INSERT ON anime_genres
    FOR EACH ROW
    BEGIN
        UPDATE genre
        SET anime_numbers = anime_numbers + 1
        WHERE NEW.genre_id = genre.genre_id;
    END//
DELIMITER ;


DELIMITER //
    -- save genres detail change(delete)
    DROP TRIGGER IF EXISTS update_genre_detail_delete //

    CREATE TRIGGER update_genre_detail_delete
    AFTER DELETE ON anime_genres
    FOR EACH ROW
    BEGIN
        UPDATE genre
        SET anime_numbers = anime_numbers - 1
        WHERE OLD.genre_id = genre.genre_id;
    END//
DELIMITER ;


DELIMITER //
    -- save genres detail change(update)
    DROP TRIGGER IF EXISTS update_genre_detail_update //

    CREATE TRIGGER update_genre_detail_update
    AFTER UPDATE ON anime_genres
    FOR EACH ROW
    BEGIN
        IF NEW.genre_id != OLD.genre_id THEN
            UPDATE genre
            SET anime_numbers = anime_numbers - 1
            WHERE genre_id = OLD.genre_id;

            UPDATE genre
            SET anime_numbers = anime_numbers + 1
            WHERE genre_id = NEW.genre_id;
        END IF;
    END//
DELIMITER ;


DELIMITER //
    -- add to list
    DROP TRIGGER IF EXISTS insert_to_list //

    CREATE TRIGGER insert_to_list
    AFTER INSERT ON list
    FOR EACH ROW
    BEGIN
		DECLARE all_watched INT;
        
        -- save log
        INSERT INTO log_list(log_status, anime_id, new_score, new_status)
        VALUES(
            'insert',
            NEW.anime_id,
            NEW.score,
            NEW.status
        );

        -- update account information
        CALL change_account_status('increase', NEW.status, NEW.account_id);

        -- update account avg score
        IF NEW.status = 'completed' OR NEW.status = 'dropped' THEN
            SET all_watched = (SELECT completed_count + dropped_count FROM account WHERE NEW.account_id = account.account_id);

            IF all_watched = 1 THEN
                UPDATE account
                SET avg_score = NEW.score
                WHERE NEW.account_id = account.account_id;
            ELSEIF all_watched > 1 THEN
                UPDATE account
                SET avg_score = calculate_score(NEW.score, NULL, avg_score, all_watched - 1, 'increase')
                WHERE NEW.account_id = account.account_id;
            END IF;
        END IF;
    END//
DELIMITER ;


DELIMITER //
    -- remove from list
    DROP TRIGGER IF EXISTS delete_from_list //

    CREATE TRIGGER delete_from_list
    AFTER DELETE ON list
    FOR EACH ROW
    BEGIN
		DECLARE all_watched INT;
        
        -- save log
        INSERT INTO log_list(log_status, anime_id, old_score, old_status)
        VALUES(
            'delete',
            OLD.anime_id,
            OLD.score,
            OLD.status
        );

        -- update account information
        CALL change_account_status('decrease', OLD.status, OLD.account_id);

        -- update account avg score
        IF OLD.status = 'completed' OR OLD.status = 'dropped' THEN
            SET all_watched = (SELECT completed_count + dropped_count FROM account WHERE OLD.account_id = account.account_id);

            IF all_watched = 0 THEN
                UPDATE account
                SET avg_score = 0
                WHERE OLD.account_id = account.account_id;
            ELSEIF all_watched > 0 THEN
                UPDATE account
                SET avg_score = calculate_score(OLD.score, NULL, avg_score, all_watched + 1, 'decrease')
                WHERE OLD.account_id = account.account_id;
            END IF;
        END IF;
    END//
DELIMITER ;


DELIMITER //
    -- update list
    DROP TRIGGER IF EXISTS update_list //

    CREATE TRIGGER update_list
    AFTER UPDATE ON list
    FOR EACH ROW
    BEGIN
        DECLARE all_watched INT;


        -- save log
        INSERT INTO log_list(log_status, anime_id, new_score, old_score, new_status, old_status)
        VALUES(
            'update',
            NEW.anime_id,
            NEW.score,
            OLD.score,
            NEW.status,
            OLD.status
        );

        -- change account statuses
        IF NEW.status != OLD.status THEN

            -- decrease old status count
            CALL change_account_status('decrease', OLD.status, OLD.account_id);

            -- increase new status count
            CALL change_account_status('increase', NEW.status, NEW.account_id);
        END IF;

        -- change account avg score
        IF NEW.score != OLD.score THEN
            -- set all watched count
            SET all_watched = (SELECT completed_count + dropped_count FROM account WHERE OLD.account_id = account.account_id);


            -- set avg score
            UPDATE account
            SET account.avg_score = calculate_score(NEW.score, OLD.score, account.avg_score, all_watched, 'update')
            WHERE NEW.account_id = account.account_id;
        END IF;
    END//
DELIMITER ;


DELIMITER //
    -- delete account
    DROP TRIGGER IF EXISTS delete_account //

    CREATE TRIGGER delete_account
    BEFORE DELETE ON account
    FOR EACH ROW
    BEGIN
        -- create temporary table for save ram after even join
        DROP TEMPORARY TABLE IF EXISTS account_list;
        
        CREATE TEMPORARY TABLE account_list (
            SELECT anime_id, score, status
            FROM list
            WHERE list.account_id = OLD.account_id
        );

		-- fix animes score
        UPDATE anime
        INNER JOIN account_list
        USING(anime_id)
        SET anime.score = calculate_score(account_list.score, NULL, anime.score, completed_count + dropped_count, 'decrease')
		WHERE account_list.status IN ('completed', 'dropped'); 
        
        -- fix animes statuses
		UPDATE anime
		INNER JOIN account_list
        USING(anime_id)
		SET anime.completed_count = anime.completed_count - 1
		WHERE account_list.status = 'completed';
        
		UPDATE anime
		INNER JOIN account_list
		USING(anime_id)
		SET anime.dropped_count = anime.dropped_count - 1
		WHERE account_list.status = 'dropped';
        
		UPDATE anime
		INNER JOIN account_list
		USING(anime_id)
		SET anime.plan_to_watch_count = anime.plan_to_watch_count - 1
		WHERE account_list.status = 'plan to watch';
        
		UPDATE anime
		INNER JOIN account_list
		USING(anime_id)
		SET anime.watching_count = anime.watching_count - 1
		WHERE account_list.status = 'watching';
		
		UPDATE anime
        INNER JOIN account_list
		USING(anime_id)
		SET anime.on_hold_count = anime.on_hold_count - 1
		WHERE account_list.status = 'on hold';
    END//
DELIMITER ;


#!stored procedures


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
        SET score_changes = score_changes + new_score
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.log_status IN ('insert', 'update')
        AND log_list.new_status IN ('completed', 'dropped');

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes + 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.new_status = 'plan to watch'
        AND log_list.log_status IN ('insert', 'update');

        UPDATE anime_changes
        SET completed_changes = completed_changes + 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.new_status = 'completed'
        AND log_list.log_status IN ('insert', 'update');

        UPDATE anime_changes
        SET dropped_changes = dropped_changes + 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.new_status = 'dropped'
        AND log_list.log_status IN ('insert', 'update');

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes + 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.new_status = 'on hold'
        AND log_list.log_status IN ('insert', 'update');

        UPDATE anime_changes
        SET watching_changes = watching_changes + 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.new_status = 'watching'
        AND log_list.log_status IN ('insert', 'update');

        -- save delete and update changes
        UPDATE anime_changes
        SET score_changes = score_changes - new_score
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.log_status IN ('delete', 'update')
        AND log_list.old_status IN ('completed', 'dropped');

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes - 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.old_status = 'plan to watch'
        AND log_list.log_status IN ('delete', 'update');

        UPDATE anime_changes
        SET completed_changes = completed_changes - 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.old_status = 'completed'
        AND log_list.log_status IN ('delete', 'update');

        UPDATE anime_changes
        SET dropped_changes = dropped_changes - 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.old_status = 'dropped'
        AND log_list.log_status IN ('delete', 'update');

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes - 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.old_status = 'on hold'
        AND log_list.log_status IN ('delete', 'update');

        UPDATE anime_changes
        SET watching_changes = watching_changes - 1
        WHERE anime_changes.anime_id = log_list.anime_id
        AND log_list.old_status = 'watching'
        AND log_list.log_status IN ('delete', 'update');

        -- update animes changes

        -- set new score
        UPDATE anime
        SET anime.score =
        ((anime.score * (anime.completed_count + anime.dropped_count)) + anime_changes.score_changes) / (anime.completed_count + anime_changes.completed_changes + anime.dropped_count + anime_changes.dropped_changes)
        WHERE anime.anime_id = anime_changes.anime_id 
        AND anime_changes.score_changes != 0;

        -- set new status count
        UPDATE anime
        SET anime.plan_to_watch_count = anime.plan_to_watch_count + anime_changes.plan_to_watch_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.plan_to_watch_changes != 0;

        UPDATE anime
        SET anime.completed_count = anime.completed_count + anime_changes.completed_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.completed_changes != 0;

        UPDATE anime
        SET anime.dropped_count = anime.dropped_count + anime_changes.dropped_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.dropped_changes != 0;

        UPDATE anime
        SET anime.on_hold_count = anime.on_hold_count + anime_changes.on_hold_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.on_hold_changes != 0;

        UPDATE anime
        SET anime.watching_count = anime.watching_count + anime_changes.watching_changes
        WHERE anime.anime_id = anime_changes.anime_id
        AND anime_changes.watching_changes != 0;

        -- clear log_list table
        TRUNCATE log_list;
    END //
DELIMITER ;


#!events


-- create event for clear log_list every 10 minute
DROP EVENT IF EXISTS clear_log_list;


CREATE EVENT clear_log_list
ON SCHEDULE
EVERY 10 MINUTE
DO
    CALL calculate_and_clear_log_list();
