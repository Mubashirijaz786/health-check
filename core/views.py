from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Person, Medicine
import requests
from django.contrib import messages
import json
import datetime

# --- DASHBOARD & ANALYTICS ---

def index(request):
    persons = Person.objects.prefetch_related('medicines').all()
    # Analytics Summary
    return render(request, 'medicine_reminder.html', {'persons': persons})

def health_analysis_hub(request):
    return render(request, 'analysis_hub.html')

def medicine_reminder_view(request):
    persons = Person.objects.prefetch_related('medicines').all()
    return render(request, 'medicine_reminder.html', {'persons': persons})

# --- HEALTH CHECKERS SUITE ---

def fever_checker(request):
    result, risk = None, "Low"
    if request.method == 'POST':
        temp = float(request.POST.get('temperature', 98.6))
        symptoms = request.POST.getlist('symptoms')
        score = 0
        if temp >= 102: score += 50
        elif temp >= 100: score += 30
        score += len(symptoms) * 10
        
        if score >= 60: risk, result = "High", "Significant fever detected. Immediate medical consultation required."
        elif score >= 30: risk, result = "Medium", "Moderate fever. Monitor vitals and rest."
        else: risk, result = "Low", "Health metrics within normal bounds."
    return render(request, 'checkers/fever.html', {'result': result, 'risk': risk})

def heart_risk_checker(request):
    result, risk, score = None, "Low", 0
    if request.method == 'POST':
        age = int(request.POST.get('age', 0))
        weight = float(request.POST.get('weight', 0))
        bp_sys = int(request.POST.get('systolic', 120))
        smoking = request.POST.get('smoking') == 'yes'
        diabetes = request.POST.get('diabetes') == 'yes'
        chest_pain = request.POST.get('chest_pain') == 'yes'
        
        if age > 50: score += 15
        if bp_sys > 140: score += 20
        if smoking: score += 25
        if diabetes: score += 15
        if chest_pain: score += 25
        
        if score >= 60: risk, result = "High", "Critical cardiovascular risk detected. Please schedule a cardiac screening."
        elif score >= 30: risk, result = "Medium", "Moderate risk. Focus on diet and exercise."
        else: risk, result = "Low", "Your cardiovascular indicators appear stable."
    return render(request, 'checkers/heart.html', {'result': result, 'risk': risk, 'score': score})

def diabetes_risk_checker(request):
    result, risk, score = None, "Low", 0
    if request.method == 'POST':
        sugar = float(request.POST.get('sugar', 100))
        age = int(request.POST.get('age', 0))
        family_h = request.POST.get('family_history') == 'yes'
        thirst = request.POST.get('thirst') == 'yes'
        fatigue = request.POST.get('fatigue') == 'yes'
        
        if sugar > 126: score += 40
        if family_h: score += 20
        if thirst: score += 15
        if fatigue: score += 10
        if age > 45: score += 15
        
        if score >= 50: risk, result = "High", "Probable diabetic condition. Fasting glucose test recommended."
        elif score >= 25: risk, result = "Medium", "Pre-diabetic indicators detected. Reduce sugar intake."
        else: risk, result = "Low", "Glycemic levels appear healthy."
    return render(request, 'checkers/diabetes.html', {'result': result, 'risk': risk, 'score': score})

def dengue_risk_checker(request):
    result, risk, severity = None, "Low", 0
    if request.method == 'POST':
        fever = request.POST.get('fever') == 'yes'
        body_pain = request.POST.get('body_pain') == 'yes'
        rash = request.POST.get('rash') == 'yes'
        platelets = int(request.POST.get('platelets', 250000))
        vomiting = request.POST.get('vomiting') == 'yes'
        
        if fever and body_pain: severity += 30
        if rash: severity += 20
        if platelets < 100000: severity += 40
        if vomiting: severity += 10
        
        if severity >= 60: risk, result = "Severe", "Emergency: High probability of Dengue Hemorrhagic Fever. Hospitalize immediately."
        elif severity >= 30: risk, result = "Moderate", "Possible Dengue. Complete blood count (CBC) recommended."
        else: risk, result = "Mild", "Symptoms do not match typical Dengue patterns."
    return render(request, 'checkers/dengue.html', {'result': result, 'risk': risk, 'score': severity})

