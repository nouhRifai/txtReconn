from django.db import models


def upload_path(instance, filename):
    return "/".join(['images', str(instance.title), filename])


class awsimage(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)