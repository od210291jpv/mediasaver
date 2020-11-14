from django.db import models
from Home.settings import MEDIA_ROOT

# Create your models here.


class UserAccount(models.Model):

    name = models.CharField(
        blank=False,
        max_length=30,
        verbose_name=u'UserAccount name'
    )

    avatar = models.ImageField(
        blank=True,
        upload_to='images'
    )

    def __str__(self):
        return "%s %s" % (self.name, self.avatar)


class Category(models.Model):

    name = models.CharField(
        max_length=256,
        blank=True
    )

    def __unicode__(self):
        return u'%s' % (self.name)


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

    likes = models.IntegerField(
        blank=False,
        verbose_name=u'Likes amount',
        default=0
    )

    publisher = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=u'Publisher'
    )

    favorite = models.ManyToManyField(
        UserAccount,
        related_name=u'Fav',
        # on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=u'Is favorite'
    )

    category = models.ManyToManyField(
        Category,
        related_name=u'Category',
        blank=True,
        null=True,
        verbose_name=u'Image category'
    )

    def __unicode__(self):
        return u'%s %s %s %s' % (self.path, self.name, self.likes, self.category)