def stress_checker(request):
    result, score = None, 0
    if request.method == 'POST':
        sleep = int(request.POST.get('sleep', 8))
        anxiety = int(request.POST.get('anxiety', 1)) # 1-10
        workload = int(request.POST.get('workload', 1)) # 1-10
        
        score = (anxiety * 5) + (workload * 4) + (8 - sleep) * 2
        score = min(100, max(0, score))
        
        if score >= 70: result = "High Stress: Practice deep breathing and consider professional counseling."
        elif score >= 40: result = "Moderate Stress: Take regular breaks and prioritize sleep."
        else: result = "Optimal Wellness: Your mental health indicators are excellent."
    return render(request, 'checkers/stress.html', {'result': result, 'score': score})

def covid_risk_checker(request):
    result, risk, oxygen = None, "Low", 98
    if request.method == 'POST':
        cough = request.POST.get('cough') == 'yes'
        fever = request.POST.get('fever') == 'yes'
        oxygen = int(request.POST.get('oxygen', 98))
        smell_loss = request.POST.get('smell_loss') == 'yes'
        
        score = 0
        if cough: score += 20
        if fever: score += 20
        if smell_loss: score += 30
        if oxygen < 94: score += 40
        
        if score >= 50 or oxygen < 92: risk, result = "High", "Critical respiratory risk. Seek immediate oxygen support and PCR test."
        elif score >= 20: risk, result = "Medium", "Possible viral infection. Isolate and monitor oxygen levels."
        else: risk, result = "Low", "Symptoms not suggestive of COVID-19."
    return render(request, 'checkers/covid.html', {'result': result, 'risk': risk, 'oxygen': oxygen})

def bmi_checker(request):
    result, category, bmi = None, "Healthy", 0
    if request.method == 'POST':
        w = float(request.POST.get('weight', 0))
        feet = float(request.POST.get('feet', 0))
        inches = float(request.POST.get('inches', 0))
        h_cm = (feet * 30.48) + (inches * 2.54)
        h_m = h_cm / 100
        if h_m > 0:
            bmi = round(w / (h_m*h_m), 1)
            if bmi < 18.5: category, result = "Underweight", "Increase nutritional intake and focus on protein-rich meals."
            elif bmi < 25: category, result = "Healthy", "Your body mass index is in the ideal clinical range."
            elif bmi < 30: category, result = "Overweight", "Regular cardiovascular exercise and caloric monitoring recommended."
            else: category, result = "Obese", "Clinical weight management plan required to mitigate health risks."
    return render(request, 'checkers/bmi.html', {'result': result, 'risk': category, 'score': min(100, int(bmi*2))})

def diet_planner(request):
    plan, calories = None, 0
    if request.method == 'POST':
        w = float(request.POST.get('weight', 0))
        feet = float(request.POST.get('feet', 0))
        inches = float(request.POST.get('inches', 0))
        h_cm = (feet * 30.48) + (inches * 2.54)
        age = int(request.POST.get('age', 25))
        goal = request.POST.get('goal', 'maintain')
        
        # Harris-Benedict Equation
        bmr = (10 * w) + (6.25 * h_cm) - (5 * age) + 5
        calories = int(bmr * 1.4)
        
        if goal == 'loss':
            calories -= 500
            plan = {
                'title': 'Weight Reduction Protocol',
                'meals': [
                    {'t': 'Breakfast', 'm': 'Oatmeal with berries and nuts (400 kcal)'},
                    {'t': 'Lunch', 'm': 'Grilled chicken salad with olive oil (500 kcal)'},
                    {'t': 'Snack', 'm': 'Greek yogurt or green apple (150 kcal)'},
                    {'t': 'Dinner', 'm': 'Baked fish with steamed broccoli (450 kcal)'}
                ]
            }
        elif goal == 'gain':
            calories += 500
            plan = {
                'title': 'Muscle Mass Enhancement',
                'meals': [
                    {'t': 'Breakfast', 'm': '4 Scrambled eggs + 2 slices whole grain toast (650 kcal)'},
                    {'t': 'Lunch', 'm': 'Beef pasta with rich tomato sauce (800 kcal)'},
                    {'t': 'Snack', 'm': 'Peanut butter smoothie with protein powder (400 kcal)'},
                    {'t': 'Dinner', 'm': 'Steak with large sweet potato and avocado (750 kcal)'}
                ]
            }
        else:
            plan = {
                'title': 'Equilibrium Maintenance',
                'meals': [
                    {'t': 'Breakfast', 'm': 'Boiled eggs and avocado toast (500 kcal)'},
                    {'t': 'Lunch', 'm': 'Turkey sandwich with soup (600 kcal)'},
                    {'t': 'Snack', 'm': 'Handful of almonds and fruit (200 kcal)'},
                    {'t': 'Dinner', 'm': 'Grilled salmon with quinoa (700 kcal)'}
                ]
            }
            
    return render(request, 'checkers/diet_planner.html', {'plan': plan, 'calories': calories})

