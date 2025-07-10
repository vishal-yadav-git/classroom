from classroom.models import Course, Faculty

def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return {'course_list': Course.objects.all()}

def faculty_list(request):
    faculties = Faculty.objects.filter(is_published=True)
    return {'faculty_list': faculties}

