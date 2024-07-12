PRAGMA foreign_keys=true;
-- Drop existing tables if you want to overwrite data (optional)
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS educational_materials;
DROP TABLE IF EXISTS studyrecords;
DROP TABLE IF EXISTS battles;
DROP TABLE IF EXISTS achievements;

CREATE TABLE players (
	id VARCHAR PRIMARY KEY,
	name VARCHAR,
	email VARCHAR,
	password VARCHAR,
	date TIMESTAMP
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
