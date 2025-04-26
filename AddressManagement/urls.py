from django.urls import path
from .views import AddressCreateView, AddressRiskView

urlpatterns = [
    path('api/addresses/', AddressCreateView.as_view()),
    path('api/addresses/<int:id>/risks/', AddressRiskView.as_view()),
]