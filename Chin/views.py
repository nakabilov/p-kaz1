from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from Petition.models import Petition, Signature
from .models import Chin
from .forms import PetitionAnswerForm
from .utils import send_notification_email


# Таблица с петициями
@login_required
def table_petit(request):
    chin = Chin.objects.filter(pk=request.user.id).exists()
    if chin:
        china = Chin.objects.get(pk=request.user.id)
        
        
        petitions = Petition.objects.filter(category=china.category) 
        context = {
            'petitions': petitions
        }
        
        return render(request, 'chin/table_petit.html', context)
    else:
        return redirect('index')


# Профиль петиции
@login_required
def detail_petit(request, id):
    chin = Chin.objects.filter(pk=request.user.id).exists()
    if chin:
        china = Chin.objects.get(pk=request.user.id)
        petition = Petition.objects.get(pk=id)
        form = PetitionAnswerForm()
        context = {
            'petition': petition,
            'form': form,
        }
        return render(request, 'chin/detail_petit.html', context)
    else:
        return redirect('index')


# Список подписавшихся
@login_required
def people_list(request, id):
    chin = Chin.objects.filter(pk=request.user.id).exists()
    
    if chin:
        petition = Petition.objects.get(pk=id)
        signatures = Signature.objects.filter(petition=petition)
        context = {
            'signatures': signatures
        }
        
        return render(request, 'chin/people_list.html', context)
    else:
        return redirect('index')


# Ответ
@login_required
def petition_answer(request, id):
    chin = Chin.objects.filter(pk=request.user.id).exists()
    if chin:
        if request.method == 'POST':
            form = PetitionAnswerForm(request.POST, request.FILES)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.petition_id = id
                answer.chinov_id = request.user.id
                answer.save()
                petition = Petition.objects.get(pk=id)
                petition.status = 4
                petition.save()
                
                # Отправляем сообщение при ответе
                send_notification_email(
                    email=petition.author.email, 
                    petition_title=petition.title,
                    answer=answer.text)
                
                return redirect('table_petit')
            else:
                print('error', form.errors)
        print('POST emes')
    print('Chin jok')
    
    

