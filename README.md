#  🎉🎉🎉 大成功です！ 🎉🎉🎉Render にデプロイ完了

```text
これからの「正しい運用ルール」
🧑‍💻 開発中（今）

DEBUG=true python manage.py runserver


これ一本でOK。

🚀 本番（Render など）

Render の Environment に：

DEBUG=false

デプロイ時に：

python manage.py collectstatic --noinput


これで manifest 方式が正しく動きます。
---
便利ワザ（毎回打ちたくない人向け）
方法1：alias（おすすめ）
alias djrun='DEBUG=true python manage.py runserver'


以後は：

djrun

方法2：.env（開発用）

.env に：

DEBUG=true


（※ .gitignore に .env を入れておく）

```





[Renderダッシュボードにログイン](https://dashboard.render.com/)

[利用github canape360](https://github.com/canape360/django_diary)

[django-diary](https://django-diary.onrender.com/)

[django-canape-1](https://django-canape-1.onrender.com/)

[Welcome to Django](https://django-diary.onrender.com/accounts/login/?next=/)

[管理画面/ログイン画面](https://django-diary.onrender.com/admin/login/?next=/admin/)

[本来のアプリ/ログイン画面](https://django-diary.onrender.com/)

[別物/ログイン画面](https://django-canape-1.onrender.com/)

[管理画面へログイン](https://django-canape-1.onrender.com/admin/)

 #管理画面へログイン

```bash
 

```


```bash
/admin/auth/user/　　　：を付けてユーザーの違いを見る
```
