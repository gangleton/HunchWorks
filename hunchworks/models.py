#!/usr/bin/env python

import datetime
import hunchworks_enums
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


PRIVACY_CHOICES = (
  (0, "Hidden"),
  (1, "Closed"),
  (2, "Open"))

PRIVACY_HELP_TEXT = "<br>".join([
  "<strong>Hidden</strong>: only visible to invited members.",
  "<strong>Closed</strong>: visible to everyone, but only invited members can participate.",
  "<strong>Open</strong>: available to any HunchWorks member."])


class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  title = models.IntegerField(choices=hunchworks_enums.UserTitle.GetChoices(), default=0)
  show_profile_reminder = models.IntegerField(default=0)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  bio_text = models.TextField(blank=True)
  phone = models.CharField(max_length=20, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.ImageField(upload_to="/profile_images/", blank=True)
  screen_name = models.CharField(max_length=45, blank=True)
  messenger_service = models.IntegerField(null=True, blank=True, choices=hunchworks_enums.MessangerServices.GetChoices(), default=0)
  default_language = models.ForeignKey('Language', default=0)

  invitation = models.ForeignKey('Invitation', unique=True, null=True, blank=True)
  connections = models.ManyToManyField('self', through='Connection', symmetrical=False, blank=True)

  roles = models.ManyToManyField("Role", blank=True)
  location_interests = models.ManyToManyField('Location', blank=True)
  skills = models.ManyToManyField('Skill', blank=True)

  qualifications = models.ManyToManyField('Education', blank=True)
  courses = models.ManyToManyField('Course', blank=True)

  def __unicode__(self):
    return self.user.username


def create_user(sender, instance, created, **kwargs):
  if created: UserProfile.objects.create(user=instance)

post_save.connect(create_user, sender=User)


class Connection(models.Model):
  user_profile       = models.ForeignKey('UserProfile', related_name="outgoing_connections")
  other_user_profile = models.ForeignKey('UserProfile', related_name="incoming_connections")
  status             = models.IntegerField(default=0)

  def __unicode__(self):
    return "%s -> %s" % (self.user_profile, self.other_user_profile)


class Hunch(models.Model):
  creator = models.ForeignKey('UserProfile', related_name="created_hunches")
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  status = models.IntegerField(choices=hunchworks_enums.HunchStatus.GetChoices(), default=2)
  title = models.CharField(max_length=100)
  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  language = models.ForeignKey('Language')
  location = models.ForeignKey('Location', null=True, blank=True)
  description = models.TextField()
  skills = models.ManyToManyField('Skill', blank=True)
  tags = models.ManyToManyField('Tag', blank=True)
  user_profiles = models.ManyToManyField('UserProfile', through='HunchUser')

  class Meta:
    verbose_name_plural = "hunches"

  def __unicode__(self):
    return self.title

  @models.permalink
  def get_absolute_url(self):
    return ("hunch", [self.pk])

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.id:
      self.time_created = now

    self.time_modified = now
    super(Hunch, self).save(*args, **kwargs)

  def is_editable_by(self, user):
    """Return True if this Hunch is editable by `user` (a Django auth user)."""
    return (self.creator.user == user)

  def is_viewable_by(self, user):
    """Return True if this Hunch is viewable by `user` (a Django auth user)."""

    if self._is_hidden():
      return (self.creator.user == user)

    # Otherwise, if the hunch is OPEN or CLOSED, anyone (even anonymous) can
    # view it. The only distinction between the levels is in the editing.
    return True

  def _is_hidden(self):
    """Return True if this Hunch is hidden."""
    return (self.privacy == hunchworks_enums.PrivacyLevel.HIDDEN)


class HunchUser(models.Model):
  hunch = models.ForeignKey('Hunch')
  user_profile = models.ForeignKey('UserProfile')
  status = models.IntegerField()


class Evidence(models.Model):
  """Class representing a response to the hunch"""
  strength = models.IntegerField(default=0)
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  description = models.TextField(blank=True)
  hunch = models.ForeignKey('Hunch')
  creator = models.ForeignKey('UserProfile')
  albums = models.ManyToManyField('Album')
  attachments = models.ManyToManyField('Attachment')
  tags = models.ManyToManyField('Tag', blank=True)

  def __unicode__(self):
    return "<Evidence:%d>" % self.pk

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.evidence_id:
      self.time_created = now

    self.time_modified = now
    super(Evidence, self).save(*args, **kwargs)


class Group(models.Model):
  name = models.CharField(max_length=100, unique=True)
  abbreviation = models.CharField(max_length=10, null=True, blank=True)
  type = models.IntegerField(choices=hunchworks_enums.GroupType.GetChoices(), default=0)
  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  location = models.ForeignKey('Location', null=True, blank=True)
  members = models.ManyToManyField('UserProfile', through='UserProfileGroup', null=True, blank=True)

  def __unicode__(self):
    return self.name

  @models.permalink
  def get_absolute_url(self):
    return ("group", [self.pk])


class UserProfileGroup(models.Model):
  user_profile = models.ForeignKey('UserProfile')
  group = models.ForeignKey('Group')
  access_level = models.IntegerField()
  status = models.IntegerField()

  def __unicode__(self):
    return "<UserProfileGroup:%d>" % self.pk


class Attachment(models.Model):
  type = models.IntegerField()
  file_location = models.CharField(max_length=100)

  def __unicode__(self):
    return "<Attachment:%d>" % self.pk


class Album(models.Model):
  name = models.CharField(max_length=45)
  attachments = models.ManyToManyField('Attachment')

  def __unicode__(self):
    return self.name


class Education(models.Model):
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)

  def __unicode__(self):
    return "<Education:%d>" % self.pk


class Course(models.Model):
  """
  An more informal educational course which does not fit neatly into the
  Education model. (E.g. "Diploma from NYC underwater welding club".)
  """

  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "classes"

  def __unicode__(self):
    return "<Course:%d>" % self.pk


class Language(models.Model):
  name = models.CharField(unique=True, max_length=45)

  def __unicode__(self):
    return self.name


class Location(models.Model):
  name = models.CharField(unique=True, max_length=45)

  def __unicode__(self):
    return self.name


class Tag(models.Model):
  name = models.CharField(max_length=40)

  def __unicode__(self):
    return self.name


class Role(models.Model):
  group = models.ForeignKey('Group')
  title = models.CharField(max_length=40)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)

  def __unicode__(self):
    return self.title


class Skill(models.Model):
  name = models.CharField(unique=True, max_length=100)
  is_language = models.IntegerField()
  is_technical = models.IntegerField()

  def __unicode__(self):
    return self.name


class Invitation(models.Model):
  email = models.CharField(max_length=100)
  invited_by = models.ForeignKey('UserProfile', related_name="invitations")
  hunch = models.ForeignKey('Hunch', null=True, blank=True)

  def __unicode__(self):
    return "%s to %s" % (self.email, self.hunch)
