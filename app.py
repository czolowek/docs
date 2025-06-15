import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timedelta

# Import models and db from models.py
from models import db, Person, SearchHistory

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "cyberpunk-secret-key-2077")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///cyberpunk_people.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)


# Routes
@app.route('/')
def index():
    """Главная страница с поиском людей"""
    # Получаем статистику
    total_people = Person.query.count()
    total_searches = SearchHistory.query.count()
    
    # Последние поиски
    recent_searches = SearchHistory.query.order_by(SearchHistory.searched_at.desc()).limit(5).all()
    
    # Последние добавленные люди
    recent_people = Person.query.order_by(Person.created_at.desc()).limit(5).all()
    
    # Статистика за последние 24 часа
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_additions = Person.query.filter(Person.created_at >= yesterday).count()
    
    # Люди с фотографиями
    with_photos = Person.query.filter(Person.photos.isnot(None), Person.photos != '').count()
    
    stats = {
        'total_people': total_people,
        'total_searches': total_searches,
        'recent_additions': recent_additions,
        'with_photos': with_photos
    }
    
    return render_template('index.html', stats=stats, 
                         recent_searches=recent_searches, 
                         recent_people=recent_people)

@app.route('/add')
def add_person():
    """Страница для добавления нового человека"""
    return render_template('add_person.html')

