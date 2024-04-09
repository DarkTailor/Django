import os, random
from django.db import models


def filename_ext(filepath):
    file_base = os.path.basename(filepath)
    filename, ext = os.path.splitext(file_base)
    return filename, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9498594795)
    name, ext = filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "pictures/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Donations(models.Model):
    DONATION_TYPES = [
        ('T', 'Tithes'),
        ('OG', 'Other Givings'),
    ]

    type = models.CharField(max_length=2, choices=DONATION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # Automatically set the date to the current date
    description = models.TextField()

    def __str__(self):
        return f"{self.get_type_display()} Donation - {self.amount}"







