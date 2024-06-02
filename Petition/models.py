import datetime
from django.db import models
from Aut.models import People


# Категория петиции
class CategoryPetition(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория петиции')
    
    class Meta:
        verbose_name = 'Категория петиции'
        verbose_name_plural = 'Категория петиции'

    def __str__(self):
        return self.name


# Модель петиции
class Petition(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок петиции')
    description = models.TextField(verbose_name='Описание петиции')
    author = models.ForeignKey(People, on_delete=models.CASCADE, related_name='author_pet')
    img = models.ImageField(upload_to='petition_img', blank=True, null=True, verbose_name='Изображение петиции')
    file = models.FileField(null=True, blank=True, verbose_name='Файл')
    category = models.ForeignKey(CategoryPetition, on_delete=models.CASCADE, related_name='categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1)
    date_end = models.DateField(null=True, blank=True)
    signature_chart = models.ImageField(upload_to='signature_charts/', blank=True, null=True)


    @property
    def signers(self):
        return self.petition_signature.count()
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = self.file.name.replace(' ', '_')

        # Дата оканчания 3 месяца после создания 
        if self.created_at:
            self.date_end = self.created_at + datetime.timedelta(days=90)
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name = 'Петиция'
        verbose_name_plural = 'Петиции'


    def __str__(self):
        return self.title
    
    
        
# Хранение изображений
class Image(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='petition_images')
    image = models.ImageField(upload_to='petition_img', blank=True, null=True)
    
    def __str__(self):
        return self.petition.title
    
    
# Подпись
class Signature(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name='people_signature')
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='petition_signature')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'Подпись'
    
    
    
    
class Grapic(models.Model):
    by_city = models.ImageField(upload_to='petition_grapic', blank=True, null=True)
    by_answer = models.ImageField(upload_to='petition_grapic', blank=True, null=True)
    by_month = models.ImageField(upload_to='petition_grapic', blank=True, null=True)
    

    def __str__(self):
        return self.petition.title
