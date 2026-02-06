from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from .models import Course
from .forms import CourseForm


class TrainerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden("Only trainers can perform this action.")
        return super().dispatch(request, *args, **kwargs)


class CourseListView(View):
    template_name = 'courses/course-list.html'

    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        return render(request, self.template_name, {'courses': courses})


class CourseDetailView(View):
    template_name = 'courses/course-detail.html'

    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        return render(request, self.template_name, {'course': course})


class CourseCreateView(TrainerRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course-form.html'
    success_url = reverse_lazy('course-list')

    def form_valid(self, form):
        form.instance.trainer = self.request.user
        return super().form_valid(form)


class CourseUpdateView(TrainerRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course-form.html'
    success_url = reverse_lazy('course-list')

    def get_queryset(self):
        return Course.objects.filter(trainer=self.request.user)


class CourseDeleteView(TrainerRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course-confirm-delete.html'
    success_url = reverse_lazy('course-list')

    def get_queryset(self):
        return Course.objects.filter(trainer=self.request.user)
