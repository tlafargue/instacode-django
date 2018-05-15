from django import forms
from .models import Profile


class UpdateProfile(forms.ModelForm):
    email = forms.EmailField()
    class Meta():
        model = Profile
        fields = ['nom_complet','langue','a_propos','ville','pays','birth_date','niveau_de_formation','gender','image']