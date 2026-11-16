from django import forms
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    website=forms.CharField(required=False,widget=forms.HiddenInput)
    class Meta:
        model=ContactMessage; fields=["name","email","subject","message","website"]
        widgets={"message":forms.Textarea(attrs={"rows":5})}
    def clean_website(self):
        value=self.cleaned_data.get("website")
        if value: raise forms.ValidationError("Invalid submission")
        return value
