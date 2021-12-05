from django.urls import path
from ranker import views

app_name = 'ranker'

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('rankings', views.rankings, name='rankings'),
    path('about', views.about, name='about'),
    path('event_ranks/<str:sex>/<str:event>', views.event_ranks, name='event_ranks'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile'),
    path('entry/edit/<int:pk>', views.EntryUpdateView.as_view(), name='entry_edit'),
    path('entry/delete/<int:pk>', views.EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/create', views.EntryCreateView.as_view(), name='entry_create')
]
