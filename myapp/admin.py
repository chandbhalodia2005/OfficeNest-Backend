from django.contrib import admin
from .models import (
    Company,
    Manager,
    Employee,
    UserLoginHistory,
    CompanyLoginHistory,
    Attendance,
    Task,
    TaskAssignment,
)

# -----------------------------
# Company Admin
# -----------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['companyName', 'email', 'city']
    fields = ('companyName', 'email', 'phone', 'city', 'password', 'num_employees', 'num_managers')
    search_fields = ('companyName', 'email', 'city')
    list_filter = ('city',)


# -----------------------------
# Attendance Admin
# -----------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'user_name',
        'user_role',
        'company',
        'date',
        'expected_entry_time',
        'real_entry_time',
        'expected_exit_time',
        'real_exit_time'
    )
    list_filter = (
        'company',
        'date',
        'user_role'
    )
    search_fields = (
        'user_name',
        'user_email',
        'company__companyName'
    )


# -----------------------------
# Manager Admin
# -----------------------------
# @admin.register(Manager)
# class ManagerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'gender', 'shift_start', 'shift_end', 'company', 'date_joined']
#     fields = (
#         'name', 'email', 'phone', 'gender', 'date_of_birth', 'department',
#         'date_joined', 'salary', 'password', 'company', 'face_image',
#         'shift_start', 'shift_end'
#     )
#     search_fields = ('name', 'email', 'company__companyName', 'department')
#     list_filter = ('company', 'gender', 'department')


# -----------------------------
# Employee Admin
# -----------------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'manager', 'shift_start', 'shift_end', 'date_joined']
    fields = (
        'name', 'email', 'phone', 'address', 'gender', 'date_of_birth',
        'shift_start', 'shift_end', 'position', 'date_joined', 'salary',
        'company', 'manager', 'password', 'face_image'
    )
    search_fields = ('name', 'email', 'company__companyName', 'position', 'manager__name')
    list_filter = ('company', 'position', 'gender', 'manager')


# -----------------------------
# Inline for Task Assignments
# -----------------------------


# -----------------------------
# Task Admin


# -----------------------------
# Other Models
# -----------------------------
admin.site.register(UserLoginHistory)
admin.site.register(CompanyLoginHistory)
admin.site.register(Manager)
admin.site.register(Task)
admin.site.register(TaskAssignment)