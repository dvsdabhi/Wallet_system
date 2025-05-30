
# Currency Transfer API (Django + JWT + PostgreSQL)

A secure wallet application with support for INR and USD balances, JWT authentication, transaction logs, and live currency exchange using [Frankfurter API](https://www.frankfurter.app/).


## 🚀 Features

- User registration & login (JWT-based)
- Wallet with multi-currency support (INR & USD)
- View wallet balance
- Send money across users (currency conversion supported)
- Transaction history with filters


## ⚙️ Tech Stack

- Python 3.10+
- Django 5.x
- PostgreSQL
- JWT (via djangorestframework-simplejwt)
- Frankfurter API (Live currency rates)
- Python-Decouple (.env support)
- atomic (support for transaction)

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/dvsdabhi/Wallet_system.git
cd your-project
```

### 2. Create & activate virtual environment

```bash
python -m venv env
source env/bin/activate
env\Scripts\activate  # On Windows:
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .venv
sudo -u postgres psql
```

### 5. Setup PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE "db_name";
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the server:
```bash

python manage.py runserver

```
