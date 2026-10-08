from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from spending.serializers import UserSerializers
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response


class SignUpRegisterview(APIView):

    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializers(data=form_data)

        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            user_object=User.objects.create_user(**cleaned_data)
            serializer_instance=UserSerializers(user_object)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class GetMeView(APIView):
    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user

        qs=User.objects.get(username=auth_user)

        serializer_instance=UserSerializers(qs)

        return Response(data=serializer_instance.data)
    