from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'feed'
urlpatterns = [
    path('', views.index, name='index'), 
    # path('<int:article_id>/', views.detail, name='detail'),

    # TODO swap game and detail urls    
    # path('<int:game_id>/', views.game, name='game'),
    # path('<int:game_id>/vote/', views.throw, name='throw'),
    # path('game/<int:game_id>/', views.game, name='game'),
]