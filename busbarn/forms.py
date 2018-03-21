from django import forms
from django.forms import ModelForm
from .models import Vehicle, Issue  ### is this needed?

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('vehicle', 'severity', 'description', 'mechanic',
                  'reason', 'repair', 'remarks', 'date_noted')


        def __init__(self, *args, **kwargs):
            super(IssueForm, self).__init__(*args, **kwargs)
            self.fields['date_completed'].required = False
            self.fields['repair'].required=False
            self.fields['remarks'].required=False

