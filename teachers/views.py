import csv
import io
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from teachers.forms import BulkImportTeachers
from teachers.models import Teacher, Subject


class SchoolDirectory(generic.TemplateView):
    template_name = 'teacher_list.html'

    def get_context_data(self, **kwargs):
        context = super(SchoolDirectory, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context


class TeacherDetail(generic.TemplateView):
    template_name = 'teacher_detail.html'

    def get_object(self):
        return Teacher.objects.filter(id=self.kwargs.get('pk')).first()

    def get(self, request, *args, **kwargs):
        teacher_obj = self.get_object()
        if not teacher_obj:
            raise Http404
        context = self.get_context_data(teacher=teacher_obj, **kwargs)
        return self.render_to_response(context)


class TeacherBulkImport(generic.FormView):
    template_name = 'bulk_import.html'
    form_class = BulkImportTeachers

    def get_success_url(self):
        return reverse('school-directory-list')

    @method_decorator(login_required(login_url='admin:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            csv_data = self.request.FILES['teacher_details'].read().decode('utf-8')
            profile_picture_data = self.request.FILES['teacher_images'].read()
            file_like_object = io.BytesIO(profile_picture_data)
            zipfile_ob = zipfile.ZipFile(file_like_object)

            profile_pictures = {}

            for file in zipfile_ob.filelist:
                profile_pictures[file.filename] = zipfile_ob.read(file.filename)

            teacher_data = csv.reader(io.StringIO(csv_data), quotechar='"')
            for index, teacher_data in enumerate(teacher_data):
                if index == 0:
                    continue
                subjects = teacher_data[6].split(',')
                subject_objs = []
                for subject in subjects:
                    subject_obj, created = Subject.objects.get_or_create(
                        name=subject.lower().capitalize()
                    )
                    subject_objs.append(subject_obj)
                teacher, created = Teacher.objects.get_or_create(
                    email=teacher_data[3],
                    defaults={
                        'first_name': teacher_data[0],
                        'last_name': teacher_data[1],
                        'phone_number': teacher_data[4],
                        'room_number': teacher_data[5],
                    }
                )
                if profile_pictures.get(teacher_data[2]):
                    teacher.profile_picture.save(teacher_data[2], ContentFile(profile_pictures[teacher_data[2]]))

                teacher.subjects_taught.clear()
                teacher.subjects_taught.add(*subject_objs)
                teacher.save()

            return HttpResponseRedirect(self.get_success_url())
        except Exception as err:
            messages.add_message(self.request, messages.ERROR, 'Unable to process provided files')
            return HttpResponseRedirect(reverse('teacher-bulk-import'))
