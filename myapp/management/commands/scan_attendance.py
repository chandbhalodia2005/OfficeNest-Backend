from django.core.management.base import BaseCommand
from scripts.attendance_face_scan import scan_and_mark_attendance

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        scan_and_mark_attendance()
