import os
import sys
import django
from types import ModuleType
from django.conf import settings
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime, timedelta


cyber_models = ModuleType('cyber_models')
cyber_models.__path__ = [os.path.abspath(os.path.dirname(__file__))]
sys.modules['cyber_models'] = cyber_models

from django.apps import AppConfig
class CyberModelsConfig(AppConfig):
    name = 'cyber_models'
    path = os.path.abspath(os.path.dirname(__file__))

cyber_models.CyberModelsConfig = CyberModelsConfig


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cyber_db.sqlite3')

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_PATH,
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'cyber_models.CyberModelsConfig',
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()


from django.apps import apps
Person = apps.get_model('cyber_models', 'Person')
SearchHistory = apps.get_model('cyber_models', 'SearchHistory')


from django.db import connection
def init_db():
    with connection.schema_editor() as schema_editor:
        tables = connection.introspection.table_names()
        if 'person' not in tables:
            schema_editor.create_model(Person)
        if 'search_history' not in tables:
            schema_editor.create_model(SearchHistory)

init_db()


app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "cyberpunk-2077-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)



@app.route('/')
def index():
    try:
        total_people = Person.objects.count()
        total_searches = SearchHistory.objects.count()
        
        recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
        recent_people = Person.objects.order_by('-created_at')[:5]
        
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_additions = Person.objects.filter(created_at__gte=yesterday).count()
        
        with_photos = Person.objects.exclude(photos__isnull=True).exclude(photos='').count()
        
        stats = {
            'total_people': total_people,
            'total_searches': total_searches,
            'recent_additions': recent_additions,
            'with_photos': with_photos
        }
        return render_template('index.html', stats=stats, 
                             recent_searches=recent_searches, 
                             recent_people=recent_people)
    except Exception as e:
        init_db()
        return f"Системная ошибка инициализации. Перезагрузите страницу. ({str(e)})", 500

@app.route('/add')
def add_person():
    return render_template('add_person.html')

@app.route('/add', methods=['POST'])
def add_person_submit():
    try:
        birth_date_str = request.form.get('birth_date')
        age_str = request.form.get('age')
        
        person = Person.objects.create(
            full_name=request.form.get('full_name'),
            nickname=request.form.get('nickname'),
            birth_date=datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str and birth_date_str.strip() else None,
            age=int(age_str) if age_str and age_str.strip() else None,
            father_name=request.form.get('father_name'),
            mother_name=request.form.get('mother_name'),
            siblings=request.form.get('siblings'),
            phone_number=request.form.get('phone_number'),
            email=request.form.get('email'),
            telegram=request.form.get('telegram'),
            vk_profile=request.form.get('vk_profile'),
            instagram=request.form.get('instagram'),
            other_social=request.form.get('other_social'),
            current_address=request.form.get('current_address'),
            home_address=request.form.get('home_address'),
            work_address=request.form.get('work_address'),
            work_place=request.form.get('work_place'),
            job_title=request.form.get('job_title'),
            education=request.form.get('education'),
            school=request.form.get('school'),
            car_info=request.form.get('car_info'),
            hobbies=request.form.get('hobbies'),
            additional_info=request.form.get('additional_info'),
            photos=request.form.get('photos'),
            added_by=request.form.get('added_by', 'Анонимный')
        )
        flash('СУБЪЕКТ ЗАРЕГИСТРИРОВАН В БАЗЕ', 'success')
        return redirect(url_for('view_person', person_id=person.id))
    except Exception as e:
        flash(f'ОШИБКА ДОСТУПА: {str(e)}', 'error')
        return redirect(url_for('add_person'))

@app.route('/search')
def search():
    from django.db.models import Q
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'name')
    results = []
    
    if query:
        search_record = SearchHistory.objects.create(
            search_query=query, search_type=search_type,
            ip_address=request.environ.get('REMOTE_ADDR', 'unknown')
        )
        if search_type == 'name':
            results = Person.objects.filter(Q(full_name__icontains=query) | Q(nickname__icontains=query))
        elif search_type == 'phone':
            results = Person.objects.filter(phone_number__icontains=query)
        elif search_type == 'email':
            results = Person.objects.filter(email__icontains=query)
        elif search_type == 'address':
            results = Person.objects.filter(Q(current_address__icontains=query) | Q(home_address__icontains=query) | Q(work_address__icontains=query))
        elif search_type == 'social':
            results = Person.objects.filter(Q(telegram__icontains=query) | Q(vk_profile__icontains=query) | Q(instagram__icontains=query))
        
        search_record.results_count = results.count()
        search_record.save()
    
    return render_template('search.html', results=results, query=query, search_type=search_type)

@app.route('/person/<int:person_id>')
def view_person(person_id):
    try:
        person = Person.objects.get(id=person_id)
        return render_template('person_dateil.html', person=person)
    except Person.DoesNotExist:
        return "ДАННЫЕ ОТСУТСТВУЮТ", 404

@app.route('/person/<int:person_id>/edit')
def edit_person(person_id):
    try:
        person = Person.objects.get(id=person_id)
        return render_template('edit_person.html', person=person)
    except Person.DoesNotExist:
        return "ДАННЫЕ ОТСУТСТВУЮТ", 404

@app.route('/person/<int:person_id>/edit', methods=['POST'])
def edit_person_submit(person_id):
    try:
        person = Person.objects.get(id=person_id)
        for field in request.form:
            if hasattr(person, field):
                val = request.form.get(field)
                if field == 'birth_date':
                    setattr(person, field, datetime.strptime(val, '%Y-%m-%d').date() if val and val.strip() else None)
                elif field == 'age':
                    setattr(person, field, int(val) if val and val.strip() else None)
                else:
                    setattr(person, field, val)
        person.save()
        flash('ДОСЬЕ ОБНОВЛЕНО', 'success')
        return redirect(url_for('view_person', person_id=person.id))
    except Exception as e:
        flash(f'СБОЙ СИНХРОНИЗАЦИИ: {str(e)}', 'error')
        return redirect(url_for('edit_person', person_id=person_id))

@app.route('/list')
def list_people():
    from django.core.paginator import Paginator
    page = request.args.get('page', 1, type=int)
    paginator = Paginator(Person.objects.order_by('-created_at'), 20)
    people = paginator.get_page(page)
    return render_template('people_list.html', people=people)

@app.route('/stats')
def stats():
    from django.db.models import Count
    pop_q = SearchHistory.objects.values('search_query').annotate(c=Count('id')).order_by('-c')[:10]
    popular_searches = [(q['search_query'], q['c']) for q in pop_q]
    
    return render_template('stats.html', 
                         total_people=Person.objects.count(), 
                         total_searches=SearchHistory.objects.count(),
                         recent_people=Person.objects.order_by('-created_at')[:10],
                         popular_searches=popular_searches)

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'total_people': Person.objects.count(),
        'total_searches': SearchHistory.objects.count(),
        'status': 'ONLINE'
    })

@app.route('/person/<int:person_id>/pdf')
def download_person_pdf(person_id):
    try:
        person = Person.objects.get(id=person_id)
        from simple_pdf import generate_person_pdf
        pdf_buffer = generate_person_pdf(person)
        filename = f"CyberDoc_{person.id}.pdf"
        return send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
    except Exception as e:
        flash(f'ОШИБКА ЭКСПОРТА: {str(e)}', 'error')
        return redirect(url_for('view_person', person_id=person_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)