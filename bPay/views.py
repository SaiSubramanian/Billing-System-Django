from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django import forms
from .forms import UserEntryForm, UserRegistrationForm, BranchesForm, InputTextForm, StudentEntryForm
from .models import Accountant, Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.core.mail import send_mail
import json, smtplib

def loginPageView(request):
    context = {}
    context['form_br'] = BranchesForm()
    context['form'] = UserEntryForm()
    return render(request, 'accountantLogin.html', context)

def adminLoginPageView(request):
    context = {}
    context['form'] = UserEntryForm()
    return render(request, 'adminLogin.html', context)

@login_required
def accountantCreationPageView(request):
    context = {}
    context['form_br'] = BranchesForm()
    context['form'] = UserRegistrationForm()
    return render(request, 'createAccountant.html', context)

"""
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

"""

@csrf_exempt
def adminAuth(request):
    form = UserEntryForm(request.POST)
    if form.is_valid():
        adminData = form.cleaned_data
        adminName = adminData['userName']
        adminPwd = adminData['passWord']
        if not(User.objects.filter(username=adminName, is_superuser=True).exists()):
            #raise forms.ValidationError("Admin doesn't exists")
            context = {}
            context['form'] = UserEntryForm()
            context['error'] = "Admin doesn't exists"
            return render(request, 'adminLogin.html', context)
        else:
            verifyAdmin = authenticate(username = adminName, password = adminPwd)
            if verifyAdmin is not None:
                login(request, verifyAdmin)
                return redirect('/adminHome/')
                #return render(request, 'adminHome.html', context=None)
            else:
                context = {}
                context['form'] = UserEntryForm()
                context['error'] = "Incorrect Password"
                return render(request, 'adminLogin.html', context)
                #raise forms.ValidationError("Incorrect Username/Password")
                #return render(request, 'adminLogin.html', {"Error" : "Incorrect Username/Password"})
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
        if not(User.objects.filter(username=userName, is_superuser=False).exists()) or not(Accountant.objects.filter(Username=userName, Branch=userBranch).exists()):
            #raise forms.ValidationError("User doesn't exists")
            context = {}
            context['form_br'] = BranchesForm()
            context['form'] = UserEntryForm()
            context['error'] = "Accountant doesn't exists"
            return render(request, 'accountantLogin.html', context)
        else:
            verifyUser = authenticate(username = userName, password = userPwd)
            if verifyUser is not None:
                login(request, verifyUser)
                return redirect('/accountantHome/')
            else:
                context = {}
                context['form_br'] = BranchesForm()
                context['form'] = UserEntryForm()
                context['error'] = "Incorrect Password"
                return render(request, 'accountantLogin.html', context)
                #raise forms.ValidationError("Incorrect Username/Password")            
    else:
        return redirect('/')

@login_required
def logOut(request):
    if User.objects.filter(username=request.user, is_superuser=True).exists():
        logout(request)
        return redirect('/adminLogin/')
    else:
        logout(request)
        return redirect('/')

