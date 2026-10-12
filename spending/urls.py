from django.urls import path
from spending.views import SignUpRegisterview,GetMeView,ExpenseListCreateView,ExpenseListRetrieveview
from spending.app_permissions import BasePermission,IsOwner
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns=[

    path('signup/',SignUpRegisterview.as_view()),
    path('Me/',GetMeView.as_view()),
    path("expense/",ExpenseListCreateView.as_view()),

    path("expense/<int:pk>/",ExpenseListRetrieveview.as_view()),

    path("token/",ObtainAuthToken.as_view()),

]