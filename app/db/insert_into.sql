PRAGMA foreign_keys=true;

-- プレイヤーテーブルのシードデータ
INSERT INTO players (id, name, email, password, date, icon_path)
VALUES
  ('9b04277d-9365-4d88-9293-6b0e40608e63', 'root', 'root@example.com', 'scrypt:32768:8:1$ILMbJhx215N7NuHp$41848dc0edd0d84ca809fb25a596d0d3d029ac91634bd50bc957788a471a26bdfd1b117172a6afb84c098ab8d67c29d1e8096c37585c3ac5f07a1d3c0b7d31de', CURRENT_TIMESTAMP, 'shikanoko.webp'),
  ('0f0cd140-e67a-4aa5-a06e-46a7772a86ac', 'player1','player1@example.com', 'scrypt:32768:8:1$p1MM4BBU6avnoQDQ$3045298a72887d1386e553e06dd102f6a676240d2209e658a96ff3b0275025ca96db4184266bf72e44516d22ad83764421227380edd3bd3590e2418a0aba9b32', CURRENT_TIMESTAMP,'yagami.jpeg')
  ;

-- 学習科目テーブルのシードデータ
INSERT INTO subjects (id, name)
VALUES
  ('67ba0d37-a146-4fd1-b75c-fce7d3178e4e', '数学'),
  ('b74a5470-8c86-46ea-8c27-c62e95c2a532', '英語');

-- 学習教材テーブルのシードデータ
INSERT INTO educational_materials (id, name, subject_id)
VALUES
  ('d00520f4-6cf7-4ea5-980e-53e8e7dc482a', '数学基礎問題集', '67ba0d37-a146-4fd1-b75c-fce7d3178e4e'),
  ('ed2a31b3-c8b1-420d-85c8-f16f757e41df', '数学応用問題集', '67ba0d37-a146-4fd1-b75c-fce7d3178e4e'),
  ('dedee4b8-3621-434e-bf55-c48b5dd54e00', '英単語問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532'),
  ('d7973ffa-f509-48ce-a87e-e8abc81372c6', '英文法問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532'),
  ('c65f72f7-7323-4770-987b-c0fd3978ce69', '英文法問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532');

-- 学習記録テーブルのシードデータ
-- INSERT INTO studyrecords (record_id, player_id, date, start_time, end_time, educational_material_id)
-- VALUES
--   ('record1_id', 'player1_id', '2024-06-27' , '2024-06-27 10:00:00', '2024-06-27 11:00:00', 'material1_id'),
--   ('record2_id', 'player2_id', '2024-06-28', '2024-06-28 12:00:00', '2024-06-28 13:00:00', 'material2_id'),
--   ('record3_id', 'player3_id', '2024-06-28', '2024-06-28 13:00:00', '2024-06-28 15:00:00', 'material3_id');

-- バトル履歴テーブルのシードデータ (今回は勝敗データなし)
-- INSERT INTO battles (id, player_id, opponent_id, date, start_time, end_time,winner_id, current_state)
-- VALUES
--   ('battle1_id', 'player2_id', 'player3_id','2024-06-28', '2024-06-28 12:00:00', '2024-06-28 17:00:00', 'player2_id', 'finished'),
--   ('battle2_id', 'player1_id', 'player3_id','2024-06-28', '2024-06-28 12:00:00', '2024-06-28 19:00:00', 'player2_id', 'finished'),
--   ('battle3_id', 'player1_id', 'player2_id','2024-06-27', '2024-06-27 10:00:00', '2024-06-27 21:00:00', 'player1_id', 'finished');

-- 到達状況テーブルのシードデータ (今回は達成度データなし)
INSERT INTO achievements (id, player_id, total_study_time, total_win, total_lose, total_draw)
VALUES
  ('1e610096-5592-44b0-91eb-a9dd032e2101', '9b04277d-9365-4d88-9293-6b0e40608e63', 0, 0, 0, 0),
  ('203b5bf6-7cc5-44a2-9378-23fd45671b25', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac', 0, 0, 0, 0);

  -- CREATE VIEW all_achievements AS SELECT p.* FROM players p JOIN achievements a ON p.id = a.player_id;