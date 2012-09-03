from django.template.defaultfilters import slugify
from django import forms
from django import forms

from google.appengine.ext.db import djangoforms

from bootstrap.forms import BootstrapMixin, Fieldset
from apps.blog.models import Entry
from apps.blog.widgets import TinyMCEEditor

class EntryForm(BootstrapMixin, djangoforms.ModelForm):
    content = forms.CharField(widget=TinyMCEEditor())

    def clean(self):
        self.cleaned_data['slug'] = str(slugify(self.cleaned_data['title']))
        return super(EntryForm, self).clean()

    class Meta:
        model = Entry
        exclude = ['created_at', 'updated_at', 'published_at', 'slug']
