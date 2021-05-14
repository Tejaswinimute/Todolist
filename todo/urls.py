from django.urls import path
from . import views

urlpatterns = [
    #Auth
    path('singupuser/',views.singupuser, name='signupuser'),
    path('logout/',views.logoutuser, name='logoutuser'),
    path('login/',views.loginuser, name='loginuser'),

    #Todos
    path('create/', views.createtodos, name='createtodos'),
    path('', views.home, name='home'),
    path('currenttodos', views.currenttodos, name='currenttodos'),
    path('completed', views.completedtodos, name='completedtodos'),
    path('todo/<int:todo_pk>', views.viewtodos, name='viewtodos'),
    path('todo/<int:todo_pk>/complete', views.completetodos, name='completetodos'),
    path('todo/<int:todo_pk>/delete', views.deletetodos, name='deletetodos'),

]
