DELIMITER //
    -- changing account status
    DROP PROCEDURE IF EXISTS change_account_status;

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
    DROP PROCEDURE IF EXISTS calculate_and_clear_log_list;

    CREATE PROCEDURE calculate_and_clear_log_list()
    BEGIN
        -- increase status count
        UPDATE anime
        SET anime.plan_to_watch_count = anime.plan_to_watch_count + 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'plan to watch' AND log_list.log_status IN ('insert', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.completed_count = anime.completed_count + 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'completed' AND log_list.log_status IN ('insert', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.dropped_count = anime.dropped_count + 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'dropped' AND log_list.log_status IN ('insert', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.on_hold_count = anime.on_hold_count + 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'on hold' AND log_list.log_status IN ('insert', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.watching_count = anime.watching_count + 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'watching' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;

        -- decrease status count
        UPDATE anime
        SET anime.plan_to_watch_count = anime.plan_to_watch_count - 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'plan to watch' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.completed_count = anime.completed_count - 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'completed' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.dropped_count = anime.dropped_count - 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'dropped' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.on_hold_count = anime.on_hold_count - 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'on hold' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;

        UPDATE anime
        SET anime.watching_count = anime.watching_count - 1
        WHERE anime.anime_id = log_list.anime_id AND log_list.new_status = 'watching' AND log_list.log_status IN ('delete', 'update') AND log_list.new_status != log_list.old_status;
    END //
DELIMITER ;