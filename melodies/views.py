from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Melody, UserProfile, Purchase
from django.contrib.auth.models import User

def home(request):
    melodies = Melody.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'melodies/home.html', {'melodies': melodies})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_creator = request.POST.get('is_creator', False) == 'on'
        
        # Simple username check
        if username and password:
            if not User.objects.filter(username=username).exists():
                # Create user with minimal validation
                user = User.objects.create_user(
                    username=username,
                    password=password,  # Will be hashed automatically
                )
                UserProfile.objects.create(user=user, is_creator=is_creator)
                messages.success(request, 'Welcome! Account created successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Username already taken')
        else:
            messages.error(request, 'Please fill in all fields')
    
    return render(request, 'registration/register.html')

@login_required
def create_melody(request):
    if not request.user.userprofile.is_creator:
        messages.error(request, 'Only creators can create melodies!')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        notes = request.POST.get('notes')
        price = request.POST.get('price')
        description = request.POST.get('description')
        
        melody = Melody.objects.create(
            creator=request.user,
            title=title,
            notes=notes,
            price=price,
            description=description,
            is_published=True
        )
        messages.success(request, 'Melody created successfully!')
        return redirect('melody_detail', pk=melody.pk)
        
    return render(request, 'melodies/create_melody.html')

def melody_detail(request, pk):
    melody = get_object_or_404(Melody, pk=pk)
    is_owner = melody.creator == request.user if request.user.is_authenticated else False
    has_purchased = False
    
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(melody=melody, buyer=request.user).exists()
    
    return render(request, 'melodies/melody_detail.html', {
        'melody': melody,
        'is_owner': is_owner,
        'has_purchased': has_purchased
    })

@login_required
def purchase_melody(request, pk):
    melody = get_object_or_404(Melody, pk=pk)
    if melody.creator == request.user:
        messages.error(request, 'You cannot purchase your own melody!')
        return redirect('melody_detail', pk=pk)
        
    if Purchase.objects.filter(melody=melody, buyer=request.user).exists():
        messages.error(request, 'You have already purchased this melody!')
        return redirect('melody_detail', pk=pk)
        
    Purchase.objects.create(
        melody=melody,
        buyer=request.user,
        price=melody.price
    )
    messages.success(request, f'Successfully purchased {melody.title}!')
    return redirect('melody_detail', pk=pk)

def play_codes(request):
    return render(request, 'play_codes.html')
