from django import forms
from django.contrib.auth.models import User, Permission

from staff.models import Staff


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    retype_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff
        fields = (
            'first_name', 'last_name', 'mobile', 'email', 'username', 'password', 'retype_password', 'pic',
            'designation')
        widgets = {
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'pic': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_retype_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('retype_password')
        if password != password2:
            raise forms.ValidationError('Password fields must match')
        return password2

    def save(self, commit=True):
        cleaned = self.cleaned_data
        user_data = {key: cleaned[key] for key in ['first_name', 'last_name', 'username', 'email', 'password']}
        user = User.objects.create_user(**user_data)
        permission = Permission.objects.get(codename='c_staff')
        user.user_permissions.add(permission)
        user.save()
        staff = Staff.objects.create(user=user, mobile=cleaned.get('mobile'), designation=cleaned.get('designation'),
                                     pic=cleaned.get('pic'))
        return staff
