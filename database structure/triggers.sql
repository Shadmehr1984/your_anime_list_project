DELIMITER //
    -- save studio detail change(insert)
    DROP TRIGGER IF EXISTS update_studio_detail_insert;

    CREATE TRIGGER update_studio_detail_insert
    AFTER INSERT ON anime_production_studio
    FOR EACH ROW
    BEGIN
        UPDATE studio
        SET product_number = product_number + 1
        WHERE studio.studio_id = anime_production_studio.studio_id;
    END//
DELIMITER ;


DELIMITER //
    -- save studio detail change(delete)
    DROP TRIGGER IF EXISTS update_studio_detail_delete;

    CREATE TRIGGER update_studio_detail_delete
    AFTER DELETE ON anime_production_studio
    FOR EACH ROW
    BEGIN
        UPDATE studio
        SET product_number = product_number - 1
        WHERE studio.studio_id = anime_production_studio.studio_id;
    END//
DELIMITER ;


DELIMITER //
    -- save genres detail change(insert)
    DROP TRIGGER IF EXISTS update_genre_detail_insert;

    CREATE TRIGGER update_genre_detail_insert
    AFTER INSERT ON anime_genres
    FOR EACH ROW
    BEGIN
        UPDATE genre
        SET anime_numbers = anime_numbers + 1
        WHERE anime_genres.genre_id = genre.genre_id;
    END//
DELIMITER ;


DELIMITER //
    -- save genres detail change(delete)
    DROP TRIGGER IF EXISTS update_genre_detail_delete;

    CREATE TRIGGER update_genre_detail_delete
    AFTER DELETE ON anime_genres
    FOR EACH ROW
    BEGIN
        UPDATE genre
        SET anime_numbers = anime_numbers - 1
        WHERE anime_genres.genre_id = genre.genre_id;
    END//
DELIMITER ;


DELIMITER //
    -- add to list
    DROP TRIGGER IF EXISTS insert_to_list;

    CREATE TRIGGER insert_to_list
    AFTER INSERT ON list
    FOR EACH ROW
    BEGIN
		DECLARE all_watched INT;
        
        -- save log
        INSERT INTO log_list
        VALUES(
            'insert',
            NEW.anime_id,
            NEW.account_id,
            NEW.score,
            NEW.status,
            NEW.episodes_watched
        );

        -- update account information
        IF NEW.status = 'completed' THEN
            UPDATE account
            SET account.completed_count = account.completed_count + 1
            WHERE NEW.account_id = account.account_id;
        ELSEIF NEW.status = 'dropped' THEN
            UPDATE account
            SET account.dropped_count = account.dropped_count + 1
            WHERE NEW.account_id = account.account_id;
        ELSEIF NEW.status = 'plan to watch' THEN
            UPDATE account
            SET account.plan_to_watch_count = account.plan_to_watch_count + 1
            WHERE NEW.account_id = account.account_id;
        ELSEIF NEW.status = 'watching' THEN
            UPDATE account
            SET account.watching_count = account.watching_count + 1
            WHERE NEW.account_id = account.account_id;
        ELSEIF NEW.status = 'on hold' THEN
            UPDATE account
            SET account.on_hold_count = account.on_hold_count + 1
            WHERE NEW.account_id = account.account_id;
        END IF;

        -- update account avg score
        IF NEW.status = 'completed' OR NEW.status = 'dropped' THEN
            UPDATE account
            SET all_watched = dropped_count + completed_count
            WHERE NEW.account_id = account.account_id;

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
    DROP TRIGGER IF EXISTS delete_account;

    CREATE TRIGGER delete_account
    BEFORE DELETE ON account
    FOR EACH ROW
    BEGIN
        -- create temporary table for save ram after even join
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