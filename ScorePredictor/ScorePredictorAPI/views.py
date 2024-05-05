from django.shortcuts import render
from django.http import JsonResponse
from joblib import load
import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'ScorePredictorAPI', 'model.joblib')


def predict_score(request):
    if request.method == 'POST':
        # Get input values from the form
        study_hours = float(request.POST.get('study_hours'))
        previous_score = float(request.POST.get('previous_score'))

        # Load the machine learning model
        model = load(model_path)

        # Make predictions
        user_data = pd.DataFrame([[study_hours, previous_score]], columns=[
                                 'Study Hours', 'Previous Exam Score'])
        predicted_score = model.predict(user_data)

        predicted_score = int(predicted_score)

        if predicted_score == 1:
            return JsonResponse({'predicted_result': "Congratualtions, you are going to Pass the Exam!"})
        else:
            print(predicted_score)
            return JsonResponse({'predicted_result': "Sorry, you are going to Fail the Exam!"})

    else:
        return render(request, 'predict.html')
