from django.contrib.auth.models import User
from spending.models import Expense
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","email","password"]

        read_only_fields=["id"]

class ExpenseSerializers(serializers.ModelSerializer):

    class Meta:

        model=Expense

        fields="__all__"

        read_only_fields=["id","owner","created_at","updated_at"]


