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

CREATE TABLE IF NOT EXISTS anime(
    anime_id INT PRIMARY KEY,
    anime_name VARCHAR(100) NOT NULL,
    anime_status ENUM('currently_airing', 'not_yet_aired', 'finished_airing') NOT NULL,
    score FLOAT(4, 2) NOT NULL DEFAULT 0,
    CONSTRAINT score_range_anime_table CHECK (score>=0 AND score<=10),
    episodes INT DEFAULT 0,
    year YEAR NOT NULL,
    season ENUM('spring', 'summer', 'fall', 'winter') NOT NULL,
    avg_episodes_time INT NOT NULL,
    plan_to_watch_count INT DEFAULT 0,
    completed_count INT DEFAULT 0,
    dropped_count INT DEFAULT 0,
    on_hold_count INT DEFAULT 0,
    watching_count INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS genre(
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(30) NOT NULL,
    anime_numbers INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS studio(
    studio_id INT PRIMARY KEY,
    studio_name VARCHAR(30) NOT NULL,
    product_numbers INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS anime_production_studio(
    anime_id INT,
    studio_id INT,
    PRIMARY KEY (anime_id, studio_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(studio_id) REFERENCES studio(studio_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS anime_genres(
    anime_id INT,
    genre_id INT,
    PRIMARY KEY (anime_id, genre_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS list(
    anime_id INT,
    account_id INT,
    PRIMARY KEY (anime_id, account_id),
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE,
    score FLOAT(4, 2) NOT NULL DEFAULT 0,
    CONSTRAINT score_range_list_table CHECK (score>=0 AND score<=10),
    status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching'),
    episodes_watched INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS log_list(
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    log_status ENUM('insert', 'delete', 'update') NOT NULL,
    anime_id INT NOT NULL,
    FOREIGN KEY(anime_id) REFERENCES anime(anime_id) ON DELETE CASCADE,
    new_score FLOAT(4, 2) DEFAULT 0,
    old_score FLOAT(4, 2) DEFAULT 0,
    CONSTRAINT new_score_range_log_list_table CHECK (new_score>=0 AND score<=10),
    CONSTRAINT old_score_range_log_list_table CHECK (old_score>=0 AND score<=10),
    new_status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching'),
    old_status ENUM('plan to watch', 'completed', 'dropped', 'on hold', 'watching')
);