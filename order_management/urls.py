from django.urls import path

from . import views

app_name = 'order_management'

urlpatterns = [
    path('new-order/', views.new_order, name='new_order')
]