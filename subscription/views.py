from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime, timedelta
from  subscription.models import paymentVoucher as payment_voucher, subscriptionDetails as subscriptions
import random
import json

# Create your views here.

def create_voucher_code():
    key_length = 20
    uppercase_string = 'ABCDEFGHIJKLMNPQRSTUVWXYZ'
    random_number = '23456789'
    voucher_code = ''.join(random.SystemRandom().choice(uppercase_string + random_number) for _ in range(key_length))
    return voucher_code


def create_vouchers(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not allowed this operation')
    else:
        if request.method == 'POST':
            voucher_count = int(request.POST.get('voucher_count'))
            category_code = request.POST.get('category_code')
            agent_code = request.POST.get('agent_code')
            amount = int(request.POST.get('amount'))
            days = int(request.POST.get('days'))
            voucher_increment = 0
            voucher_list = []
            while voucher_increment < voucher_count:
                voucher_code = create_voucher_code()
                voucher_list.append(voucher_code)
                current_date = datetime.now()
                expiry_date = current_date + timedelta(60)
                voucher_data = payment_voucher(voucher_number=voucher_code, category_code=category_code,
                                               voucher_agent_code=agent_code, created_date=current_date,
                                               expiry_date=expiry_date, voucher_price=amount,number_of_days = days)
                voucher_data.save()
                voucher_increment += 1
            context = {'vouchers': voucher_list}
            return render(request, 'display_vouchers.html', context)
        else:
            return render(request, 'voucher_data.html')


def payment_voucher_ajax_request(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            username = request.user.username
            voucher_code_input = request.POST.get('voucher_code_input')
            check_voucher = payment_voucher.objects.filter(voucher_number=voucher_code_input)

            """ The below function checks whether the voucher code exist or not and returns error message """
            if not check_voucher.exists():
                # Todo add code to check the length of the input voucher. There are some errors
                data_return = {'status': 'fail', 'message': 'Incorrect Voucher Code'}
                return HttpResponse(json.dumps(data_return), content_type='application/json')

            else:
                check_voucher = payment_voucher.objects.get(voucher_number=voucher_code_input)
                if check_voucher.is_active == 0:

                    """ Check whether the voucher is already used"""

                    data_return = {'status': 'fail', 'message': 'Voucher already used'}
                    return HttpResponse(json.dumps(data_return), content_type='application/json')

                else:

                    """ Check whether the voucher is for mentioned category """
                    current_date = datetime.now()
                    end_date  = current_date +timedelta(30)

                    update_subscription = subscriptions.objects.filter(username = username)
                    try:
                        days = check_voucher.number_of_days
                        update_subscription = subscriptions.objects.get(username = username)
                        end_date = update_subscription.end_date
                        new_end_date = datetime.now() + timedelta(days)
                        update_subscription.end_date = new_end_date
                        update_subscription.save()
                    except:
                        create_subscription = subscriptions(username = username ,
                                                            start_date = current_date ,
                                                            end_date = end_date,
                                                            voucher_number = voucher_code_input)
                        create_subscription.save()

                    check_voucher.is_active = 0
                    check_voucher.used_by = request.user.username
                    check_voucher.save()
                    data_return = {'status': 'success', 'message': 'Question Set Activated'}

            return HttpResponse(json.dumps(data_return), content_type='application/json')
        else:
            data_return = {'status': 'fail', 'message': 'Kindly Login for activation'}
            return HttpResponse(json.dumps(data_return), content_type='application/json')
    else:
        return render(request, 'sample.html')