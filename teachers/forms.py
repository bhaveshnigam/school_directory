from django.forms import forms


class BulkImportTeachers(forms.Form):
    teacher_details = forms.FileField()
    teacher_images = forms.FileField()
