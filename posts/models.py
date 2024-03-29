from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.

import misaka

from groups.models import Group


from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, relate_name='posts')
    created_at = models.DataTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwagrs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwagrs)

    def get_absolute_url(self):
        return reverse('posts:single', kwagrs={'username':self.user.username,
                                                'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_togeher = ['user','message']