def bp_checker(request):
    result, status = None, "Normal"
    if request.method == 'POST':
        sys = int(request.POST.get('systolic', 120))
        dia = int(request.POST.get('diastolic', 80))
        if sys >= 180 or dia >= 120: status, result = "Crisis", "HYPERTENSIVE CRISIS. Immediate emergency care required."
        elif sys >= 140 or dia >= 90: status, result = "High", "Hypertension detected. Consult a physician."
        elif sys >= 120: status, result = "Elevated", "Monitor diet and reduce sodium intake."
        else: result = "Healthy blood pressure levels."
    return render(request, 'checkers/bp.html', {'result': result, 'status': status})

def get_medicine_data_api(request):
    persons = Person.objects.prefetch_related('medicines').all()
    data = []
    for p in persons:
        data.append({
            'name': p.name,
            'medicines': [{
                'name': m.name,
                'dosage': m.dosage,
                'times': m.times
            } for m in p.medicines.all()]
        })
    return JsonResponse({'persons': data})

# --- EXISTING MANAGEMENT VIEWS ---

def hospital_finder(request):
    return render(request, 'hospital_finder.html')

def find_hospitals_api(request):
    location = request.GET.get('location', '')
    if not location: return JsonResponse({'error': 'Location required'}, status=400)
    try:
        headers = {'User-Agent': 'AuraHealthAI/5.0'}
        search_url = f"https://nominatim.openstreetmap.org/search?q=hospitals+in+{location}&format=json&addressdetails=1&limit=20"
        res = requests.get(search_url, headers=headers, timeout=12).json()
        hospitals = []
        for i in res:
            if i.get('type') in ['hospital', 'clinic', 'doctors']:
                hospitals.append({
                    'name': i.get('display_name', '').split(',')[0],
                    'address': i.get('display_name', '').split(',')[1:3],
                    'lat': i.get('lat'), 'lon': i.get('lon')
                })
        return JsonResponse({'hospitals': hospitals})
    except: return JsonResponse({'error': 'Service busy'}, status=503)

def add_person(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        p = Person.objects.create(name=data.get('person_name'))
        for m in data.get('medicines', []):
            Medicine.objects.create(person=p, name=m['name'], dosage=m['dosage'], total_days=m['total_days'], times=m['times'])
        return JsonResponse({'success': True})
    return render(request, 'add_person.html')

def delete_person(request, person_id):
    Person.objects.filter(id=person_id).delete()
    return redirect('index')

def add_medicine(request, person_id):
    p = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        times = [v for k,v in request.POST.items() if k.startswith('time_')]
        Medicine.objects.create(person=p, name=request.POST.get('name'), dosage=request.POST.get('dosage'), total_days=request.POST.get('total_days'), times=times)
        return redirect('index')
    return render(request, 'add_medicine_to_person.html', {'person': p})

def edit_medicine(request, person_id, medicine_id):
    m = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        m.name, m.dosage, m.total_days = request.POST.get('name'), request.POST.get('dosage'), request.POST.get('total_days')
        m.times = [v for k,v in request.POST.items() if k.startswith('time_')]
        m.save()
        return redirect('index')
    return render(request, 'edit_medicine.html', {'medicine': m, 'person': m.person})

def delete_medicine(request, person_id, medicine_id):
    Medicine.objects.filter(id=medicine_id).delete()
    return redirect('index')
