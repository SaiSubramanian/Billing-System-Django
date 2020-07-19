from django.db import models

class Administrators(models.Model):
    adminName = models.CharField(max_length=16)
    adminPwd = models.CharField(max_length=16)

    def __str__(self):
        return self.adminName

class Accountants(models.Model):
    id = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=16)
    userPwd = models.CharField(max_length=16)
    dateOfJoining = models.DateField()
    dateOfBirth = models.DateField()
    salary = models.CharField(max_length=10)
    branch = models.CharField(max_length=50)

    def __str__(self):
        return (str(self.id) + "-" + self.userName + "-" + self.salary + "-" + self.branch)
    
    def getBranch(self):
        return self.branch

class Branches(models.Model):
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.branch