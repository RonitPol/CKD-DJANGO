import os
import joblib
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def predict_ckd(request):
    if request.method == 'POST':
        try:
            # Load model inside the function
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(BASE_DIR, 'ckd_model.pkl')
            
            if not os.path.exists(model_path):
                return JsonResponse({'error': 'Model file not found at expected location.'}, status=500)

            model = joblib.load(model_path)

            # Parse input data
            data = json.loads(request.body)

            input_data = np.array([[
                data['age'], data['bp'], data['sg'], data['al'], data['su'],
                data['rbc'], data['pc'], data['pcc'], data['ba'], data['bgr'],
                data['bu'], data['sc'], data['sod'], data['pot'], data['hemo'],
                data['pcv'], data['wc'], data['rc'], data['htn'], data['dm'],
                data['cad'], data['appet'], data['pe'], data['ane'],
            ]])

            prediction = model.predict(input_data)[0]
            result = 'CKD' if prediction == 1 else 'Not CKD'
            return JsonResponse({'prediction': result})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Send a POST request with input data.'})



from django.shortcuts import render

def ckd_form(request):
    fields = ["age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba", "bgr", 
              "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc", "htn", "dm", 
              "cad", "appet", "pe", "ane"]

    result = None

    if request.method == "POST":
        try:
            data = {field: float(request.POST[field]) for field in fields}
            import requests
            import json

            response = requests.post(
                'http://127.0.0.1:8000/predict/',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            result = response.json().get('prediction', 'Error in prediction.')

        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'predictor/form.html', {'fields': fields, 'result': result})
