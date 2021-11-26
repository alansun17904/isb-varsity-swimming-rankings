from django.urls import path
from ranker import views

app_name = 'ranker'

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('rankings', views.rankings, name='rankings'),
    path('about', views.about, name='about'),
    path('event_ranks/<str:sex>/<str:event>',
        views.event_ranks, name='event_ranks')
]
