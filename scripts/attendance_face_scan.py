import os
import django
import cv2
import face_recognition
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
django.setup()

from my_app.models import Employee, Attendance

known_encodings = []
known_ids = []

for emp in Employee.objects.exclude(face_image=''):
    img_path = emp.face_image.path
    image = face_recognition.load_image_file(img_path)
    enc = face_recognition.face_encodings(image)
    if enc:
        known_encodings.append(enc[0])
        known_ids.append(emp.id)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        if True in matches:
            idx = matches.index(True)
            emp = Employee.objects.get(id=known_ids[idx])
            today = datetime.today().date()
            now = datetime.now().time()
            att, _ = Attendance.objects.get_or_create(employee=emp, date=today)
            if not att.entry_time:
                att.entry_time = now
            else:
                att.exit_time = now
            att.save()
            print(f"Marked attendance for {emp.full_name}")

    cv2.imshow("Scanner", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Done 🎉
