from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_person_pdf(person):
    """Создает PDF с информацией о человеке в киберпанк стиле"""
    
    # Создаем буфер для PDF
    buffer = BytesIO()
    
    # Создаем документ
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Киберпанк стили
    title_style = ParagraphStyle(
        'CyberTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.green,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=20,
        spaceBefore=10
    )
    
    section_style = ParagraphStyle(
        'CyberSection',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold',
        spaceAfter=10,
        spaceBefore=15
    )
    
    content_style = ParagraphStyle(
        'CyberContent',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        fontName='Helvetica',
        spaceAfter=5
    )
    
    # Содержимое документа
    story = []
    
    # Заголовок
    story.append(Paragraph("CYBERPUNK DATABASE 2077", title_style))
    story.append(Paragraph("NIGHT CITY PERSONNEL RECORD", content_style))
    story.append(Spacer(1, 20))
    
    # Заголовок с именем
    title_text = f"ЛИЧНОЕ ДЕЛО: {person.full_name.upper()}"
    if person.nickname:
        title_text += f' "{person.nickname.upper()}"'
    story.append(Paragraph(title_text, section_style))
    story.append(Spacer(1, 15))
    
    # ID информация
    story.append(Paragraph(f"ID: NC-{person.id:06d} | STATUS: ACTIVE | CLEARANCE: LVL-{(person.id % 5) + 1}", content_style))
    story.append(Spacer(1, 15))
    
    # Основная информация
    if any([person.full_name, person.nickname, person.age, person.birth_date]):
        story.append(Paragraph("[ БИОМЕТРИЧЕСКИЕ ДАННЫЕ ]", section_style))
        
        bio_data = []
        if person.full_name:
            bio_data.append(["ПОЛНОЕ ИМЯ:", person.full_name])
        if person.nickname:
            bio_data.append(["КОДОВОЕ ИМЯ:", person.nickname])
        if person.age:
            bio_data.append(["ВОЗРАСТ:", f"{person.age} лет"])
        if person.birth_date:
            bio_data.append(["ДАТА РОЖДЕНИЯ:", person.birth_date.strftime('%d.%m.%Y')])
        
        if bio_data:
            bio_table = Table(bio_data, colWidths=[2*inch, 4*inch])
            bio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(bio_table)
            story.append(Spacer(1, 15))
    
    # Контактная информация
    if any([person.phone_number, person.email, person.telegram, person.vk_profile, person.instagram]):
        story.append(Paragraph("[ КАНАЛЫ СВЯЗИ ]", section_style))
        
        contact_data = []
        if person.phone_number:
            contact_data.append(["ТЕЛЕФОН:", person.phone_number])
        if person.email:
            contact_data.append(["EMAIL:", person.email])
        if person.telegram:
            contact_data.append(["TELEGRAM:", person.telegram])
        if person.vk_profile:
            contact_data.append(["VK PROFILE:", person.vk_profile])
        if person.instagram:
            contact_data.append(["INSTAGRAM:", person.instagram])
        
        if contact_data:
            contact_table = Table(contact_data, colWidths=[2*inch, 4*inch])
            contact_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(contact_table)
            story.append(Spacer(1, 15))
    
    # Геолокация
    if any([person.current_address, person.home_address, person.work_address]):
        story.append(Paragraph("[ КООРДИНАТЫ МЕСТОПОЛОЖЕНИЯ ]", section_style))
        
        location_data = []
        if person.current_address:
            location_data.append(["ТЕКУЩИЙ АДРЕС:", person.current_address])
        if person.home_address:
            location_data.append(["ДОМАШНИЙ АДРЕС:", person.home_address])
        if person.work_address:
            location_data.append(["РАБОЧИЙ АДРЕС:", person.work_address])
        
        if location_data:
            location_table = Table(location_data, colWidths=[2*inch, 4*inch])
            location_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(location_table)
            story.append(Spacer(1, 15))
    
    # Профессиональная деятельность
    if any([person.work_place, person.job_title, person.education, person.school]):
        story.append(Paragraph("[ ПРОФЕССИОНАЛЬНАЯ ДЕЯТЕЛЬНОСТЬ ]", section_style))
        
        work_data = []
        if person.work_place:
            work_data.append(["КОРПОРАЦИЯ:", person.work_place])
        if person.job_title:
            work_data.append(["ДОЛЖНОСТЬ:", person.job_title])
        if person.education:
            work_data.append(["ОБРАЗОВАНИЕ:", person.education])
        if person.school:
            work_data.append(["УЧЕБНОЕ ЗАВЕДЕНИЕ:", person.school])
        
        if work_data:
            work_table = Table(work_data, colWidths=[2*inch, 4*inch])
            work_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(work_table)
            story.append(Spacer(1, 15))
    
    # Семейные связи
    if any([person.father_name, person.mother_name, person.siblings]):
        story.append(Paragraph("[ СЕМЕЙНЫЕ СВЯЗИ ]", section_style))
        
        family_data = []
        if person.father_name:
            family_data.append(["ОТЕЦ:", person.father_name])
        if person.mother_name:
            family_data.append(["МАТЬ:", person.mother_name])
        if person.siblings:
            family_data.append(["РОДСТВЕННИКИ:", person.siblings])
        
        if family_data:
            family_table = Table(family_data, colWidths=[2*inch, 4*inch])
            family_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(family_table)
            story.append(Spacer(1, 15))
    
    # Дополнительная информация
    if any([person.car_info, person.hobbies, person.additional_info]):
        story.append(Paragraph("[ ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ ]", section_style))
        
        additional_data = []
        if person.car_info:
            additional_data.append(["ТРАНСПОРТ:", person.car_info])
        if person.hobbies:
            additional_data.append(["ИНТЕРЕСЫ:", person.hobbies])
        if person.additional_info:
            additional_data.append(["ПРИМЕЧАНИЯ:", person.additional_info])
        
        if additional_data:
            additional_table = Table(additional_data, colWidths=[2*inch, 4*inch])
            additional_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(additional_table)
            story.append(Spacer(1, 15))
    
    # Метаданные
    story.append(Paragraph("[ МЕТАДАННЫЕ СИСТЕМЫ ]", section_style))
    
    meta_data = [
        ["ДАТА СОЗДАНИЯ:", person.created_at.strftime('%d.%m.%Y %H:%M') if person.created_at else 'Неизвестно'],
        ["ПОСЛЕДНЕЕ ОБНОВЛЕНИЕ:", person.updated_at.strftime('%d.%m.%Y %H:%M') if person.updated_at else 'Неизвестно'],
        ["ДОБАВЛЕНО ОПЕРАТОРОМ:", person.added_by or 'System Admin']
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(meta_table)
    
    # Финальная подпись
    story.append(Spacer(1, 30))
    story.append(Paragraph("--- END OF RECORD ---", ParagraphStyle(
        'Signature', parent=styles['Normal'], fontSize=8, textColor=colors.darkgreen,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )))
    story.append(Paragraph("This document contains classified information", ParagraphStyle(
        'Signature2', parent=styles['Normal'], fontSize=8, textColor=colors.darkgrey,
        alignment=TA_CENTER, fontName='Helvetica'
    )))
    story.append(Paragraph("Unauthorized access is prohibited by law", ParagraphStyle(
        'Signature3', parent=styles['Normal'], fontSize=8, textColor=colors.darkgrey,
        alignment=TA_CENTER, fontName='Helvetica'
    )))
    
    # Генерируем PDF
    doc.build(story)
    
    # Возвращаем буфер
    buffer.seek(0)
    return buffer