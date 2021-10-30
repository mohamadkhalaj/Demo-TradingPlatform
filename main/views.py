from django.shortcuts import render
from django.http import HttpResponse
from .models import UsrRegistration,TradeHistory,Portfolio


def write_to_db():
    print("writing to database...")
    # registration = UsrRegistration(firstName='Steve', lastName='Harris', nationalId=1111111112,
    #                                address='Blub Blub Blub Blub', phoneNumber=46088194, mobileNumber=9305898647,
    #                                email='sample@gmail.com', password='123456789abc')
    # registration.save()

    # history = TradeHistory(type='b',cryptoName='Ethereum', price='4000',amount='0.09',equivalentAmount='500')
    # history.save()

    # portfolio = Portfolio(cryptoName='Ethereum', price='4000',amount='0.09',equivalentAmount='500')
    # portfolio.save()

    

def read_UsrRegistration(pk):
    print("___________________ UsrRegistration _____________________")
    obj = UsrRegistration.objects.get(nationalId=pk)
    print(UsrRegistration.objects.all())
    print(obj.firstName)
    print(obj.lastName)
    print(obj.nationalId)
    print(obj.address)
    print(obj.phoneNumber)
    print(obj.mobileNumber)
    print(obj.email)
    print(obj.password)
    print(obj.mainBalance)


def read_TradeHistory(pk):
    print("___________________ TradeHistory _____________________")
    print(TradeHistory.objects.all())
    obj = TradeHistory.objects.get(id=pk)
    print(obj.id)
    print(obj.type)
    print(obj.cryptoName)
    print(obj.price)
    print(obj.date)
    print(obj.amount)
    print(obj.equivalentAmount)


def read_Portfolio(pk):
    print("___________________ Portfolio _____________________")
    print(Portfolio.objects.all())
    obj = Portfolio.objects.get(id=pk)
    print(obj.id)
    print(obj.cryptoName)
    print(obj.price)
    print(obj.date)
    print(obj.amount)
    print(obj.equivalentAmount)

def delete_db_columns():
    print("deleting columns...")
    UsrRegistration.objects.all().delete()
    TradeHistory.objects.all().delete()
    Portfolio.objects.all().delete()

# ______________________________________________________________________________


def home(request):
    # write_to_db()
    # read_UsrRegistration(1111111112)
    # read_TradeHistory(2)
    # read_Portfolio(1)
    # delete_db_columns()

    return HttpResponse("Hi")