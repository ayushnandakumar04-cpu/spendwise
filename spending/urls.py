from django.urls import path
from spending.views import SignUpRegisterview,GetMeView,ExpenseListCreateView,ExpenseListRetrieveview
urlpatterns=[

    path('signup/',SignUpRegisterview.as_view()),
    path('Me/',GetMeView.as_view()),
    path("expense/",ExpenseListCreateView.as_view()),

    path("expense/<int:pk>/",ExpenseListRetrieveview.as_view()),
]