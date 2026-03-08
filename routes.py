from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app
from models import Person, SearchHistory
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.core.paginator import Paginator

@app.route('/')
def index():
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
    
    return render_template('cyber_index.html', stats=stats, 
                         recent_searches=recent_searches, 
                         recent_people=recent_people)

@app.route('/add')
def add_person():
    return render_template('add_person.html')

@app.route('/add', methods=['POST'])
def add_person_submit():
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
        
        person.save()
        
        flash('Информация о человеке успешно добавлена!', 'success')
        return redirect(url_for('view_person', person_id=person.id))
        
    except Exception as e:
        flash(f'Ошибка при добавлении: {str(e)}', 'error')
        return redirect(url_for('add_person'))

@app.route('/search')
def search():

    query = request.args.get('q', '')
    search_type = request.args.get('type', 'name')
    results = []
    
    if query:
        search_record = SearchHistory()
        search_record.search_query = query
        search_record.search_type = search_type
        search_record.ip_address = request.environ.get('REMOTE_ADDR', 'unknown')
        
        if search_type == 'name':
            results = list(Person.objects.filter(Q(full_name__icontains=query) | Q(nickname__icontains=query)))
        elif search_type == 'phone':
            results = list(Person.objects.filter(phone_number__icontains=query))
        elif search_type == 'email':
            results = list(Person.objects.filter(email__icontains=query))
        elif search_type == 'address':
            results = list(Person.objects.filter(Q(current_address__icontains=query) | Q(home_address__icontains=query) | Q(work_address__icontains=query)))
        elif search_type == 'social':
            results = list(Person.objects.filter(Q(telegram__icontains=query) | Q(vk_profile__icontains=query) | Q(instagram__icontains=query)))
        
        search_record.results_count = len(results)
        search_record.save()
    
    return render_template('search.html', results=results, query=query, search_type=search_type)

@app.route('/person/<int:person_id>')
def view_person(person_id):
    try:
        person = Person.objects.get(id=person_id)
        return render_template('person_detail.html', person=person)
    except Person.DoesNotExist:
        return "Не найдено", 404

@app.route('/person/<int:person_id>/edit')
def edit_person(person_id):
    try:
        person = Person.objects.get(id=person_id)
        return render_template('edit_person.html', person=person)
    except Person.DoesNotExist:
        return "Не найдено", 404

@app.route('/person/<int:person_id>/edit', methods=['POST'])
def edit_person_submit(person_id):
    try:
        person = Person.objects.get(id=person_id)
        
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
        
        person.save()
        flash('Информация обновлена!', 'success')
        return redirect(url_for('view_person', person_id=person.id))
        
    except Person.DoesNotExist:
        return "Не найдено", 404
    except Exception as e:
        flash(f'Ошибка при обновлении: {str(e)}', 'error')
        return redirect(url_for('edit_person', person_id=person_id))

@app.route('/list')
def list_people():
    page = request.args.get('page', 1, type=int)
    people_query = Person.objects.order_by('-created_at')
    
    paginator = Paginator(people_query, 20)
    people = paginator.get_page(page)
    
    return render_template('people_list.html', people=people)

@app.route('/stats')
def stats():
    total_people = Person.objects.count()
    total_searches = SearchHistory.objects.count()
    recent_people = Person.objects.order_by('-created_at')[:10]
    
    popular_searches_query = SearchHistory.objects.values('search_query').annotate(
        count=Count('id')).order_by('-count')[:10]
        
    popular_searches = [(s['search_query'], s['count']) for s in popular_searches_query]
    
    return render_template('stats.html', 
                         total_people=total_people, 
                         total_searches=total_searches,
                         recent_people=recent_people,
                         popular_searches=popular_searches)

@app.route('/api/stats')
def api_stats():

    stats = {
        'total_people': Person.objects.count(),
        'total_searches': SearchHistory.objects.count(),
        'people_this_week': Person.objects.filter(created_at__gte=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)).count(),
        'unique_visitors': SearchHistory.objects.values('ip_address').distinct().count()
    }
    return jsonify(stats)