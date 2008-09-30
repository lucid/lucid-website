from django import forms
from desktopsite.apps.repository.models import *

class PackageForm(forms.ModelForm):
    class Meta:
        model=Package
        exclude=['maintainer']
        
class VersionForm(forms.ModelForm):
    class Meta:
        model=Version
        exclude=['package', 'verified_safe']

class EditVersionForm(forms.ModelForm):
    class Meta:
        model=Version
        exclude=['package', 'verified_safe', 'package_file']
