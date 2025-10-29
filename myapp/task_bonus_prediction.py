from django.db import models
from yourproject.tasks.models import TaskAssignment # Adjust the import path as needed
from yourproject.employees.models import Employee # Assuming these models are in 'employees'
from yourproject.employees.models import Manager # Assuming these models are in 'employees'

class TaskBonus(models.Model):
    task_assignment = models.OneToOneField(
        TaskAssignment,
        on_delete=models.CASCADE,
        related_name='bonus',
        help_text="The task assignment for which the bonus is predicted."
    )
    predicted_bonus_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The predicted bonus amount."
    )
    is_awarded = models.BooleanField(
        default=False,
        help_text="Whether the bonus has been officially awarded."
    )
    awarded_date = models.DateField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bonus for {self.task_assignment.task.title}"