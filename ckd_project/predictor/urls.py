from django.urls import path
from .views import predict_ckd, ckd_form

urlpatterns = [
    path('predict/', predict_ckd, name='predict_ckd'),
    path('', ckd_form, name='ckd_form'),  # <- default home route
]
