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
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.log_status IN ('insert', 'update') AND log_list.new_status IN ('completed', 'dropped'));

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes + 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'plan to watch' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET completed_changes = completed_changes + 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'completed' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET dropped_changes = dropped_changes + 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'dropped' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes + 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'on hold' AND log_list.log_status IN ('insert', 'update'));

        UPDATE anime_changes
        SET watching_changes = watching_changes + 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.new_status = 'watching' AND log_list.log_status IN ('insert', 'update'));

        -- save delete and update changes
        UPDATE anime_changes
        SET score_changes = score_changes - new_score
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.log_status IN ('delete', 'update') AND log_list.old_status IN ('completed', 'dropped'));

        UPDATE anime_changes
        SET plan_to_watch_changes = plan_to_watch_changes - 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'plan to watch' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET completed_changes = completed_changes - 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'completed' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET dropped_changes = dropped_changes - 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'dropped' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET on_hold_changes = on_hold_changes - 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'on hold' AND log_list.log_status IN ('delete', 'update'));

        UPDATE anime_changes
        SET watching_changes = watching_changes - 1
        WHERE anime_changes.anime_id IN (SELECT anime_id FROM log_list WHERE log_list.old_status = 'watching' AND log_list.log_status IN ('delete', 'update'));

        -- update animes changes

        -- set new score
        UPDATE anime
        SET anime.score =
        ((anime.score * (anime.completed_count + anime.dropped_count)) + anime_changes.score_changes) / (anime.completed_count + anime_changes.completed_changes + anime.dropped_count + anime_changes.dropped_changes)
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.score_changes != 0);

        -- set new status count
        UPDATE anime
        SET anime.plan_to_watch_count = anime.plan_to_watch_count + anime_changes.plan_to_watch_changes
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.plan_to_watch_changes != 0);

        UPDATE anime
        SET anime.completed_count = anime.completed_count + anime_changes.completed_changes
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.completed_changes != 0);

        UPDATE anime
        SET anime.dropped_count = anime.dropped_count + anime_changes.dropped_changes
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.dropped_changes != 0);

        UPDATE anime
        SET anime.on_hold_count = anime.on_hold_count + anime_changes.on_hold_changes
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.on_hold_changes != 0);

        UPDATE anime
        SET anime.watching_count = anime.watching_count + anime_changes.watching_changes
        WHERE anime.anime_id IN (SELECT anime_id FROM anime_changes WHERE anime_changes.watching_changes != 0);

        -- clear log_list table
        TRUNCATE log_list;
    END //
DELIMITER ;