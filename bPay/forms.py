from django import forms
from .models import Branch_Name, Student

class UserEntryForm(forms.Form):
    
    userName = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    passWord = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

class UserRegistrationForm(forms.Form):

    userName = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
    )
    passWord = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    DOJ = forms.DateField(
        required = True,
        label = 'Date of Joining',
        help_text = ' Enter in mm/dd/yyyy format',
        widget = forms.DateInput()
    )
    DOB = forms.DateField(
        required = True,
        label = 'Date of Birth',
        help_text = ' Enter in mm/dd/yyyy format',
        widget = forms.DateInput()
    )
    salary = forms.CharField(
        required = True,
        label = 'Salary',
        max_length = 10
    )

class BranchesForm(forms.Form):

    branch = forms.ModelChoiceField(
        required = True,
        label = 'Branch',
        queryset = Branch_Name.objects.all().values_list('Branch', flat=True)
    )

class InputTextForm(forms.Form):

    inputText = forms.CharField(
        required = True,
        label = 'Find'
    )

class StudentEntryForm(forms.ModelForm):

    class Meta:

        model = Student
        fields = ['Name', 'Course', 'Mobile', 'Father_name', 'Mother_name', 'Qualification', 'DOB', 
                  'Date_of_Joining', 'Date_of_Submission', 'Paid', 'Fee', 'Balance', 'Address', 
                  'Description', 'Trainer']