from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('boards/<int:id>/',views.board_topic,name='board_topic'),
    path('boards/<int:id>/new/',views.new_topic,name='new_topic'),
    path('boards/<int:id>/topics/<int:topic_id>/',views.topics_posts,name='topics_posts'),
    path('boards/<int:id>/topics/<int:topic_id>/reply/',views.reply_topic,name='reply_topic'),
    path('boards/<int:id>/topics/<int:topic_id>/posts/<int:post_id>/edit',views.PostUpdateview.as_view(),name='edit_post'),



]
