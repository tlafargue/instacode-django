from django import forms
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self,*arg, **kwargs):
        emai = self.cleaned_data.get('email')
        userss = User.objects.get(email=emai.lower()).username
        password = self.cleaned_data.get('password')
        user = authenticate(username=userss, password=password)
        if userss and password:
            if not user:
                raise forms.ValidationError('This user doesnt exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is no longer active')
        return  super(UserLoginForm,self).clean(*arg, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']
