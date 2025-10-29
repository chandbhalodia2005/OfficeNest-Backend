from rest_framework import serializers
from .models import Company, Manager, Employee,Attendance,Task
from django.contrib.auth.hashers import make_password, check_password # Added check_password for internal debug
from rest_framework.exceptions import ValidationError
# ------------------------- Company Serializers -------------------------

class CompanySignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id', 'companyName', 'email', 'phone', 'city', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print(f"CompanySignupSerializer: Raw password received: {validated_data.get('password')}")
        if validated_data.get('password'):
            raw_password = validated_data['password']
            validated_data['password'] = make_password(raw_password)
            print(f"CompanySignupSerializer: Hashed password created: {validated_data['password']}")
            # Optional: Verify the hash right after creation
            if not check_password(raw_password, validated_data['password']):
                print("CompanySignupSerializer: !!! ERROR - Hashed password does not match raw password immediately after hashing !!!")
        return Company.objects.create(**validated_data)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

# ------------------------- Employee Serializer -------------------------

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'
#         extra_kwargs = {
#             'password': {'write_only': True, 'required': False},
#             'manager': {'required': False, 'allow_null': True},
#             'face_image': {'required': False, 'allow_null': True},
#         }
#         read_only_fields = ['date_joined']

#     def to_internal_value(self, data):
#         # Normalize time fields to HH:MM:SS
#         if data.get('shift_start') and len(data['shift_start']) == 5:
#             data['shift_start'] += ':00'
#         if data.get('shift_end') and len(data['shift_end']) == 5:
#             data['shift_end'] += ':00'
#         return super().to_internal_value(data)

#     # def create(self, validated_data):
#     #     raw_password = validated_data.pop('password')
#     #     validated_data['password'] = make_password(raw_password)
#     #     print(f"EmployeeSerializer: Raw password received: {raw_password}")
#     #     print(f"EmployeeSerializer: Hashed password created: {validated_data['password']}")
#     #     return Employee.objects.create(**validated_data)
#     def create(self, validated_data):
#         company_id = validated_data.pop('company_id') # Get company_id from validated data
#         try:
#             company_instance = Company.objects.get(pk=company_id)
#         except Company.DoesNotExist:
#             raise serializers.ValidationError({"company_id": "Company with this ID does not exist."})

#         # The 'company' field should be set here if not automatically handled by model relations
#         # and if it's not already in validated_data from a different field.
#         employee = Employee.objects.create(company=company_instance, **validated_data)
#         return employee
# ------------------------- Manager Serializer -------------------------

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Manager, Company

