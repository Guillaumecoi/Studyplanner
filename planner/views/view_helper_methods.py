from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from planner.models import Course

def check_user_course_permission(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user == course.user:
        # Return a 403 Forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")
    return None
