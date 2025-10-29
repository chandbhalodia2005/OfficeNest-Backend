from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Company, Employee, Manager, Attendance  # Replace myapp with your actual app name

class Command(BaseCommand):
    help = 'Populates daily attendance records for all employees and managers in all companies.'

    def handle(self, *args, **kwargs):
        today = timezone.localdate()  # Get today's date

        self.stdout.write(f"Starting daily attendance population for {today}...")

        companies = Company.objects.all()
        if not companies.exists():
            self.stdout.write(self.style.WARNING("No companies found. Skipping attendance population."))
            return

        for company in companies:
            self.stdout.write(f"\nProcessing company: {company.companyName} (ID: {company.company_id})")

            # ------------------ Employees ------------------
            employees = Employee.objects.filter(company=company)
            if not employees.exists():
                self.stdout.write(f"  No employees found for {company.companyName}.")
            for employee in employees:
                if not Attendance.objects.filter(
                    company=company,
                    employee=employee,
                    date=today
                ).exists():
                    Attendance.objects.create(
                        company=company,
                        employee=employee,
                        user_email=employee.email,
                        user_name=employee.name,
                        user_role='employee',
                        date=today,
                        expected_entry_time=employee.shift_start,  # ✅ now being saved
                        expected_exit_time=employee.shift_end,      # ✅ now being saved
                        real_entry_time=None,
                        real_exit_time=None
                    )
                    self.stdout.write(f"  ✅ Created attendance for employee: {employee.name}")
                else:
                    self.stdout.write(f"  ⚠️ Attendance already exists for employee: {employee.name}")

            # ------------------ Managers ------------------
            managers = Manager.objects.filter(company=company)
            if not managers.exists():
                self.stdout.write(f"  No managers found for {company.companyName}.")
            for manager in managers:
                if not Attendance.objects.filter(
                    company=company,
                    manager=manager,
                    date=today
                ).exists():
                    Attendance.objects.create(
                        company=company,
                        manager=manager,
                        user_email=manager.email,
                        user_name=manager.name,
                        user_role='manager',
                        date=today,
                        expected_entry_time=manager.shift_start,  # ✅ now being saved
                        expected_exit_time=manager.shift_end,      # ✅ now being saved
                        real_entry_time=None,
                        real_exit_time=None
                    )
                    self.stdout.write(f"  ✅ Created attendance for manager: {manager.name}")
                else:
                    self.stdout.write(f"  ⚠️ Attendance already exists for manager: {manager.name}")

        self.stdout.write(self.style.SUCCESS("\n✅ Daily attendance population completed."))
