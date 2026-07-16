from django.urls import path
from . import views

urlpatterns = [
    path('', views.preset_list, name='preset_list'),
    path('api/presets/', views.presets_json, name='presets_json'),
    path('presets/new/', views.preset_create, name='preset_create'),
    path('presets/<int:pk>/', views.preset_detail, name='preset_detail'),
    path('presets/<int:pk>/edit/', views.preset_edit, name='preset_edit'),
    path('presets/<int:pk>/delete/', views.preset_delete, name='preset_delete'),
    path('presets/<int:pk>/download/', views.preset_download, name='preset_download'),
    path('register/', views.register, name='register'),
]
