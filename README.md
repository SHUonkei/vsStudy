
# vsStudy
勉強時間対戦アプリ

## リレーション


![image](https://github.com/user-attachments/assets/7b837bbf-18a7-46ee-94eb-9291a7180563)



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

## 画面イメージ


![image](https://github.com/user-attachments/assets/33269b30-1815-4ae4-9497-c5704b09b4cb)
![image](https://github.com/user-attachments/assets/1d4bf694-8d1b-47a2-aa40-e8ff96428a82)

