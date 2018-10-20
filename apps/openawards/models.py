from django.db import models
from django.db.models.signals import pre_save, post_save, post_init
from apps.openawards.lib.utils import slugify_model
from apps.openawards.exceptions import EnrollNotValidException, NotValidVoteException, NotEnoughCreditsException
from apps.users.models import BaseUser
from django.contrib.auth import get_user_model
from constance import config
from django.utils import timezone
from django.db.models import Sum


# upload_to=lazy_upload_to('user.avatar/{0}/{1}')
def lazy_upload_to(str_to_format):
    def _path_to_upload(instance, filename):
        return str_to_format.format(instance.id, filename)
    return _path_to_upload


def upload_path(instance, filename):
    if isinstance(instance, User):
        return 'user.avatar/{0}/{1}'.format(instance.id, filename)
    elif isinstance(instance, Work):
        return 'work.cover/{0}/{1}'.format(instance.id, filename)
    elif isinstance(instance, Award):
        return 'award.image/{0}/{1}'.format(instance.id, filename)


class User(BaseUser):
    avatar = models.ImageField(null=True, upload_to=upload_path)

    def vote(self, work, award):
        if work.creator == self \
                or Vote.objects.filter(award=award, work=work, fan=self).first() is not None\
                or work not in award.works.all()\
                or not award.active:
            raise NotValidVoteException

        if not self.has_credits:
            raise NotEnoughCreditsException

        Vote(award=award, work=work, fan=self, voted_on=timezone.now()).save()

    @classmethod
    def post_save(cls, sender, instance, **kwargs):
        if kwargs['created'] and config.CREDITS_WHEN_CREATED > 0:
            CreditAcquisition(
                quantity=config.CREDITS_WHEN_CREATED,
                acquired_on=timezone.now(),
                acquired_by=instance
            ).save()

    @property
    def remain_credits(self):
        _v = self.credits.aggregate(Sum('quantity'))['quantity__sum']
        total_credits = 0 if _v is None else _v
        given_votes = self.votes.count()
        return total_credits - given_votes

    @property
    def has_credits(self):
        return self.remain_credits > 0

    def give_credits(self, quantity, source):
        CreditAcquisition(
            quantity=quantity,
            source=source,
            acquired_on=timezone.now(),
            acquired_by=self
        ).save()


class CreditAcquisition(models.Model):
    CREDIT_ACQUISITION_SOURCES = (
        ('C', 'Creation'),      # When user is created
        ('A', 'Admin'),         # When an admin adds credits
        ('P', 'PayPal'),         # When the user adds credits by PayPal platform
        ('D', 'Dev'),            # When the user get credits on development time
    )
    quantity = models.IntegerField()
    source = models.CharField(max_length=1, choices=CREDIT_ACQUISITION_SOURCES, default='C')
    acquired_on = models.DateTimeField(null=False, blank=False)
    acquired_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='credits')


class AdminCreditAcquisition(CreditAcquisition):
    giver = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    @classmethod
    def post_init(cls, sender, instance, **kwargs):
        instance.source = 'A'


class PayPalCreditAcquisition(CreditAcquisition):
    reference = models.CharField(max_length=200, blank=False, unique=True)

    @classmethod
    def post_init(cls, sender, instance, **kwargs):
        instance.source = 'P'


class License(models.Model):
    name = models.CharField(max_length=200, help_text="Find it in <a target='_blank' href='http://creativecommons.org'>creativecommons.org</a>", blank=False, unique=True)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    license = models.ForeignKey('License', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    cover = models.ImageField(null=True, blank=True, upload_to=upload_path)
    created = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='works')
    url = models.CharField(max_length=200, blank=False, unique=True)

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')


class Award(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a video title", unique=True)
    slug = models.CharField(max_length=100, unique=True)
    created = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to=upload_path)
    active = models.BooleanField(default=False)
    description = models.TextField()
    works = models.ManyToManyField(Work, blank=True, related_name='awards')
    starts_on = models.DateTimeField(null=True, blank=False)
    ends_on = models.DateTimeField(null=True, blank=False)
    winners = models.ManyToManyField(Work, blank=True, related_name='won_at')
    max_winners_position = models.IntegerField(default=3)

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

    def finish(self):
        pass


class Vote(models.Model):
    fan = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='votes')
    work = models.ForeignKey('Work', on_delete=models.CASCADE, null=False, related_name='votes')
    award = models.ForeignKey('Award', on_delete=models.CASCADE, null=False)
    voted_on = models.DateTimeField(null=True, blank=False)


pre_save.connect(Award.pre_save, sender=Award)
pre_save.connect(Work.pre_save, sender=Work)
post_save.connect(User.post_save, sender=User)
post_init.connect(PayPalCreditAcquisition.post_init, sender=PayPalCreditAcquisition)
post_init.connect(AdminCreditAcquisition.post_init, sender=AdminCreditAcquisition)
