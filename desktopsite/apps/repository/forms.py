from django import forms
from desktopsite.apps.repository.models import *
from desktopsite.apps.downloads.models import Release
from django.utils import simplejson as json
import zipfile

class PackageForm(forms.ModelForm):
    class Meta:
        model=Package
        exclude=['maintainer']
        
class VersionForm(forms.ModelForm):
    _compatible_objs = []
    class Meta:
        model=Version
        exclude=['name', 'package', 'verified_safe', 'compatible']
    def clean_package_file(self):
        self._compatible_objs = []
        file = self.cleaned_data["package_file"]
        #validate the package, pull some info
        try:
            zip = zipfile.ZipFile(file, "r")
            if "meta.json" in zip.namelist():
                raw_json = zip.read("meta.json")
                try:
                    data = json.loads(raw_json)
                except (ValueError, TypeError), (err):
                    raise forms.ValidationError("Package's meta.json file has malformed json (Error was: %s)" % err)
                if data.has_key("type"):
                    type = data["type"]
                    if type != "application" and type != self._requested_package.category:
                        raise forms.ValidationError("Uploaded package's type does not fit the current package's category")
                    elif type == "application" and data["category"].lower() != self._requested_package.category:
                        raise forms.ValidationError("Uploaded package's category does not match the current package's catgory")
                    if type == "application":
                        if not (data.has_key("sysname") and data["sysname"] == self._requested_package.sysname):
                            raise forms.ValidationError("Uploaded package's sysname does not match the current package's sysname")
                else:
                    raise forms.ValidationError("Package's meta.json missing a 'type' property")
                if data.has_key("compatible"):
                    compat = data["compatible"]
                    for version in compat:
                        try:
                            release = Release.objects.get(name=version)
                            self._compatible_objs.append(release)
                        except(Release.DoesNotExist):
                            raise forms.ValidationError("Version %s specified in compatible property does not exist" % version)
                            
                else:
                    raise forms.ValidationError("Package's meta.json missing a 'compatible' property")
                if data.has_key("version"):
                    self.cleaned_data["name"] = data['version']
                    self.clean_name()
                else:
                    raise forms.ValidationError("Package's meta.json missing a 'version' property")
            else:
                raise forms.ValidationError("Package did not contain a meta.json file")

        except zipfile.error:
            raise forms.ValidationError("Upload must be a lucid package")
        return file
    def clean_name(self):
        try:
            Version.objects.get(name=self.cleaned_data["name"], package=self._requested_package)
            raise forms.ValidationError("Version with that name already exists")
        except Version.DoesNotExist:
            return self.cleaned_data["name"]
    def clean(self):
        self.cleaned_data["compatibility"] = self._compatible_objs
        return self.cleaned_data

class EditVersionForm(VersionForm):
    class Meta(VersionForm.Meta):
        exclude=['name', 'package', 'verified_safe', 'package_file', 'compatibility']
