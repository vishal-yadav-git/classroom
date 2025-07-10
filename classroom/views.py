from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, LoginForm
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from .models import CustomUser, Lecture, SlideBanner, Franchisee, Filter, Comment, FacultyComment, Course, Faculty
from math import ceil
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    lectures = Lecture.objects.filter(is_published=True, show_on_homepage=True) 
    faculty = Faculty.objects.filter(is_published=True, show_on_homepage=True) 
    franchisee = Franchisee.objects.filter(is_published=True)
    banner = SlideBanner.objects.filter(is_published=True)
    context = {
        'lectures': lectures,
        'franchisee': franchisee,
        'banner': banner,
        'faculty': faculty
    }
    return render(request, 'site/index.html', context)

def base(request):
    return render(request, 'site/base.html')

def breadcrumbs(request):
    return render(request, 'include/breadcrumbs.html')

def user(request):
        user = User.objects.all()
        print('user', user)
        return render(request, template_name='site/index.html')

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)  # Hash the password
            user.user_type = 'student'  
            user.save()
            
            # Auto-login after registration
            user = authenticate(request, email=user.email, password=password)
            if user:
                auth_login(request, user)
                return redirect('student_dash:dashboard')  # update with your actual dashboard URL name
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'site/register.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.user_type == 'admin':
                    auth_login(request, user)
                    return redirect('/admin/')
                else:
                    auth_login(request, user)
                    return redirect('student_dash:dashboard')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid email or password. Please register if you don't have an account.")
    else:
        form = LoginForm()
    return render(request, 'site/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("classroom:login")


def lecture(request):
    lectures = Lecture.objects.filter(is_published=True).select_related('faculty', 'course')  
    total_lectures = lectures.count()
    slides = ceil(total_lectures / 4)  

    # Get filter values
    title = request.GET.get('title')
    faculty_id = request.GET.get('faculty')
    course_id = request.GET.get('category')
    price = request.GET.get('price')

    # Apply filters
    if title:
        lectures = lectures.filter(title__icontains=title)
    if faculty_id:
        lectures = lectures.filter(faculty__id=faculty_id)
    if course_id:
        lectures = lectures.filter(course__id=course_id)
    if price:
        lectures = lectures.filter(price__lte=price)

    # Get unique dropdown values
    title = Lecture.objects.filter(is_published=True).values_list('title', flat=True).distinct()
    faculty = Lecture.objects.filter(is_published=True).values('faculty', 'faculty__name').distinct()
    courses = Lecture.objects.filter(is_published=True).values('course', 'course__name').distinct()


    context = {
        'no_of_slides': slides,
        'range': range(1, slides + 1),
        'lectures': lectures,
        'faculty': faculty,
        'courses': courses,
        'title': title 
    }

    return render(request, 'site/lecture.html', context)

def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    comments = Comment.objects.filter(post=lecture, parent__isnull=True).order_by('-created_at')
    recommended = Lecture.objects.exclude(pk=pk).order_by('?')[:4]
    recent_comments = comments[:3]
    remaining_comments = comments[3:]

    if request.method == "POST":
        name = request.POST.get('name')
        content = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')  # hidden input
        parent = Comment.objects.get(id=parent_id) if parent_id else None
        Comment.objects.create(parent=parent, post=lecture, name=name, content=content)
        return redirect('site:lecture_detail', pk=pk)

    return render(request, 'site/lecture_detail.html', {
        'lecture': lecture,
        'comments': comments,
        'recommended': recommended,
        'recent_comments': recent_comments,
        'remaining_comments': remaining_comments,
    })

def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    comments = FacultyComment.objects.filter(post=faculty, parent__isnull=True).order_by('-created_at')
    recommended = Faculty.objects.exclude(pk=pk).order_by('?')[:4]
    recent_comments = comments[:3]
    remaining_comments = comments[3:]
    lectures = Lecture.objects.filter(faculty=faculty, is_published=True).order_by('-pub_date')
    
    if request.method == "POST":
        name = request.POST.get('name')
        content = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')  # hidden input
        parent = FacultyComment.objects.get(id=parent_id) if parent_id else None
        FacultyComment.objects.create(parent=parent, post=faculty, name=name, content=content)
        return redirect('site:faculty_detail', pk=pk)

    return render(request, 'site/faculty_detail.html', {
        'faculty': faculty,
        'comments': comments,
        'recommended': recommended,
        'recent_comments': recent_comments,
        'remaining_comments': remaining_comments,
        'lectures': lectures,
    })


def faculty(request):
    faculty = Faculty.objects.filter(is_published=True)  # Only show published lectures
    total_faculties = len(faculty)
    slides = total_faculties // 4 + ceil((total_faculties / 4) - (total_faculties // 4))

    context = {
        'no_of_slides': slides,
        'range': range(1, slides + 1),
        'faculty': faculty
    }

    return render(request, 'site/faculty.html', context)


# def login(request):
    # return render(request, 'site/login.html')

def enroll(request):
    return render(request, 'include/enroll_form.html')



