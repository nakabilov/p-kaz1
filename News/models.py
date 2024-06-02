from django.db import models
from Petition.models import Petition
from Aut.models import User, People



class Smi(User):
    company_name = models.CharField(max_length=80)
    insta = models.CharField(max_length=80)
    site_url = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Сми'
        verbose_name_plural = 'Сми'

    def __str__(self):
        return self.company_name


class News(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(Smi, on_delete=models.CASCADE, related_name='author_smi')
    image = models.ImageField(upload_to='news_images', blank=True)
    file = models.FileField(upload_to='news_files', blank=True)
    views = models.PositiveBigIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def count_likes(self):
        return self.news_like.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name='people_id', blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_comments', blank=True)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.people.username} написал {self.text}'



class Like(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name='people_like')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_like')
    
    def __str__(self) -> str:
        return self.people.username
