from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User


class License(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", blank=False, unique=True)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    license = models.ForeignKey('License', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    cover = models.ImageField(null=True)
    created = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Award(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", unique=True)
    # TODO: Non editable in admin
    slug = models.CharField(max_length=100, unique=True)
    created = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True)
    active = models.BooleanField(default=False)
    description = models.TextField()

    def get_absolute_url(self):
        # return reverse('award-detail', args=[str(self.slug)])
        pass

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Award)
def video_pre_save(sender, instance, *args, **kwargs):
    # TODO: Ensure there is a proper procedure if repeated when assigned
    instance.slug = slugify(instance.title)


class Vote(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    work = models.ForeignKey('Work', on_delete=models.CASCADE, null=False)
    award = models.ForeignKey('Award', on_delete=models.CASCADE, null=False)
