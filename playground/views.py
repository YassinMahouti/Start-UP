from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from .forms import CreateUserForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from .models import StripeCustomer
from django.contrib.auth.models import User
import stripe


def say_hello(request):
    return render(request, 'hello.html', {'name': 'Yassin'})


def index(request):
    context = {}
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        return render(request, 'index.html', {
            'subscription': subscription,
            'product': product,
        })
    except:
        return render(request, 'index.html', context=context)


@login_required(login_url='login')
def userPage(request):
    context = {}
    return render(request, 'user.html', context)


################################################################ AUTHENTICATION #################################################################


@csrf_exempt
def loginPage(request):
    # form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('user-page')
    else:
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


@csrf_exempt
def registrationPage(request):
    if request.user.is_authenticated:
        return redirect('user-page')
    else:
        form = CreateUserForm()
        # Handle user registration (Unique Username, hash password ...)
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, user + ' registered successfully')
                return redirect('login')
            else:
                messages.info(
                    request, 'Something went wrong, please try again')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'registration.html', context)


@login_required(login_url='login')
@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('login')

################################################################ --------------- #################################################################


################################################################ STRIPE #################################################################


@login_required(login_url='login')
@csrf_exempt
# Handle the AJAX request
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@login_required(login_url='login')
@ csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'playground/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'playground/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required(login_url='login')
@ csrf_exempt
def create_checkout_session_silver(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'playground/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'playground/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID_SILVER,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required(login_url='login')
@ csrf_exempt
def create_checkout_session_bronze(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'playground/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'playground/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID_BRONZE,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@ login_required(login_url='login')
def success(request):
    return render(request, 'subscription/success.html')


@ login_required(login_url='login')
def cancel(request):
    return render(request, 'subscription/cancel.html')


@login_required(login_url='login')
@ csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)

################################################################ --------------- #################################################################

################################################################ Restricted subscription pages #################################################################


@login_required(login_url='login')
def subsPage(request):
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'subshome.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'subshome.html')


@login_required(login_url='login')
@ csrf_exempt
def prediction(request):
    return render(request, 'predict.html')


@login_required(login_url='login')
@ csrf_exempt
def predict_member(request):
    return render(request, 'predict_member.html')


@login_required(login_url='login')
@ csrf_exempt
def acccounting(request):
    return render(request, 'accounting.html')


@login_required(login_url='login')
@ csrf_exempt
def charts(request):
    return render(request, 'charts.html')


################################################################ --------------- #################################################################
