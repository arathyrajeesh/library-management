from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Book
from .forms import BookForm


def home(request):
    return render(request,'home.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all-book')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def book_list(request):
    query = request.GET.get('q', '')
    available_only = request.GET.get('available', '')

    books = Book.objects.all()

    query = request.GET.get('q', '')
    available_only = request.GET.get('available', '') == 'on'

    books = Book.objects.all()

    if query:
        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        ) | books.filter(
            category__icontains=query
        )

    if available_only:
        books = books.filter(availability=True)



    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books_list.html', {
        'page_obj': page_obj,
        'query': query,
        'available_only': available_only,
    })


@login_required(login_url='login')
def add_book(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied! Only admins can add books.")
        return redirect('all-book')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all-book')  
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required(login_url='login')
def delete_book(request, book_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied! Only admins can delete books.")
        return redirect('all-book')

    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('all-book')

@login_required(login_url='login')
def update_book(request, book_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied! Only admins can update books.")
        return redirect('all-book')

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('all-book')
    else:
        form = BookForm(instance=book)

    return render(request, 'add_book.html', {'form': form, 'update': True})
