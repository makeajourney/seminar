from django import forms

from .models import Profile

class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input__wide',
            'autofocus': 'autofocus',
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'organization', 'image', 'biography')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, *kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['organization'].widget.attrs.update({
            'class': 'input__wide',
        })
        self.fields['image'].widget.attrs.update({
            'class': 'btn--tiny btn--black',
        })
