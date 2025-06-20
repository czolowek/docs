from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Person(db.Model):
    __tablename__ = 'person'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Основная информация
    full_name = db.Column(db.String(200), nullable=False)
    nickname = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    
    # Семья
    father_name = db.Column(db.String(200))
    mother_name = db.Column(db.String(200))
    siblings = db.Column(db.Text)
    
    # Контакты
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(120))
    telegram = db.Column(db.String(100))
    vk_profile = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    other_social = db.Column(db.Text)
    
    # Адрес
    current_address = db.Column(db.String(500))
    home_address = db.Column(db.String(500))
    work_address = db.Column(db.String(500))
    
    # Работа/учеба
    work_place = db.Column(db.String(300))
    job_title = db.Column(db.String(200))
    education = db.Column(db.String(300))
    school = db.Column(db.String(300))
    
    # Дополнительная информация
    car_info = db.Column(db.String(200))
    hobbies = db.Column(db.Text)
    additional_info = db.Column(db.Text)
    photos = db.Column(db.Text)  # URLs фотографий
    
    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by = db.Column(db.String(100))  # Кто добавил
    
    def __repr__(self):
        return f'<Person {self.full_name}>'

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(500), nullable=False)
    search_type = db.Column(db.String(50))  # name, phone, email, etc
    results_count = db.Column(db.Integer, default=0)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Search {self.search_query}>'
