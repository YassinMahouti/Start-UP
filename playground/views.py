from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def say_hello(request):
    return render(request, 'hello.html', {'name': 'Yassin'})


@login_required(login_url='login')
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def loginPage(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'login.html')


def registrationPage(request):
    form = CreateUserForm()
    # Handle user registration (Unique Username, hash password ...)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ' registered successfully')
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
