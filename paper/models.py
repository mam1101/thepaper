import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

WORD_LIST_DIR = 'words_alpha.txt'


def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)


class PaperItemManager(models.Manager):

    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]


class PaperItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(blank=True)
    body = models.TextField()
    published = models.BooleanField(default=False)
    last_saved = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)

    objects = PaperItemManager()

    class Meta:
        verbose_name = 'Paper Item'
        verbose_name_plural = 'Paper Items'

    def save(self, *args, **kwargs):
        if not self.pk:
            cancel = False
            slug_str = ''
            while not cancel:
                slug = []
                for i in range(0, 3):
                    slug.append(random_line(WORD_LIST_DIR))
                slug_str = '-'.join(slug)
                if not PaperItem.objects.filter(slug=slug_str).exists():
                    cancel = True
            self.slug = slug_str
        super(PaperItem, self).save(*args, **kwargs)


class PaperSubscription(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscription = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subscription')
