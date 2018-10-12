from django.db import models
from django.db.models.signals import pre_save
from apps.openawards.lib.utils import slugify_model
from apps.openawards.exceptions import EnrollNotValidException, NotValidVoteException
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, null=False, unique=True)

    def vote(self, work, award):
        if work.creator == self \
                or Vote.objects.filter(award=award, work=work, fan=self).first() is not None\
                or work not in award.works.all()\
                or not award.active:
            raise NotValidVoteException
        Vote(award=award, work=work, fan=self).save()


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
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')


class Award(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", unique=True)
    slug = models.CharField(max_length=100, unique=True)
    created = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True)
    active = models.BooleanField(default=False)
    description = models.TextField()
    works = models.ManyToManyField(Work)

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'name')

    def get_absolute_url(self):
        # return reverse('award-detail', args=[str(self.slug)])
        pass

    def __str__(self):
        return self.name

    def enroll_work(self, work):
        if not self.active or work in self.works.all():
            raise EnrollNotValidException()
        self.works.add(work)
        self.save()


class Vote(models.Model):
    fan = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    work = models.ForeignKey('Work', on_delete=models.CASCADE, null=False)
    award = models.ForeignKey('Award', on_delete=models.CASCADE, null=False)


pre_save.connect(Award.pre_save, sender=Award)
pre_save.connect(Work.pre_save, sender=Work)
