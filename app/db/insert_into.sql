PRAGMA foreign_keys=true;

-- プレイヤーテーブルのシードデータ
INSERT INTO players (id, name, email, password, date)
VALUES
  ('player1_id', 'プレイヤー1', 'player1@example.com', 'password1', CURRENT_TIMESTAMP),
  ('player2_id', 'プレイヤー2', 'player2@example.com', 'password2', CURRENT_TIMESTAMP),
  ('player3_id', 'プレイヤー3', 'player3@example.com', 'password3', CURRENT_TIMESTAMP);

-- 学習科目テーブルのシードデータ
INSERT INTO subjects (id, name)
VALUES
  ('subject1_id', '数学'),
  ('subject2_id', '英語'),
  ('subject3_id', '理科');

-- 学習教材テーブルのシードデータ
INSERT INTO educational_materials (id, name, subject_id)
VALUES
  ('material1_id', '数学基礎問題集', 'subject1_id'),
  ('material2_id', '英単語帳', 'subject2_id'),
  ('material3_id', '理科実験ノート', 'subject3_id'),
  ('material4_id', '数学応用問題集', 'subject1_id'),
  ('material5_id', '英文法問題集', 'subject2_id'),
  ('material6_id', '理科実験レポート', 'subject3_id');

-- 学習記録テーブルのシードデータ
INSERT INTO studyrecords (record_id, player_id, date, start_time, end_time, educational_material_id)
VALUES
  ('record1_id', 'player1_id', '2024-06-27' , '2024-06-27 10:00:00', '2024-06-27 11:00:00', 'material1_id'),
  ('record2_id', 'player2_id', '2024-06-28', '2024-06-28 12:00:00', '2024-06-28 13:00:00', 'material2_id'),
  ('record3_id', 'player3_id', '2024-06-28', '2024-06-28 13:00:00', '2024-06-28 15:00:00', 'material3_id');

-- バトル履歴テーブルのシードデータ (今回は勝敗データなし)
INSERT INTO battles (id, player_id, opponent_id, date, start_time, end_time,winner_id)
VALUES
  ('battle1_id', 'player2_id', 'player3_id','2024-06-28', '2024-06-28 12:00:00', '2024-06-28 17:00:00', 'player2_id'),
  ('battle2_id', 'player1_id', 'player3_id','2024-06-28', '2024-06-28 12:00:00', '2024-06-28 19:00:00', 'player2_id'),
  ('battle3_id', 'player1_id', 'player2_id','2024-06-27', '2024-06-27 10:00:00', '2024-06-27 21:00:00', 'player1_id');

-- 到達状況テーブルのシードデータ (今回は達成度データなし)
INSERT INTO achievements (id, player_id, total_study_time, total_win, total_lose, total_draw)
VALUES
  ('achievement1_id', 'player1_id', 1, 1, 1, 0),
  ('achievement2_id', 'player2_id', 1, 2, 0, 0),
  ('achievement3_id', 'player3_id', 2, 0, 2, 0);

  CREATE VIEW all_achievements AS SELECT p.* FROM players p JOIN achievements a ON p.id = a.player_id;