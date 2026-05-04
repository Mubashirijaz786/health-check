from flask import render_template, request, redirect, url_for, flash, jsonify
from data_manager import load_data, save_data
import uuid
from datetime import datetime

def register_routes(app):

    @app.route('/')
    def index():
        data = load_data()
        return render_template('index.html', data=data)

    @app.route('/add_person', methods=['GET', 'POST'])
    def add_person():
        """Form to add a person and multiple medicines dynamically using JavaScript."""
        if request.method == 'POST':
            req_data = request.json
            person_name = req_data.get('person_name')
            meds_input = req_data.get('medicines', [])
            
            data = load_data()
            new_person = {
                "id": str(uuid.uuid4()),
                "name": person_name,
                "medicines": []
            }
            
            for m in meds_input:
                new_person["medicines"].append({
                    "id": str(uuid.uuid4()),
                    "name": m.get("name"),
                    "dosage": m.get("dosage"),
                    "times": m.get("times", []),
                    "total_days": m.get("total_days", 1),
                    "start_date": datetime.now().strftime("%Y-%m-%d")
                })
                
            data["persons"].append(new_person)
            save_data(data)
            flash(f'Successfully added {person_name} and their medicines!', 'success')
            return jsonify({"success": True})
            
        return render_template('add_person.html')

    @app.route('/delete_person/<person_id>', methods=['POST'])
    def delete_person(person_id):
        data = load_data()
        data["persons"] = [p for p in data["persons"] if p.get("id") != person_id]
        save_data(data)
        flash('Person deleted.', 'success')
        return redirect(url_for('index'))

    @app.route('/add_medicine_to_person/<person_id>', methods=['GET', 'POST'])
    def add_medicine_to_person(person_id):
        """Add a new medicine to an existing person."""
        data = load_data()
        person = next((p for p in data["persons"] if p.get("id") == person_id), None)
        if not person:
            flash('Person not found.', 'error')
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            name = request.form.get('name')
            dosage = request.form.get('dosage')
            total_days = int(request.form.get('total_days', 1))
            
            # Gather dynamic times
            times = []
            for key in request.form:
                if key.startswith('time_'):
                    times.append(request.form.get(key))
                    
            person["medicines"].append({
                "id": str(uuid.uuid4()),
                "name": name,
                "dosage": dosage,
                "times": sorted(times),
                "total_days": total_days,
                "start_date": datetime.now().strftime("%Y-%m-%d")
            })
            save_data(data)
            flash('Medicine added!', 'success')
            return redirect(url_for('index'))
            
        return render_template('add_medicine_to_person.html', person=person)

    @app.route('/edit_medicine/<person_id>/<medicine_id>', methods=['GET', 'POST'])
    def edit_medicine(person_id, medicine_id):
        """Edit a specific medicine for a person."""
        data = load_data()
        person = next((p for p in data["persons"] if p.get("id") == person_id), None)
        if not person:
            return redirect(url_for('index'))
            
        medicine = next((m for m in person["medicines"] if m.get("id") == medicine_id), None)
        if not medicine:
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            medicine['name'] = request.form.get('name')
            medicine['dosage'] = request.form.get('dosage')
            medicine['total_days'] = int(request.form.get('total_days', 1))
            
            times = []
            for key in request.form:
                if key.startswith('time_'):
                    val = request.form.get(key)
                    if val:
                        times.append(val)
            medicine['times'] = sorted(times)
            
            save_data(data)
            flash('Medicine updated!', 'success')
            return redirect(url_for('index'))
            
        return render_template('edit_medicine.html', person=person, medicine=medicine)

    @app.route('/delete_medicine/<person_id>/<medicine_id>', methods=['POST'])
    def delete_medicine(person_id, medicine_id):
        data = load_data()
        person = next((p for p in data["persons"] if p.get("id") == person_id), None)
        if person:
            person["medicines"] = [m for m in person["medicines"] if m.get("id") != medicine_id]
            save_data(data)
            flash('Medicine deleted.', 'success')
        return redirect(url_for('index'))

    @app.route('/fever_checker', methods=['GET', 'POST'])
    def fever_checker():
        """Route for the Fever Risk Checker feature."""
        result = None
        risk_level = None
        
        if request.method == 'POST':
            try:
                temperature = float(request.form.get('temperature', 0))
                symptoms = request.form.getlist('symptoms')
                
                if temperature >= 39.0:
                    risk_level = "High"
                    result = "Your temperature is quite high. Please consult a doctor immediately."
                elif temperature >= 38.0:
                    if len(symptoms) >= 2:
                        risk_level = "High"
                        result = "You have a moderate fever with multiple symptoms. You should see a doctor."
                    else:
                        risk_level = "Medium"
                        result = "You have a moderate fever. Rest and monitor your symptoms."
                elif temperature >= 37.5:
                    risk_level = "Medium"
                    result = "You have a mild fever. Drink plenty of fluids."
                else:
                    if len(symptoms) >= 3:
                        risk_level = "Medium"
                        result = "Your temperature is normal, but you have multiple symptoms. Take care."
                    else:
                        risk_level = "Low"
                        result = "Your temperature is normal and you have few or no symptoms."
                        
            except ValueError:
                flash('Please enter a valid number for temperature.', 'error')
                
        return render_template('fever_checker.html', result=result, risk_level=risk_level)
