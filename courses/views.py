import time
import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from SoftwareProject import settings
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

@csrf_exempt
def payment_success(request):
    # Handle successful payment
    return render(request, 'payment_success.html')

@csrf_exempt
def payment_fail(request):
    # Handle failed payment
    return render(request, 'payment_fail.html')

@csrf_exempt
def payment_cancel(request):
    # Handle canceled payment
    return render(request, 'payment_cancel.html')

def initiate_payment(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    course = get_object_or_404(Course, id=course_id)
    url = 'https://sandbox.sslcommerz.com/gwprocess/v3/api.php'
    tran_id = f"ORDER_{course_id}_{request.user.id if request.user.is_authenticated else 'guest'}_{int(time.time())}"
    data = {
        'store_id': settings.SSL_COMMERZ['store_id'],
        'store_passwd': settings.SSL_COMMERZ['store_passwd'],
        'total_amount': str(course.price),
        'currency': 'BDT',
        'tran_id': tran_id,
        'success_url': request.build_absolute_uri('/payment-success/'),
        'fail_url': request.build_absolute_uri('/payment-fail/'),
        'cancel_url': request.build_absolute_uri('/payment-cancel/'),
        'cus_name': request.user.get_full_name() if request.user.is_authenticated else 'Guest User',
        'cus_email': request.user.email if request.user.is_authenticated else 'guest@example.com',
        'cus_add1': 'Dhaka',
        'cus_phone': '01700000000',
        'shipping_method': 'NO',
        'product_name': course.title,
        'product_category': 'Course',
        'product_profile': 'education',
    }
    response = requests.post(url, data=data)
    response_data = response.json()

    if response_data['status'] == 'SUCCESS':
        return redirect(response_data['GatewayPageURL'])
    else:
        return JsonResponse({'error': 'Payment initiation failed', 'details': response_data})