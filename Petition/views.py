import matplotlib.pyplot as plt

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from Aut.models import People, City
from Chin.models import PetitionAnswer

from .models import Petition, CategoryPetition, Image, Signature, Grapic
from .utils import generate_signature_chart


# Создание петиции
@login_required
def create_petition(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        files = request.FILES.getlist('img') 
        file = request.FILES.get('file')
        author = People.objects.get(pk=request.user.id) 

        category_id = request.POST.get('category')
        
        category = CategoryPetition.objects.get(pk=category_id)
        
        # Создаем петицию с полученными данными
        petition = Petition.objects.create(
            title=title, 
            description=description, 
            file=file,
            img=files[0],
            author=author,
            category=category,
        )
        petition.save()
        
        for img in files[1:]:
            Image.objects.create(petition=petition, image=img)
      
        return redirect('all_petition')
    
    categories = CategoryPetition.objects.all()
    context = {
        'categories': categories
    }
        
    return render(request, 'petition/create_petition.html', context)


# Отображение всех петиций 
@login_required
def all_petition(request):
    petitions = Petition.objects.all().order_by('-created_at')
    categories = CategoryPetition.objects.all()
    cities = City.objects.all()

    # Get filter parameters from the request
    category_id = request.GET.get('category')
    city = request.GET.get('city')
    min_signatures = request.GET.get('min_signatures')
    keyword = request.GET.get('keyword')
        

    # Apply filters
    if keyword:
        petitions = petitions.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))

    if category_id:
        petitions = petitions.filter(category_id=category_id)
    
    if city:
        petitions = petitions.filter(author__city=city)

    if min_signatures:
        petitions = [petition for petition in petitions if petition.signers >= int(min_signatures)]
    

    context = {
        'petitions': petitions,
        'categories': categories,
        'cities': cities,
    }
    return render(request, 'petition/all_petition.html', context)


# Страница петиции
@login_required
def detail_pet(request, id):
    is_signed = False
    petition = Petition.objects.get(pk=id)
    
    # Генерация графика подписей для текущей петиции
    chart_file_path = generate_signature_chart(petition.id)
    
    # Обновление пути к графику в объекте петиции
    petition.signature_chart = chart_file_path
    petition.save()
    
    if request.user.status == 'Народ':
        if Signature.objects.filter(petition=petition, people=request.user).exists():
            is_signed = True
            
    context = {
        'petition': petition,
        'is_signed': is_signed, 
    }    
    return render(request, 'petition/detail_pet.html', context)

# Подпись
@login_required
def signature(request, p_id):
    petition = Petition.objects.get(pk=p_id)
    people = People.objects.get(pk=request.user.id)
    if Signature.objects.filter(petition=petition, people=people).exists():
        return redirect('detail_pet', p_id)
    Signature.objects.create(petition=petition, people=people)
    return redirect('detail_pet', p_id)
    


def get_petition_count_by_city():
    cities = City.objects.all()
    data = {}

    for i in cities:
        data[i.name] = Petition.objects.filter(author__city=i).count()

    return data


def get_petition_count_by_month():
    petitions_by_month = Petition.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        petition_count=Count('id')
    ).order_by('month')

    # Преобразование результатов запроса в словарь
    petition_count_by_month = {entry['month'].strftime('%Y.%m'): entry['petition_count'] for entry in petitions_by_month}

    return petition_count_by_month




def get_answered_petitions_count():
    # Получение данных о количестве ответов на каждую петицию
    answers_count = PetitionAnswer.objects.values('petition').annotate(answer_count=Count('id'))

    # Подсчет количества петиций, на которые были даны ответы
    answered_petitions_count = {entry['petition']: entry['answer_count'] for entry in answers_count}

    return answered_petitions_count


# Matplotlip
@login_required
def chart(request):
    # Получение данных о количестве петиций и отвеченных петиций
    total_petitions_count = Petition.objects.count()
    answered_petitions_count = len(get_answered_petitions_count())

    # Создание графика для соотношения петиций и отвеченных петиций
    plt.figure(figsize=(8, 6))  # Размер графика (ширина, высота)
    categories = ['Всего петиций', 'Отвеченные петиции']
    counts = [total_petitions_count, answered_petitions_count]
    plt.bar(categories, counts, color=['blue', 'green'])
    plt.xlabel('Категории')            # Название оси x
    plt.ylabel('Количество петиций')   # Название оси y
    plt.title('Соотношение всех петиций и отвеченных петиций')  # Заголовок графика
    for index, value in enumerate(counts):
        plt.text(index, value, str(value), ha='center', va='bottom', fontsize=10, color='black')
    temp_file_path = "chart_ans.png"
    plt.savefig('media/' + temp_file_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    # Создание графика для количества петиций по городам
    data_city = get_petition_count_by_city()
    cities = list(data_city.keys())
    values_city = list(data_city.values())
    plt.figure(figsize=(10, 6))  # Размер графика (ширина, высота)
    plt.bar(cities, values_city, color='orange', align='center')
    plt.xlabel('Города')            # Название оси x
    plt.ylabel('Количество петиций') # Название оси y
    plt.title('Количество петиций в разных городах')  # Заголовок графика
    for index, value in enumerate(values_city):
        plt.text(index, value, str(value), ha='center', va='bottom', fontsize=10, color='black')
    temp_file_path_city = "chart_city.png"
    plt.savefig('media/' + temp_file_path_city, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    # Создание графика для количества петиций по месяцам
    data_month = get_petition_count_by_month()
    months = list(data_month.keys())
    values_month = list(data_month.values())
    plt.figure(figsize=(10, 6))  # Размер графика (ширина, высота)
    plt.plot(months, values_month, marker='o', color='b', linestyle='-')
    plt.xlabel('Месяц')                 # Название оси x
    plt.ylabel('Количество петиций')    # Название оси y
    plt.title('Количество петиций по месяцам')  # Заголовок графика
    plt.xticks(rotation=45)
    for i, count in enumerate(values_month):
        plt.text(months[i], count, str(count), ha='center', va='bottom')
    temp_file_path_month = "chart_month.png"
    plt.savefig('media/' + temp_file_path_month, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    # Обновление или создание записи в модели Grapic
    g, created = Grapic.objects.update_or_create(
        by_city=temp_file_path_city,
        by_answer=temp_file_path,
        by_month=temp_file_path_month,
    )

    # Передача путей к временным файлам в контекст шаблона
    context = {'g': g}

    # Отображение шаблона с графиками
    return render(request, 'chart.html', context)
