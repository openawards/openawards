# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/
from django.core.management.base import BaseCommand, CommandError

from openawards.models import User, License, Work, Award, Vote

import random, time, string

class Command(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'
    #TODO: Check that it's actually development and not production environment.

    def handle(self, *args, **options):
        #TODO: Use get_or_create() for the licenses, to prevent the duplicated index exception?
        reg = License(name="Attribution 2.0 Generic (CC BY 2.0)",
                      link="https://creativecommons.org/licenses/by/2.0/")
        reg.save()
        reg = License(name="Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
                      link="https://creativecommons.org/licenses/by-sa/4.0/")
        reg.save()
        reg = License(name="Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
                      link="https://creativecommons.org/licenses/by-nc/4.0/")
        reg.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'License'))

        reg = Award(name="Animated shorts award",
                    created=strTimeProp(prop=random.random()), active=True,
                    description=random_string_generator(random.randint(50,500), True))
        reg.save()
        reg = Award(name="Open Music Best Album",
                    created=strTimeProp(prop=random.random()), active=True,
                    description=random_string_generator(random.randint(50,500), True))
        reg.save()
        reg = Award(name="Fiction Novel Collective Culture Award",
                    created=strTimeProp(prop=random.random()), active=True,
                    description=random_string_generator(random.randint(50,500), True))
        reg.save()
        reg = Award(name="Essay and Academic Open Knowledge Award",
                    created=strTimeProp(prop=random.random()), active=True,
                    description=random_string_generator(random.randint(50,500), True))
        reg.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Awards'))

        for x in range(200):
            reg = User(username=random_string_generator(random.randint(5,15)), email="hola@codi.coop",
                       password="test", first_name=random_string_generator(random.randint(5,10)),
                       last_name=random_string_generator(random.randint(5,10)))
            reg.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Users'))

        for x in range(50):
            reg = Work(title=random_string_generator(random.randint(5,15), True),
                       license=License.objects.order_by('?').first(),
                       description=random_string_generator(random.randint(200,2000), True),
                       created=strTimeProp(prop=random.random()),
                       creator=User.objects.order_by('?').first())
            reg.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Works'))

        for award in Award.objects.order_by("id").all():
            if award.id == 1:
                for x in range(1, 12):
                    award.enroll_work(work=x)
            elif award.id == 2:
                for x in range(13, 24):
                    award.enroll_work(work=x)
            elif award.id == 3:
                for x in range(25, 36):
                    award.enroll_work(work=x)
            elif award.id == 4:
                for x in range(37, 50):
                    award.enroll_work(work=x)
        self.stdout.write(self.style.SUCCESS('Works enrolled to corresponding awards.'))

        for user in User.objects.order_by("id").all():
            # Randomly deciding how many votes this user will cast
            for x in range(random.randint(5,30)):
                # Going through all 50 works…
                for w in range(1,50):
                    # …and randomly making this user vote to 25% of them.
                    if random.randint(0,3) == 3:
                        #TODO: Trying to loop through all the Awards that this Work is enrolled at, but failing!
                        work = Work.objects.get(id=w)
                        for enrolled_award in work.award_set.all():
                            user.vote(work=work, award=enrolled_award)
        self.stdout.write(self.style.SUCCESS('All users voted to random works, in every award this work is enrolled.'))


def random_string_generator(size=10, with_space=False, chars=string.ascii_lowercase + string.digits):
    if with_space:
        chars += " "
    return ''.join(random.choice(chars) for _ in range(size))

def strTimeProp(prop, format='%Y-%m-%d', start="2018-01-01", end="2018-12-30",):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))