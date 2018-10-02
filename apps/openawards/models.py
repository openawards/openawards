from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from apps.openawards.lib.utils import slugify_model


class License(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", blank=False, unique=True)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    license = models.ForeignKey('License', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    cover = models.ImageField(null=True)
    created = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


@receiver(pre_save, sender=Work)
def work_pre_save(sender, instance, *args, **kwargs):
    slugify_model(instance, 'title')


class Award(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", unique=True)
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
def award_pre_save(sender, instance, *args, **kwargs):
    slugify_model(instance, 'name')


class Vote(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    work = models.ForeignKey('Work', on_delete=models.CASCADE, null=False)
    award = models.ForeignKey('Award', on_delete=models.CASCADE, null=False)
