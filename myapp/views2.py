 # core/views.py
from email.utils import parsedate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated # Already there, but good to confirm
# ... other imports (Response, status, etc.)
from datetime import timedelta, time # <--- Add this import
from django.utils.dateparse import parse_date
from rest_framework import viewsets

from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password # <--- Added check_password
from .models import Company, Employee, Manager, CompanyLoginHistory, UserLoginHistory,Attendance
import json
from django.views.decorators.http import require_http_methods
from django.db.models import Q, F
from django.db.models import F, ExpressionWrapper, DurationField
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from rest_framework import serializers
from datetime import datetime, timedelta
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from .models import Employee, Attendance
from rest_framework.parsers import MultiPartParser, FormParser
import face_recognition
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from rest_framework.generics import CreateAPIView , RetrieveUpdateAPIView# For EmployeeCreateView

from myapp.models import Employee, Company
from .serializers import EmployeeSerializer ,AttendanceSerializer,TaskSerializer
from .models import Attendance, Employee, Manager,Task
from datetime import date
from rest_framework.permissions import IsAuthenticated
# Import generic views for listing
from rest_framework import generics # <--- New import
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views import View # For class-based views
from rest_framework.views import APIView # Assuming this is from DRF based on your EmployeeUpdateView
from rest_framework.response import Response # For DRF APIView responses
from rest_framework import status # For DRF HTTP status codes
from django.db.models import Q # For OR queries
from django.forms.models import model_to_dict #
from .models import Company, Manager, Employee
from django.utils.timezone import now

from .serializers import (
    CompanySignupSerializer,
    CompanySerializer, # If you have a serializer for Company model, though not directly used here
    ManagerSerializer,
    EmployeeSerializer
    
)
# In your views.py file
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
from .models import Attendance, Company