class ManagerSerializer(serializers.ModelSerializer):
    # This is a write-only field for accepting the company ID on create/update
    company_id = serializers.IntegerField(write_only=True, required=True)

    # Use to get a Manager's company, but not for creating a company object
    company = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Manager
        fields = [
            'manager_id', 'name', 'email', 'phone', 'address',
            'gender', 'date_of_birth', 'date_joined', 'salary',
            'shift_start', 'shift_end', 'company', 'company_id',
            'face_image'
        ]
        extra_kwargs = {
            # Make password write-only for security (this is just an example, as password is not in fields)
            'password': {'write_only': True},
            # Allow face_image to be optional and writable
            'face_image': {'required': False, 'allow_null': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'date_joined': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        company_id = validated_data.pop('company_id', None)
        # Note: face_image is automatically in validated_data if a file was uploaded
        # and the serializer is correctly configured. No need to pop it explicitly.

        if company_id is None:
            raise ValidationError({"company_id": "Company ID is required for manager creation."})

        try:
            company_instance = Company.objects.get(company_id=company_id)
        except Company.DoesNotExist:
            raise ValidationError({"company_id": "Company with this ID does not exist."})

        # Add the company instance to the validated data
        validated_data['company'] = company_instance

        # Use the parent create method which handles all validated data and saves the model
        return super().create(validated_data)

    def update(self, instance, validated_data):
        company_id = validated_data.pop('company_id', None)
        if company_id is not None:
            try:
                company_instance = Company.objects.get(company_id=company_id)
                instance.company = company_instance
            except Company.DoesNotExist:
                raise ValidationError({"company_id": "Company with this ID does not exist."})

        # The super() update method handles all other fields, including face_image
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        # This method is for customizing the output format, e.g., for the face_image URL
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance.face_image and request:
            ret['face_image'] = request.build_absolute_uri(instance.face_image.url)
        return ret
# class EmployeeSerializer(serializers.ModelSerializer):
#     # Use WriteOnlyField for company_id if you only want to receive it and not send it back
#     # company_id is sent by frontend, and we map it to the 'company' ForeignKey
#     company_id = serializers.IntegerField(write_only=True) 

#     # Manager field handling:
#     # Option 1: Expect manager ID as integer (most common for foreign keys)
#     # If the manager is optional and you want to accept an empty string or null
#     # from the frontend, then `allow_null=True` and `required=False` are important.
#     manager = serializers.PrimaryKeyRelatedField(
#         queryset=Manager.objects.all(), 
#         allow_null=True, 
#         required=False # Allow manager field to be optional
#     )

#     # If you want to include manager details when GETting an employee, 
#     # you can define a read-only field:
#     # manager_details = ManagerSerializer(source='manager', read_only=True)

#     class Meta:
#         model = Employee
#         fields = '__all__' # Include all fields from the model
#         # Alternatively, list them explicitly including 'company' and 'manager':
#         # fields = [
#         #     'id', 'name', 'email', 'phone', 'address', 'position', 'gender',
#         #     'date_of_birth', 'date_joined', 'salary', 'shift_start', 'shift_end',
#         #     'department', 'manager', 'face_image', 'company_id', # company_id for writing
#         #     # 'manager_details' # if using manager_details for reading
#         # ]

#     # Custom create method to handle the company_id field
#     def create(self, validated_data):
#         company_id = validated_data.pop('company_id')
#         try:
#             company_instance = Company.objects.get(pk=company_id)
#         except Company.DoesNotExist:
#             raise serializers.ValidationError({"company_id": "Company with this ID does not exist."})
        
#         # Now save the employee, linking it to the found company instance
#         employee = Employee.objects.create(company=company_instance, **validated_data)
#         return employee
#     def to_internal_value(self, data):
#         # Normalize time fields to HH:MM:SS
#         if data.get('shift_start') and len(data['shift_start']) == 5:
#             data['shift_start'] += ':00'
#         if data.get('shift_end') and len(data['shift_end']) == 5:
#             data['shift_end'] += ':00'
#         return super().to_internal_value(data)

#     # Optional: Custom validation for manager, if you want to handle specific string inputs like "null"
#     def validate_manager(self, value):
#         # The PrimaryKeyRelatedField generally handles 'None' for null.
#         # If your frontend sends a string "null" and you want to convert it to actual None,
#         # you might do it in the frontend's FormData preparation, or here if necessary.
#         # But with PrimaryKeyRelatedField(allow_null=True, required=False), 
#         # an empty string or absence should lead to None.
#         if value is None or value == '': # Handle empty string from frontend as None
#             return None
#         return value

#     # You might also want to ensure manager belongs to the same company
#     def validate(self, data):
#         company_id = data.get('company_id')
#         manager = data.get('manager')

#         if company_id and manager:
#             # Check if the manager belongs to the specified company
#             if manager.company_id != company_id:
#                 raise serializers.ValidationError(
#                     {"manager": "Manager does not belong to the specified company."}
#                 )
#         return data
class EmployeeSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True, required=True) # Set required=True for creation

    company = serializers.PrimaryKeyRelatedField(read_only=True) # This will output the company's PK (company_id)

    manager = serializers.PrimaryKeyRelatedField(
        queryset=Manager.objects.all(),
        allow_null=True,
        required=False
    )

    date_of_birth = serializers.DateField( format="%Y-%m-%d", read_only=True)
    date_joined = serializers.DateField(format="%Y-%m-%d", read_only=True)

    face_image= serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'employee_id', # *** CRITICAL FIX: Use employee_id here ***
            'name', 'email', 'phone', 'address', 'position',
            'gender', 'date_of_birth', 'date_joined', 'salary', 'shift_start', 'shift_end',
            'company', 'company_id', 'manager', 'face_image'
        ]

        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'allow_null': True, 'allow_blank': True},
            'date_of_birth': {'write_only': True, 'required': False, 'allow_null': True},
            'date_joined': {'write_only': True, 'required': False, 'allow_null': True},
            'face_image': {'write_only': True, 'required': False, 'allow_null': True} # This is the actual model field
        }

    face_image= serializers.SerializerMethodField()

    def get_face_image(self, obj):
        if obj.face_image and hasattr(obj.face_image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.face_image.url)
            return obj.face_image.url
        return None
    def to_internal_value(self, data):
        data = data.copy()

        if 'shift_start' in data and data['shift_start']:
            if len(data['shift_start']) == 5:
                data['shift_start'] += ':00'
        if 'shift_end' in data and data['shift_end']:
            if len(data['shift_end']) == 5:
                data['shift_end'] += ':00'

        if 'manager' in data and data['manager'] == '':
            data['manager'] = None

        if 'date_of_birth' in data:
            if data['date_of_birth'] == '':
                data['date_of_birth'] = None
            if data['date_of_birth'] is not None:
                data['date_of_birth'] = data.pop('date_of_birth')

        if 'date_joined' in data:
            if data['date_joined'] == '':
                data['date_joined'] = None
            if data['date_joined'] is not None:
                data['date_joined'] = data.pop('date_joined')
        
        # Mapping `face_image` from incoming data to the `face_image` model field
        # The MultiPartParser will put the file directly into request.data['face_image']
        # if the input field is named 'face_image'.
        # If your frontend is sending it as `face_image`, it will be processed directly.
        # If frontend sends `face_image_idx` and you mapped it to `face_image` in view, that's fine too.
        # Ensure the model field is `face_image`.
        if 'face_image' in data:
            pass # Let DRF handle the file. It will map to the model field `face_image` due to Meta.fields `face_image`.

        return super().to_internal_value(data)

    def create(self, validated_data):
        company_id = validated_data.pop('company_id', None)
        manager_instance = validated_data.pop('manager', None)
        password = validated_data.pop('password', None)
        face_image= validated_data.pop('face_image', None) # Pop the file object

        if company_id is None:
            raise ValidationError({"company_id": "Company ID is required for employee creation."})

        try:
            company_instance = Company.objects.get(company_id=company_id) # Use company_id for lookup
        except Company.DoesNotExist:
            raise ValidationError({"company_id": "Company with this ID does not exist."})

        employee = Employee(
            company=company_instance,
            manager=manager_instance,
            face_image=face_image, # Assign the file directly
            **validated_data
        )

        if password:
            employee.set_password(password)
        elif self.context.get('default_password_for_new_employees'):
            employee.set_password(self.context['default_password_for_new_employees'])

        employee.save()
        return employee

    def update(self, instance, validated_data):
        company_id = validated_data.pop('company_id', None)
        if company_id is not None:
            try:
                company_instance = Company.objects.get(company_id=company_id)
                instance.company = company_instance
            except Company.DoesNotExist:
                raise ValidationError({"company_id": "Company with this ID does not exist."})

        manager_instance = validated_data.pop('manager', None)
        instance.manager = manager_instance

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        if 'face_image' in validated_data:
            instance.face_image= validated_data.pop('face_image')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate_manager(self, value):
        return value

    def validate(self, data):
        company_id_for_validation = data.get('company_id')
        manager_instance = data.get('manager')

        if company_id_for_validation and manager_instance:
            if manager_instance.company.company_id != company_id_for_validation: # Ensure manager's company_id matches
                raise ValidationError(
                    {"manager": "Manager does not belong to the specified company."}
                )
        return data