@app.route('/add', methods=['POST'])
def add_person_submit():
    """Обработка формы добавления человека"""
    try:
        birth_date_str = request.form.get('birth_date')
        age_str = request.form.get('age')
        
        person = Person()
        person.full_name = request.form.get('full_name')
        person.nickname = request.form.get('nickname')
        person.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str and birth_date_str.strip() else None
        person.age = int(age_str) if age_str and age_str.strip() else None
        person.father_name = request.form.get('father_name')
        person.mother_name = request.form.get('mother_name')
        person.siblings = request.form.get('siblings')
        person.phone_number = request.form.get('phone_number')
        person.email = request.form.get('email')
        person.telegram = request.form.get('telegram')
        person.vk_profile = request.form.get('vk_profile')
        person.instagram = request.form.get('instagram')
        person.other_social = request.form.get('other_social')
        person.current_address = request.form.get('current_address')
        person.home_address = request.form.get('home_address')
        person.work_address = request.form.get('work_address')
        person.work_place = request.form.get('work_place')
        person.job_title = request.form.get('job_title')
        person.education = request.form.get('education')
        person.school = request.form.get('school')
        person.car_info = request.form.get('car_info')
        person.hobbies = request.form.get('hobbies')
        person.additional_info = request.form.get('additional_info')
        person.photos = request.form.get('photos')
        person.added_by = request.form.get('added_by', 'Анонимный')
        
        db.session.add(person)
        db.session.commit()
        
        flash('Информация о человеке успешно добавлена в базу данных!', 'success')
        return redirect(url_for('view_person', person_id=person.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при добавлении: {str(e)}', 'error')
        return redirect(url_for('add_person'))

@app.route('/search')
def search():
    """Страница поиска"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'name')
    results = []
    
    if query:
        # Сохраняем поиск в историю
        search_record = SearchHistory()
        search_record.search_query = query
        search_record.search_type = search_type
        search_record.ip_address = request.environ.get('REMOTE_ADDR', 'unknown')
        
        if search_type == 'name':
            results = Person.query.filter(
                Person.full_name.ilike(f'%{query}%') |
                Person.nickname.ilike(f'%{query}%')
            ).all()
        elif search_type == 'phone':
            results = Person.query.filter(Person.phone_number.ilike(f'%{query}%')).all()
        elif search_type == 'email':
            results = Person.query.filter(Person.email.ilike(f'%{query}%')).all()
        elif search_type == 'address':
            results = Person.query.filter(
                Person.current_address.ilike(f'%{query}%') |
                Person.home_address.ilike(f'%{query}%') |
                Person.work_address.ilike(f'%{query}%')
            ).all()
        elif search_type == 'social':
            results = Person.query.filter(
                Person.telegram.ilike(f'%{query}%') |
                Person.vk_profile.ilike(f'%{query}%') |
                Person.instagram.ilike(f'%{query}%')
            ).all()
        
        search_record.results_count = len(results)
        db.session.add(search_record)
        db.session.commit()
    
    return render_template('search.html', results=results, query=query, search_type=search_type)

@app.route('/person/<int:person_id>')
def view_person(person_id):
    """Просмотр информации о человеке"""
    person = Person.query.get_or_404(person_id)
    return render_template('person_detail.html', person=person)

@app.route('/person/<int:person_id>/edit')
def edit_person(person_id):
    """Редактирование информации о человеке"""
    person = Person.query.get_or_404(person_id)
    return render_template('edit_person.html', person=person)

@app.route('/person/<int:person_id>/edit', methods=['POST'])
def edit_person_submit(person_id):
    """Обработка редактирования"""
    person = Person.query.get_or_404(person_id)
    
    try:
        person.full_name = request.form.get('full_name')
        person.nickname = request.form.get('nickname')
        birth_date_edit = request.form.get('birth_date')
        age_edit = request.form.get('age')
        person.birth_date = datetime.strptime(birth_date_edit, '%Y-%m-%d').date() if birth_date_edit and birth_date_edit.strip() else None
        person.age = int(age_edit) if age_edit and age_edit.strip() else None
        person.father_name = request.form.get('father_name')
        person.mother_name = request.form.get('mother_name')
        person.siblings = request.form.get('siblings')
        person.phone_number = request.form.get('phone_number')
        person.email = request.form.get('email')
        person.telegram = request.form.get('telegram')
        person.vk_profile = request.form.get('vk_profile')
        person.instagram = request.form.get('instagram')
        person.other_social = request.form.get('other_social')
        person.current_address = request.form.get('current_address')
        person.home_address = request.form.get('home_address')
        person.work_address = request.form.get('work_address')
        person.work_place = request.form.get('work_place')
        person.job_title = request.form.get('job_title')
        person.education = request.form.get('education')
        person.school = request.form.get('school')
        person.car_info = request.form.get('car_info')
        person.hobbies = request.form.get('hobbies')
        person.additional_info = request.form.get('additional_info')
        person.photos = request.form.get('photos')
        person.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('view_person', person_id=person.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении: {str(e)}', 'error')
        return redirect(url_for('edit_person', person_id=person_id))

@app.route('/list')
def list_people():
    """Список всех людей"""
    page = request.args.get('page', 1, type=int)
    people = Person.query.order_by(Person.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('people_list.html', people=people)

@app.route('/stats')
def stats():
    """Статистика базы данных"""
    total_people = Person.query.count()
    total_searches = SearchHistory.query.count()
    recent_people = Person.query.order_by(Person.created_at.desc()).limit(10).all()
    popular_searches = db.session.query(SearchHistory.search_query, db.func.count(SearchHistory.id)).group_by(SearchHistory.search_query).order_by(db.func.count(SearchHistory.id).desc()).limit(10).all()
    
    return render_template('stats.html', 
                         total_people=total_people, 
                         total_searches=total_searches,
                         recent_people=recent_people,
                         popular_searches=popular_searches)

@app.route('/api/stats')
def api_stats():
    """API endpoint для статистики"""
    stats = {
        'total_people': Person.query.count(),
        'total_searches': SearchHistory.query.count(),
        'people_this_week': Person.query.filter(Person.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)).count(),
        'unique_visitors': SearchHistory.query.distinct(SearchHistory.ip_address).count()
    }
    return jsonify(stats)


@app.route('/person/<int:person_id>/pdf')
def download_person_pdf(person_id):
    """Скачивание PDF карточки человека в стиле киберпанк"""
    person = Person.query.get_or_404(person_id)
    
    try:
        from simple_pdf import generate_person_pdf
        pdf_buffer = generate_person_pdf(person)
        
        # Создаем имя файла
        safe_name = "".join(c for c in person.full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"Cyberpunk_Profile_{safe_name}_{person.id}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Ошибка при создании PDF: {str(e)}', 'error')
        return redirect(url_for('view_person', person_id=person_id))


# Создание таблиц при запуске
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
