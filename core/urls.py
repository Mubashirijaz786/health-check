from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health_analysis/', views.health_analysis_hub, name='analysis_hub'),
    
    # Advanced AI Checkers
    path('checkers/fever/', views.fever_checker, name='fever_checker'),
    path('checkers/heart/', views.heart_risk_checker, name='heart_checker'),
    path('checkers/diabetes/', views.diabetes_risk_checker, name='diabetes_checker'),
    path('checkers/dengue/', views.dengue_risk_checker, name='dengue_checker'),
    path('checkers/stress/', views.stress_checker, name='stress_checker'),
    path('checkers/covid/', views.covid_risk_checker, name='covid_checker'),
    path('checkers/bmi/', views.bmi_checker, name='bmi_checker'),
    path('checkers/diet/', views.diet_planner, name='diet_planner'),
    path('checkers/bp/', views.bp_checker, name='bp_checker'),
    
    # Utilities & Management
    path('hospital_finder/', views.hospital_finder, name='hospital_finder'),
    path('add_person/', views.add_person, name='add_person'),
    path('delete_person/<uuid:person_id>/', views.delete_person, name='delete_person'),
    path('add_medicine/<uuid:person_id>/', views.add_medicine, name='add_medicine'),
    path('edit_medicine/<uuid:person_id>/<uuid:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/<uuid:person_id>/<uuid:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('api/hospitals/', views.find_hospitals_api, name='find_hospitals_api'),
    path('api/medicine_data/', views.get_medicine_data_api, name='get_medicine_data_api'),
]
