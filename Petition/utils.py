import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from django.db.models import Count
from .models import Petition, Signature

def generate_signature_chart(petition_id):
    petition = Petition.objects.get(pk=petition_id)
    
    # Получение данных о количестве подписей за каждый день для данной петиции
    signatures_by_day = Signature.objects.filter(petition=petition).values('created_at__date').annotate(signature_count=Count('id'))
    
    # Разделение данных на даты и количество подписей
    dates = [entry['created_at__date'] for entry in signatures_by_day]
    signature_counts = [entry['signature_count'] for entry in signatures_by_day]
    
    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.plot(dates, signature_counts, marker='o', color='b', linestyle='-')
    plt.xlabel('Дата')
    plt.ylabel('Количество подписей')
    plt.title(f'Количество подписей за каждый день для петиции "{petition.title}"')
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # Формат даты по оси x
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Сохранение графика во временный файл
    temp_file_path = f"signature_chart_{petition_id}.png"
    plt.savefig('media/' + temp_file_path)
    plt.close()
    
    return temp_file_path
