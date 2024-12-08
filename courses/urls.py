from django.urls import path
from . import views
from .views_auth import register_view, login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
]
urlpatterns += [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
urlpatterns += [
    path('initiate-payment/<int:course_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]

