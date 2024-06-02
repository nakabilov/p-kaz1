import re

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import People, City, User
from .signals import send_registration_email
from .utils import send_password_email
from django.contrib.auth import update_session_auth_hash
import random
import string




# Регистрация
def auth(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        iin = request.POST['iin']
        city_id = request.POST['city']
        father_name = request.POST['father_name']
        
        city = City.objects.get(id=city_id)
        
        if password != password2:
            messages.error(request, 'Құпия сөздер бірдей емес!')
            return render(request, 'auth.html', {'city': City.objects.all()})
        
        if not re.match(r'^\d{12}$', iin):
            messages.error(request, 'ЖСН 12 саннан бос орынсыз жазылуы керек')
            return render(request, 'auth.html', {'city': City.objects.all()})

        if len(password) < 8:
            messages.error(request, 'Құпия сөзде кемінде 8 таңба болуы керек')
            return render(request, 'auth.html', {'city': City.objects.all()})

        if People.objects.filter(email=email).exists():
            messages.error(request, 'бұл email қазірдің өзінде тіркелген!')
            return render(request, 'auth.html', {'city': City.objects.all()})

        if not first_name.isalpha():
            messages.error(request, '')
            return render(request, 'auth.html', {'city': City.objects.all()})
        
        if not last_name.isalpha():
            messages.error(request, 'Сіздің тегіңізде тек әріптер болуы керек!')
            return render(request, 'auth.html', {'city': City.objects.all()})

        if not father_name.isalpha():
            messages.error(request, 'Әкесінің аты: тек әріптер болуы керек!')
            return render(request, 'auth.html', {'city': City.objects.all()})

        
        user = People.objects.create(
            email=email, 
            first_name=first_name,
            last_name=last_name,
            password=password,
            password2=password2,
            father_name=father_name,
            iin=iin,
            city=city,
        )        
        login(request, user)
        
        send_registration_email(email)  
        
        return redirect('index') 

    city = City.objects.all()
    context = {
        'city': city
    }

    return render(request, 'auth.html', context)



def logins(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
        
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Сіз сәтті кірдіңіз!')
                return redirect('index')
            else:
                messages.error(request, 'Логин немесе құпия сөз дұрыс емес!')
        # except Exception:
                messages.error(request, 'Аутентификация кезінде қате пайда болды. Қайталап көріңіз.')
        else:
            messages.warning(request, 'Барлық өрістерді толтырыңыз!')
    
    return render(request, 'auth.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Сіз сәтті шықтыңыз!')
    return redirect('auth')


# Профиль
@login_required
def profile(request):
    return render(request, 'profile/profile.html')


@login_required
def edit_profile(request):
    try:
        profile = People.objects.get(id=request.user.id)
    except People.DoesNotExist:
        return redirect('index')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('father_name')
        image = request.FILES.get('image')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if current_password and new_password:
            if not request.user.check_password(current_password):
                context = {
                    'profile': profile,
                    'message': 'Ағымдағы құпия сөз дұрыс енгізілмеген'
                }
                return render(request, 'profile/edit_profile.html', context)
            
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

        profile.first_name = first_name
        profile.last_name = last_name
        profile.father_name = father_name
        if image:
            profile.image = image
        profile.save()
        
        return redirect('profile')
    
    context = {
        'profile': profile
    }
    return render(request, 'profile/edit_profile.html', context)



def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        print(user)
        print(email)
        if not user:
            context = {
                'message': 'Мұндай email бар пайдаланушы табылмады'
            }
            return render(request, 'auth/reset_password.html', context)
        
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        user.set_password(new_password)
        user.save()
        text = f"Сіздің жаңа құпия сөзіңіз: {new_password}"
        send_password_email(email, text)
        context = {
                'message': 'Поштаға жаңа құпия сөз жіберілді!'
            }
        return render(request, 'auth.html', context)
    return render(request, 'auth/reset_password.html')

    

@login_required
def change_password(request):
    print('change_password view accessed')
    if request.method == 'POST':
        print('POST request received')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user

        # Проверяем, что текущий пароль введен правильно
        if not user.check_password(current_password):
            context = {
                'message': 'Ағымдағы құпия сөз дұрыс енгізілмеген'
            }
            print('Incorrect current password')
            return render(request, 'profile/edit_profile.html', context)

        # Устанавливаем новый пароль
        print('Setting new password')
        user.set_password(new_password)
        user.save()

        # Обновляем сессию пользователя, чтобы он оставался залогиненным после смены пароля
        update_session_auth_hash(request, user)
        
        context = {
            'message': 'Құпия сөз сәтті өзгертілді!'
        }
        print('Password changed successfully')
        return render(request, 'auth.html', context)

    print('Rendering edit_profile.html')
    return render(request, 'profile/edit_profile.html')
