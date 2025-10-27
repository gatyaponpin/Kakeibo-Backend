from django.db import models

class TimeStampedSoftDelete(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True

class UserGroup(TimeStampedSoftDelete):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=256)
    class Meta:
        db_table = "user_groups"

class User(TimeStampedSoftDelete):
    id = models.AutoField(primary_key=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    username = models.CharField(max_length=100)
    class Meta:
        db_table = "users"
        indexes = [models.Index(fields=["email"])]