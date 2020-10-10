from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('boards/<int:board_id>/',views.board_topic,name='board_topic'),
]
