from django import forms
class SkillSearchForm(forms.Form):
    searches = forms.CharField()
    category = forms.ChoiceField()