# coding=utf-8
from django.urls import path

from .views import (
    SampleFormView,
    SampleModelFormView,
    SuccessView,
)


urlpatterns = [
    path('sample_form/', SampleFormView.as_view(), name='sample_form'),
    path('model_form/', SampleModelFormView.as_view(), name='model_form'),
    path('success/', SuccessView.as_view(), name='success'),
]
