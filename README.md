#  🎉 Render にデプロイ完了 

 ## 構成

```text
Python Webフレームワーク  : Django
PaaS（クラウド公開        : Render
ソースコード管理.         : GitHub
```

## 開発環境（ローカル）

 #基本ルール
開発中は Django の開発サーバーを使用
DEBUG=True で動かす

 #起動コマンド🧑‍💻 開発中

```bash
s
DEBUG=true python manage.py runserver

```

### 「作る・試す」はローカル、「公開」は GitHub に push した瞬間

無料プランでは「本番サーバーに入るターミナル」は存在しません

## 本番環境（Render）

 #基本ルール
DEBUG は必ず False
環境変数は Render 側で管理
静的ファイルは collectstatic + WhiteNoise（manifest方式）

 #Render の Environment 設定

 ```text
 DEBUG=false
 ```

 #デプロイ時に実行されるコマンド

 ```bash
 python manage.py collectstatic --noinput
 ```

 これにより：
staticfiles.json（manifest）が生成される
WhiteNoise が正しく静的ファイルを配信する
本番向けの安全な挙動になる

デプロイ時に実行されるコマンド
python manage.py collectstatic --noinput

これにより：
staticfiles.json（manifest）が生成される
WhiteNoise が正しく静的ファイルを配信する
本番向けの安全な挙動になる

🛠 便利ワザ（開発効率UP）
方法①：alias（おすすめ）
毎回長いコマンドを打たないために：

```bash
alias djrun='DEBUG=true python manage.py runserver'

以後はこれだけ👇
djrun
```

方法②：.env ファイル（開発用）

.env

DEBUG=true

⚠️ 注意：
.env は 必ず .gitignore に追加
本番では使わない（Render の Environment を使う）

## アクセス先

[PaaS「クラウド公開サービス」](https://dashboard.render.com/)　/
[GitHub「プログラムの保管」 ](https://github.com/canape360/django_diary)　/

[管理画面/ログイン画面](https://django-diary.onrender.com/admin/login/?next=/admin/)　/
[アプリ/ログイン画面](https://django-diary.onrender.com/)　/

[日記アプリ/ログイン画面](https://django-canape-1.onrender.com/)　/
[管理画面へログイン](https://django-canape-1.onrender.com/admin/)

```bash
/admin/auth/user/　　　：を付けてユーザーの違いを見る
```
