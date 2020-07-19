from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django import forms
from .forms import UserEntryForm, UserRegistrationForm, BranchesForm
from .models import Administrators, Accountants
import json

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form'] = UserEntryForm()
        return render(request, 'accountantLogin.html', context)
    def post(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form'] = UserEntryForm()
        return render(request, 'accountantLogin.html', context)

class AdminLoginPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        context['form'] = UserEntryForm()
        return render(request, 'adminLogin.html', context)
    def post(self, request, **kwargs):
        context = {}
        context['form'] = UserEntryForm()
        return render(request, 'adminLogin.html', context)
    #template_name = 'adminLogin.html'

class AccountantCreationPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form'] = UserRegistrationForm()
        return render(request, 'createAccountant.html', context)
    def post(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form'] = UserRegistrationForm()
        return render(request, 'createAccountant.html', context)
    #template_name = 'createAccountant.html'  

"""
class AdminHomePageView(TemplateView):
    def get(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form_ip'] = InputTextForm()
        return render(request, 'adminHome.html', context)
    def post(self, request, **kwargs):
        context = {}
        context['form_br'] = BranchesForm()
        context['form_ip'] = InputTextForm()
        return render(request, 'adminHome.html', context)
"""

@csrf_exempt
def adminAuth(request):
    form = UserEntryForm(request.POST)
    if form.is_valid():
        adminData = form.cleaned_data
        adminName = adminData['userName']
        adminPwd = adminData['passWord']
        #ad = Administrators()
        if not (Administrators.objects.filter(adminName = adminName).exists()):
            raise forms.ValidationError("Admin doesn't exists")
            #return render(request, 'adminLogin.html', {"Error" : "Admin doesn't exists"})
        else:
            verifyAdmin = Administrators.objects.get(adminName = adminName)
            if adminName == verifyAdmin.adminName and adminPwd == verifyAdmin.adminPwd:
                return redirect('/adminHome/')
            else:
                raise forms.ValidationError("Incorrect Username/Password")
            """
            verifyAdmin = authenticate(username = adminName, password = adminPwd)
            if verifyAdmin is not None:
                #return render(request, 'adminHome.html', context=None)
                return redirect('/adminHome/')
            else:
                raise forms.ValidationError("Incorrect Username/Password")
                #return render(request, 'adminLogin.html', {"Error" : "Incorrect Username/Password"})
            """
    else:
        return redirect('/adminLogin/')

@csrf_exempt
def accountantAuth(request):
    form = UserEntryForm(request.POST)
    if form.is_valid():
        userData = form.cleaned_data
        userName = userData['userName']
        userPwd = userData['passWord']
        userBranch = request.POST['branch']
        print(userBranch)
        if not (Accountants.objects.filter(userName = userName).exists()):
            raise forms.ValidationError("Accountant doesn't exists")
            #return render(request, 'adminLogin.html', {"Error" : "Admin doesn't exists"})
        else:
            verifyUser = Accountants.objects.get(userName = userName)
            if userName == verifyUser.userName and userPwd == verifyUser.userPwd and userBranch == verifyUser.branch:
                return redirect('/accountantHome/')
            else:
                raise forms.ValidationError("Incorrect Username/Password")
            """
            verifyUser = authenticate(username = userName, password = userPwd)
            if verifyUser is not None:
                #return render(request, 'adminHome.html', context=None)
                return redirect('/userHome/')
            else:
                raise forms.ValidationError("Incorrect Username/Password")
                #return render(request, 'adminLogin.html', {"Error" : "Incorrect Username/Password"})
            """
    else:
        return redirect('/')

@csrf_exempt
def createAccountant(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        userData = form.cleaned_data
        Accountants.objects.create(
            userName = userData['userName'],
            userPwd = userData['passWord'],
            dateOfJoining = userData['DOJ'],
            dateOfBirth = userData['DOB'],
            salary = userData['salary'],
            branch = request.POST['branch']
        )
        return redirect('/adminHome/')   
    else:
        return redirect('/accountantCreation/')

@csrf_exempt
def route2adminHome(request):
    context = {}
    context['form_br'] = BranchesForm()
    return render(request, 'adminHome.html', context)

@csrf_exempt
def route2accountantHome(request):
    context = {}
    context['form_br'] = BranchesForm()
    return render(request, 'accountantHome.html', context)

@csrf_exempt
def adminGetDetails(request):
    branch = request.POST['branchName']
    name = request.POST['nameEntered']
    if not (Accountants.objects.filter(userName__startswith = name).exists()):
        raise forms.ValidationError("No Accountant exists")
    else:
        ac = list(Accountants.objects.filter(userName__startswith = name))
        people_list, people = [], {}
        for i in ac:
            i = str(i).split('-')
            if branch == i[3]:
                people['Id'] = i[0]
                people['Username'] = i[1]
                people['Salary'] = i[2]
                people_list.append(people)
        return HttpResponse(json.dumps(people_list))
        #return redirect('/adminHome/', people_list)
        """context = {}
        context['form_br'] = BranchesForm()
        context['data'] = people_list
        print(context)
        return render(request, 'adminHome.html', context)"""