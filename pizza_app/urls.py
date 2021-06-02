from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('pizza', views.pizza),
    path('pizza/create', views.create),
    path('pizza/add', views.add),
    path('pizza/order/<int:id>', views.order),
    path('pizza/favorite', views.createFavorite),
    path('pizza/random', views.random),
    path('account/<int:id>', views.account),
    path('account/<int:id>/update', views.update),
    path('account/<int:id>/favorite', views.favorite),
    path('account/<int:id>/remove', views.remove)
    
]