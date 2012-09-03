from django import forms
from django import forms

from django import forms

from bootstrap.forms import BootstrapMixin, Fieldset
from apps.blog.models import Entry
from apps.blog.widgets import TinyMCEEditor

class EntryForm(BootstrapMixin, forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=TinyMCEEditor())
    tags = forms.CharField(widget=forms.Textarea())
    status = forms.ChoiceField(choices=[('draft', 'draft'),
                                        ('published', 'published')])

    def clean_tags(self):
        return [x.strip() for x in self.cleaned_data['tags'].split('\n')]

    class Meta:
        model = Entry
        exclude = ['created_at', 'updated_at', 'published_at', 'slug']
