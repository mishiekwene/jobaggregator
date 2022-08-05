from django import forms
class SkillSearchForm(forms.Form):
    searches = forms.CharField()
    category = forms.ChoiceField()

class FilterForm(forms.Form):
    job_type = forms.ChoiceField()
    state = forms.ChoiceField()