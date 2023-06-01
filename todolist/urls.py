from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import TaskList, CustomLoginView, RegisterPage, TaskCreate, TaskDeleteView, TaskDetail, TaskUpdate

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('add', views.TitleCreate.as_view(), name='add_view'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/', TaskDetail.as_view(), name="task"),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('calendar/', views.calendar, name='calendar'),
]