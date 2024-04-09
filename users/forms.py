from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Member.models import Member  # Adjust the import path based on your actual app structure
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from Member.models import Member




class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()




class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ["name", "surname", "username", "telephone", "location", "new_believer_school", "pays_tithe", "working", "schooling", "picture"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
