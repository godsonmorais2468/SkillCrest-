from django.shortcuts import render, get_object_or_404
from django.views import View
from courses.models import Course
from payments.models import CoursePurchase

class CourseLessonsView(View):
    template_name = "learning/course-lessons.html"

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        # 🔒 Only paid users can access
        if not request.user.is_authenticated or not CoursePurchase.objects.filter(
            user=request.user, course=course, is_paid=True
        ).exists():
            return render(request, "learning/not-enrolled.html")

        lessons = course.lessons.all()

        return render(request, self.template_name, {
            "course": course,
            "lessons": lessons
        })
