-- create event for clear log_list every 10 minute
DROP EVENT IF EXISTS clear_log_list //


CREATE EVENT clear_log_list
ON SCHEDULE
EVERY 10 MINUTE
DO
    CALL calculate_and_clear_log_list();