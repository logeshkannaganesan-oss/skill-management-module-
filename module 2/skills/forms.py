from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'skill_level']
        widgets = {
            'skill_name': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Enter Skill Name (e.g. Python, Design)',
                'autocomplete': 'off',
            }),
            'skill_level': forms.Select(attrs={
                'class': 'form-select glass-input',
            }),
        }
        error_messages = {
            'skill_name': {
                'required': 'Skill name cannot be empty.',
            }
        }

    def clean_skill_name(self):
        skill_name = self.cleaned_data.get('skill_name')
        if not skill_name or not skill_name.strip():
            raise forms.ValidationError("Skill name cannot be empty.")
        # Strip trailing/leading spaces and format nicely
        return skill_name.strip()
