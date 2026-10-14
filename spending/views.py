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
from datetime import datetime
from django.db.models import Sum
from spending.ai_service import get_budget_plan
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

class ExpenseSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        response_data={
            "total_today":0
        }
        cur_date=datetime.now().date()
        cur_month=datetime.now().month
        cur_year=datetime.now().year

        monthly_transactions=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        if monthly_transactions:
            monthly_total=monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")
            response_data["monthly_total"]=monthly_total
        todays_transaction=Expense.objects.filter(owner=request.user,created_at__date=cur_date)
        if todays_transaction:
            total_today=todays_transaction.values("amount").aggregate(total=Sum("amount")).get("total")
            #todays category
            category=todays_transaction.values("category").annotate(total=Sum("amount"))

            #response_data={"total_today":total_today}
            #response_data={"total_category":category}
            #monthly

        return Response(data=response_data)


class BudgetPlanView(APIView):
       authentication_classes=[authentication.TokenAuthentication]
       permission_classes=[permissions.IsAuthenticated]

       def get (self,request):
           user=request.user
           #monthly total
        
           curr_month=datetime.now().month
           curr_year=datetime.now().year

           response_data={"monthly_Expense_total":0}
           monthly_transations=Expense.objects.filter(owner=request.user,created_at__month=curr_month,created_at__year=curr_year)
           if monthly_transations:
               monthly_total=monthly_transations.values("amount").aggregate(monthly_total=Sum("amount")).get("total")
               response_data["monthly_total"]=monthly_total
               category_summary=monthly_transations.values("category").annotate(total=Sum("amount"))
               response_data["category_summary"]=category_summary
               get_budget_plan(response_data)
           return Response(response_data)