from django.db import models
from Aut.models import User, City
from Petition.models import Petition
from Petition.models import CategoryPetition


# Чиновник
class Chin(User):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_chin')
    category = models.ForeignKey(CategoryPetition, on_delete=models.CASCADE, related_name='category_chin')
    iin = models.CharField(max_length=12)
    
    class Meta:
        verbose_name = 'Чиновник'
        verbose_name_plural = 'Чиновник'

        
    def __str__(self):
        return self.username
    

# Ответ Чиновника
class PetitionAnswer(models.Model):
    chinov = models.ForeignKey(Chin, on_delete=models.CASCADE, related_name='chinov', blank=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='petition_answer', blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.chinov}, {self.text}'
    