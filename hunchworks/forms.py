#!/usr/bin/env python

import json
from hunchworks import models, custom_fields
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.utils.datastructures import MultiValueDict, MergeDict


class TagsWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    if value == None:
		value = []
	
    flat_value = ",".join(map(unicode, value))

    attrs["data-prepopulate"] = json.dumps([
      {"id": pk, "name": unicode(self.choices.queryset.get(pk=pk))}
      for pk in value
    ])

    attrs["data-search-url"] = "/hunchworks/tags"
    attrs["class"] = "tags"

    return super(TagsWidget, self).render(name, flat_value, attrs)

  def value_from_datadict(self, data, files, name):
    return [pk for pk in data.get(name).split(",") if pk.isdigit()]


class TagsField(forms.ModelMultipleChoiceField):
  widget = TagsWidget

  def __init__(self, *args, **kwargs):
    super(TagsField, self).__init__(
      models.Tag.objects.all(),
      *args, **kwargs)


class HunchForm(ModelForm):
  tags = TagsField(required=False)

  class Meta:
    model = models.Hunch
    exclude = (
      "creator", "time_created", "time_modified", "status", "user_profiles"
    )


class EvidenceForm(ModelForm):
  class Meta:
    model = models.Evidence
    exclude = (
    'hunch_id', 'creator_id', 'evidence_strength', 'time_created',
    'time_modified', 'attachments', 'albums', 'hunch', 'evidence_tags'
    )


class GroupForm(ModelForm):
  group_collaborators = forms.CharField(required=False,
    help_text="The HunchWorks members you wish to invite to this group.<br>" +
              "You can only invite members who you are connected with.")

  class Meta:
    model = models.Group
    exclude = ("members", "logo")
    widgets = {
      'name': forms.TextInput(attrs={ 'size': 50 }),
      'abbreviation': forms.TextInput(attrs={ 'size': 15 })
    }



class HomepageForm(ModelForm):
  class Meta:
    model = models.User

class UserForm(ModelForm):
  class Meta:
    model= models.UserProfile

class InvitePeople(forms.Form):
  invited_emails = custom_fields.MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))
  
  def save(self, *args, **kwargs):
    created_user = models.User.objects.get(pk=1)
    print self.cleaned_data
    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invited_email = models.Invitation( email=email_input )
      invited_user = models.UserInvites( invited_email=invited_email, user=created_user, status=0)
      invited_user.save()
    
