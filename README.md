
# vsStudy
勉強時間対戦アプリ


全国の学生が勉強時間を競い合い、学力向上を目指すためのオンライン学習プラットフォーム。ユーザーは勉強記録を登録し、ランキングを通じて他の学生と競い合うことができ、ユーザ同士で日付ごとの勉強時間の多さを競うことができる。



ログイン機能を持つため、サンプルユーザを示す。適宜新規登録してください。
- メールアドレス：root@example.com
- パスワード：password


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

