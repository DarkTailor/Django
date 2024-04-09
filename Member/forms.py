from django import forms

from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'telephone', 'new_believer_school', 'pays_tithe', 'working', 'schooling',
                  'picture']

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        not_required = ('telephone', 'fathers_name', 'mothers_name', 'guardians_name', 'picture')
        for field in not_required:
            self.fields[field].required = False


