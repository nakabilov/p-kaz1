from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
  
    def create(self, email, password=None, password2=None, **extra_fields):
        print(email, password, password2, extra_fields)
        email = self.normalize_email(email)
        if not email:
            raise ValueError('Электрондық пошта өрісі орнатылуы керек!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create(email, password=password, **extra_fields)


# Модель ABS
class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=80, verbose_name='Фамилия')
    father_name = models.CharField(max_length=80, verbose_name='Отчество')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)

    STATUS_CHOICES = [
        ('Народ', 'Народ'),
        ('Сми', 'СМИ'),
        ('Чиновник', 'Чиновник'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Народ')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']    
    objects = UserManager()


    def __str__(self):
        return f' {self.last_name} {self.first_name}'



# Модель Города
class City(models.Model): 
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Город'

    def __str__(self):
        return self.name


# Модель народа
class People(User):
    iin = models.CharField(max_length=12, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='citizens')
    image = models.ImageField(upload_to='static/images/', null=True, blank=True)
    
    @property
    def count_petitions(self):
        return self.author_pet.count()

    
    class Meta:
        verbose_name = 'Народ'
        verbose_name_plural = 'Народ'

    def __str__(self):
        return self.username