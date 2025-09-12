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