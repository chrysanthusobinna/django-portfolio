from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('edit/<str:username>/', views.edit_user_profile, name='edit_user_portfolio'),

    path('portfolio/add/', views.add_portfolio, name='add_portfolio'),
    path('portfolio/edit/<int:id>/', views.edit_portfolio, name='edit_portfolio'),
    path('portfolio/delete/<int:id>/', views.delete_portfolio, name='delete_portfolio'),

    path('certification/add/', views.add_certification, name='add_certification'),
    path('certification/edit/<int:id>/', views.edit_certification, name='edit_certification'),
    path('certification/delete/<int:id>/', views.delete_certification, name='delete_certification'),

    path('education/add/', views.add_education, name='add_education'),
    path('education/edit/<int:id>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:id>/', views.delete_education, name='delete_education'),

    path('employment/add/', views.add_employment, name='add_employment'),
    path('employment/edit/<int:id>/', views.edit_employment, name='edit_employment'),
    path('employment/delete/<int:id>/', views.delete_employment, name='delete_employment'),

    path('about/save/', views.save_about, name='save_about'),
    path('about/delete/', views.delete_about, name='delete_about'),
]
