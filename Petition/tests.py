# # from django.test import TestCase
# # from .models import Petition, CategoryPetition
# # from Aut.models import People, City




# # def get_petition_count_by_city():
# #     cities = City.objects.all()
# #     data = {}

# #     for i in cities:
# #         data[i.name] = Petition.objects.filter(author__city=i).count()

# #     return data

# data = {'Алматы': 36, 'Астана': 35, 'Караганды': 37, 'Атырау': 0}




# # Отображение графика
# # plt.show()

# # plt.bar(categories, amounts)
# # plt.title("График финансовых расходов!")
# user_id = 12
# temp_file_path = f"{user_id}_temp.png"
# plt.savefig(temp_file_path)

# with open(temp_file_path, "rb") as temp_file:
#     tuser.chart.save(f"{tuser.user_id}.png", temp_file)
    
# plt.close()
# os.remove(temp_file_path)
