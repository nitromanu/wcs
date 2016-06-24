from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from forms import RegistrationForm, LoginForm
from models import UserProfile as user_profile
from subscription.models import subscriptionDetails as user_subscribtion, paymentVoucher as pay_voucher
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
            next_url = login_details.get('next')
            error_message = None
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect("/home/")

                else:
                    return HttpResponse('Your user account disabled')
            else:
                error_message = "Incorrect Username or Password"
                context = {
                'message':error_message,
                    'username':user_name,
                    'password':password
            }

                return render(request, 'login.html',context )

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
    user_marks  = student_response.objects.filter(username = username)
    marks_data = False
    attempted = False
    if user_marks.exists():
        marks_data = True
    date_today = datetime.date.today()
    question_data = questions.objects.filter(Q(startDate__lte=date_today) & Q(endDate__gte=date_today))
    if question_data.exists():
        question_data = question_data[0]
        response_data = student_response.objects.filter(Q(username=username) & Q(questionSetID=question_data.questionSetID))
        if response_data.exists():
            attempted = True
        question_active = 1
    else:
        question_active = 0
    if subscription_data.exists():
        subscription_data = subscription_data[0]
        # if subscription_data.end_date < datetime.date.today():
        if subscription_data.attempts_remaining <= 0:
            is_active = 0
        else:
            is_active = 1

    else:
        is_active = 0
    context = {
        'subscription':subscription_data,
        'is_active':is_active,
        'question_active':question_active,
        'question_data':question_data,
        'marks_data':marks_data,
        'user_marks':user_marks,
        'name':request.user.first_name,
        'attempted':attempted
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

@login_required(login_url='/login/')
def dashboard(request):
    if request.user.is_staff:
        users  = User.objects.all()
        date_today = datetime.date.today()
        subscribed_users = user_subscribtion.objects.filter(end_date__gte = date_today)
        voucher_15_days = len(pay_voucher.objects.filter(number_of_days = 15))
        voucher_30_days = len(pay_voucher.objects.filter(number_of_days = 30))
        voucher_15_active = len(pay_voucher.objects.filter(Q(number_of_days=15) & Q(is_active=1)))
        voucher_30_active = len(pay_voucher.objects.filter(Q(number_of_days=30) & Q(is_active=1)))
        total_users = len(users)
        context = {
            'total_users':total_users,
            'active_subscriptions': len(subscribed_users),
            'voucher_15':voucher_15_days,
            'voucher_30':voucher_30_days,
            'voucher_15_active':voucher_15_active,
            'voucher_30_active':voucher_30_active
        }
        return render(request,'dashboard.html',context)
    else:
        raise Http404
