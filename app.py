from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Настройка подключения к базе данных PostgreSQL:
#   - postgres:postgres - логин и пароль для подключения,
#   - db:5432 - контейнер db и порт,
#   - counter_db - название базы данных.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/counter_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Counter - это таблица в базе данных, имеет поля id, datetime, client_info 
class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    client_info = db.Column(db.String, nullable=False)

    def as_dict(self):
        return {"id": self.id, "datetime": self.datetime, "client_info": self.client_info}

# Создание таблицы
with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    # Получение заголовка User-Agent из запроса
    client_info = request.headers.get('User-Agent')
    # Создание новой записи в таблице Counter
    entry = Counter(datetime=datetime.now(timezone.utc), client_info=client_info)
    db.session.add(entry)
    db.session.commit()

    entries = Counter.query.all()
    return jsonify([entry.as_dict() for entry in entries]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
