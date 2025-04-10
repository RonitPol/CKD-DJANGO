from django.urls import path
from .views import predict_ckd, ckd_form ,result_ckd

urlpatterns = [
    path('predict/', predict_ckd, name='predict_ckd'),
    path('result/',result_ckd, name='result'),
    path('', ckd_form, name='ckd_form'),  # <- default home route
]
