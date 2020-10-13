from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('boards/<int:id>/',views.board_topic,name='board_topic'),
    path('boards/<int:id>/new/',views.new_topic,name='new_topic'),

]
