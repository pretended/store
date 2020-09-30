from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('product/<str:id>/', views.product, name='product'),
]