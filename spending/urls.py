from django.urls import path
from spending.views import SignUpRegisterview,GetMeView
urlpatterns=[

    path('signup/',SignUpRegisterview.as_view()),
    path('Me/',GetMeView.as_view())
]