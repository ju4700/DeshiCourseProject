from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course

def home(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(title__icontains=query) if query else Course.objects.all()

    # Pagination logic: Show 9 courses per page
    paginator = Paginator(courses, 9)  # 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'courses/home.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})