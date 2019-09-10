from _datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Choice(models.Model):
    tv_name = models.CharField(verbose_name='Имя', max_length=255)
    tv_price = models.FloatField()

    class Meta:
        verbose_name = 'Каналы'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return "{}".format(self.tv_name)


class Post(models.Model):
    text = models.TextField()
    complete = models.BooleanField(default=False)
    order_date = models.DateTimeField(default=datetime.now)
    post_dates = models.CharField(max_length=255)
    quantity_symbols = models.PositiveIntegerField(null=True, blank=True)
    quantity_days = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE, related_name="posts")
    reception = models.BooleanField(default=False, )
    choice = models.ForeignKey(Choice, related_name='posts', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = 'Обьявления'
        verbose_name_plural = 'Обьявления'

    def __str__(self):
        return '{}{}{}'.format(self.text, self.order_date, self.quantity_symbols, )


@receiver(pre_save, sender=Post)
def total_price(sender, instance, **kwargs):
    try:
        str_text = instance.text.replace(" ", "")
        instance.quantity_days = len(instance.post_dates.split(','))
        instance.total_price = (len(str_text) * instance.choice.tv_price) * instance.quantity_days
        instance.quantity_symbols = len(str_text)
    except:
        raise ValidationError('Choise is null')