from rest_framework import serializers
from .models import Attendance, Employee, Manager, Company
from datetime import datetime
class AttendanceSerializer(serializers.ModelSerializer):
    # Add 'totalHours' to the fields list
    totalHours = serializers.SerializerMethodField()
    employeeId = serializers.CharField(source='employee.employee_id', read_only=True)
    name = serializers.CharField(source='user_name', read_only=True)
    department = serializers.CharField(source='employee.position', read_only=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'attendance_id',
            'employeeId',
            'name',
            'department',
            'status',
            'date',
            'expected_entry_time',
            'expected_exit_time',
            'real_entry_time',
            'real_exit_time',
            'totalHours' # This is the field causing the error, now it's defined
        ]

    # This method calculates the total hours
    def get_totalHours(self, obj):
        if obj.real_entry_time and obj.real_exit_time:
            # Create datetime objects for calculation
            entry_datetime = datetime.combine(obj.date, obj.real_entry_time)
            exit_datetime = datetime.combine(obj.date, obj.real_exit_time)
            
            # Calculate the time difference
            time_difference = exit_datetime - entry_datetime
            
            # Convert to hours and minutes
            total_seconds = time_difference.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            
            return f"{hours}h {minutes}m"
        return "N/A"

    def get_status(self, obj):
        # A more robust status logic can be implemented here based on your business rules
        if obj.real_entry_time and obj.real_exit_time:
            return "Present"
        if obj.real_entry_time and not obj.real_exit_time:
            return "Present (In-progress)"
        return "Absent"
from rest_framework.permissions import AllowAny # Import AllowAny



# In your serializers.py filefrom rest_framework import serializers
from .models import Task, TaskAssignment, Employee, Manager



# /Users/chandbhalodia/Documents/INDI_PRJ5 2/Backend/myapp/serializers.py

from rest_framework import serializers
from .models import Task, TaskAssignment, Employee, Manager

