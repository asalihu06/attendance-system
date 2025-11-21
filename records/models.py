import os
from io import BytesIO
from datetime import time
from django.db import models
from django.core.files import File
from decouple import config
import qrcode
from PIL import Image

class Staff(models.Model):
    name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # USE BASE_URL from .env instead of hard coding
        base_url = config('BASE_URL')

        if not self.qr_code:
            qr_data = f"{base_url}/dashboard/mark/{self.staff_id}/"

            qr_img = qrcode.make(qr_data).convert("RGB")

            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            file_name = f"qr_{self.staff_id}.png"

            self.qr_code.save(file_name, File(buffer), save=False)
            buffer.close()

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.staff_id})"

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.staff.name} - {self.status}"
