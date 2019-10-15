from django.db import models
from django.db.models.signals import pre_save, post_save, post_init
from apps.openawards.lib.utils import slugify_model
from apps.openawards.exceptions import EnrollNotValidException, NotValidVoteException, NotEnoughCreditsException,\
    CouponAlreadyExchangedException
from apps.users.models import BaseUser
from apps.users.managers import CCUserManager
from django.contrib.auth import get_user_model
from constance import config
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import reverse
from uuid import uuid4
import datetime


# upload_to=lazy_upload_to('user.avatar/{0}/{1}')
def lazy_upload_to(str_to_format):
    def _path_to_upload(instance, filename):
        return str_to_format.format(instance.id, filename)
    return _path_to_upload


def upload_path(instance, filename):
    """
    When you add a cover to a new work or award, it does not have an id yet. The url would take None as id
    so it won't overwrite the previous image and the new one won't take effect.
    """
    if isinstance(instance, User):
        return 'user.avatar/{0}/avatar.png'.format(instance.username, filename)
    elif isinstance(instance, Work):
        return 'work.cover/{0}/cover.png'.format(str(uuid4()), filename)
    elif isinstance(instance, Award):
        return 'award.image/{0}/image.png'.format(str(uuid4()), filename)


class User(BaseUser):
    avatar = models.ImageField(null=True, upload_to=upload_path, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()
    username = models.CharField(unique=False, max_length=255)

    def vote(self, work, award):
        if work.creator == self \
                or Vote.objects.filter(award=award, work=work, fan=self).first() is not None\
                or work not in award.works.all()\
                or not award.active\
                or award.starts_on > timezone.now()\
                or award.ends_on < timezone.now():
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

    @property
    def full_name(self):
        return self.get_full_name() if self.get_full_name() else self.username

    @property
    def profile_url(self):
        return reverse('profile', args=[str(self.username)])


class CreditAcquisition(models.Model):
    CREDIT_ACQUISITION_SOURCES = (
        ('C', 'Creation'),      # When user is created
        ('A', 'Admin'),         # When an admin adds credits
        ('P', 'PayPal'),         # When the user adds credits by PayPal platform
        ('D', 'Dev'),            # When the user get credits on development time
        ('O', 'Coupon'),         # When it comes from exchanging a coupon code.
        ('R', 'Vote received'),  # When it comes one of your works being voted.
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
    name = models.CharField(
        max_length=200,
        help_text="Find it in <a target='_blank' href='http://creativecommons.org'>creativecommons.org</a>",
        blank=False,
        unique=True
    )
    url = models.CharField(max_length=200)

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
    AUTHORSHIP_CHOICES = [('Y', config.WORK_AUTHORSHIP_YES),
               ('N', config.WORK_AUTHORSHIP_NO),
               ('M', config.WORK_AUTHORSHIP_MAYBE)]
    authorship = models.CharField(choices=AUTHORSHIP_CHOICES, max_length=1, null=False, blank=False)

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    def __str__(self):
        return self.title

    @property
    def absolute_url(self):
        return reverse('work', args=[str(self.slug)])

    @property
    def current_awards(self):
        return [award for award in self.awards.all() if award.active and award.current]

    def can_be_voted(self, user, award):
        return self.votes.filter(fan=user, award=award).first() is None


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

    @property
    def absolute_url(self):
        return reverse('award', args=[str(self.slug)])

    def __str__(self):
        return self.name

    def enroll_work(self, work):
        if not self.active or work in self.works.all():
            raise EnrollNotValidException()
        self.works.add(work)
        self.save()

    def finish(self):
        pass

    @property
    def current(self):
        return True if self.starts_on < timezone.now() < self.ends_on else False


class Vote(models.Model):
    class Meta:
        ordering = ['-voted_on']

    fan = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name='votes')
    work = models.ForeignKey('Work', on_delete=models.CASCADE, null=False, related_name='votes')
    award = models.ForeignKey('Award', on_delete=models.CASCADE, null=False)
    voted_on = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        return f"Vote by {self.fan} for the work '{self.work}' in the award '{self.award}', casted: {self.voted_on}"


class CouponCampaign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    campaign = models.ForeignKey(CouponCampaign, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    exchanged = models.BooleanField()
    date_created = models.DateTimeField("created on", auto_now_add=True)
    date_exchanged = models.DateTimeField("exchanged on", null=True, blank=True)
    code = models.CharField(max_length=36, default=uuid4, editable=False)

    def __str__(self):
        return str(self.code)

    def exchange(self):
        if self.exchanged is True:
            raise CouponAlreadyExchangedException()
        self.exchanged = True
        self.date_exchanged = datetime.datetime.now()
        self.save()
        self.user.give_credits(round(self.price), 'O')


pre_save.connect(Award.pre_save, sender=Award)
pre_save.connect(Work.pre_save, sender=Work)
post_save.connect(User.post_save, sender=User)
post_init.connect(PayPalCreditAcquisition.post_init, sender=PayPalCreditAcquisition)
post_init.connect(AdminCreditAcquisition.post_init, sender=AdminCreditAcquisition)
