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


