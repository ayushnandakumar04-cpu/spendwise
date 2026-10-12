from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.shortcuts import get_object_or_404
from spending.serializers import UserSerializers,ExpenseSerializers
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from spending.models import Expense
from spending.app_permissions import IsOwner

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
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user

        qs=User.objects.get(username=auth_user)

        serializer_instance=UserSerializers(qs)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        qs=Expense.objects.filter(owner=request.user)
        serializer_instants=ExpenseSerializers(qs,many=True)
        return Response(data=serializer_instants.data)
    
    def post(self,request):
        form_data=request.data
        serializer_instance=ExpenseSerializers(data=form_data)
        if serializer_instance.is_valid() :
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class ExpenseListRetrieveview(APIView):
     authentication_classes=[authentication.TokenAuthentication]
     permission_classes=[IsOwner]

     def get(self,request,pk=None):
        qs=get_object_or_404(Expense,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance=ExpenseSerializers(qs)
        return Response(data=serializer_instance.data)
     
     def put(self,request,pk=None):
         instance=get_object_or_404(Expense,id=pk)
         self.check_object_permissions(request,instance)
         form_data=request.data
         serializer_instance=ExpenseSerializers(data=form_data,instance=instance)
         if serializer_instance.is_valid(): 
             serializer_instance.save()
             return Response(serializer_instance.data)
         else:
            return Response(serializer_instance.errors)
          

     def delete(self,request,pk=None):
         instance=get_object_or_404(Expense,id=pk)
         self.check_object_permissions(request,instance)
         instance.delete()
         return Response({"message": "Expense deleted successfully"})


     