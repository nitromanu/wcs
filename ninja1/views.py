from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from forms import RegistrationForm, LoginForm
from models import UserProfile as user_profile
from subscription.models import subscriptionDetails as user_subscribtion
from result.models import studentResponse as student_response
import datetime
from quiz.models import Questions as questions
from django.db.models import Q
# Create your views here.

def home(request):
    return render(request,'index.html')


def user_login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            login_details = request.POST
            user_name = login_details.get('username')
            password = login_details.get('password')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/home/")
                else:
                    return HttpResponse('Your user account disabled')
            else:
                return HttpResponse(user_name)

        else:
            return render(request, 'login.html')

    else:
        return HttpResponseRedirect("/home/")


def render_register(request):
    """
    Handles the register request. If the request is not a POST request, it will render the signup page
    otherwise it will handles the post request

    """
    if not request.user.is_authenticated():
        if request.method == 'POST':
            user_data = request.POST
            register_form = RegistrationForm(user_data)
            if register_form.is_valid():
                user = register_form.save()
                user.email = user_data.get('username')
                password = user.password
                user.set_password(user.password)
                user.save()

                # Following code is to save user profile.

                user_fullname = user_data.get('first_name') + " " + user_data.get('last_name')
                user_email = user_data.get('username')
                user_phone = user_data.get('phone')
                school_data = user_data.get('school')
                current_user_profile = user_profile(email=user_email,
                                                    full_name=user_fullname,
                                                    phone_number=user_phone,
                                                    school_name = school_data)
                current_user_profile.save()
                user = authenticate(username=user_email, password=password)
                login(request, user)
                return HttpResponseRedirect("/home/")
            else:
                return HttpResponse(register_form.errors['username'])

        else:
            return render(request, 'register.html')
    else:
        return HttpResponseRedirect('/home/')

@login_required(login_url='/login/')
def user_home(request):
    username = request.user.username
    subscription_data = user_subscribtion.objects.filter(username = username)
    date_today = datetime.date.today()
    question_data = questions.objects.filter(Q(startDate__lte=date_today) & Q(endDate__gte=date_today))
    if question_data.exists():
        question_data = question_data[0]
        question_active = 1
    else:
        question_active = 0
    if subscription_data.exists():
        subscription_data = subscription_data[0]
        if subscription_data.end_date < datetime.date.today():
            is_active = 0
        else:
            is_active = 1

    else:
        is_active = 0
    context = {
        'subscription':subscription_data,
        'is_active':is_active,
        'question_active':question_active,
        'question_data':question_data
    }
    return render(request,'account.html',context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_account(request):
    username = request.user.username
    subscription_data = user_subscribtion.objects.filter(username = username)
    student_response_data = student_response.objects.filter(username = username)
    if subscription_data.exists():
        subscription_data = subscription_data[0]
    else:
        subscription_data = None

    if not student_response_data.exists():
        student_response_data = None

    context = {
        'subscription':subscription_data,
        'student_response_data':student_response_data
    }
    return render(request,'history.html',context)