from django.urls import path
from . import views

urlpatterns = [
    # We will add our Auth, Dashboard, and CRUD routes here next
    path('register/', view=views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-transaction/', view=views.add_transaction, name='add_transaction'),
]