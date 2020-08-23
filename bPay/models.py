from django.db import models

class Accountant(models.Model):
    Username = models.CharField(max_length=16)
    Date_of_Joining = models.DateField()
    DOB = models.DateField()
    Salary = models.CharField(max_length=10)
    Branch = models.CharField(max_length=50)

    def __str__(self):
        return self.Username
    
    def getBranch(self):
        return self.Branch

    def getDetails(self):
        return {'Username':self.Username, 'Date_of_Joining':str(self.Date_of_Joining), 'DOB':str(self.DOB), 'Salary':self.Salary}

class Branch_Name(models.Model):
    Branch = models.CharField(max_length=50)

    def __str__(self):
        return self.Branch

class Student(models.Model):
    Name = models.CharField(max_length=50)
    Course = models.CharField(max_length=50)
    Mobile = models.BigIntegerField()
    Father_name = models.CharField(max_length=50)
    Mother_name = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=15)
    DOB = models.DateField()
    Date_of_Joining = models.DateField()
    Date_of_Submission = models.DateField()
    Paid = models.IntegerField()
    Fee = models.IntegerField()
    Balance = models.IntegerField()
    Address = models.TextField()
    Description = models.TextField()
    Trainer = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

    def getFeeDetails(self):
        return {'Paid':self.Paid, 'Fee':self.Fee, 'Balance':self.Balance}

    def getCourseDetails(self):
        return {'Name':self.Name, 'Course':self.Course, 'Mobile':self.Mobile, 
                'Date_of_Submission':str(self.Date_of_Submission),'Paid':self.Paid, 
                'Fee':self.Fee, 'Balance':self.Balance}

    def getGeneralDetails(self):
        return {'Name':self.Name, 'Course':self.Course, 'Mobile':self.Mobile, 'Father_name':self.Father_name, 
                'Mother_name':self.Mother_name, 'Qualification':self.Qualification, 'DOB':str(self.DOB), 
                'Date_of_Joining':str(self.Date_of_Joining), 'Date_of_Submission':str(self.Date_of_Submission), 
                'Address':self.Address, 'Description':self.Description, 'Trainer':self.Trainer}