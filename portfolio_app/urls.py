from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/', views.templates_page, name='templates_page'),
    path('template-preview/<str:template_name>/', views.template_preview, name='template_preview'),
    path('template-preview-raw/<str:template_name>/', views.template_preview_raw, name='template_preview_raw'),
    path('select-template/<int:template_id>/', views.select_template, name='select_template'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('edit/<str:username>/', views.edit_user_profile, name='edit_user_profile'),

    path('portfolio/add/', views.add_portfolio, name='add_portfolio'),
    path('portfolio/edit/<int:id>/', views.edit_portfolio, name='edit_portfolio'),
    path('portfolio/delete/<int:id>/', views.delete_portfolio, name='delete_portfolio'),
    path('portfolio/delete-all/', views.delete_all_portfolio, name='delete_all_portfolio'),

    path('certification/add/', views.add_certification, name='add_certification'),
    path('certification/edit/<int:id>/', views.edit_certification, name='edit_certification'),
    path('certification/delete/<int:id>/', views.delete_certification, name='delete_certification'),
    path('certification/delete-all/', views.delete_all_certifications, name='delete_all_certifications'),

    path('education/add/', views.add_education, name='add_education'),
    path('education/edit/<int:id>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:id>/', views.delete_education, name='delete_education'),
    path('education/delete-all/', views.delete_all_education, name='delete_all_education'),

    path('employment/add/', views.add_employment, name='add_employment'),
    path('employment/edit/<int:id>/', views.edit_employment, name='edit_employment'),
    path('employment/delete/<int:id>/', views.delete_employment, name='delete_employment'),
    path('employment/delete-all/', views.delete_all_employment, name='delete_all_employment'),

    path('about/save/', views.save_about, name='save_about'),
    path('about/delete/', views.delete_about, name='delete_about'),

    path('skills/save/', views.save_skills, name='save_skills'),
    path('skills/delete/', views.delete_skills, name='delete_skills'),

    path('contact-method/add/', views.add_contact_method, name='add_contact_method'),
    path('contact-method/edit/<int:id>/', views.edit_contact_method, name='edit_contact_method'),
    path('contact-method/delete/<int:id>/', views.delete_contact_method, name='delete_contact_method'),
    path('contact-method/delete-all/', views.delete_all_contact_methods, name='delete_all_contact_methods'),

    path('profile/save-photo/', views.save_profile_photo, name='save_profile_photo'),
    path('profile/delete-photo/', views.delete_profile_photo, name='delete_profile_photo'),

    path('account/settings/', views.account_settings, name='account_settings'),
]
