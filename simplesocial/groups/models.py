from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

import misaka # For using markdown in the description

from django.contrib.auth import get_user_model
User = get_user_model()

# Allows us to use related names for foreign keys
from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="GroupMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) # Removes spaces and lowercases
        self.description_html = misaka.html(self.description) # Shows marked down text without markdown annotations
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name'] # Order by name

# template.Library()
class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_groups", on_delete=models.CASCADE) # Will be used in html tagging

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user') # Every user is uniquely linked to a group
