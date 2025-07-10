from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Playlist, Lecture, LectureNote
from django.core.serializers.json import DjangoJSONEncoder
import json
from classroom.models import Lecture as Course, CartItem
from django.db import transaction


# Create your views here.

@login_required
def dashboard(request):
    user = request.user
#onlu allow student or faculty to access this page
    if user.user_type in ['student', 'faculty']:
        return render(request, 'dashboard/index.html', {'user': user})  # Redirect to login if not a student or faculty
    else:
        return redirect('/admin/')  # If user is not logged in, redirect to login page


def dash_base(request):
    return render(request, 'dashboard/base.html')

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('image')

        user.first_name = first_name
        user.last_name = last_name
        if image:
            user.image = image

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('student_dash:profile')

    return render(request, 'dashboard/profile_info.html')

@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, course=course)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{course.title} added to cart.")
    return redirect('site:lecture_detail', pk=course_id)

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'dashboard/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('student_dash:view_cart')

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('student_dash:view_cart')
    
    total_price = sum(item.total_price() for item in cart_items)

    if user.wallet_balance < total_price:
        messages.error(request, "Insufficient wallet balance. Please Top Up.")
        return redirect('student_dash:view_cart')

    with transaction.atomic():
        user.wallet_balance -= total_price
        user.save()
        cart_items.delete()

    messages.success(request, f"Checkout successful! ₹{total_price} deducted from your wallet.")
    return render(request, 'dashboard/payment_verified.html', {'cart_items': [], 'total_price': 0})



def lecture_view(request):
    playlists = Playlist.objects.filter(is_published=True)
    context = {
        'playlist': playlists
    }
    return render(request, 'dashboard/lectures.html', context)


def playlist_lecture_view(request):
    playlist_id = request.GET.get('playlist_id')
    playlist = get_object_or_404(Playlist, id=playlist_id)
    lectures = Lecture.objects.filter(playlist=playlist)

    # Prepare JSON-safe lecture list
    lectures_data = []
    for lecture in lectures:
        notes_list = [note.file.url for note in lecture.notes.all()]
        lectures_data.append({
            'title': lecture.title,
            'description': lecture.description,
            'video_url': lecture.youtube_url,
            'notes': notes_list,
        })

    context = {
        'playlist': playlist,
        'lectures': lectures,
        'lectures_json': json.dumps(lectures_data)
    }

    return render(request, 'dashboard/single_lecture.html', context)

