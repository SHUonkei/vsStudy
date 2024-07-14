# vsStudy
勉強時間対戦アプリ

## initialization


```
cd db
sqlite3 -column -header studybattle.db
```


.dbファイルを共有しているため、以下の初期化はdbの変更をしたときに行うなどしてください.
sqlite内で以下を実行.


```
sqlite> .read create_table.sql
sqlite> .read insert_into.sql
```


.env ファイルを.env.sampleを参照に作成してください.


## 注釈

- 慶應義塾大学理工学部情報工学科3年授業内での製作
- 外部ライブラリを基本用いてはならない制約のもと
