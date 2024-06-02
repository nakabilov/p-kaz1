from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse  
from .models import News, Smi, Comment, Like
from Petition.models import Petition
from .forms import CommentForms
from django.db.models import Count
from Aut.models import People
from django.contrib.auth.decorators import login_required




# Создание новости СМИ
@login_required
def create_news(request, p_id):
    smi_exists = Smi.objects.filter(pk=request.user.id).exists()
    if smi_exists:
        if request.method == 'POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            # file = request.FILES.get('file')
            image = request.FILES.getlist('image')            
            created_at = request.POST.get('created_at')
            author = Smi.objects.get(pk=request.user.id) 
            
            petition = Petition.objects.get(pk=p_id)
            
            cr_news = News(
                title=title,
                desc=desc,
                # file=file,
                image=image[0],
                petition=petition,
                author=author,
                created_at=created_at,
            )
            cr_news.save()
            
            return redirect('index')
        else:
            context = {
                'petition': Petition.objects.get(pk=p_id)
            }
            return render(request, 'news/create_news.html', context=context)    
    else:
        return redirect('index')


# Отображение главной страницы новостей
@login_required
def index(request):
    
    news = News.objects.all().order_by('-created_at')
    context = {
        'news': news
    }
    if request.user.is_authenticated:
        if request.user.status == 'Сми':
            context['smi'] = Smi.objects.get(pk=request.user.id)

    return render(request, 'index.html', context)


# Комменты
@login_required
def detail_news(request, id):
    news = News.objects.annotate(num_comments=Count('news_comments')).get(pk=id)
    # news = News.objects.get(pk=id)
    if request.method == 'POST':
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.people = request.user.people 
            comment.news = news
            comment.save()
            return redirect('detail_news', id=id)
    else:
        form = CommentForms()
    context = {
        'news': news,
        'form': form,
    }
    return render(request, 'news/detail_news.html', context)



@login_required
def like(request, n_id):
    news = get_object_or_404(News, pk=n_id)
    user = get_object_or_404(People, pk=request.user.id)
    
    if Like.objects.filter(news=news, people=user).exists():
        return redirect('index') 
    
    Like.objects.create(news=news, people=user)
    news.like = news.count_likes
    news.save()
    
    return redirect('index')
