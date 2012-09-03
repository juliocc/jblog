import re

from django import forms

from bootstrap.forms import BootstrapMixin, Fieldset
from apps.blog.models import Entry
from apps.blog.widgets import TinyMCEEditor

tag_re = re.compile('[^\w _-]')

class EntryForm(BootstrapMixin, forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=TinyMCEEditor())
    tags = forms.CharField(widget=forms.Textarea())
    status = forms.ChoiceField(choices=[('draft', 'draft'),
                                        ('published', 'published')])

    def clean_tags(self):
        tags = [x.strip() for x in self.cleaned_data['tags'].split('\n') if x.strip()]
        for tag in tags:
            if tag_re.search(tag):
                raise forms.ValidationError('tags should only contain letters, '
                                            'numbers, whitespace and dashes')
        return tags
        

    class Meta:
        model = Entry
        exclude = ['created_at', 'updated_at', 'published_at', 'slug']