class TaskSerializer(serializers.ModelSerializer):
    assigned_employees_status = serializers.SerializerMethodField()
    assigned_managers_status = serializers.SerializerMethodField()
    def get_is_completed_by_user(self, obj):
        employee_name = self.context.get("employee_name")
        assignment = TaskAssignment.objects.filter(task=obj, employee__name=employee_name).first()
        return assignment.is_completed_by_user if assignment else False
    def get_assigned_employees_status(self, obj):
        assignments = TaskAssignment.objects.filter(task=obj, employee__isnull=False)
        return [
            {
                # Assuming 'employee_id' is the primary key and 'name' is a field
                'employee': {'id': a.employee.employee_id, 'name': a.employee.name},
                'is_completed_by_employee': a.is_completed_by_user,
                'completion_notes': a.completion_notes,
            }
            for a in assignments
        ]
    def get_assignees(self, obj):
        assigned_names = []
        for assignment in TaskAssignment.objects.filter(task=obj):
            if assignment.employee:
                assigned_names.append(assignment.employee.name)
            elif assignment.manager:
                assigned_names.append(assignment.manager.name)
        return list(set(assigned_names))  
    def get_assigned_managers_status(self, obj):
        assignments = TaskAssignment.objects.filter(task=obj, manager__isnull=False)
        return [
            {
                # Assuming 'manager_id' is the primary key and 'name' is a field
                'manager': {'id': a.manager.manager_id, 'name': a.manager.name},
                'is_completed_by_employee': a.is_completed_by_user,
                'completion_notes': a.completion_notes,
            }
            for a in assignments
        ]
        
    def update(self, instance, validated_data):
        # Your existing update logic for the task
        instance = super().update(instance, validated_data)

        # Check for the completion of all assignees
        total_employees = instance.assigned_employees.count()
        total_managers = instance.assigned_managers.count()
        total_assignees = total_employees + total_managers
        
        # Count assignments for this task that are marked as completed
        completed_assignees = TaskAssignment.objects.filter(
            task=instance,
            is_completed_by_user=True
        ).count()

        # Update the task's overall completion status
        if total_assignees > 0 and completed_assignees == total_assignees:
            instance.is_completed = True
        else:
            instance.is_completed = False
            
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = '__all__'
from rest_framework import serializers
from .models import TaskAssignment, Employee, Manager, Task

class TaskAssignmentSerializer(serializers.ModelSerializer):
    # This field is used to display the employee's name in the serializer output
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    # This field is used to display the task's title in the serializer output
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = TaskAssignment
        fields = [
            'id', 
            'task', 
            'employee', 
            'manager', 
            'employee_name', 
            'task_title',
            'is_completed_by_user', 
            'completion_notes'
        ]
        # These fields are read-only and cannot be updated via the serializer
        read_only_fields = ['is_completed_by_user', 'completion_notes']

    def update(self, instance, validated_data):
        """
        Custom update method to handle partial updates of the TaskAssignment.
        """
        # Ensure that only specific fields can be updated via the API
        instance.is_completed_by_user = validated_data.get('is_completed_by_user', instance.is_completed_by_user)
        instance.completion_notes = validated_data.get('completion_notes', instance.completion_notes)
        instance.save()
        return instance
class WeeklyAttendanceSummarySerializer(serializers.Serializer):
    """
    Serializer for the aggregated weekly attendance data, not a direct model.
    """
    name = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=20)
    days_present = serializers.IntegerField()
    days_absent = serializers.IntegerField()
    late = serializers.IntegerField()
    avg_entry = serializers.CharField(max_length=50, default='N/A')
    avg_exit = serializers.CharField(max_length=50, default='N/A')
class EmployeeTaskSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source='task.title')
    description = serializers.CharField(source='task.description')
    start_date = serializers.DateField(source='task.start_date')
    end_date = serializers.DateField(source='task.end_date')
    is_completed = serializers.BooleanField(source='task.is_completed')
    
    class Meta:
        model = TaskAssignment
        fields = ['task', 'description', 'start_date', 'end_date', 'is_completed', 'is_completed_by_user', 'completion_notes']
from rest_framework import serializers

class TaskBonusPredictionSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=200)
    user_type = serializers.CharField(max_length=50)
    task_title = serializers.CharField(max_length=200)
    is_completed_by_user = serializers.BooleanField()
    predicted_bonus = serializers.FloatField()
from rest_framework import serializers

from rest_framework import serializers

class OverallBonusPredictionSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=200)
    user_type = serializers.CharField(max_length=50)
    total_tasks_completed = serializers.IntegerField()
    total_tasks_assigned = serializers.IntegerField()
    predicted_total_bonus = serializers.FloatField()