@login_required
@csrf_exempt
def createAccountant(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        userData = form.cleaned_data
        if not(User.objects.filter(username=userData['userName'], is_superuser=False).exists()):
            Accountant.objects.create(
                Username = userData['userName'],
                Date_of_Joining = userData['DOJ'],
                DOB = userData['DOB'],
                Salary = userData['salary'],
                Branch = request.POST['branch']
            )
            User.objects.create_user(userData['userName'], '', userData['passWord'])
            return redirect('/adminHome/')   
        else:
            context = {}
            context['form_br'] = BranchesForm()
            context['form'] = UserRegistrationForm()
            context['error'] = 'Username already taken'
            return render(request, 'createAccountant.html', context)

    else:
        context = {}
        context['form_br'] = BranchesForm()
        context['form'] = UserRegistrationForm()
        context['error'] = 'Invalid Data entered'
        return render(request, 'createAccountant.html', context)        

@login_required
@csrf_exempt
def route2adminHome(request):
    context = {}
    context['form_br'] = BranchesForm()
    context['form_ip'] = InputTextForm()
    return render(request, 'adminHome.html', context)

@login_required
@csrf_exempt
def route2accountantHome(request):
    context = {}
    context['form_ip'] = InputTextForm()
    return render(request, 'accountantHome.html', context)

@csrf_exempt
def adminGetDetails(request):
    branch = request.POST['branch']
    name = request.POST['inputText']
    if not (Accountant.objects.filter(Username__startswith = name, Branch = branch).exists()):
        context = {}
        context['form_br'] = BranchesForm()
        context['form_ip'] = InputTextForm()
        context['error'] = 'No Accountant match found!'
        return render(request, 'adminHome.html', context)
        #raise forms.ValidationError("No Accountant exists")
    else:
        shortData_list = Accountant.objects.filter(Username__startswith = name, Branch = branch)
        """people_list = []
        for i in ac:
            people = {}
            i = str(i).split('-')
            print(i)
            if branch == i[3]:
                people['Id'] = i[0]
                people['Username'] = i[1]
                people['Salary'] = i[2]
                people_list.append(people)
        print(people_list)
        #return HttpResponse(json.dumps(people_list))
        return redirect('/adminHome/', data = people_list)
        """
        context = {}
        context['form_br'] = BranchesForm()
        context['form_ip'] = InputTextForm()
        context['shortData'] = shortData_list
        return render(request, 'adminHome.html', context) 

@csrf_exempt
def adminGetAllDetails(request):
    userIdVal = request.POST.get('userID')
    #acnt_details = get_object_or_404(Accountant, acnt_pk)
    completeData = (Accountant.objects.get(pk = userIdVal)).getDetails()
    return HttpResponse(json.dumps(completeData))

def deleteData(request):
    userIdVal = request.POST.get('userID')
    data = Accountant.objects.get(pk = userIdVal)
    data.delete()
    ud = User.objects.get(pk = userIdVal)
    ud.delete()
    return True

def accountantGetDetails(request):
    name = request.POST['inputText']
    if not (Student.objects.filter(Name__startswith = name).exists()):
        context = {}
        context['form_ip'] = InputTextForm()
        context['error'] = 'No Student Account match found!'
        return render(request, 'accountantHome.html', context)
        #raise forms.ValidationError("No Student Account exists")
    else:
        shortData_list = Student.objects.filter(Name__startswith = name)
        """people_list = []
        for i in ac:
            people = {}
            i = str(i).split('-')
            print(i)
            if branch == i[3]:
                people['Id'] = i[0]
                people['Username'] = i[1]
                people['Salary'] = i[2]
                people_list.append(people)
        print(people_list)
        #return HttpResponse(json.dumps(people_list))
        return redirect('/adminHome/', data = people_list)
        """
        context = {}
        context['form_ip'] = InputTextForm()
        context['shortData'] = shortData_list
        return render(request, 'accountantHome.html', context) 

def accountantGetFeeDetails(request):
    userIdVal = request.POST.get('userID')
    feeData = (Student.objects.get(pk = userIdVal)).getFeeDetails()
    return HttpResponse(json.dumps(feeData))

def accountantGetCourseDetails(request):
    userIdVal = request.POST.get('userID')
    courseData = (Student.objects.get(pk = userIdVal)).getCourseDetails()
    return HttpResponse(json.dumps(courseData))

def accountantGetGeneralDetails(request):
    userIdVal = request.POST.get('userID')
    generalData = (Student.objects.get(pk = userIdVal)).getGeneralDetails()
    return HttpResponse(json.dumps(generalData))

def acHome(request):
    if User.objects.filter(username=request.user, is_superuser=False).exists():
        return redirect('/accountantHome/')
    else:
        return redirect('/')

def adHome(request):
    if User.objects.filter(username=request.user, is_superuser=True).exists():
        return redirect('/adminHome/')
    else:
        return redirect('/adminLogin/')

@login_required
def accessRegisterStudentPage(request):
    if User.objects.filter(username=request.user, is_superuser=False).exists():
        return redirect('/registerStudent/')
    else:
        return redirect('/')

@login_required
def accessModifyStudentPage(request):
    if User.objects.filter(username=request.user, is_superuser=False).exists():
        return redirect('/modifyStudent/')
    else:
        return redirect('/')

def registerStudentPage(request):
    context = {}
    context['form_st'] = StudentEntryForm()
    return render (request, 'registerStudent.html', context)

@login_required
def modifyStudentPage(request):
    context = {}
    context['form_ip'] = InputTextForm()
    #context['form_st'] = StudentEntryForm()
    return render (request, 'modifyStudent.html', context)

def contactPage(request):
    if User.objects.filter(username=request.user).exists():
        print(User.objects.filter(username=request.user))        
        return render (request, 'contactUs.html', context={'userThere' : True})
    else:
        print('No')
        return render (request, 'contactUs.html', context=None)

@csrf_exempt
def registerStudentDetails(request):
    form = StudentEntryForm(request.POST)
    if form.is_valid():
        form.save()
        """studentData = form.cleaned_data
        Student.objects.create(
            Name = studentData['Name'], 
            Course = studentData['Course'],
            Mobile = studentData['Mobile'],
            Father_name = studentData['Father_name'],
            Mother_name = studentData['Mother_name'],
            Qualification = studentData['Qualification'],
            DOB = studentData['DOB'],
            Date_of_Joining = studentData['Date_of_Joining'],
            Date_of_Submission = studentData['Date_of_Submission'],
            Paid = studentData['Paid'],
            Fee = studentData['Fee'],
            Balance = studentData['Balance'],
            Address = studentData['Address'],
            Description = studentData['Description'],
            Trainer = studentData['Trainer']            
        )  """
        return redirect('/accountantHome/')
    else:
        return redirect('/registerStudent/')

def getStudentDetails(request):
    name = request.POST['inputText']
    if not (Student.objects.filter(Name__startswith = name).exists()):
        raise forms.ValidationError("No Student Account exists")
    else:
        shortData_list = Student.objects.filter(Name__startswith = name)
        context = {}
        context['form_ip'] = InputTextForm()
        context['shortData'] = shortData_list
        return render(request, 'modifyStudent.html', context) 

def fillStudentDetails(request):
    userIdVal = request.POST.get('userID')
    formData = Student.objects.get(pk=userIdVal)
    form = StudentEntryForm(instance=formData)
    context = {}
    context['form_ip'] = InputTextForm()
    context['form'] = form
    return render(request, 'modifyStudent.html', context) 
    """studentData = (Student.objects.get(pk=userIdVal)).getGeneralDetails()
    studentData.update((Student.objects.get(pk=userIdVal)).getFeeDetails())
    return HttpResponse(json.dumps(studentData)) """

def modifyStudentDetails(request):
    form = StudentEntryForm(request.POST)
    if form.is_valid():
        eF = form.cleaned_data
        existingForm = Student.objects.get(Name=eF['Name'])
        form = StudentEntryForm(request.POST, instance=existingForm)
        form.save()
        return redirect('/accountantHome/')
    else:
        return redirect('/modifyStudent/')

def sendMail(request):
    userId = request.POST.get('mailID')
    userQuery = request.POST.get('query')
    print('B4')
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail('contactsubramanianr@gmail.com', 'saisubramanian97@gmail.com', userQuery)         
    """send_mail(
        'Query from' + str(userId),
        userQuery,
        'contactsubramanianr@gmail.com',
        ['saisubramanian97@gmail.com'],
        fail_silently=False
    )"""
    print('After')

