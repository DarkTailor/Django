import os, random
from django.db import models
from django.utils import timezone



def filename_ext(filepath):
    file_base = os.path.basename(filepath)
    filename, ext = os.path.splitext(file_base)
    return filename, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9498594795)
    name, ext = filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "pictures/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Events(models.Model):
    Event = models.CharField(max_length=255)
    Date = models.DateField(default=timezone.now)
    Time = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.name


