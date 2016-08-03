import uuid
from django.db import models

class group(models.Model):
    uuid = models.CharField(max_length=20, default='custom_id', help_text='g', unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='')
    created = models.DateTimeField(auto_now_add=True, editable=False)

class user(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=20, default='enable')
    email = models.CharField(max_length=255, default='')
    language = models.CharField(max_length=30)
    timezone = models.CharField(max_length=30)
    group = models.ForeignKey('group', to_field='uuid', null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class token(models.Model):
    user = models.ForeignKey('user', to_field='user_id')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class openvpn_user(models.Model):
    name = models.CharField(max_length=20, unique=True)
    ou = models.CharField(max_length=20, default='My Organization')
    email = models.CharField(max_length=255, default='')
    ca = models.CharField(max_length=20)
    crt = models.CharField(max_length=20)
    key = models.CharField(max_length=20)
    ovpn = models.CharField(max_length=10240)
    created = models.DateTimeField(auto_now_add=True, editable=False)