# ------------------------- Company Signup -------------------------
@method_decorator(csrf_exempt, name='dispatch')
class CompanySignupView(APIView):
    def post(self, request):
        serializer = CompanySignupSerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save(password=make_password(serializer.validated_data['password'])) # Hash password
            return Response({"message": "Company created", "company_id": company.company_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ------------------------- Company Login -------------------------
# @api_view(["POST"])
# def login_user(request):
#     print("Received request data:", request.data)

#     email = request.data.get("email")
#     password = request.data.get("password")

#     if not email or not password:
#         return Response({"status": "error", "message": "Email and password are required"}, status=400)

#     try:
#         # Company login
#         try:
#             company = Company.objects.get(email=email)

#             # ✅ Hash if stored password is in plain text
#             if not company.password.startswith("pbkdf2_"):
#                 company.password = make_password(company.password)
#                 company.save()

#             if company.check_password(password):
#                 CompanyLoginHistory.objects.create(
#                     company=company,
#                     company_name=company.companyName,
#                     username=company.companyName,
#                     email=company.email
#                 )
#                 return Response({
#                     "status": "success",
#                     "role": "company",
#                     "username": company.companyName,
#                     "company_id": company.company_id,
#                     "message": f"Logged in as company: {company.companyName}"
#                 })
#         except Company.DoesNotExist:
#             pass

#         # Manager login
#         try:
#             manager = Manager.objects.get(email=email)

#             if not manager.password.startswith("pbkdf2_"):
#                 manager.password = make_password(manager.password)
#                 manager.save()

#             if manager.check_password(password):
#                 UserLoginHistory.objects.create(
#                     user_email=manager.email,
#                     username=manager.name,
#                     role="manager"
#                 )
#                 return Response({
#                     "status": "success",
#                     "role": "manager",
#                     "username": manager.name,
#                     "manager_id": manager.manager_id,
#                     "message": f"Logged in as manager: {manager.name}"
#                 })
#         except Manager.DoesNotExist:
#             pass

#         # Employee login
#         try:
#             employee = Employee.objects.get(email=email)

#             if not employee.password.startswith("pbkdf2_"):
#                 employee.password = make_password(employee.password)
#                 employee.save()

#             if employee.check_password(password):
#                 UserLoginHistory.objects.create(
#                     user_email=employee.email,
#                     username=employee.name,
#                     role="employee"
#                 )
#                 return Response({
#                     "status": "success",
#                     "role": "employee",
#                     "username": employee.name,
#                     "employee_id": employee.employee_id,
#                     "message": f"Logged in as employee: {employee.name}"
#                 })
#         except Employee.DoesNotExist:
#             pass

#         return Response({"status": "error", "message": "Invalid email or password"}, status=400)

#     except Exception as e:
#         return Response({"status": "error", "message": str(e)}, status=500)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password  # Added import

from .models import Company, Employee, Manager, CompanyLoginHistory, UserLoginHistory
from .serializers import ManagerSerializer, EmployeeSerializer # Assuming these exist

from django.contrib.auth.hashers import check_password, make_password # Import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import logging

from .models import Company, Manager, Employee, UserLoginHistory, CompanyLoginHistory

# Configure logging
logger = logging.getLogger(__name__)

@api_view(["POST"])
def login_user(request):
    logger.info(f"Received request data: {request.data}")

    email = request.data.get("email", "").strip()
    password = request.data.get("password", "").strip()

    if not email or not password:
        logger.warning("Bad Request: Email and password are required.")
        return Response({
            "status": "error",
            "message": "Email and password are required",
        }, status=status.HTTP_400_BAD_REQUEST)

    # --- Company login ---
    try:
        company = Company.objects.get(email__iexact=email) # Use iexact for case-insensitive email matching
        if company.password and check_password(password, company.password):
            employee_count = Employee.objects.filter(company=company).count()
            manager_count = Manager.objects.filter(company=company).count()
            CompanyLoginHistory.objects.create(
                company=company,
                company_name=company.companyName,
                username=company.companyName,
                email=company.email,
            )
            logger.info(f"Company login successful for email: {email}")
            return JsonResponse({
                'status': 'success',
                'role': 'company',
                'company_id': company.company_id,
                'company_email': company.email,
                'company_name': company.companyName,
                'employee_count': employee_count,
                'manager_count': manager_count,
            })
        else:
            logger.warning(f"Invalid password for company email: {email}")
    except Company.DoesNotExist:
        logger.info(f"No company found with email: {email}")
        pass

    # --- Manager login ---
    try:
        manager = Manager.objects.get(email__iexact=email)
        if manager.password and check_password(password, manager.password):
            company_name = manager.company.companyName if hasattr(manager, 'company') else ''
            company_id = manager.company.company_id if hasattr(manager, 'company') else None

            UserLoginHistory.objects.create(
                user_email=manager.email,
                username=manager.name,
                role="manager"
            )
            logger.info(f"Manager login successful for email: {email}")
            return Response({
                "status": "success",
                "role": "manager",
                "name": manager.name,
                "company_name": company_name,
                "company_id": company_id,   # ✅ Added

                "manager_id": manager.manager_id,
                "message": f"Logged in as manager: {manager.name}"
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Invalid password for manager email: {email}")
    except Manager.DoesNotExist:
        logger.info(f"No manager found with email: {email}")
        pass

    # --- Employee login ---
    try:
        employee = Employee.objects.get(email__iexact=email)
        if employee.password and check_password(password, employee.password):
            company_name = employee.company.companyName if hasattr(employee, 'company') else ''
            UserLoginHistory.objects.create(
                user_email=employee.email,
                username=employee.name,
                role="employee"
            )
            logger.info(f"Employee login successful for email: {email}")
            return Response({
                "status": "success",
                "role": "employee",
                "name": employee.name,
                "company_name": company_name,
                "employee_id": employee.employee_id,
                "message": f"Logged in as employee: {employee.name}"
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Invalid password for employee email: {email}")
    except Employee.DoesNotExist:
        logger.info(f"No employee found with email: {email}")
        pass

    logger.warning(f"Failed login attempt for email: {email}")
    return Response({
        "status": "error",
        "message": "Invalid email or password"
    }, status=status.HTTP_401_UNAUTHORIZED) # Use 401 for authentication failure

@method_decorator(csrf_exempt, name='dispatch') # Apply csrf_exempt if needed
class CompanyChangePasswordView(APIView):
    def post(self, request, company_id):
        new_password = request.data.get('password')
        if not new_password:
            return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(pk=company_id)
            company.set_password(new_password) # Uses the model's method to hash and save
            return Response({'success': 'Password updated'}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)


# ------------------------- Manager Creation (Single) -------------------------
@method_decorator(csrf_exempt, name='dispatch')
class ManagerCreateView(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()
        mutable_data['password'] = make_password(password) # Hash password before passing to serializer

        serializer = ManagerSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Manager created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------- Manager Creation (Bulk) -------------------------
@method_decorator(csrf_exempt, name='dispatch')
class ManagerBulkCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser] # Ensure this is present

    def post(self, request):
        try:
            company_id = request.data.get("company_id")
            managers_json_str = request.data.get("managers_json")

            print("Received company_id:", company_id)
            print("Received managers_json_str (raw):", managers_json_str) # Print raw JSON string

            if not company_id or not managers_json_str:
                return Response({"error": "Missing company_id or managers data"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                managers_data = json.loads(managers_json_str)
                print("Parsed managers_data (JSON):", managers_data) # Print parsed JSON data
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format for managers data"}, status=status.HTTP_400_BAD_REQUEST)

            if not managers_data:
                return Response({"error": "No manager records found in JSON data"}, status=status.HTTP_400_BAD_REQUEST)

            company = Company.objects.get(company_id=company_id)

            created_ids = []
            errors = []
            for index, mgr_data in enumerate(managers_data):
                password = mgr_data.get('password')
                hashed_password = make_password(password) if password else None

                gender_input = mgr_data.get("gender")
                gender_char = gender_input[0].upper() if gender_input and isinstance(gender_input, str) and len(gender_input) > 0 else None

                face_image_key = f"face_image_{index}"
                face_image_file = request.FILES.get(face_image_key)

                # Ensure face_image_file is None if face_image_idx was not sent or no file was uploaded
                if mgr_data.get('face_image_idx') is not None and not face_image_file:
                    print(f"Warning: face_image_idx present for manager {index} but no file found for {face_image_key}")
                    face_image_file = None # Explicitly set to None if file is missing

                serializer = ManagerSerializer(data={
                    "name": mgr_data.get("name"),
                    "email": mgr_data.get("email"),
                    "phone": mgr_data.get("phone"),
                    "department": mgr_data.get("department"),
                    "gender": gender_char,
                    "date_of_birth": mgr_data.get("dob"),
                    "date_joined": mgr_data.get("joining_date"),
                    "salary": mgr_data.get("salary"),
                    "shift_start": mgr_data.get("shift_start"),
                    "shift_end": mgr_data.get("shift_end"),
                    "company": company_id,
                    "password": hashed_password,
                    'face_image': face_image_file
                })

                if serializer.is_valid():
                    manager = serializer.save()
                    created_ids.append(manager.manager_id)
                else:
                    print(f"Manager {index} serializer errors: {serializer.errors}") # <-- CRITICAL DEBUG PRINT
                    errors.append({"data": mgr_data, "errors": serializer.errors})

            if errors:
                return Response({"message": "Some managers could not be created", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Managers created", "manager_ids": created_ids}, status=status.HTTP_201_CREATED)

        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unhandled exception in ManagerBulkCreateView: {e}") # Debug unhandled exceptions
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------- Employee Creation (Bulk) -------------------------

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction # Import transaction

import json

# Import your models and serializers
from .models import Company, Employee, Manager, CompanyLoginHistory, UserLoginHistory # Assuming these are your models
from .serializers import EmployeeSerializer, CompanySignupSerializer, ManagerSerializer # Assuming these are your serializers

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeBulkCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            company_id_from_request = request.data.get("company_id")
            employees_json_str = request.data.get("employees_json")

            print("Received company_id:", company_id_from_request)
            print("Received employees_json_str (raw):", employees_json_str)

            if not company_id_from_request or not employees_json_str:
                return Response({"error": "Missing company_id or employees data"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                employees_data = json.loads(employees_json_str)
                print("Parsed employees_data (JSON):", employees_data)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format for employees data"}, status=status.HTTP_400_BAD_REQUEST)

            if not employees_data:
                return Response({"error": "No employee records found in JSON data"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                company = Company.objects.get(company_id=company_id_from_request)
            except Company.DoesNotExist:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"Error during Company lookup: {e}")
                return Response({"error": f"Error fetching company: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            created_ids = []
            errors = []

            with transaction.atomic():
                for index, emp_data in enumerate(employees_data):
                    password = emp_data.get('password')
                    hashed_password = make_password(password) if password else None

                    gender_input = emp_data.get("gender")
                    gender_char = gender_input[0].upper() if gender_input and isinstance(gender_input, str) and len(gender_input) > 0 else None

                    face_image_key = f"face_image_{index}"
                    face_image_file = request.FILES.get(face_image_key)

                    if emp_data.get('face_image_idx') is not None and not face_image_file:
                        print(f"Warning: face_image_idx present for employee {index} but no file found for {face_image_key}")
                        face_image_file = None

                    serializer_data = {
                        "name": emp_data.get("name"),
                        "email": emp_data.get("email"),
                        "phone": emp_data.get("phone"),
                        "address": emp_data.get("address"),
                        "position": emp_data.get("designation"),
                        "gender": gender_char,
                        "dob": emp_data.get("dob"),
                        "date_of_joining": emp_data.get("joining_date"),
                        "salary": emp_data.get("salary"),
                        "shift_start": emp_data.get("shift_start"),
                        "shift_end": emp_data.get("shift_end"),
                        "company_id": company.company_id,
                        "manager": emp_data.get("manager"),
                        "password": hashed_password,
                        "face_image": face_image_file
                    }

                    # Pass request context to serializer for get_image method
                    serializer = EmployeeSerializer(data=serializer_data, context={'request': request})

                    if serializer.is_valid():
                        employee = serializer.save()
                        # *** CRITICAL FIX: Use employee.employee_id instead of employee.id ***
                        created_ids.append(employee.employee_id)
                    else:
                        print(f"Employee {index} serializer errors: {serializer.errors}")
                        errors.append({"data": emp_data, "errors": serializer.errors})

            if errors:
                return Response({"message": "Some employees could not be created", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Employees created", "employee_ids": created_ids}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Unhandled exception in EmployeeBulkCreateView: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------- Manager Update -------------------------
@method_decorator(csrf_exempt, name='dispatch') # Apply csrf_exempt if needed
class ManagerUpdateView(APIView):
    permission_classes = [IsAuthenticated] # Example: requires authentication

    def patch(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
        except Manager.DoesNotExist:
            return Response({"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND)

        protected_fields = ['shift_start', 'shift_end', 'date_joined', 'salary']
        for field in protected_fields:
            if field in request.data:
                return Response(
                    {f"error": f"{field} can only be modified by the company"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = ManagerSerializer(manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------- Attendance Update API -------------------------
@method_decorator(csrf_exempt, name='dispatch') # Apply csrf_exempt if needed
class AttendanceUpdateView(APIView):
    """
    API endpoint to update real_entry_time or real_exit_time for attendance records.
    Expects JSON data:
    {
        "email": "user@example.com",
        "time": "HH:MM:SS",
        "type": "entry" or "exit"
    }
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        time_str = data.get('time')
        update_type = data.get('type') # 'entry' or 'exit'

        if not all([email, time_str, update_type]):
            return Response(
                {"status": "error", "message": "Missing required fields: email, time, type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Convert time string to time object
            current_time = timezone.datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            return Response(
                {"status": "error", "message": "Invalid time format. Use HH:MM:SS"},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = timezone.localdate()

        try:
            # Find the attendance record for today for the given email
            # Note: The Attendance model directly stores user_email, so we can query that.
            attendance_record = Attendance.objects.get(
                user_email=email,
                date=today
            )
        except Attendance.DoesNotExist:
            return Response(
                {"status": "error", "message": f"Attendance record not found for {email} on {today}"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Attendance.MultipleObjectsReturned:
            # This case should ideally not happen due to unique_together constraint,
            # but good to handle defensively.
            return Response(
                {"status": "error", "message": f"Multiple attendance records found for {email} on {today}. Contact admin."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Update the appropriate time field
        if update_type == 'entry':
            if attendance_record.real_entry_time:
                return Response(
                    {"status": "warning", "message": f"Real entry time already recorded for {email} today."},
                    status=status.HTTP_200_OK # Still a success, but with a warning
                )
            attendance_record.real_entry_time = current_time
            message = f"Real entry time updated for {email}."
        elif update_type == 'exit':
            if attendance_record.real_exit_time:
                return Response(
                    {"status": "warning", "message": f"Real exit time already recorded for {email} today."},
                    status=status.HTTP_200_OK # Still a success, but with a warning
                )
            attendance_record.real_exit_time = current_time
            message = f"Real exit time updated for {email}."
        else:
            return Response(
                {"status": "error", "message": "Invalid 'type' specified. Must be 'entry' or 'exit'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance_record.save()
        return Response({"status": "success", "message": message}, status=status.HTTP_200_OK)


# ------------------------- Attendance List API -------------------------
@method_decorator(csrf_exempt, name='dispatch') # Apply csrf_exempt if needed
class AttendanceListView(APIView):
    """
    API endpoint to retrieve attendance records.
    Can be filtered by company_id (query parameter).
    """
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        today = timezone.localdate()

        attendance_records = Attendance.objects.filter(date=today)

        if company_id:
            try:
                company = Company.objects.get(company_id=company_id)
                attendance_records = attendance_records.filter(company=company)
            except Company.DoesNotExist:
                return Response(
                    {"status": "error", "message": f"Company with ID {company_id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Convert queryset to a list of dictionaries for JSON response
        data = []
        for record in attendance_records:
            record_dict = {
                'attendance_id': record.attendance_id,
                'user_name': record.user_name,
                'user_email': record.user_email,
                'user_role': record.user_role,
                'date': record.date.strftime('%Y-%m-%d'), # Format date for JSON
                'expected_entry_time': record.expected_entry_time.strftime('%H:%M:%S') if record.expected_entry_time else None,
                'expected_exit_time': record.expected_exit_time.strftime('%H:%M:%S') if record.expected_exit_time else None,
                'real_entry_time': record.real_entry_time.strftime('%H:%M:%S') if record.real_entry_time else None,
                'real_exit_time': record.real_exit_time.strftime('%H:%M:%S') if record.real_exit_time else None,
                'company_name': record.company.companyName, # Include company name
            }
            data.append(record_dict)

        return Response(data, status=status.HTTP_200_OK)
# @method_decorator(csrf_exempt, name='dispatch')
# class EmployeeCreateView(APIView):
#     def post(self, request):
#         password = request.data.get('password')
#         if not password:
#             return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

#         mutable_data = request.data.copy()
#         mutable_data['password'] = make_password(password)

#         serializer = EmployeeSerializer(data=mutable_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Employee created successfully.'}, status=status.HTTP_201_CREATED)
class EmployeeCreateView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # This block will only execute if serializer.is_valid() is True
        serializer.save()

    # Override create to get detailed error messages
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # THIS IS THE CRITICAL DEBUGGING PART
            print("\n--- SERIALIZER ERRORS ---")
            print(serializer.errors) # <--- This will print the detailed validation errors
            print("--- REQUEST DATA ---")
            print(request.data) # <--- See what data DRF received
            print("--- EXCEPTION ---")
            print(e)
            print("-------------------------\n")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def mark_attendance(request):
#     email = request.POST.get('email')
#     action = request.POST.get('action')  # 'entry' or 'exit'
#     uploaded_image = request.FILES.get('face_image')

#     if not email or not action or not uploaded_image:
#         return Response({'message': 'Missing data'}, status=400)

#     # Load uploaded image
#     try:
#         uploaded_image_data = face_recognition.load_image_file(uploaded_image)
#         uploaded_encodings = face_recognition.face_encodings(uploaded_image_data)
#         if len(uploaded_encodings) == 0:
#             return Response({'message': 'No face detected'}, status=400)
#         uploaded_encoding = uploaded_encodings[0]
#     except:
#         return Response({'message': 'Invalid image'}, status=400)

#     # Find user
#     user = None
#     try:
#         user = Employee.objects.get(email=email)
#     except:
#         try:
#             user = Manager.objects.get(email=email)
#         except:
#             return Response({'message': 'User not found'}, status=404)

#     # Compare with stored face image
#     if not user.face_image:
#         return Response({'message': 'No reference image stored'}, status=400)

#     known_image = face_recognition.load_image_file(user.face_image.path)
#     known_encodings = face_recognition.face_encodings(known_image)

#     if not known_encodings:
#         return Response({'message': 'No face in reference image'}, status=400)

#     match_result = face_recognition.compare_faces([known_encodings[0]], uploaded_encoding)[0]

#     if not match_result:
#         return Response({'message': 'Face does not match'}, status=403)

#     # Match successful - update today's attendance
#     today = date.today()
#     try:
#         record = Attendance.objects.get(user_email=email, date=today)
#         if action == 'entry':
#             record.real_entry_time = now().time()
#         elif action == 'exit':
#             record.real_exit_time = now().time()
#         record.save()
#         return Response({'message': f'{action.capitalize()} marked successfully'})
#     except Attendance.DoesNotExist:
#         return Response({'message': 'Attendance record not found'}, status=404)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def mark_attendance(request):
    email = request.POST.get('email')
    action = request.POST.get('action')
    face_image_file = request.FILES.get('face_image')

    if not all([email, action, face_image_file]):
        return Response({'message': 'Missing data.'}, status=400)

    # Search in both Employee and Manager
    user = None
    role = None
    try:
        user = Employee.objects.get(email=email)
        role = "Employee"
    except Employee.DoesNotExist:
        try:
            user = Manager.objects.get(email=email)
            role = "Manager"
        except Manager.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)

    # Load and encode stored image
    stored_image = face_recognition.load_image_file(user.face_image.path)
    stored_encoding = face_recognition.face_encodings(stored_image)
    if not stored_encoding:
        return Response({'message': 'No face found in stored image.'}, status=400)

    # Load and encode uploaded live image
    uploaded_image = face_recognition.load_image_file(face_image_file)
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)
    if not uploaded_encoding:
        return Response({'message': 'No face found in uploaded image.'}, status=400)

    # Compare faces
    match = face_recognition.compare_faces([stored_encoding[0]], uploaded_encoding[0])[0]
    if not match:
        return Response({'message': 'Face does not match.'}, status=403)

    # Save attendance record
    today = datetime.today().date()
    record, created = Attendance.objects.get_or_create(user_email=email, date=today, defaults={
        'user_name': user.name,
        'user_role': role,
    })

    if action == 'entry' and not record.real_entry_time:
        record.real_entry_time = now().time()
    elif action == 'exit' and not record.real_exit_time:
        record.real_exit_time = now().time()
    else:
        return Response({'message': f'{action.capitalize()} already marked.'}, status=200)

    record.save()
    return Response({'message': f'{action.capitalize()} marked successfully.'}, status=200)
# views.py
def get_counts_by_name(request):
    company_name = request.GET.get('company_name')
    try:
        company = Company.objects.get(name=company_name)
        employee_count = Employee.objects.filter(company=company).count()
        manager_count = Manager.objects.filter(company=company).count()
        return JsonResponse({
            'total_employees': employee_count,
            'total_managers': manager_count
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)
@api_view(['POST'])
def get_counts(request):
    """
    API endpoint to fetch company name, employee count, and manager count
    for a given company email, sent via POST request.
    """
    email = request.data.get('email')

    # Basic validation for email presence
    if not email:
        return Response(
            {'error': 'Email is required in the request body.'},
            status=status.HTTP_400_BAD_REQUEST # Use status.HTTP for clarity
        )

    try:
        # Retrieve the company based on the provided email
        # Assuming 'email' is a unique field in your Company model
        company = Company.objects.get(email=email)
    except Company.DoesNotExist:
        # Return a 404 error if the company is not found
        return Response(
            {'error': 'Company with the provided email not found.'},
            status=status.HTTP_404_NOT_FOUND # Use status.HTTP for clarity
        )
    except Exception as e:
        # Catch any other potential database errors during company retrieval
        print(f"Error fetching company for email {email}: {e}") # Log the error for debugging
        return Response(
            {'error': 'An internal server error occurred while fetching company information.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Count employees and managers associated with this company
    # Assumes 'company' is the ForeignKey field name in Employee and Manager models
    employee_count = Employee.objects.filter(company=company).count()
    manager_count = Manager.objects.filter(company=company).count()

    # Return the company name and counts in the response
    return Response({
        'company_name': company.companyName,  # Assuming 'companyName' is the field for company name
        'employee_count': employee_count,
        'manager_count': manager_count,
    }, status=status.HTTP_200_OK) #
@api_view(['GET'])
@csrf_exempt # Use this for development. For production, implement proper CSRF protection.
def get_employees(request):
    if request.method == "GET":
        company_id_param = request.query_params.get("company_id")

        if not company_id_param:
            return JsonResponse({"error": "Company ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = int(company_id_param)
            # --- CRITICAL FIX HERE ---
            # Instead of company__id, explicitly get the Company object by its primary key
            # and filter employees by that Company object.
            # Or, directly use company_id if 'id' is the primary key of Company model.
            # Assuming 'id' is the primary key for Company model (which is Django's default if not specified)
            employees = Employee.objects.filter(company__pk=company_id) # Using pk for clarity
            # OR, if you want to be super explicit and catch if company doesn't exist:
            # target_company = Company.objects.get(pk=company_id)
            # employees = Employee.objects.filter(company=target_company)
            # The first option (company__pk) is usually sufficient and more direct.

        except ValueError:
            return JsonResponse({"error": "Invalid Company ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in get_employees view: {e}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        for emp in employees:
            data.append({
                "name": emp.name,
                "employeeId": emp.employee_id,
                "position": emp.position,
                "email": emp.email,
                "phone": emp.phone, # Model field is 'phone'
                "address": emp.address,
                "gender": emp.gender,
                "dob": str(emp.date_of_birth) if emp.date_of_birth else 'N/A',
                "date_of_joining": str(emp.date_joined) if emp.date_joined else 'N/A',
                "shift_start": str(emp.shift_start) if emp.shift_start else 'N/A',
                "shift_end": str(emp.shift_end) if emp.shift_end else 'N/A',
                "salary": str(emp.salary) if emp.salary is not None else 'N/A',
                "face_image": emp.face_image.url if emp.face_image else "https://via.placeholder.com/48",
            })
        return JsonResponse(data, safe=False)
@api_view(['GET'])
@csrf_exempt
def get_new_hires_count(request):
    """
    Returns the count of employees who joined in the current month for a given company.
    """
    if request.method == "GET":
        company_id_param = request.query_params.get("company_id")

        if not company_id_param:
            return JsonResponse({"error": "Company ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = int(company_id_param)
            today = timezone.now() 
            new_hires_count = Employee.objects.filter(
                company__pk=company_id,
                date_joined__year=today.year,
                date_joined__month=today.month
            ).count()

            return JsonResponse({"new_hires_count": new_hires_count}, status=status.HTTP_200_OK)

        except ValueError:
            return JsonResponse({"error": "Invalid Company ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in get_new_hires_count view: {e}")
            return JsonResponse({"error": f"An internal server error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@csrf_exempt
def get_new_managers_count(request):
    if request.method == "GET":
        company_id_param = request.query_params.get("company_id")

        if not company_id_param:
            return JsonResponse({"error": "Company ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = int(company_id_param)
            today = timezone.now()

            new_managers_count = Manager.objects.filter(
                company__pk=company_id,
                date_of_joining__year=today.year,
                date_of_joining__month=today.month
            ).count()

            return JsonResponse({"new_managers_count": new_managers_count}, status=status.HTTP_200_OK)

        except ValueError:
            return JsonResponse({"error": "Invalid Company ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in get_new_managers_count view: {e}")
            return JsonResponse({"error": f"An internal server error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCompanyNameView(APIView):
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # CHANGE IS HERE: Use pk= instead of id=
            company = Company.objects.get(pk=company_id)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # It's good practice to log the full exception in production for debugging
            print(f"Error in GetCompanyNameView: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# yo
# from rest_framework.permissions import IsAuthenticated # Uncomment if needed

from .models import Employee, Manager, Company # Ensure these are imported

# ... (other imports and views like CompanySignupView, EmployeeCreateView, etc.) ...

# --- Helper function for employees (if you keep employees-detail/ and employees-count/) ---
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_employees(request):
    """
    Retrieves a list of all employees for a given company.
    Requires 'company_id' query parameter.
    """
    company_id = request.query_params.get('company_id')
    if not company_id:
        return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        company_id = int(company_id)
        # For the /employees-detail/ endpoint, return the serialized data
        employees = Employee.objects.filter(company_id=company_id).order_by('name')
        from .serializers import EmployeeSerializer # Import locally to avoid circular dependency
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "Invalid company_id."}, status=status.HTTP_400_BAD_REQUEST)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_managers(request):
    """
    Retrieves a list of all managers for a given company.
    Requires 'company_id' query parameter.
    """
    company_id = request.query_params.get('company_id')
    if not company_id:
        return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        company_id = int(company_id)
        # For the /managers-detail/ endpoint, return the serialized data
        managers = Manager.objects.filter(company_id=company_id).order_by('name')
        from .serializers import ManagerSerializer  # Import locally to avoid circular dependency
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "Invalid company_id."}, status=status.HTTP_400_BAD_REQUEST)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- New endpoint for fetching dashboard counts ---
@api_view(['GET'])
# @permission_classes([IsAuthenticated]) # Uncomment and implement proper authentication for production
def get_dashboard_counts(request):
    """
    Retrieves company name, total employee count, and total manager count
    for the given company_id.
    """
    company_id = request.query_params.get('company_id')

    if not company_id:
        return Response({"error": "company_id is required as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        company_id = int(company_id)
        # Use company_id as the primary key lookup for the Company model
        company = Company.objects.get(company_id=company_id) # Use company_id, not pk, if company_id is the actual PK field name

        employee_count = Employee.objects.filter(company=company).count()
        manager_count = Manager.objects.filter(company=company).count()

        data = {
            "company_name": company.companyName, # <--- This is correct based on previous logs (companyName, not company_name or name)
            "employee_count": employee_count,
            "manager_count": manager_count
        }
        return Response(data, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Invalid company_id provided. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
    except Company.DoesNotExist:
        return Response({"error": "Company not found for the provided ID."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the detailed exception for debugging on the server side
        print(f"Error in get_dashboard_counts: {e}")
        return Response({"error": "An internal server error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeDetailView(RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id' # This tells DRF to use 'employee_id' from the URL for lookup
    # permission_classes = [IsAuthenticated] # Add authentication if required

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'request': self.request} 
class ManagerDetailView(RetrieveUpdateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    lookup_field = 'manager_id' # This tells DRF to use 'employee_id' from the URL for lookup
    # permission_classes = [IsAuthenticated] # Add authentication if required

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'request': self.request} 
# views.py
class EmployeeListAPIView(APIView):
    def get(self, request):
        company_id = request.query_params.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employees = Employee.objects.filter(company__company_id=company_id)
            serializer = EmployeeSerializer(employees, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching employees:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# In your app's views.py file

from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeListView(generics.ListAPIView):
    """
    A view that returns a list of all employees for a specific company.
    It expects a 'company_id' query parameter.
    """
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Get the company_id from the query parameters, e.g., /api/employees/?company_id=1
        company_id = self.request.query_params.get('company_id')
        
        # If a company_id is provided, filter the employees by that company.
        if company_id:
            return Employee.objects.filter(company_id=company_id)        
        # If no company_id is provided, return an empty queryset to prevent
        # returning all employees across all companies without a specific filter.
        return Employee.objects.none()
# myapp/views.py
def get_queryset(self):
    company_id = self.request.query_params.get('company_id')
    if company_id:
        # Correctly filters on the company's primary key
        return Employee.objects.filter(company__company_id=company_id) 
    return Employee.objects.none()
@api_view(['GET'])
def attendance_list(request):
    company_id = request.GET.get('company_id')
    if not company_id:
        return Response({'error': 'Missing company_id'}, status=400)
    
    records = Attendance.objects.filter(company_id=company_id, date=timezone.now().date())
    serializer = AttendanceSerializer(records, many=True)

    return Response(serializer.data)
@method_decorator(csrf_exempt, name='dispatch')
class TodayAttendanceListView(APIView):
    """
    API endpoint to retrieve today's attendance records for a company.
    Can be filtered by company_id (query parameter).
    """
    def get(self, request, *args, **kwargs):
        company_id_str = request.query_params.get('company_id')
        
        if not company_id_str:
            return Response({'error': 'company_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = int(company_id_str)
            company = Company.objects.get(pk=company_id)
        except (ValueError, TypeError):
            return Response({'error': 'company_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({'error': f'Company with ID {company_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            today = timezone.localdate()
            
            # --- FIX: Removed the select_related call to bypass the error
            # --- This will be less performant but will work
            attendance_records = Attendance.objects.filter(
                company=company,
                date=today
            )
            # You can add 'manager' back as it's a direct foreign key and works
            # attendance_records = Attendance.objects.filter(
            #     company=company,
            #     date=today
            # ).select_related('manager')

            if not attendance_records.exists():
                return Response([], status=status.HTTP_200_OK)

            data = []
            for record in attendance_records:
                user_id = 'N/A'
                department_name = 'N/A'
                
                # Determine user details and handle department name separately
                if record.employee:
                    # Now you can directly access the employee field
                    user_id = record.employee.employee_id
                    department_name = 'Employee'
                elif record.manager:
                    user_id = record.manager.manager_id
                    department_name = 'Management'
                
                status_value = "Absent"
                total_hours = "0h 0m"
                check_in_time = 'N/A'
                check_out_time = 'N/A'
                
                # --- FIX: Apply the same conditional formatting to both times ---
                expected_check_in_time = record.expected_entry_time.strftime('%I:%M %p') if record.expected_entry_time else 'N/A'
                expected_check_out_time = record.expected_exit_time.strftime('%I:%M %p') if record.expected_exit_time else 'N/A'
                
                if record.real_entry_time:
                    check_in_time = record.real_entry_time.strftime('%I:%M %p')
                    status_value = "Present"
                    
                    if record.expected_entry_time and record.real_entry_time > record.expected_entry_time:
                        status_value = "Late"
                    
                    if record.real_exit_time:
                        check_out_time = record.real_exit_time.strftime('%I:%M %p')
                        
                        time_delta = (datetime.combine(date.min, record.real_exit_time) - 
                                      datetime.combine(date.min, record.real_entry_time))
                        
                        total_seconds = time_delta.total_seconds()
                        hours = int(total_seconds // 3600)
                        minutes = int((total_seconds % 3600) // 60)
                        total_hours = f"{hours}h {minutes}m"
                    else:
                        status_value = "Present (In-progress)"

                data.append({
                    'id': record.attendance_id,
                    'name': record.user_name,
                    'employeeId': user_id,
                    'department': department_name,
                    'expectedCheckInTime': expected_check_in_time,
                    'expectedCheckOutTime': expected_check_out_time,
                    'checkInTime': check_in_time,
                    'checkOutTime': check_out_time,
                    'totalHours': total_hours,
                    'status': status_value
                })

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            # This will log any unexpected error and return a 500 response
            return Response({'error': f'An unexpected server error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@method_decorator(csrf_exempt, name='dispatch')
class DateAttendanceListView(APIView):
    """
    API endpoint to retrieve today's attendance records for a company.
    Can be filtered by company_id and date (query parameters).
    """
    def get(self, request, *args, **kwargs):
        company_id_str = request.query_params.get('company_id')
        date_str = request.query_params.get('date') # <-- Retrieve the date parameter
        
        if not company_id_str:
            return Response({'error': 'company_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = int(company_id_str)
            company = Company.objects.get(pk=company_id)
        except (ValueError, TypeError):
            return Response({'error': 'company_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({'error': f'Company with ID {company_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # --- Handle the date query parameter ---
        if not date_str:
            return Response({'error': 'date query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Parse the date string from the request
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'date must be in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use the parsed date from the query parameter
            attendance_records = Attendance.objects.filter(
                company=company,
                date=query_date # <-- Use the validated date
            )

            # Rest of your code remains the same...
            if not attendance_records.exists():
                return Response([], status=status.HTTP_200_OK)
            
            data = []
            for record in attendance_records:
                user_id = 'N/A'
                department_name = 'N/A'
                
                if record.employee:
                    user_id = record.employee.employee_id
                    department_name = 'Employee'
                elif record.manager:
                    user_id = record.manager.manager_id
                    department_name = 'Management'
                
                status_value = "Absent"
                total_hours = "0h 0m"
                check_in_time = 'N/A'
                check_out_time = 'N/A'
                
                expected_check_in_time = record.expected_entry_time.strftime('%I:%M %p') if record.expected_entry_time else 'N/A'
                expected_check_out_time = record.expected_exit_time.strftime('%I:%M %p') if record.expected_exit_time else 'N/A'
                
                if record.real_entry_time:
                    check_in_time = record.real_entry_time.strftime('%I:%M %p')
                    status_value = "Present"
                    
                    if record.expected_entry_time and record.real_entry_time > record.expected_entry_time:
                        status_value = "Late"
                    
                    if record.real_exit_time:
                        check_out_time = record.real_exit_time.strftime('%I:%M %p')
                        
                        time_delta = (datetime.combine(date.min, record.real_exit_time) - 
                                      datetime.combine(date.min, record.real_entry_time))
                        
                        total_seconds = time_delta.total_seconds()
                        hours = int(total_seconds // 3600)
                        minutes = int((total_seconds % 3600) // 60)
                        total_hours = f"{hours}h {minutes}m"
                    else:
                        status_value = "Present (In-progress)"
                        
                data.append({
                    'id': record.attendance_id,
                    'name': record.user_name,
                    'employeeId': user_id,
                    'department': department_name,
                    'expectedCheckInTime': expected_check_in_time,
                    'expectedCheckOutTime': expected_check_out_time,
                    'checkInTime': check_in_time,
                    'checkOutTime': check_out_time,
                    'totalHours': total_hours,
                    'status': status_value
                })

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'An unexpected server error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AttendancePDFExportView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Generates and returns a PDF of daily attendance records for a given company and date.
        
        It retrieves attendance records, formats the data, and uses reportlab to
        create a well-styled PDF table. Missing check-in/out times are replaced with "___".
        """
        
        company_id_str = request.query_params.get('company_id')
        date_str = request.query_params.get('date')

        # --- Input Validation ---
        if not company_id_str or not date_str:
            return Response({'error': 'company_id and date query parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            company_id = int(company_id_str)
            company = Company.objects.get(pk=company_id)
            export_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return Response({'error': 'company_id must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({'error': f'Company with ID {company_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'date must be in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

        # --- Data Fetching ---
        attendance_records = Attendance.objects.filter(
            company=company,
            date=export_date
        ).select_related('employee', 'manager')
        
        # --- PDF Generation with reportlab ---
        buffer = BytesIO()
        
        # 1. Change page size to landscape and reduce margins
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=landscape(A4),
            rightMargin=0.5 * inch, 
            leftMargin=0.5 * inch, 
            topMargin=0.5 * inch, 
            bottomMargin=0.5 * inch
        )
        styles = getSampleStyleSheet()

        elements = []
        
        # Add a title to the PDF
        title = Paragraph(f"Daily Attendance Report for {export_date.strftime('%B %d, %Y')}", styles['Title'])
        elements.append(title)
        
        if not attendance_records.exists():
            no_data_msg = Paragraph("No attendance records found for this date.", styles['Normal'])
            elements.append(no_data_msg)
        else:
            # Prepare data for the table
            data = [
                ['Name', 'Check In', 'Check Out', 'Total Hours', 'Status']
            ]
            
            for record in attendance_records:
                employee_name = record.employee.name if record.employee else record.manager.name
                employee_id = record.employee.employee_id if record.employee else record.manager.manager_id
                
                check_in_time = record.real_entry_time.strftime('%I:%M %p') if record.real_entry_time else '___'
                check_out_time = record.real_exit_time.strftime('%I:%M %p') if record.real_exit_time else '___'
                
                total_hours = '___'
                status = "Absent"
                
                if record.real_entry_time and record.real_exit_time:
                    time_delta = datetime.combine(export_date, record.real_exit_time) - \
                                 datetime.combine(export_date, record.real_entry_time)
                    
                    total_seconds = time_delta.total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    total_hours = f"{hours}h {minutes}m"
                    status = "Present"
                elif record.real_entry_time:
                    status = "Present (In-progress)"

                data.append([
                    
                    employee_name,
                    check_in_time,
                    check_out_time,
                    total_hours,
                    status
                ])

            # Define table style for a clean look
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#37a096')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d6d8db')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])

            # 2. Define custom column widths to fit the landscape page
            col_widths = [
                2.2 * inch,  # Employee ID
                1.5 * inch,  # Name
                1.5 * inch,  # Check In
                1.5 * inch,  # Check Out
                1.5 * inch,  # Total Hours
                1.5 * inch   # Status
            ]

            # Create the table with the new column widths
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            elements.append(table)
            
        doc.build(elements)
        buffer.seek(0)

        # Return the PDF file as a response
        return FileResponse(buffer, as_attachment=True, filename=f"Attendance_Report_{date_str}.pdf")
    
class PresentCountView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Calculates and returns the number of employees and managers present today,
        along with the total count of all employees and managers.
        """
        today = date.today()

        # Count records where either an employee or a manager is present today
        present_count = Attendance.objects.filter(
            date=today
        ).filter(
            Q(real_entry_time__isnull=False) | Q(real_exit_time__isnull=False)
        ).count()
        
        # Count all employees and managers to get the total workforce size
        total_employees = Employee.objects.count()
        total_managers = Manager.objects.count()
        total_workforce = total_employees + total_managers

        # Prepare the response data
        data = {
            'present_count': present_count,
            'total_employees': total_workforce,
        }
        
        return Response(data, status=status.HTTP_200_OK)
class LateArrivalsCountView(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        try:
            # For employees: late if > 20 mins
            employee_late_duration = ExpressionWrapper(
                F('real_entry_time') - F('expected_entry_time'),
                output_field=DurationField()
            )
            late_employees = Attendance.objects.annotate(
                delay=employee_late_duration
            ).filter(
                date=today,
                employee__isnull=False,
                real_entry_time__isnull=False,
                expected_entry_time__isnull=False,
                delay__gt=timedelta(minutes=20)
            ).values('employee').distinct().count()

            # For managers: late if > 30 mins
            manager_late_duration = ExpressionWrapper(
                F('real_entry_time') - F('expected_entry_time'),
                output_field=DurationField()
            )
            late_managers = Attendance.objects.annotate(
                delay=manager_late_duration
            ).filter(
                date=today,
                manager__isnull=False,
                real_entry_time__isnull=False,
                expected_entry_time__isnull=False,
                delay__gt=timedelta(minutes=30)
            ).values('manager').distinct().count()

            total_late = late_employees + late_managers

            return Response({
                'late_arrivals_count': total_late
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'Internal Server Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AbsentCountAPIView(APIView):
    """
    API view to get the total count of absent employees and managers for the current day.
    """
    def get(self, request, *args, **kwargs):
        try:
            today = date.today()

            # Find the IDs of all employees and managers who have a recorded attendance for today.
            # Corrected: Use 'employee__employee_id' to get the primary key of the employee.
            present_staff_ids = Attendance.objects.filter(
                date=today
            ).values_list('employee__employee_id', flat=True)

            # Get the total count of all employees and managers.
            total_staff_count = Employee.objects.count()

            # The absent count is the total number of staff minus those who are present.
            present_staff_count = len(present_staff_ids)
            absent_count = abs(total_staff_count - present_staff_count)

            return Response({
                "absent_count": absent_count,
                "date": today.isoformat()
            })

        except Exception as e:
            # For debugging, it's good to print the actual error
            print(f"Error in AbsentCountAPIView: {e}")
            # Return a 500 error response to the client
            return Response({"error": "An internal server error occurred."}, status=500)
class AttendanceReportsAPIView(APIView):
    """
    API view to get attendance reports based on a time frame.
    Supports weekly, monthly, and custom date range reports.
    """
    def get(self, request, *args, **kwargs):
        # 1. Get and validate company_id
        company_id_str = request.query_params.get('company_id')
        if not company_id_str:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            company_id = int(company_id_str)
        except ValueError:
            return Response({"error": "Invalid company_id format."}, status=status.HTTP_400_BAD_REQUEST)
            
        # 2. Determine the date range based on report_type
        report_type = request.query_params.get('report_type')
        end_date = date.today()
        start_date = None

        if report_type == 'weekly':
            # Get the date of the previous Monday
            start_date = end_date - timedelta(days=end_date.weekday())
        elif report_type == 'monthly':
            # Get the first day of the current month
            start_date = end_date.replace(day=1)
        elif report_type == 'custom':
            # Get start and end dates from query parameters
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            if not start_date_str or not end_date_str:
                return Response({"error": "start_date and end_date are required for custom reports."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid or missing 'report_type'. Use 'weekly', 'monthly', or 'custom'."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Fetch attendance data for the calculated date range
        if start_date and end_date:
            # We filter all attendance records for the given company and date range.
            # Using F() to calculate working hours in the database
            attendance_records = Attendance.objects.filter(
                employee__company_id=company_id,
                date__range=[start_date, end_date]
            ).annotate(
                # Example of a calculation you could do
                working_hours=F('real_exit_time') - F('real_entry_time')
            ).select_related('employee')

            # 4. Serialize the data
            report_data = []
            for record in attendance_records:
                report_data.append({
                    "id": record.id,
                    "employee_name": record.employee.name,
                    "date": record.date,
                    "real_entry_time": record.real_entry_time,
                    "real_exit_time": record.real_exit_time,
                    "status": record.status, # Assuming you have a status field
                    # 'working_hours' might be a timedelta, convert to a string
                    "working_hours": str(record.working_hours) if record.working_hours else None
                })

            return Response(report_data, status=status.HTTP_200_OK)
        
        return Response({"error": "Could not determine report date range."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WeeklyAttendanceSummaryView(APIView):
    def get(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({"error": "Missing company_id"}, status=400)

        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        users_in_week = Attendance.objects.filter(
            company_id=company_id,
            date__range=(start_of_week, end_of_week)
        ).values('user_email', 'user_name', 'user_role').distinct()

        response_data = []

        for user in users_in_week:
            user_email = user['user_email']

            user_records = Attendance.objects.filter(
                company_id=company_id,
                user_email=user_email,
                date__range=(start_of_week, end_of_week)
            )

            present_records = user_records.filter(real_entry_time__isnull=False)

            days_present = present_records.count()
            late_count = present_records.filter(
                real_entry_time__gt=F('expected_entry_time')
            ).count()

            # Handle average entry and exit time safely
            total_entry_seconds = sum(
                t.real_entry_time.hour * 3600 + t.real_entry_time.minute * 60 + t.real_entry_time.second
                for t in present_records
                if t.real_entry_time
            )

            total_exit_seconds = sum(
                t.real_exit_time.hour * 3600 + t.real_exit_time.minute * 60 + t.real_exit_time.second
                for t in present_records
                if t.real_exit_time
            )

            try:
                avg_entry_seconds = total_entry_seconds // days_present
                avg_exit_seconds = total_exit_seconds // days_present

                avg_entry = (datetime.min + timedelta(seconds=avg_entry_seconds)).time().strftime("%I:%M %p")
                avg_exit = (datetime.min + timedelta(seconds=avg_exit_seconds)).time().strftime("%I:%M %p")
            except ZeroDivisionError:
                avg_entry = "N/A"
                avg_exit = "N/A"

            total_days_in_week = (end_of_week - start_of_week).days + 1
            days_absent = total_days_in_week - days_present

            response_data.append({
                "name": user['user_name'],
                "role": user['user_role'].capitalize(),
                "days_present": days_present,
                "days_absent": days_absent,
                "late": late_count,
                "avg_entry": avg_entry,
                "avg_exit": avg_exit,
            })

        return Response(response_data)
class DailyAttendanceRatioView(APIView):
    # If you want to restrict this to logged-in users only
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required"}, status=400)

        today = now().date()
        data = []

        for i in range(7):
            day = today - timedelta(days=i)

            # Count total employees/managers under this company
            total_users = Employee.objects.filter(company__id=company_id).count() + \
                          Manager.objects.filter(company__id=company_id).count()

            # Count present users for the day
            present_count = Attendance.objects.filter(date=day, company__id=company_id, status="Present").count()

            # Calculate ratio as percentage
            attendance_ratio = round((present_count / total_users) * 100, 2) if total_users > 0 else 0

            data.append({
                "date": day.strftime('%Y-%m-%d'),
                "ratio": attendance_ratio
            })

        # Reverse to keep oldest first (left to right in graph)
        data.reverse()

        return Response(data)

class DailyAttendanceRatioView(APIView):
    """
    Calculates the daily attendance ratio for the last 7 days.
    """
    def get(self, request):
        company_id = request.query_params.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # CORRECTED: Fetching total employees and managers for the specified company
            total_employees = Employee.objects.filter(company_id=company_id).count()
            total_managers = Manager.objects.filter(company_id=company_id).count()
            total_headcount = total_employees + total_managers
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        if total_headcount == 0:
            return Response({"error": "No employees or managers found for this company."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        date_range = [today - timedelta(days=i) for i in range(7)]

        data = []
        for day in reversed(date_range):
            present_count = Attendance.objects.filter(
                employee__company_id=company_id,
                date=day,
                real_entry_time__isnull=False
            ).count()

            attendance_ratio = (present_count / total_headcount) if total_headcount > 0 else 0

            data.append({
                "date": day.strftime('%Y-%m-%d'),
                "total_employees": total_headcount,
                "present_count": present_count,
                "attendance_ratio": attendance_ratio
            })

        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def daily_punctuality_ratio(request):
    company_id = request.GET.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'Company ID is required.'}, status=400)

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    date_list = [start_date + timedelta(days=i) for i in range(7)]

    results = []
    for date in date_list:
        # Filter attendance for the specific company and date
        attendance_for_day = Attendance.objects.filter(
            company_id=company_id,
            date=date
        )

        # Assuming an expected entry time of 9:00 AM for punctuality check
        # You can get this from a company settings model if available.
        on_time_threshold = time(9, 0, 0)

        # Calculate employee punctuality
        employees_on_day = attendance_for_day.filter(user_role='employee')
        employees_total = employees_on_day.count()
        employees_on_time = employees_on_day.filter(
            real_entry_time__lte=on_time_threshold
        ).count()
        employee_ratio = (employees_on_time / employees_total) if employees_total > 0 else 0

        # Calculate manager punctuality
        managers_on_day = attendance_for_day.filter(user_role='manager')
        managers_total = managers_on_day.count()
        managers_on_time = managers_on_day.filter(
            real_entry_time__lte=on_time_threshold
        ).count()
        manager_ratio = (managers_on_time / managers_total) if managers_total > 0 else 0

        results.append({
            'date': date,
            'employee_ratio': employee_ratio,
            'manager_ratio': manager_ratio,
        })

    return JsonResponse(results, safe=False)
@api_view(['GET'])
def export_weekly_attendance_pdf(request):
    company_id = request.GET.get('company_id')
    if not company_id:
        return HttpResponse("Company ID is required.", status=400)

    # Fetch the weekly attendance summary data (re-using the logic from your table)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    weekly_attendance = Attendance.objects.filter(
        company_id=company_id,
        date__range=[start_date, end_date]
    ).values('user_name', 'user_role').annotate(
        days_present=Count('date', filter=~Q(real_entry_time=None)),
        days_absent=Count('date', filter=Q(real_entry_time=None)),
        late=Count('date', filter=Q(real_entry_time__gt='09:00')), # Example
    )

    # Create the HTTP response with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="weekly_attendance_report_{end_date}.pdf"'

    # PDF generation using ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Weekly Attendance Report", styles['Title'])
    elements.append(title)
    elements.append(Paragraph(f"For the week ending: {end_date.strftime('%B %d, %Y')}", styles['Normal']))

    # Table data
    data = [['Name', 'Role', 'Days Present', 'Days Absent', 'Late']]
    for record in weekly_attendance:
        data.append([
            record['user_name'],
            record['user_role'],
            str(record['days_present']),
            str(record['days_absent']),
            str(record['late']),
        ])

    # Table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    # Create the table and add it to the elements
    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    # Build the PDF
    doc.build(elements)
    return response
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

def create_attendance_report(data):
    """
    Generates a PDF report with the same data and a similar layout as the React dashboard.

    Args:
        data (dict): A dictionary containing all the necessary dashboard data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch/2, leftMargin=inch/2,
                            topMargin=inch/2, bottomMargin=inch/2)

    styles = getSampleStyleSheet()
    elements = []

    # --- Header and Title ---
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, alignment=1, spaceAfter=20)
    elements.append(Paragraph("Weekly Attendance Report", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # --- Summary Cards (as a table) ---
    summary_data = [
        ["Total Hours", "On-Time Rate", "Employees Present", "Overtime Hours"],
        ["4,320", "92.4%", "88 / 95", "123.3"]
    ]
    summary_table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f8f9fa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dee2e6')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#dee2e6')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ])
    summary_table = Table(summary_data)
    summary_table.setStyle(summary_table_style)
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))

    # --- Weekly Attendance Summary Table ---
    elements.append(Paragraph("<b>Weekly Attendance Summary</b>", styles['h2']))
    elements.append(Spacer(1, 0.2*inch))
    
    table_data = [
        ['Name', 'Role', 'Days Present', 'Days Absent', 'Late', 'Avg. Entry', 'Avg. Exit']
    ]
    for item in data['attendance_summary']:
        table_data.append([
            item['name'],
            item['role'],
            str(item['days_present']),
            str(item['days_absent']),
            str(item['late']),
            item['avg_entry'],
            item['avg_exit']
        ])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E9ECEF')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ])
    
    summary_table = Table(table_data)
    summary_table.setStyle(table_style)
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))

    # --- Employee Status Pie Chart (using ReportLab graphics) ---
    elements.append(Paragraph("<b>Employee Status</b>", styles['h2']))
    elements.append(Spacer(1, 0.2*inch))
    
    total_present = sum(item['days_present'] for item in data['attendance_summary'])
    total_absent = sum(item['days_absent'] for item in data['attendance_summary'])
    total_late = sum(item['late'] for item in data['attendance_summary'])

    drawing = Drawing(400, 150)
    pie_chart = Pie()
    pie_chart.x = 50
    pie_chart.y = 10
    pie_chart.width = 100
    pie_chart.height = 100
    pie_chart.data = [total_present, total_late, total_absent]
    pie_chart.labels = ['Present', 'Late', 'Absent']
    pie_chart.slices[0].fillColor = colors.cyan
    pie_chart.slices[1].fillColor = colors.purple
    pie_chart.slices[2].fillColor = colors.lightpink
    pie_chart.slices.label_box_pos = 1.05
    drawing.add(pie_chart)
    
    # Add a legend
    legend_data = [(colors.cyan, 'Present'), (colors.purple, 'Late'), (colors.lightpink, 'Absent')]
    legend_text = []
    for color, label in legend_data:
        legend_text.append(Paragraph(f'<font color="{color.hex()}" size="10">■</font> {label}', styles['Normal']))
    
    legend_table = Table([[Paragraph(f'<font size="10">Present ({total_present})</font>', styles['Normal'])],
                          [Paragraph(f'<font size="10">Late ({total_late})</font>', styles['Normal'])],
                          [Paragraph(f'<font size="10">Absent ({total_absent})</font>', styles['Normal'])]])
    legend_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('LEFTPADDING', (0,0), (-1,-1), 120),
    ]))
    
    elements.append(legend_table)
    elements.append(drawing)
    elements.append(Spacer(1, 0.2*inch))
    
    # --- Build the document and return the buffer ---
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == '__main__':
    # This is an example of how you would call the function
    # In a real app, this data would come from your database
    mock_data = {
        'attendance_summary': [
            {'name': 'Jane Doe', 'role': 'Manager', 'days_present': 5, 'days_absent': 0, 'late': 1, 'avg_entry': '09:05', 'avg_exit': '17:02'},
            {'name': 'John Smith', 'role': 'Employee', 'days_present': 4, 'days_absent': 1, 'late': 2, 'avg_entry': '09:15', 'avg_exit': '17:10'},
            {'name': 'Peter Jones', 'role': 'Employee', 'days_present': 5, 'days_absent': 0, 'late': 0, 'avg_entry': '08:58', 'avg_exit': '17:05'},
            {'name': 'Sarah Lee', 'role': 'Employee', 'days_present': 3, 'days_absent': 2, 'late': 0, 'avg_entry': '09:01', 'avg_exit': '17:01'},
        ],
        'punctuality_ratio': [
            {'date': '2025-08-01', 'employee_ratio': 0.95, 'manager_ratio': 0.98},
            {'date': '2025-08-02', 'employee_ratio': 0.92, 'manager_ratio': 0.97},
        ]
    }
    
    pdf_content = create_attendance_report(mock_data)

    # Save the PDF to a file for demonstration
    with open('weekly_attendance_report.pdf', 'wb') as f:
        f.write(pdf_content)

    print("PDF generated successfully: weekly_attendance_report.pdf")
class AssignTaskView(APIView):
    def post(self, request):
        data = request.data
        try:
            title = data['title']
            description = data['description']
            start_date = data['start']
            end_date = data['end']
            assignees = data.get('team') or [data.get('assignee')]

            task = Task.objects.create(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                assigned_by=request.user  # or custom user
            )
            for name in assignees:
                employee = Employee.objects.get(name=name)
                task.assignees.add(employee)

            return Response({'message': 'Task assigned successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'User profile not found'}, status=404)

# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Employee, Manager

@require_http_methods(["GET"])
def personnel_list(request):
    """
    Fetches employees and managers for a given company ID.
    """
    company_id = request.GET.get('company_id')
    
    if not company_id:
        return JsonResponse({"error": "company_id query parameter is required"}, status=400)

    try:
        # Fetch data using the standard 'id' field
        employees = Employee.objects.filter(company_id=company_id).values("id", "name")
        managers = Manager.objects.filter(company_id=company_id).values("id", "name")

        # Use 'id' when creating the response dictionaries
        employees_list = [{"id": e["id"], "name": e["name"], "role": "Employee"} for e in employees]
        managers_list = [{"id": m["id"], "name": m["name"], "role": "Manager"} for m in managers]

        combined_list = sorted(employees_list + managers_list, key=lambda x: x["name"])

        return JsonResponse(combined_list, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
@require_http_methods(["POST"])
def assign_task(request):
    """
    Assigns a new task to selected individuals or a team.
    This version correctly handles existing employees and managers.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        title = data.get("title")
        description = data.get("description")
        
        start_date = parse_date(data.get("start"))
        end_date = parse_date(data.get("end"))
        assignee_names = data.get("assignees", []) # Correctly expecting "assignees" list

        if not start_date or not end_date:
            return JsonResponse({"error": "Start date and end date are required."}, status=400)

        # Create the task
        task = Task.objects.create(
            title=title,
            description=description or "",
            start_date=start_date,
            end_date=end_date,
            is_completed=False
        )

        # Find all employees and managers by name from the list
        employees_to_assign = Employee.objects.filter(name__in=assignee_names)
        managers_to_assign = Manager.objects.filter(name__in=assignee_names)

        # Assign the found objects to the task's ManyToManyFields
        task.assigned_employees.set(employees_to_assign)
        task.assigned_managers.set(managers_to_assign)

        return JsonResponse({"message": "Task assigned successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Company, Employee, Manager, Task, TaskAssignment # Make sure to import Task, TaskAssignment
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction

@csrf_exempt
@require_http_methods(["GET", "POST"])
def task_list(request):
    company_id_str = request.GET.get('company_id')
    if not company_id_str:
        return JsonResponse({"error": "company_id query parameter is required"}, status=400)

    try:
        company_id = int(company_id_str)
        company = Company.objects.get(company_id=company_id)
    except (ValueError, Company.DoesNotExist):
        return JsonResponse({"error": "Invalid or non-existent company_id"}, status=400)

    if request.method == 'GET':
        try:
            # CORRECTED: Filter tasks by the company foreign key
            tasks_queryset = Task.objects.filter(company=company).prefetch_related('assigned_employees', 'assigned_managers')
            
            task_list_data = []
            for task in tasks_queryset:
                assignee_names = list(task.assigned_employees.all().values_list('name', flat=True))
                assignee_names.extend(list(task.assigned_managers.all().values_list('name', flat=True)))
                
                task_list_data.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "start": task.start_date.isoformat() if task.start_date else None,
                    "end": task.end_date.isoformat() if task.end_date else None,
                    "is_completed": task.is_completed,
                    "assignees": assignee_names
                })
            return JsonResponse(task_list_data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            title = data.get("title")
            description = data.get("description")
            start_date_str = data.get("start")
            end_date_str = data.get("end")
            assignee_names = data.get("assignees", [])

            if not title or not start_date_str or not end_date_str:
                return JsonResponse({"error": "Title, start date, and end date are required."}, status=400)
            
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            with transaction.atomic():
                task = Task.objects.create(
                    company=company, # Pass the company instance
                    title=title,
                    description=description or "",
                    start_date=start_date,
                    end_date=end_date,
                    is_completed=False
                )

                employees_to_assign = Employee.objects.filter(name__in=assignee_names, company=company)
                managers_to_assign = Manager.objects.filter(name__in=assignee_names, company=company)
                
                # Check if any assignees were found
                if not employees_to_assign and not managers_to_assign:
                    return JsonResponse({"error": "No valid employees or managers found for assignment."}, status=400)

                # Use bulk_create for efficiency
                assignments = []
                for emp in employees_to_assign:
                    assignments.append(TaskAssignment(task=task, employee=emp))
                for mgr in managers_to_assign:
                    assignments.append(TaskAssignment(task=task, manager=mgr))

                if assignments:
                    TaskAssignment.objects.bulk_create(assignments)

            return JsonResponse({"message": "Task assigned successfully", "id": task.id}, status=201)
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
@csrf_exempt
@require_http_methods(["PATCH"])
def update_task_status(request, task_id):
    """
    Updates the completion status of a task.
    """
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body.decode("utf-8"))
        
        if 'is_completed' in data:
            task.is_completed = data['is_completed']
            task.save()
            return JsonResponse({"message": f"Task {task_id} status updated to {task.is_completed}"}, status=200)

        return JsonResponse({"error": "Invalid data provided. 'is_completed' field is required."}, status=400)

    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def task_dashboard_data(request):
    """
    This view should fetch real data from the database.
    """
    company_id = request.GET.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'Company ID is required'}, status=400)
    
    try:
        company = Company.objects.get(id=company_id)
        total_tasks = Task.objects.filter(company=company).count()
        completed_tasks = Task.objects.filter(company=company, is_completed=True).count()
        
        # Simple placeholder logic for pending/delayed
        pending_tasks = Task.objects.filter(company=company, is_completed=False, end_date__gte=date.today()).count()
        delayed_tasks = Task.objects.filter(company=company, is_completed=False, end_date__lt=date.today()).count()

        monthly_completion_data = {} # You would implement aggregation here
        
        response_data = {
            'summary': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'delayed_tasks': delayed_tasks,
            },
            'monthly_completion': [], # Placeholder for real data
            'status_ratio': {
                'completed': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                'pending': (pending_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                'delayed': (delayed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            }
        }
        return JsonResponse(response_data, safe=False)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_task_status(request, task_id):
    """
    Toggles the completion status of a task.
    """
    try:
        task = Task.objects.get(id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({"message": f"Task {task_id} status updated to {task.is_completed}"}, status=200)

    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, Company # Ensure you import your Company model
from .serializers import TaskSerializer

# myapp/views.py

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Company, Manager, Employee, Task, TaskAssignment
from .serializers import TaskSerializer  # Assuming you have this serializer

# ... (keep your other imports and views as they were, like PersonnelListView)

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Company, Manager, Employee, Task, TaskAssignment
from .serializers import TaskSerializer  # Ensure you have this serializer


# ... (keep other views)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Company, Manager, Employee, Task
from .serializers import TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (PATCH), and delete a single Task by pk.
    PATCH payload can include: title, description, start, end, assignees, is_completed
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        data = request.data or {}

        # Update simple fields
        title = data.get("title")
        description = data.get("description")
        start_date = data.get("start")
        end_date = data.get("end")
        is_completed = data.get("is_completed", None)
        assignees = data.get("assignees", None)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if start_date is not None:
            task.start_date = start_date
        if end_date is not None:
            task.end_date = end_date
        if is_completed is not None:
            task.is_completed = is_completed

        task.save()

        # Corrected: If assignees provided, replace M2M relationships
        if isinstance(assignees, list):
            # To handle the case where the company might not be attached to the task
            # (due to old data), we use the first available company.
            company = task.company
            if not company:
                try:
                    company = Company.objects.first()
                except Company.DoesNotExist:
                    return Response({"error": "No company found in the database."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Find all employees and managers that match the names in the assignees list
            employee_assignees = Employee.objects.filter(company=company, name__in=assignees)
            manager_assignees = Manager.objects.filter(company=company, name__in=assignees)

            # Set the new relationships using the set() method
            # This automatically clears the old ones and adds the new ones
            task.assigned_employees.set(employee_assignees)
            task.assigned_managers.set(manager_assignees)

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response

MOCK_TASK_DATA = {
    '1': {
        'total_tasks': 120,
        'completed_tasks': 95,
        'pending_tasks': 15,
        'delayed_tasks': 10,
        'monthly_completion': [
            {'month': 'Jan', 'tasks_completed': 10},
            {'month': 'Feb', 'tasks_completed': 15},
            {'month': 'Mar', 'tasks_completed': 20},
            {'month': 'Apr', 'tasks_completed': 25},
            {'month': 'May', 'tasks_completed': 25},
        ]
    },
    '6': {  # Data for the logged-in user's company
        'total_tasks': 55,
        'completed_tasks': 40,
        'pending_tasks': 10,
        'delayed_tasks': 5,
        'monthly_completion': [
            {'month': 'Jan', 'tasks_completed': 8},
            {'month': 'Feb', 'tasks_completed': 10},
            {'month': 'Mar', 'tasks_completed': 12},
            {'month': 'Apr', 'tasks_completed': 10},
            {'month': 'May', 'tasks_completed': 10},
        ]
    }
}

@require_http_methods(["GET"])
def task_dashboard_data(request):
    """
    Consolidated API endpoint for the task report dashboard.
    Returns summary, monthly completion, and status ratio data.
    """
    company_id = request.GET.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'Company ID is required'}, status=400)

    # Fetch data from the mock "database"
    task_data = MOCK_TASK_DATA.get(str(company_id), {})
    if not task_data:
        return JsonResponse({'error': 'No task data found for this company.'}, status=404)

    # Calculate status ratio for the doughnut chart
    total_tasks = task_data['total_tasks']
    status_ratio = {
        'completed': (task_data['completed_tasks'] / total_tasks) * 100 if total_tasks > 0 else 0,
        'pending': (task_data['pending_tasks'] / total_tasks) * 100 if total_tasks > 0 else 0,
        'delayed': (task_data['delayed_tasks'] / total_tasks) * 100 if total_tasks > 0 else 0,
    }

    # Prepare the final response
    response_data = {
        'summary': {
            'total_tasks': task_data['total_tasks'],
            'completed_tasks': task_data['completed_tasks'],
            'pending_tasks': task_data['pending_tasks'],
            'delayed_tasks': task_data['delayed_tasks'],
        },
        'monthly_completion': task_data['monthly_completion'],
        'status_ratio': status_ratio
    }

    return JsonResponse(response_data, safe=False)

class DashboardMeasurementsView(APIView):
    """
    API endpoint for the top-level measurement cards.
    """
    def get(self, request, company_id):
        data = {
            "total_spend": "₹55.5L",
            "spend_change": "+3.45%",
            "total_employees": "47,403",
            "employees_change": "-11.2%",
            "avg_punctuality": "95%",
            "punctuality_change": "+0.5%",
            "total_overtime": "2500 Hrs",
            "overtime_change": "+4.46%",
        }
        return Response(data)

class PunctualityGraphView(APIView):
    """
    API endpoint for the Punctuality Score doughnut chart.
    """
    def get(self, request, company_id):
        # Placeholder data
        data = {
            "labels": ["On-time", "Late", "Absent"],
            "values": [85, 10, 5],
            "colors": ["#4bc0c0", "#ff6384", "#ffcd56"]
        }
        return Response(data)

class OvertimeGraphView(APIView):
    """
    API endpoint for the Overtime Hours bar chart.
    """
    def get(self, request, company_id):
        # Placeholder data
        data = {
            "labels": ["John", "Jane", "Doe", "Smith", "Alice"],
            "values": [25, 18, 12, 15, 20],
        }
        return Response(data)
from datetime import timedelta
import pandas as pd
import numpy as np
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from sklearn.ensemble import RandomForestRegressor
from .models import Employee, Manager, Attendance

# your_project/your_app/views.py

# your_project/your_app/views.py

from datetime import timedelta
import pandas as pd
import numpy as np
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee, Manager, Attendance
from .punctuality_model import PunctualityPredictor

class PunctualityPredictionGraphView(APIView):
    def get(self, request, company_id):
        one_month_ago = timezone.now().date() - timedelta(days=30)
        employees = Employee.objects.filter(company_id=company_id)
        managers = Manager.objects.filter(company_id=company_id)

        predictor = PunctualityPredictor()
        df = predictor.prepare_data(employees, managers, one_month_ago)

        if df is None or df.empty:
            return Response({"graphData": {}, "sortedPunctualUsers": []})
        
        df = predictor.train_and_predict(df)
        
        df_sorted = df.sort_values(by="predicted_score", ascending=False)
        
        graph_labels = df_sorted["name"].tolist()
        graph_data = df_sorted["predicted_score"].tolist()

        response_data = {
            "graphData": {
                "labels": graph_labels,
                "datasets": [{
                    "label": "Predicted Punctuality Score (Next Month)",
                    "data": graph_data,
                    "backgroundColor": "rgba(54, 162, 235, 0.6)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1,
                }]
            },
            "sortedPunctualUsers": df_sorted[["name", "predicted_score", "role"]]
                .rename(columns={"predicted_score": "score"})
                .to_dict(orient="records"),
        }

        return Response(response_data)

class RecommendationView(APIView):
    def get(self, request, company_id):
        data = [
            {"employee_name": "Jane Doe", "text": "Outstanding punctuality and performance.", "type": "Bonus"},
            {"employee_name": "Alex Smith", "text": "Consistently high performance score.", "type": "Promotion"}
        ]
        return Response(data)

class RecommendationView(APIView):
    def get(self, request, company_id):
        data = [
            {"employee_name": "Jane Doe", "text": "Outstanding punctuality and performance.", "type": "Bonus"},
            {"employee_name": "Alex Smith", "text": "Consistently high performance score.", "type": "Promotion"}
        ]
        return Response(data)
from datetime import timedelta, datetime # 🚨 Add datetime here

# src/your_app_name/views.py

# your_project/your_app/views.py

import pandas as pd
import numpy as np
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Company
from .late_model import LatePredictor # 👈 Import the new class

class LatePredictionAPIView(APIView):
    def get(self, request, companyId, format=None):
        try:
            # 1. Fetch Company and Attendance Data
            company = get_object_or_404(Company, pk=companyId)
            today = timezone.now().date()
            one_month_ago = today - timedelta(days=30)

            attendance_records = Attendance.objects.filter(
                company=company,
                date__gte=one_month_ago,
                real_entry_time__isnull=False,
                expected_entry_time__isnull=False
            ).values()

            # 2. Initialize and use the LatePredictor
            predictor = LatePredictor()
            df = predictor.preprocess_data(attendance_records, today)

            if df is None:
                return Response({
                    "sortedLateUsers": [],
                    "graphData": {"labels": [], "datasets": [{"label": "Late Probability Score (%)", "data": []}]},
                    "message": "No attendance records found for this company in the last month."
                }, status=status.HTTP_200_OK)

            if not predictor.train_model(df):
                return Response({
                    "sortedLateUsers": [],
                    "graphData": {"labels": [], "datasets": [{"label": "Late Probability Score (%)", "data": []}]},
                    "message": "Not enough data to train the prediction model. Both late and on-time records are required."
                }, status=status.HTTP_200_OK)

            sorted_late_users = predictor.predict_future_lateness(df, today)

            # 3. Format the Final Response
            if not sorted_late_users:
                 return Response({
                    "sortedLateUsers": [],
                    "graphData": {"labels": [], "datasets": [{"label": "Late Probability Score (%)", "data": []}]},
                    "message": "No unique users found for prediction."
                }, status=status.HTTP_200_OK)


            graph_labels = [user['name'] for user in sorted_late_users]
            graph_data_points = [user['late_score'] for user in sorted_late_users]

            response_data = {
                'sortedLateUsers': sorted_late_users,
                'graphData': {
                    'labels': graph_labels,
                    'datasets': [
                        {
                            'label': 'Predicted Late Probability Score (%)',
                            'data': graph_data_points,
                        }
                    ]
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An unexpected error occurred in the LatePredictionAPIView: {e}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# src/your_app_name/views.py

import pandas as pd
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Company, Employee, Manager
from .absence_model import AbsentPredictor # 👈 Import the new class

class AbsentPredictionAPIView(APIView):
    def get(self, request, companyId):
        try:
            one_month_ago = timezone.now() - timedelta(days=30)
            
            attendance_records = Attendance.objects.filter(
                date__gte=one_month_ago,
                company_id=companyId
            ).values(
                "user_email", "user_name", "user_role", "date", "real_entry_time"
            )

            # Initialize the predictor
            predictor = AbsentPredictor()

            # Preprocess the data
            df = predictor.preprocess_data(attendance_records)

            if df is None:
                 return Response({
                    "message": "No attendance data available for this company in the last month.",
                    "graphData": {"labels": [], "datasets": [{"data": []}]},
                    "sortedAbsentUsers": []
                }, status=status.HTTP_200_OK)

            # Train the model
            if not predictor.train_model(df):
                return Response({
                    "message": "Not enough data to train the model. Need both absent and present records.",
                    "graphData": {"labels": [], "datasets": [{"data": []}]},
                    "sortedAbsentUsers": []
                }, status=status.HTTP_200_OK)

            # Make predictions
            predictions = predictor.predict_absence_probabilities(df)

            graph_labels = [user['name'] for user in predictions]
            graph_data = [user['absenceScore'] for user in predictions]

            response_data = {
                "message": "Prediction successful.",
                "graphData": {
                    'labels': graph_labels,
                    'datasets': [{
                        'label': 'Absence Prediction Score (%)',
                        'data': graph_data,
                        'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'borderWidth': 1,
                    }]
                },
                "sortedAbsentUsers": predictions,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An unexpected error occurred in the AbsentPredictionAPIView: {e}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# your_project/your_app/views.py

import pandas as pd
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Company 
from .overtime_model import OvertimePredictor # 👈 Import the new class

class OvertimePredictionAPIView(APIView):
    def get(self, request, companyId):
        try:
            one_month_ago = timezone.now() - timedelta(days=30)
            
            attendance_records = Attendance.objects.filter(
                date__gte=one_month_ago,
                company_id=companyId,
                real_exit_time__isnull=False,
                expected_exit_time__isnull=False
            ).values(
                "user_email", "user_name", "user_role", "date", "real_exit_time", "expected_exit_time"
            )
            
            predictor = OvertimePredictor()
            df = predictor.preprocess_data(attendance_records)

            if df is None:
                return Response({
                    "message": "No attendance data available for this company to predict overtime.",
                    "graphData": {"labels": [], "datasets": [{"data": []}]},
                    "sortedOvertimeUsers": []
                }, status=status.HTTP_200_OK)

            predictions = predictor.train_and_predict(df)

            if not predictions:
                return Response({
                    "message": "No overtime records found in the last month. Cannot predict.",
                    "graphData": {"labels": [], "datasets": [{"data": []}]},
                    "sortedOvertimeUsers": []
                }, status=status.HTTP_200_OK)

            graph_labels = [user['name'] for user in predictions]
            graph_data = [user['overtimeMinutes'] for user in predictions]

            response_data = {
                "message": "Total overtime prediction successful.",
                "graphData": {
                    'labels': graph_labels,
                    'datasets': [{
                        'label': 'Predicted Overtime (Minutes)',
                        'data': graph_data,
                        'backgroundColor': 'rgba(255, 159, 64, 0.6)',
                        'borderColor': 'rgba(255, 159, 64, 1)',
                        "borderWidth": 1,
                    }]
                },
                "sortedOvertimeUsers": predictions,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An unexpected error occurred in the OvertimePredictionAPIView: {e}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# your_project/your_app/views.py

import os
import joblib
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Import your models and other prediction views
from .models import Employee, Manager

# Get the absolute path to the current script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the model path by going one directory up to the project root
MODEL_PATH = os.path.join(BASE_DIR, "..", "bonus_prediction_model.joblib")

# --- Model Loading Logic ---
BONUS_MODEL = None
try:
    if os.path.exists(MODEL_PATH):
        BONUS_MODEL = joblib.load(MODEL_PATH)
        print("ML Bonus Prediction Model loaded successfully.")
    else:
        print(f"Error: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading ML model: {e}")

class AttendanceBonusPredictionAPIView(APIView):
    def get_user_email(self, name, company_id):
        try:
            employee = Employee.objects.get(name=name, company_id=company_id)
            return employee.email
        except Employee.DoesNotExist:
            try:
                manager = Manager.objects.get(name=name, company_id=company_id)
                return manager.email
            except Manager.DoesNotExist:
                return None

    def get_df_from_response(self, data, data_key, original_score_key, company_id):
        if not data or data_key not in data or not isinstance(data[data_key], list):
            return pd.DataFrame()

        df = pd.DataFrame(data[data_key])
        
        # Add this crucial check for an empty DataFrame
        if df.empty:
            return pd.DataFrame(columns=["user_email", original_score_key]) # Ensure empty DF has expected columns

        if "user_email" not in df.columns:
            if "name" in df.columns:
                df["user_email"] = df["name"].apply(lambda n: self.get_user_email(n, company_id))
                df = df.dropna(subset=["user_email"])
            else:
                return pd.DataFrame(columns=["user_email", original_score_key])

        if original_score_key not in df.columns:
            return pd.DataFrame(columns=["user_email", original_score_key])

        return df[["user_email", original_score_key]]

    def get(self, request, company_id):
        if BONUS_MODEL is None:
            return Response({"error": "ML model is not loaded. Please contact the administrator."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            employees = Employee.objects.filter(company_id=company_id)
            managers = Manager.objects.filter(company_id=company_id)

            master_users_data = []
            for emp in employees:
                master_users_data.append({"user_email": emp.email, "name": emp.name, "role": "Employee"})
            for mgr in managers:
                master_users_data.append({"user_email": mgr.email, "name": mgr.name, "role": "Manager"})

            master_df = pd.DataFrame(master_users_data).drop_duplicates(subset=["user_email"])

            if master_df.empty:
                return Response({"message": "No employee or manager data available for this company."},
                                status=status.HTTP_200_OK)

            punctuality_data = PunctualityPredictionGraphView().get(request, company_id).data
            late_data = LatePredictionAPIView().get(request, company_id).data
            absent_data = AbsentPredictionAPIView().get(request, company_id).data
            overtime_data = OvertimePredictionAPIView().get(request, company_id).data

            punctuality_df = self.get_df_from_response(punctuality_data, "sortedPunctualUsers", "score", company_id)
            late_df = self.get_df_from_response(late_data, "sortedLateUsers", "lateScore", company_id)
            absent_df = self.get_df_from_response(absent_data, "sortedAbsentUsers", "absenceScore", company_id)
            overtime_df = self.get_df_from_response(overtime_data, "sortedOvertimeUsers", "overtimeScore", company_id)

            combined_df = master_df.copy()
            
            combined_df = combined_df.merge(punctuality_df.rename(columns={"score": "punctuality_score"}), on="user_email", how="left")
            combined_df = combined_df.merge(late_df.rename(columns={"lateScore": "late_score"}), on="user_email", how="left")
            combined_df = combined_df.merge(absent_df.rename(columns={"absenceScore": "absent_score"}), on="user_email", how="left")
            combined_df = combined_df.merge(overtime_df.rename(columns={"overtimeScore": "overtime_score"}), on="user_email", how="left")

            combined_df = combined_df.fillna(50)

            # This is where your date parsing code is, in some helper function not shown here.
            # You need to find and update that code with the explicit format.
            # For example, if you have a function to calculate a score based on time,
            # you would update it like this:
            # combined_df['time_diff'] = pd.to_datetime(combined_df["real_entry_time"].astype(str), format="%H:%M:%S", errors="coerce") - pd.to_datetime(combined_df["expected_entry_time"].astype(str), format="%H:%M:%S", errors="coerce")


            features_for_prediction = combined_df[['punctuality_score', 'late_score', 'absent_score', 'overtime_score']]
            combined_df['bonus_score'] = BONUS_MODEL.predict(features_for_prediction)
            combined_df['bonus_score'] = combined_df['bonus_score'].clip(0, 100)

            sorted_df = combined_df.sort_values(by="bonus_score", ascending=False)
            bonus_list = sorted_df[["name", "role", "bonus_score"]].to_dict("records")

            graph_labels = sorted_df["name"].tolist()
            graph_data = sorted_df["bonus_score"].tolist()

            return Response({
                "message": "ML-based attendance bonus predictions generated successfully.",
                "bonus_list": bonus_list,
                "graphData": {
                    "labels": graph_labels,
                    "datasets": [{
                        "label": "Attendance Bonus Score (Out of 100)",
                        "data": graph_data,
                        "backgroundColor": "rgba(75, 192, 192, 0.6)",
                        "borderColor": "rgba(75, 192, 192, 1)",
                        "borderWidth": 1
                    }]
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in AttendanceBonusPredictionAPIView: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import status
from django.db.models import F
from datetime import date, timedelta
from django.db.models import Count, Q
from django.utils import timezone
import calendar

# Assume your models are imported like this
from .models import Employee,Attendance, Manager, Task 
# You will also have to import the Task model from your models.py

# Your other existing views go here...

# ... (imports remain the same)
class TaskStatusSummaryView(APIView):
    """
    API view to get a summary of task statuses (pending, ongoing, completed) for the company.
    """
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')

        if not company_id:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        today = date.today()

        # Query all tasks for the company, without a month filter
        all_company_tasks = Task.objects.filter(
            Q(assigned_employees__company_id=company_id) | Q(assigned_managers__company_id=company_id)
        ).distinct()

        # Calculate counts for each status
        completed_tasks = all_company_tasks.filter(is_completed=True).count()
        
        # A task is 'ongoing' if it has started but not yet completed
        ongoing_tasks = all_company_tasks.filter(
            is_completed=False,
            start_date__lte=today,
            end_date__gte=today
        ).count()

        # A task is 'pending' if it is not completed and its start date is in the future
        pending_tasks = all_company_tasks.filter(
            is_completed=False,
            end_date__lt=today
        ).count()
        
        data = {
            "pending": pending_tasks,
            "ongoing": ongoing_tasks,
            "completed": completed_tasks
        }
        
        return Response(data, status=status.HTTP_200_OK)
class AssignedTasksView(APIView):
    """
    API view to get a list of currently assigned (pending or ongoing) tasks.
    """
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')

        if not company_id:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get all tasks that are not yet completed
        uncompleted_tasks = Task.objects.filter(
            Q(assigned_employees__company_id=company_id) | Q(assigned_managers__company_id=company_id)
        ).filter(
            is_completed=False
        ).distinct()

        today = date.today()
        task_list = []

        for task in uncompleted_tasks:
            # Combine names of assigned employees and managers
            assigned_to = []
            assigned_to.extend([emp.name for emp in task.assigned_employees.all()])
            assigned_to.extend([mgr.name for mgr in task.assigned_managers.all()])
            
            # Determine status based on start date
            if task.start_date > today:
                status_text = "Pending"
            else:
                status_text = "Ongoing"

            task_list.append({
                "title": task.title,
                "assigned_to": ", ".join(assigned_to),  # Join names into a single string
                "status": status_text,
                "due_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else 'N/A'
            })

        return Response(task_list, status=status.HTTP_200_OK)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import Task # Assuming your Task model is in the same app
import calendar

class TaskCompletionMonthlyAggregationView(APIView):
    """
    API view to get the total number of tasks completed per month of the year,
    aggregated across all years for a specific company.
    """
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')

        if not company_id:
            return Response({"error": "company_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Query completed tasks for the given company_id and group by month number (1-12)
        monthly_counts_queryset = Task.objects.filter(
            company_id=company_id,
            is_completed=True
        ).annotate(
            month_number=ExtractMonth('end') # Changed 'end_date' to 'end' to match your form data
        ).values('month_number').annotate(
            completed_count=Count('id')
        ).order_by('month_number')

        # Create a dictionary to hold all 12 months, initialized to 0
        monthly_data = {
            i: {"month_name": calendar.month_name[i], "count": 0} for i in range(1, 13)
        }

        # Fill in the counts from the database query
        for item in monthly_counts_queryset:
            month_num = item['month_number']
            if month_num in monthly_data:
                monthly_data[month_num]['count'] = item['completed_count']

        # Convert the dictionary to a list of values for the frontend
        data = list(monthly_data.values())

        return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
def predict_task_completion(request):
    """
    Simulates task completion predictions based on mock data and simple rules.
    """
    company_id = request.query_params.get('company_id')
    if not company_id:
        return Response({"error": "Company ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    mock_tasks = [
        {"id": 1, "title": "Finalize Q3 Budget", "assigned_to": "Jane Doe", "due_date": "2025-10-15"},
        {"id": 2, "title": "Design new website landing page", "assigned_to": "Emily White", "due_date": "2025-08-20"},
        {"id": 3, "title": "Review marketing materials", "assigned_to": "John Smith", "due_date": "2025-09-01"},
    ]

    predictions = []
    for task in mock_tasks:
        prediction_status = get_mock_prediction(task['title'])
        predictions.append({
            "id": task['id'],
            "title": task['title'],
            "assigned_to": task['assigned_to'],
            "due_date": task['due_date'],
            "prediction": prediction_status
        })

    return Response(predictions)


@api_view(['GET'])
def predict_employee_task_capacity(request):
    """
    Simulates predicting which employee is capable of taking on more tasks.
    """
    company_id = request.query_params.get('company_id')
    if not company_id:
        return Response({"error": "Company ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    # Simulated prediction data
    capacity_predictions = [
        {"employee_name": "Sarah Johnson", "capacity_score": 95, "recommendation": "Ready for new tasks"},
        {"employee_name": "Mike Chen", "capacity_score": 75, "recommendation": "Monitor workload"},
        {"employee_name": "Emily Davis", "capacity_score": 88, "recommendation": "Ready for new tasks"},
    ]
    return Response(capacity_predictions)
import joblib

try:
    MODEL = joblib.load('task_completion_model.pkl')
    MODEL_FEATURES = joblib.load('model_features.pkl')
    print("Machine learning model loaded successfully.")
except FileNotFoundError:
    print("Warning: ML model files not found. Run train_model.py first.")
    MODEL = None
    MODEL_FEATURES = None
class TaskPredictionViewSet(viewsets.ViewSet):

    def predict_with_model(self, task):
        if not MODEL or not MODEL_FEATURES:
            return "On-Track" # Fallback if model isn't loaded

        # Prepare the data for the model
        task_data = {
            'assigned_experience': [task.assigned_experience],
            'duration_days': [(task.end_date - date.today()).days],
            'complexity': [task.complexity]
        }
        df = pd.DataFrame(task_data)
        
        # Preprocess the task data to match the training data format
        df_encoded = pd.get_dummies(df, columns=['complexity'], drop_first=True)
        
        # Ensure all columns from the training set are present, filling missing ones with 0
        df_final = df_encoded.reindex(columns=MODEL_FEATURES, fill_value=0)
        
        # Make the prediction
        prediction_result = MODEL.predict(df_final)[0]

        # Return a human-readable string based on the prediction
        if task.is_completed:
            return "Completed"
        
        if prediction_result == 1:
            return "On-Track"
        else:
            return "At Risk"

    def list(self, request):
        # This simulates fetching data for the last month from your Django models.
        # In a real project, you would query Task.objects.filter(start_date__gte=month_ago)
        mock_tasks = [
            Task(id=1, title="Finalize Q3 Budget", description="Annual budget finalization.", start_date=date(2025, 7, 1), end_date=date(2025, 9, 30), is_completed=False, complexity="High", assigned_experience=7),
            Task(id=2, title="Review marketing materials", description="Review all new marketing content.", start_date=date(2025, 8, 1), end_date=date(2025, 8, 25), is_completed=False, complexity="Low", assigned_experience=3),
            Task(id=3, title="Prepare client presentation", description="Create presentation for a new client.", start_date=date(2025, 8, 10), end_date=date(2025, 8, 20), is_completed=False, complexity="Medium", assigned_experience=5),
            Task(id=4, title="Team meeting notes", description="Write up notes from the last team meeting.", start_date=date(2025, 8, 18), end_date=date(2025, 8, 19), is_completed=False, complexity="Low", assigned_experience=1),
        ]
        
        tasks_with_predictions = []
        for task in mock_tasks:
            prediction = self.predict_with_model(task)
            serialized_task = TaskSerializer(task).data
            serialized_task['prediction'] = prediction
            tasks_with_predictions.append(serialized_task)

        return Response(tasks_with_predictions)
    


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Employee, Attendance, Company
from datetime import date
import json

# Placeholder functions for other views mentioned in the React code
def today(request):
    # This view would fetch attendance for all employees in a company
    # and return a JSON response.
    company_id = request.GET.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'Company ID is required'}, status=400)
    
    try:
        attendance_records = Attendance.objects.filter(company__company_id=company_id, date=date.today())
        # Format records into a list of dictionaries
        data = [{
            'id': record.attendance_id,
            'name': record.user_name,
            'employeeId': record.employee.employee_id if record.employee else None,
            'department': record.employee.position if record.employee else None,
            'expectedCheckInTime': record.expected_entry_time.strftime('%H:%M') if record.expected_entry_time else None,
            'checkInTime': record.real_entry_time.strftime('%H:%M') if record.real_entry_time else None,
            'expectedCheckOutTime': record.expected_exit_time.strftime('%H:%M') if record.expected_exit_time else None,
            'checkOutTime': record.real_exit_time.strftime('%H:%M') if record.real_exit_time else None,
            'totalHours': "N/A", # Logic to calculate this would go here
            'status': "Present" # Logic to determine status would go here
        } for record in attendance_records]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def employee_today(request):
    """
    Fetches the attendance record for a specific employee for the current day.
    Requires employee_id as a GET parameter.
    """
    employee_id = request.GET.get('employee_id')
    if not employee_id:
        return JsonResponse({'error': 'Employee ID is required'}, status=400)

    try:
        attendance_record = Attendance.objects.get(
            employee__employee_id=employee_id,
            date=date.today()
        )
        
        # Format the single record into a dictionary
        data = {
            'id': attendance_record.attendance_id,
            'name': attendance_record.user_name,
            'employeeId': attendance_record.employee.employee_id,
            'department': attendance_record.employee.position,
            'expectedCheckInTime': attendance_record.expected_entry_time.strftime('%H:%M') if attendance_record.expected_entry_time else None,
            'checkInTime': attendance_record.real_entry_time.strftime('%H:%M') if attendance_record.real_entry_time else None,
            'expectedCheckOutTime': attendance_record.expected_exit_time.strftime('%H:%M') if attendance_record.expected_exit_time else None,
            'checkOutTime': attendance_record.real_exit_time.strftime('%H:%M') if attendance_record.real_exit_time else None,
            'totalHours': "N/A", # Logic to calculate this would go here
            'status': "Present" # Logic to determine status would go here
        }
        return JsonResponse(data)
    except Attendance.DoesNotExist:
        return JsonResponse({'error': 'No attendance record found for today.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Other placeholder views for completeness
def present_count(request):
    # This view would count present employees for a company
    return JsonResponse({'present_count': 10, 'total_employees': 12})

def late_arrivals_count(request):
    # This view would count late arrivals
    return JsonResponse({'late_arrivals_count': 2})

def absent_count(request):
    # This view would count absent employees
    return JsonResponse({'absent_count': 0})

def particular_date(request):
    # This view would fetch attendance for a specific date
    return JsonResponse([], safe=False)

def export_pdf(request):
    # This view would generate and return a PDF file
    return HttpResponse(b"PDF content", content_type='application/pdf')
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from datetime import date, datetime
from .models import Attendance, Employee
from .serializers import AttendanceSerializer

class CompanyTodayAttendanceView(APIView):
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({"error": "Company ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        today = date.today()
        attendance_records = Attendance.objects.filter(
            date=today,
            employee__company_id=company_id
        ).select_related('employee')
        
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

class EmployeeTodayAttendanceView(APIView):
    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        today = date.today()
        try:
            attendance_record = Attendance.objects.get(
                date=today,
                employee_id=employee_id
            )
            serializer = AttendanceSerializer(attendance_record)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response({"error": "No attendance record found for today."}, status=status.HTTP_404_NOT_FOUND)

class AttendanceByDateView(APIView):
    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        date_str = request.query_params.get('date')

        if not company_id or not date_str:
            return Response({"error": "Company ID and date are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        attendance_records = Attendance.objects.filter(
            date=attendance_date,
            employee__company_id=company_id
        ).select_related('employee')
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

class EmployeeAttendanceByDateView(APIView):
    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee_id')
        date_str = request.query_params.get('date')

        if not employee_id or not date_str:
            return Response({"error": "Employee ID and date are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attendance_record = Attendance.objects.get(
                date=attendance_date,
                employee_id=employee_id
            )
            serializer = AttendanceSerializer(attendance_record)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response({"error": "No attendance record found for this date."}, status=status.HTTP_404_NOT_FOUND)

# Dashboard stats views
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

# ... other views and imports

# /Users/chandbhalodia/Documents/INDI_PRJ5 2/Backend/myapp/views.py
# In your Django app's views.py file
from django.db.models import Q
from rest_framework import generics
from .models import Task, TaskAssignment
from .serializers import TaskSerializer

class EmployeeTasksView(generics.ListAPIView):
    # This serializer will handle the conversion of Task objects to JSON
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Get the 'employee_id' from the URL query parameters (e.g., ?employee_id=123)
        employee_id = self.request.query_params.get('employee_id')
        
        # If no employee_id is provided, return an empty list of tasks
        if not employee_id:
            return Task.objects.none()

        # Filter tasks where the employee is either the assignee or the manager
        # Q objects allow for complex queries with OR conditions
        return Task.objects.filter(
            Q(taskassignment__employee_id=employee_id) | Q(taskassignment__manager_id=employee_id)
        ).prefetch_related(
            # Pre-fetch related data to avoid multiple database queries (improves performance)
            'taskassignment_set__employee', 
            'taskassignment_set__manager'
        ).distinct()
# Dashboard stats views
 # Use distinct to avoid duplicate tasks if an employee is both an assignee and manager for the same task


# In your Django app's views.py file
from django.db.models import Q
from rest_framework import generics
from .models import Task, TaskAssignment # Make sure TaskAssignment is imported
from .serializers import TaskSerializer

class EmployeeTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        employee_id = self.request.query_params.get('employee_id')
        if not employee_id:
            return Task.objects.none()

        # Ensure employee_id is integer
        try:
            employee_id = int(employee_id)
        except ValueError:
            return Task.objects.none()

        # Only filter by employees (not managers, since this is EmployeeTaskListView)
        return Task.objects.filter(
            taskassignment__employee_id=employee_id
        ).select_related(
            'company'
        ).prefetch_related(
            'taskassignment_set__employee'
        ).distinct().order_by('end_date')

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        employee_id = request.data.get('employee_id') # Pass the current user's employee_id

        try:
            # Update the individual employee's completion status on the task
            task_assignment = TaskAssignment.objects.get(task=task, employee__employee_id=employee_id)
            task_assignment.is_completed_by_employee = True
            task_assignment.save()

            # Check if all assigned employees have now completed the task
            all_assignments = TaskAssignment.objects.filter(task=task)
            if all(assignment.is_completed_by_employee for assignment in all_assignments):
                task.is_completed = True
                # You can also add completion notes here if needed
                task.save()
            
            # Return the updated task object
            return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)

        except TaskAssignment.DoesNotExist:
            return Response({"detail": "You are not assigned to this task."}, status=status.HTTP_403_FORBIDDEN)
# In your views.py, update the TaskCompletionView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task, TaskAssignment
from .serializers import TaskSerializer

class TaskCompletionView(APIView):

    def patch(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        
        employee_id = request.data.get('employee_id')
        manager_id = request.data.get('manager_id')
        completion_notes = request.data.get('completion_notes', '')

        if not employee_id and not manager_id:
            return Response({'error': 'Either employee_id or manager_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if employee_id:
                assignment = get_object_or_404(
                    TaskAssignment, 
                    task=task, 
                    employee__employee_id=employee_id
                )
            else:
                assignment = get_object_or_404(
                    TaskAssignment, 
                    task=task, 
                    manager__manager_id=manager_id
                )
        except TaskAssignment.DoesNotExist:
            return Response({'error': 'Task assignment not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        assignment.is_completed_by_user = True
        assignment.completion_notes = completion_notes
        assignment.save()

        all_assignments = TaskAssignment.objects.filter(task=task)
        all_completed = all(a.is_completed_by_user for a in all_assignments)

        if all_completed:
            task.is_completed = True
            task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Task, TaskAssignment
from .serializers import TaskSerializer
from django.db.models import F

class TaskWithPredictionView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Retrieve all tasks that are not yet completed
        return Task.objects.filter(is_completed=False).prefetch_related(
            'taskassignment_set__employee', 
            'taskassignment_set__manager'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Add a prediction to each task object
        data = serializer.data
        for task_data in data:
            # --- Simplified Prediction Logic ---
            # In a real-world application, this is where you would
            # use a trained ML model to predict task status.
            # This example uses a simple rule-based approach.
            
            end_date = task_data.get('end_date')
            if end_date:
                from datetime import date
                due_date = date.fromisoformat(end_date)
                today = date.today()
                days_to_go = (due_date - today).days

                # Example prediction logic:
                if days_to_go <= 0:
                    prediction = "Late"
                elif days_to_go < 7:
                    prediction = "At Risk"
                else:
                    prediction = "On-Track"
            else:
                prediction = "On-Track"
            
            task_data['prediction'] = prediction
            
            # Add a simplified assigned_to field
            assigned_names = []
            for assignment in task_data.get('assigned_employees_status', []):
                assigned_names.append(assignment.get('employee', {}).get('name'))
            for assignment in task_data.get('assigned_managers_status', []):
                assigned_names.append(assignment.get('manager', {}).get('name'))
            
            task_data['assigned_to'] = ", ".join(assigned_names)
            # ------------------------------------

        return Response(data, status=status.HTTP_200_OK)
# views.py (assuming you have your ML model and the necessary imports)
# your_project/your_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Employee, Manager, TaskAssignment
import joblib
import pandas as pd
import os

# Define the path to the model file
MODEL_PATH = 'bonus_prediction_model.pkl'

# Load the trained model once when the server starts
try:
    bonus_model = joblib.load(MODEL_PATH)
    print("Bonus prediction model loaded successfully.")
except FileNotFoundError:
    bonus_model = None
    print(f"Warning: {MODEL_PATH} not found. Please run the training script first.")
except Exception as e:
    bonus_model = None
    print(f"Error loading the model: {e}")

class BonusPredictionViewML(APIView):
    def get(self, request, user_type, user_id):
        if not bonus_model:
            return Response(
                {'error': 'Prediction model is not available.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            if user_type == 'employee':
                user = get_object_or_404(Employee, employee_id=user_id)
                is_manager_flag = 0
                tasks_filter = TaskAssignment.objects.filter(employee=user)
            elif user_type == 'manager':
                user = get_object_or_404(Manager, manager_id=user_id)
                is_manager_flag = 1
                tasks_filter = TaskAssignment.objects.filter(manager=user)
            else:
                return Response(
                    {'error': 'Invalid user type.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch user's performance metrics from the database
            total_tasks = tasks_filter.count()
            
            # Count tasks completed on or before the end date
            completed_on_time_tasks = tasks_filter.filter(
                is_completed_by_user=True,
                task__end_date__gte=F('completion_date')
            ).count()

            # Calculate on-time completion percentage
            on_time_percentage = (
                (completed_on_time_tasks / total_tasks) * 100
            ) if total_tasks > 0 else 0

            # Prepare data for prediction
            user_data = pd.DataFrame(
                [[total_tasks, on_time_percentage, is_manager_flag]],
                columns=['tasks_completed', 'on_time_percentage', 'is_manager']
            )

            # Make prediction using the ML model
            prediction = bonus_model.predict(user_data)
            prediction_text = "High chance of a bonus." if prediction[0] == 1 else "Low chance of a bonus."

            return Response({
                'user_name': user.name,
                'tasks_completed': total_tasks,
                'on_time_percentage': f"{on_time_percentage:.2f}%",
                'prediction': prediction_text
            }, status=status.HTTP_200_OK)

        except (Employee.DoesNotExist, Manager.DoesNotExist):
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from datetime import date, timedelta
from django.db.models import Count, Q, F, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Attendance, Employee, Company, TaskAssignment
from .serializers import (
    AttendanceSerializer,
    TaskSerializer,
    WeeklyAttendanceSummarySerializer,
    EmployeeTaskSerializer
)

class EmployeeWeeklyAttendanceSummaryView(APIView):
    """
    API view to get a single logged-in employee's weekly attendance summary.
    This view requires authentication and uses request.user to get the employee's data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            employee = request.user.employee  # Assuming a OneToOneField from User to Employee
        except Employee.DoesNotExist:
            return Response({'error': 'User is not a registered employee.'}, status=status.HTTP_404_NOT_FOUND)
        
        end_date = date.today()
        start_date = end_date - timedelta(days=6)
        total_days_in_week = 7 

        # Filter attendance records for the specific employee and date range
        records = Attendance.objects.filter(
            employee=employee,
            date__range=[start_date, end_date]
        )
        
        # Aggregate the data
        days_present = records.filter(real_entry_time__isnull=False).count()
        days_absent = total_days_in_week - days_present
        
        late_count = records.filter(
            real_entry_time__gt=F('expected_entry_time')
        ).count()

        avg_entry_time = records.aggregate(avg_entry=Avg('real_entry_time'))['avg_entry']
        avg_exit_time = records.aggregate(avg_exit=Avg('real_exit_time'))['avg_exit']
        
        summary_data = {
            'name': employee.name,
            'role': employee.position, # Assuming 'position' is the role
            'days_present': days_present,
            'days_absent': days_absent,
            'late': late_count,
            'avg_entry': avg_entry_time.strftime('%H:%M') if avg_entry_time else 'N/A',
            'avg_exit': avg_exit_time.strftime('%H:%M') if avg_exit_time else 'N/A',
        }
        
        serializer = WeeklyAttendanceSummarySerializer(summary_data)
        return Response(serializer.data)


class EmployeeDailyAttendanceRatioView(APIView):
    """
    Calculates and returns the daily attendance ratio for the logged-in employee's company.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            return Response({'error': 'User is not a registered employee.'}, status=status.HTTP_404_NOT_FOUND)
            
        company_id = employee.company.company_id
        end_date = date.today()
        start_date = end_date - timedelta(days=6)

        total_personnel = Employee.objects.filter(company_id=company_id).count() + \
                          Manager.objects.filter(company_id=company_id).count()

        if total_personnel == 0:
            return Response([])

        attendance_by_day = Attendance.objects.filter(
            company_id=company_id,
            date__range=[start_date, end_date],
            real_entry_time__isnull=False
        ).values('date').annotate(
            present_count=Count('date')
        ).order_by('date')

        chart_data = [
            {
                'date': item['date'].isoformat(),
                'attendance_ratio': round(item['present_count'] / total_personnel, 2)
            }
            for item in attendance_by_day
        ]

        return Response(chart_data)


class EmployeeDailyPunctualityRatioView(APIView):
    """
    A view to get daily punctuality ratios for the logged-in employee's company.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = request.user.employee
        except Employee.DoesNotExist:
            return Response({'error': 'User is not a registered employee.'}, status=status.HTTP_404_NOT_FOUND)
            
        company_id = employee.company.company_id
        end_date = date.today()
        start_date = end_date - timedelta(days=6)
        
        employee_punctuality_data = Attendance.objects.filter(
            company_id=company_id,
            user_role='employee',
            date__range=[start_date, end_date]
        ).values('date').annotate(
            on_time_count=Count('date', filter=Q(real_entry_time__lte=F('expected_entry_time'))),
            total_present=Count('date', filter=Q(real_entry_time__isnull=False)),
        ).order_by('date')
        
        manager_punctuality_data = Attendance.objects.filter(
            company_id=company_id,
            user_role='manager',
            date__range=[start_date, end_date]
        ).values('date').annotate(
            on_time_count=Count('date', filter=Q(real_entry_time__lte=F('expected_entry_time'))),
            total_present=Count('date', filter=Q(real_entry_time__isnull=False)),
        ).order_by('date')

        employee_ratios = {item['date'].isoformat(): item['on_time_count'] / item['total_present'] if item['total_present'] > 0 else 0 for item in employee_punctuality_data}
        manager_ratios = {item['date'].isoformat(): item['on_time_count'] / item['total_present'] if item['total_present'] > 0 else 0 for item in manager_punctuality_data}
        
        dates = [start_date + timedelta(days=i) for i in range(7)]
        
        chart_data = [
            {
                'date': d.isoformat(),
                'employee_ratio': employee_ratios.get(d.isoformat(), 0),
                'manager_ratio': manager_ratios.get(d.isoformat(), 0)
            } for d in dates
        ]
        
        return Response(chart_data)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta
from .models import Attendance

@api_view(['GET'])
def weekly_employee_summary_by_name(request):
    """
    Returns a weekly attendance summary for a single employee.
    Filters by company_id and employee_name.
    """
    company_id = request.query_params.get('company_id')
    employee_name = request.query_params.get('employee_name')

    if not company_id or not employee_name:
        return Response({"error": "company_id and employee_name are required"}, status=400)

    # Calculate the start date of the last 7 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    # Correct filter: company FK lookup
    attendance_records = Attendance.objects.filter(
        company__company_id=company_id,   # ✅ Correct lookup
        user_name__iexact=employee_name,  # Case-insensitive name match
        date__range=[start_date, end_date]
    ).select_related('employee')

    if not attendance_records.exists():
        return Response({"error": "No attendance records found for this employee in the last 7 days."}, status=404)

    # Days present = days with any record
    days_present = attendance_records.count()

    # Late = entry time later than expected
    late_count = attendance_records.filter(
        Q(real_entry_time__gt=F('expected_entry_time'))
    ).count()

    # Average entry time
    total_entry_seconds = sum(
        t.real_entry_time.hour * 3600 + t.real_entry_time.minute * 60 + t.real_entry_time.second
        for t in attendance_records if t.real_entry_time
    )
    avg_entry_seconds = total_entry_seconds // days_present if days_present > 0 else 0
    avg_entry = f"{avg_entry_seconds // 3600:02d}:{(avg_entry_seconds % 3600) // 60:02d}"

    # Average exit time
    total_exit_seconds = sum(
        t.real_exit_time.hour * 3600 + t.real_exit_time.minute * 60 + t.real_exit_time.second
        for t in attendance_records if t.real_exit_time
    )
    avg_exit_seconds = total_exit_seconds // days_present if days_present > 0 else 0
    avg_exit = f"{avg_exit_seconds // 3600:02d}:{(avg_exit_seconds % 3600) // 60:02d}"

    summary_data = {
        'name': employee_name,
        'role': 'employee',  # Could be fetched from Employee model if needed
        'days_present': days_present,
        'days_absent': 7 - days_present,
        'late': late_count,
        'avg_entry': avg_entry,
        'avg_exit': avg_exit,
    }

    return Response(summary_data, status=200)
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import Attendance

def get_user_attendance(request):
    company_id = request.GET.get("company_id")
    user_name = request.GET.get("user_name")

    if not company_id or not user_name:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    records = Attendance.objects.filter(
        company__company_id=company_id,
        user_name__iexact=user_name.strip(),
        date__gte=week_ago
    ).order_by("date")

    if not records.exists():
        return JsonResponse([], safe=False)

    data = [
        {
            "date": record.date.strftime("%Y-%m-%d"),
            "real_entry_time": record.real_entry_time.strftime("%H:%M") if record.real_entry_time else None,
            "real_exit_time": record.real_exit_time.strftime("%H:%M") if record.real_exit_time else None,
            "expected_entry_time": record.expected_entry_time.strftime("%H:%M") if record.expected_entry_time else None,
            "expected_exit_time": record.expected_exit_time.strftime("%H:%M") if record.expected_exit_time else None,
        }
        for record in records
    ]

    return JsonResponse(data, safe=False)
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Company, Manager, Employee, Task, TaskAssignment
from .serializers import TaskSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Company, Employee, Manager

class PersonnelListView(generics.ListAPIView):
    """
    API view to get a combined list of all employees and managers for a specific company.
    """

    def get(self, request, *args, **kwargs):
        company_id = self.request.query_params.get('company_id')
        if not company_id:
            return Response({"error": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(pk=int(company_id))

            employees = Employee.objects.filter(company=company)
            managers = Manager.objects.filter(company=company)

            employee_data = [
                {"id": emp.employee_id, "name": emp.name, "role": "employee"}
                for emp in employees
            ]
            manager_data = [
                {"id": mgr.manager_id, "name": mgr.name, "role": "manager"}
                for mgr in managers
            ]

            personnel_list = employee_data + manager_data
            return Response(personnel_list, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response({"error": "Company with this ID not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid company ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskListCreateView(APIView):
    """
    GET: list tasks filtered by company_id (query param).
    POST: create a task for the given company_id.
    Accepts payload shape:
    {
      title, description, start (YYYY-MM-DD), end (YYYY-MM-DD), assignees: [names], is_completed
    }
    """

    def get(self, request, *args, **kwargs):
        company_id = request.query_params.get("company_id")
        if company_id:
            # look up by your Company PK field (adjust if your Company PK is 'company_id')
            try:
                # If your Company model's pk field is 'company_id' use company_id field:
                company = Company.objects.get(company_id=company_id)
            except Company.DoesNotExist:
                return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

            qs = Task.objects.filter(company=company).order_by("-created_at")
        else:
            qs = Task.objects.all().order_by("-created_at")

        serializer = TaskSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company_id = request.query_params.get("company_id")
        if not company_id:
            return Response({"error": "company_id is required in query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch company instance safely
        try:
            company = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        # Parse JSON body (should already be parsed by DRF)
        data = request.data or {}
        title = data.get("title")
        description = data.get("description", "")
        start = data.get("start")  # expecting YYYY-MM-DD or empty
        end = data.get("end")
        assignees = data.get("assignees", []) or []
        is_completed = data.get("is_completed", False)

        if not title:
            return Response({"error": "title is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Build Task instance
        task = Task(
            title=title,
            description=description,
            is_completed=is_completed
        )

        # If your Task model has fields start_date / end_date use them; otherwise this will be ignored.
        # We attempt to set values if model has them
        if hasattr(task, "start_date") and start:
            task.start_date = start
        if hasattr(task, "end_date") and end:
            task.end_date = end

        # Assign company if model has company FK
        if hasattr(task, "company"):
            task.company = company

        # Save first to get an id, then set many-to-many
        task.save()

        # Map assignees (list of names) to Employee / Manager and add to M2M fields if present
        for name in assignees:
            # try Employee first
            try:
                emp = Employee.objects.filter(name=name, company=company).first()
                if emp and hasattr(task, "assigned_employees"):
                    task.assigned_employees.add(emp)
                    continue
            except Exception:
                pass

            # try Manager
            try:
                mgr = Manager.objects.filter(name=name, company=company).first()
                if mgr and hasattr(task, "assigned_managers"):
                    task.assigned_managers.add(mgr)
                    continue
            except Exception:
                pass

            # If not found, ignore silently (or you can log or store unassigned names)

        # Refresh from DB
        task.refresh_from_db()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (PATCH), and delete a single Task by pk.
    PATCH payload can include: title, description, start, end, assignees, is_completed
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        data = request.data or {}

        # Update simple fields
        title = data.get("title")
        description = data.get("description")
        start = data.get("start")
        end = data.get("end")
        is_completed = data.get("is_completed", None)
        assignees = data.get("assignees", None)  # if provided, we will replace M2M lists

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if hasattr(task, "start_date") and start is not None:
            task.start_date = start
        if hasattr(task, "end_date") and end is not None:
            task.end_date = end
        if is_completed is not None:
            task.is_completed = is_completed

        task.save()

        # If assignees provided, replace M2M relations
        if isinstance(assignees, list):
            # Clear existing
            if hasattr(task, "assigned_employees"):
                task.assigned_employees.clear()
            if hasattr(task, "assigned_managers"):
                task.assigned_managers.clear()

            # Re-add
            for name in assignees:
                emp = Employee.objects.filter(name=name, company=task.company).first() if hasattr(task, "company") else Employee.objects.filter(name=name).first()
                if emp and hasattr(task, "assigned_employees"):
                    task.assigned_employees.add(emp)
                    continue
                mgr = Manager.objects.filter(name=name, company=task.company).first() if hasattr(task, "company") else Manager.objects.filter(name=name).first()
                if mgr and hasattr(task, "assigned_managers"):
                    task.assigned_managers.add(mgr)
                    continue
                # otherwise ignore

        task.refresh_from_db()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Company
from .serializers import CompanySerializer

class CompanyDetailView(APIView):
    """
    API view to retrieve, update, or delete a single company instance.
    """
    def get_object(self, pk):
        """
        Helper method to get a Company object or raise a 404 error.
        """
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieves a company instance by its primary key.
        """
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Updates a company instance.
        """
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Employee, Manager, TaskAssignment
from .serializers import TaskSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, TaskAssignment, Employee, Manager

ogger = logging.getLogger(__name__)

@api_view(['GET'])
def get_employee_tasks(request):
    """
    Fetches all tasks assigned to a specific employee or manager by name.
    """
    employee_name = request.query_params.get('employee_name', None)
    company_id = request.query_params.get('company_id', None)

    if not employee_name or not company_id:
        return Response(
            {"error": "Employee name and company ID are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Find the employee or manager by name and company
        employee = Employee.objects.get(name__iexact=employee_name, company__company_id=company_id)
        # Fetch tasks assigned to this employee through the intermediate model
        assigned_tasks = TaskAssignment.objects.filter(employee=employee)

    except Employee.DoesNotExist:
        try:
            # If not an employee, check if they are a manager
            manager = Manager.objects.get(name__iexact=employee_name, company__company_id=company_id)
            # Fetch tasks assigned to this manager
            assigned_tasks = TaskAssignment.objects.filter(manager=manager)
        except Manager.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching employee tasks: {str(e)}")
        return Response(
            {"error": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    task_list = []
    for assignment in assigned_tasks:
        task = assignment.task
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'start_date': task.start_date,
            'end_date': task.end_date,
            'is_completed_by_user': assignment.is_completed_by_user,
        }
        task_list.append(task_data)

    return Response(task_list, status=status.HTTP_200_OK)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, TaskAssignment, Employee, Company
from .serializers import TaskSerializer

@api_view(['GET'])
def get_employee_tasks(request):
    employee_name = request.query_params.get('employee_name')
    company_id = request.query_params.get('company_id')

    if not employee_name or not company_id or company_id == "undefined":
        return Response({"error": "Employee name and valid company ID are required."}, status=400)

    try:
        employee = Employee.objects.get(name=employee_name, company_id=company_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found in this company."}, status=404)

    assignments = TaskAssignment.objects.filter(employee=employee).select_related('task')
    tasks = [a.task for a in assignments]

    serializer = TaskSerializer(tasks, many=True, context={"employee_name": employee_name})
    return Response(serializer.data, status=200)


@api_view(['PATCH'])
def update_task_status(request, task_id):
    employee_name = request.data.get("completed_by")
    if not employee_name:
        return Response({"error": "Employee name is required."}, status=400)

    try:
        assignment = TaskAssignment.objects.get(task_id=task_id, employee__name=employee_name)
    except TaskAssignment.DoesNotExist:
        return Response({"error": "Task assignment not found for this employee."}, status=404)

    new_status = request.data.get("is_completed_by_user")
    if new_status is not None:
        assignment.is_completed_by_user = new_status
        assignment.save()

    return Response({"message": "Task status updated successfully."}, status=200)
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task, Company
from .serializers import TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        # Get company_id from URL query parameters
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response(
                {"error": "company_id is required in the URL query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and save the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the Company instance
        company = get_object_or_404(Company, id=company_id)
        
        # Save the new Task object with the correct company instance
        self.perform_create(serializer, company=company)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        # Pass the company instance to the serializer's save method
        serializer.save(**kwargs)