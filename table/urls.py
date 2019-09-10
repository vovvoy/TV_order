from django.urls import path
from .views import *

urlpatterns = [
    path('', SubPostListView.as_view(), name='post_list'),
    path('create/', addTodo, name='main'),
    path('complete/<todo_id>', completeTodo, name='complete'),
    path('deletecomplete', deleteCompleted, name='deletecomplete'),
    path('deleteall', deleteAll, name='deleteall'),
    path('changestatus/<todo_id>', changeStatus, name='change_status'),
    path('export/csv/$', export_users_csv, name='export_users_csv'),

]