import os
import joblib
import numpy as np
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict_ckd(request):
    if request.method == 'POST':
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            model = joblib.load(os.path.join(BASE_DIR, 'ckd_model.pkl'))
            
            data = json.loads(request.body)
            
            # Map and validate all input fields
            input_data = np.array([[
                float(data['age']),
                float(data['bp']),
                float(data['sg']),
                float(data['al']),
                float(data['su']),
                int(data['rbc']),
                int(data['pc']),
                int(data['pcc']),
                int(data['ba']),
                float(data['bgr']),
                float(data['bu']),
                float(data['sc']),
                float(data['sod']),
                float(data['pot']),
                float(data['hemo']),
                float(data['pcv']),
                float(data['wc']),
                float(data['rc']),
                int(data['htn']),
                int(data['dm']),
                int(data['cad']),
                int(data['appet']),
                int(data['pe']),
                int(data['ane']),
            ]])

            prediction = model.predict(input_data)[0]
            return JsonResponse({'prediction': 'CKD' if prediction == 1 else 'Not CKD'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'message': 'Send POST request with valid data'}, status=400)

def ckd_form(request):
    if request.method == "POST":
        try:
            # Map form data to expected format
            form_data = {
                'age': request.POST.get('age'),
                'bp': request.POST.get('bp'),
                'sg': request.POST.get('sg'),
                'al': request.POST.get('al'),
                'su': request.POST.get('su'),
                'rbc': request.POST.get('rbc'),
                'pc': request.POST.get('pc'),
                'pcc': request.POST.get('pcc'),
                'ba': request.POST.get('ba'),
                'bgr': request.POST.get('bgr'),
                'bu': request.POST.get('bu'),
                'sc': request.POST.get('sc'),
                'sod': request.POST.get('sod'),
                'pot': request.POST.get('pot'),
                'hemo': request.POST.get('hemo'),
                'pcv': request.POST.get('pcv'),
                'wc': request.POST.get('wc'),
                'rc': request.POST.get('rc'),
                'htn': request.POST.get('htn'),
                'dm': request.POST.get('dm'),
                'cad': request.POST.get('cad'),
                'appet': request.POST.get('appet'),
                'pe': request.POST.get('pe'),
                'ane': request.POST.get('ane'),
            }

            # Convert data types
            for key in ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'pe', 'ane']:
                form_data[key] = int(float(form_data[key]))

            response = requests.post(
                'http://localhost:8000/predict/',
                json=form_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json().get('prediction', 'Error in prediction')
                request.session['prediction_result'] = result
                request.session.modified = True
                return redirect('result')
            else:
                result = f"API Error: {response.status_code} - {response.text}"

        except ValueError as ve:
            result = f"Invalid input: {str(ve)}"
        except requests.RequestException as re:
            result = f"Connection error: {str(re)}"
        except Exception as e:
            result = f"Error: {str(e)}"

        return redirect('result')

    return render(request, 'predictor/form.html')


def result_ckd(request):
    # Get result from session
    result = request.session.get('prediction_result')
    error = request.session.get('prediction_error')
    
    # Clear session data after retrieval
    if 'prediction_result' in request.session:
        del request.session['prediction_result']
    if 'prediction_error' in request.session:
        del request.session['prediction_error']
    
    return render(request, 'predictor/result.html', {
        'result': result,
        'error': error
    })