from django import forms
from desktopsite.apps.repository.models import *

class PackageForm(forms.ModelForm):
    class Meta:
        model=Package
        
class VersionForm(forms.ModelForm):
    class Meta:
        model=Version