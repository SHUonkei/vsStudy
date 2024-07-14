PRAGMA foreign_keys=true;
-- Drop existing tables if you want to overwrite data (optional)
DROP TABLE IF EXISTS achievements;
DROP TABLE IF EXISTS battles;
DROP TABLE IF EXISTS educational_materials;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS studyrecords;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
	id VARCHAR PRIMARY KEY,
	name VARCHAR,
	email VARCHAR,
	password VARCHAR,
	date TIMESTAMP,
	icon_path VARCHAR
);

-- drop table tracks;
CREATE TABLE studyrecords (
	record_id VARCHAR,
	player_id VARCHAR,
	date TIMESTAMP,
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	educational_material_id VARCHAR,
	FOREIGN KEY (player_id) REFERENCES players (id),
	FOREIGN KEY (educational_material_id) REFERENCES educational_materials (id)
);

CREATE TABLE subjects (
	id VARCHAR PRIMARY KEY,
	name VARCHAR
);

CREATE TABLE educational_materials (
	id VARCHAR PRIMARY KEY,
	name VARCHAR,
	subject_id VARCHAR,
	FOREIGN KEY (subject_id) REFERENCES subjects (id)
);

CREATE TABLE battles(
	id VARCHAR PRIMARY KEY,
	player_id VARCHAR,
	opponent_id VARCHAR,
	date TIMESTAMP,
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	winner_id VARCHAR,
	current_state VARCHAR,-- 'pending', 'playing', 'finished'
	FOREIGN KEY (player_id) REFERENCES players (id),
	FOREIGN KEY (opponent_id) REFERENCES players (id),
	FOREIGN KEY (winner_id) REFERENCES players (id)
);


CREATE TABLE achievements (
	id VARCHAR PRIMARY KEY,
	player_id VARCHAR,
	total_study_time INTEGER,
	total_win INTEGER,
	total_lose INTEGER,
	total_draw INTEGER,
	FOREIGN KEY (player_id) REFERENCES players (id)
);

-- ビューの作成
# このビューは、プレイヤーのランキングを表示するためのビュー
create view rankings as
SELECT 
    p.name,
    p.icon_path,
    a.total_study_time,
    a.total_win,
    a.total_lose,
    a.total_draw
FROM players p
JOIN achievements a
ON p.id = a.player_id

-- プレイヤーのランキングを表示するためのビュー
