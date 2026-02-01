from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parent_phone = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.school.name}"



class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.score}"
