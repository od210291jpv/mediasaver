from django.db import models
from Home.settings import MEDIA_ROOT

# Create your models here.


class ImageFile(models.Model):

    class Meta(object):
        verbose_name = u'Image File'
        verbose_name_plural = u'Image Files'

    path = models.ImageField(
        upload_to='images',
        blank=False,
    )

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u'Image name'
    )

    category = models.CharField(
        max_length=256,
        blank=True,
        verbose_name = u'Category'
    )

    likes = models.IntegerField(
        blank=False,
        verbose_name=u'Likes amount',
        default=0
    )

    def __unicode__(self):
        return u'%s %s %s %s' % (self.path, self.name, self.category, self.likes)


class Category(models.Model):

    name = models.CharField(
        max_length=256,
        blank=True
    )
