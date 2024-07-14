PRAGMA foreign_keys=true;

-- プレイヤーテーブルのシードデータ
INSERT INTO players (id, name, email, password, date, icon_path)
VALUES
  ('9b04277d-9365-4d88-9293-6b0e40608e63', 'root', 'root@example.com', '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', CURRENT_TIMESTAMP, 'shikanoko.webp'),
  ('0f0cd140-e67a-4aa5-a06e-46a7772a86ac', 'player1', 'player1@example.com', '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', CURRENT_TIMESTAMP, 'yagami.jpeg'),
  ('bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc', 'player2', 'player2@example.com', '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', CURRENT_TIMESTAMP, 'kuroe.webp'),
  ('96c2fe8c-2635-4864-9ee2-58553fb661bd', 'player3', 'player3@example.com', '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', CURRENT_TIMESTAMP, 'girl1.jpg')
  ;

-- 学習科目テーブルのシードデータ
INSERT INTO subjects (id, name)
VALUES
  ('67ba0d37-a146-4fd1-b75c-fce7d3178e4e', '数学'),
  ('b74a5470-8c86-46ea-8c27-c62e95c2a532', '英語'),
  ('c1b1b1b1-8as6-46ea-8c27-c62e95cqwvet', '国語'),
  ('d1b1b1b1-8af6-46ea-8c27-c62e9qwvetv2', '理科'),
  ('e1b1b1b1-8fs6-asfd-fweg-c62eqwvet532', '社会');

-- 学習教材テーブルのシードデータ
INSERT INTO educational_materials (id, name, subject_id)
VALUES
  ('d00520f4-6cf7-4ea5-980e-53e8e7dc482a', '数学基礎問題集', '67ba0d37-a146-4fd1-b75c-fce7d3178e4e'),
  ('ed2a31b3-c8b1-420d-85c8-f16f757e41df', '数学応用問題集', '67ba0d37-a146-4fd1-b75c-fce7d3178e4e'),
  ('dedee4b8-3621-434e-bf55-c48b5dd54e00', '英単語問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532'),
  ('d7973ffa-f509-48ce-a87e-e8abc81372c6', '英文法問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532'),
  ('c65f72f7-7323-4770-987b-c0fd3978ce69', '英文法問題集', 'b74a5470-8c86-46ea-8c27-c62e95c2a532')
  ;

-- 学習記録テーブルのシードデータ
INSERT INTO studyrecords (record_id, player_id, date, start_time, end_time, educational_material_id)
VALUES
  ('5d89b6e5-2e4a-4c19-b9d4-05c6c4e9b18d', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac', '2024-06-27', '2024-06-27 10:00:00', '2024-06-27 11:00:00', 'd00520f4-6cf7-4ea5-980e-53e8e7dc482a'),
  ('3e5f8a53-2a42-4f5c-a5d7-b9084c61b6c9', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc', '2024-06-28', '2024-06-28 12:00:00', '2024-06-28 13:00:00', 'ed2a31b3-c8b1-420d-85c8-f16f757e41df'),
  ('e763e1b2-5f3d-4729-8057-bf8c8d2e1f18', '9b04277d-9365-4d88-9293-6b0e40608e63', '2024-06-28', '2024-06-28 13:00:00', '2024-06-28 15:00:00', 'dedee4b8-3621-434e-bf55-c48b5dd54e00');

-- バトル履歴テーブルのシードデータ
INSERT INTO battles (id, player_id, opponent_id, date, start_time, end_time, winner_id)
VALUES
  ('d84d0985-ef4f-44a8-b56f-4b949d4c2763', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc', '9b04277d-9365-4d88-9293-6b0e40608e63', '2024-06-28', '2024-06-28 12:00:00', '2024-06-28 17:00:00', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc'),
  ('2a3b7a94-9e5c-4d4e-96a6-7eb2b0f18776', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac', '9b04277d-9365-4d88-9293-6b0e40608e63', '2024-06-28', '2024-06-28 12:00:00', '2024-06-28 19:00:00', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc'),
  ('6c2338a4-0b91-470f-a3f0-6db8b5c6b831', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc', '2024-06-27', '2024-06-27 10:00:00', '2024-06-27 21:00:00', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac');

-- 到達状況テーブルのシードデータ
INSERT INTO achievements (id, player_id, total_study_time, total_win, total_lose, total_draw)
VALUES
  ('1e610096-5592-44b0-91eb-a9dd032e2101', '9b04277d-9365-4d88-9293-6b0e40608e63', 120, 0, 1, 0),
  ('203b5bf6-7cc5-44a2-9378-23fd45671b25', '0f0cd140-e67a-4aa5-a06e-46a7772a86ac', 60, 1, 1, 0),
  ('q0qqwecr-dddq-aaa2-rrr8-23fasfwerqwv', 'bb4f74a0-65fc-41c0-b5a5-7ac8627a42bc', 60, 2, 0, 0),
  ('werb5bf6-7cc5-44a2-9378-23fd45671b25', '96c2fe8c-2635-4864-9ee2-58553fb661bd', 60, 0, 0, 0);

