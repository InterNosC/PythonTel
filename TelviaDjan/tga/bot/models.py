from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='user ID',
    )
    name = models.TextField(
        verbose_name='username',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'


class Message(models.Model):
    profile = models.ForeignKey(
        to='bot.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text'
    )
    created_at = models.DateTimeField(
        verbose_name='Time:',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Msg {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Messages'
