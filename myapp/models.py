from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    num_employees = models.IntegerField(default=0)
    num_managers = models.IntegerField(default=0)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.companyName

    
class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shift_start = models.TimeField(blank=True, null=True)
    shift_end = models.TimeField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    password = models.CharField(max_length=128, blank=True, null=True)
    face_image = models.ImageField(upload_to='manager_faces/', blank=True, null=True)

    def __str__(self):
        return self.name

    
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shift_start = models.TimeField(blank=True, null=True)
    shift_end = models.TimeField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, db_column='manager_id')
    password = models.CharField(max_length=128, blank=True, null=True)
    face_image = models.ImageField(upload_to='employee_faces/', blank=True, null=True)

    def __str__(self):
        return self.name

   
class CompanyLoginHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.company_name} logged in at {self.login_time}"


class UserLoginHistory(models.Model):
    user_email = models.EmailField()
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} ({self.role}) at {self.login_time}"
class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Link to either Employee or Manager, one of them will be null
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)

    # Storing email and name directly for easier lookup and historical data if employee/manager is deleted
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    user_role = models.CharField(max_length=20, choices=[('employee', 'Employee'), ('manager', 'Manager')]) # 'employee' or 'manager'

    date = models.DateField(default=timezone.now)
    expected_entry_time = models.TimeField(null=True, blank=True)
    expected_exit_time = models.TimeField(null=True, blank=True)
    real_entry_time = models.TimeField(null=True, blank=True) # To be filled by OpenCV later
    real_exit_time = models.TimeField(null=True, blank=True) # To be filled by OpenCV later

    class Meta:
        # Ensures that for a given company, user, and date, there's only one attendance record
        unique_together = ('company', 'user_email', 'date')
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"Attendance for {self.user_name} ({self.user_role}) on {self.date} at {self.company.companyName}"

# models.py
# (Your existing models above this)

from django.db import models

class Task(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Corrected ManyToManyFields with the through model
    assigned_employees = models.ManyToManyField(
        'Employee',
        through='TaskAssignment', 
        related_name='employee_tasks',
        blank=True
    )
    assigned_managers = models.ManyToManyField(
        'Manager',
        through='TaskAssignment',
        related_name='manager_tasks',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}-{self.description}'



# This is the crucial model that was missing or incorrectly named.
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    is_completed_by_user = models.BooleanField(default=False)
    completion_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        if self.employee:
            return f'{self.employee.name} assigned to {self.task.title}'
        elif self.manager:
            return f'{self.manager.name} assigned to {self.task.title}'
        return f'Assigned to {self.task.title}'