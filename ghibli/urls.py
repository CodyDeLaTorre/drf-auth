from django.urls import path
from .views import GhibliList, GhibliDetail

urlpatterns = [
  path('', GhibliList.as_view(), name='ghibli_list'),
  path('<int:pk>/', GhibliDetail.as_view(), name='ghibli_detail'),
]
