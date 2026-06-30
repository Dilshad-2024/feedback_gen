from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_form, name='create_form'),
    path('form/<int:form_id>/', views.fill_form, name='fill_form'),
    path('responses/', views.responses, name='responses'),
    path('my-forms/', views.my_forms, name='my_forms'),
    path('submitted/',views.feedback_submitted,name='feedback_submitted'),
    path('my-forms/',views.my_forms,name='my_forms'),
    path('created/<int:form_id>/',views.form_created,name='form_created'),
    path('edit-form/<int:form_id>/', views.edit_form, name='edit_form'),
    path('form-analytics/<int:form_id>/', views.form_analytics, name='form_analytics'),
    path('ai_analysis/<int:form_id>/', views.ai_analysis, name='ai_analysis'),
    path('comments/<int:form_id>/',views.view_comments,name='view_comments'),
    path("delete/<int:form_id>/",views.delete_form,name="delete_form")
]