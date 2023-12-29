from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout_view,name="logout"),
    path('about/',views.about,name="about"),
    path('help/',views.help,name="help"),
    path('login/',views.login_view,name="login"),
    path('add_task/', views.add_task, name='add_task'),
    path('mark_completed/<int:task_id>/', views.mark_completed, name='mark_completed'),
    path('remark/<int:task_id>/', views.remark, name='remark'),
    path('delete/<int:task_id>/', views.remark, name='delete'),
    path("create/", views.create_entry, name="create_entry"),
    path("view_all/", views.view_all, name="view_all"),
]