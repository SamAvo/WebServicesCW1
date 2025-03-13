from django.db import models

# Create your models here.

class Module(models.Model):
    code = models.CharField(max_length = 10)
    name = models.CharField(max_length = 30)

class Professor(models.Model):
    code = models.CharField(max_length = 5)
    firstname = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)

class User(models.Model):
    username = models.CharField(max_length = 30)
    email = models.EmailField()
    password = models.CharField(max_length = 30)

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    professors = models.ManyToManyField(Professor)
    year = models.IntegerField()
    semester = models.IntegerField()

class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    moduleinstance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    score = models.IntegerField()

