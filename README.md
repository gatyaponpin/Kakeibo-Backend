# 環境構築

## 仮想環境作成&アクティベート

```bash
python -m venv venv
source venv/bin/activate 
```

## Django プロジェクト作成

```bash
pip install django djangorestframework psycopg2-binary dj-database-url python-dotenv django-cors-headers djangorestframework-simplejwt
django-admin startproject backend
cd backend
python manage.py startapp accounts
python manage.py startapp ledger
```

- 適宜モデルを修正
- マイグレーション

```bash
python manage.py makemigrations
python manage.py migrate
```
