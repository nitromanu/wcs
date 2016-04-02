from django.conf.urls import patterns, include, url
from django.contrib import admin
from ninja1 import views
from quiz import views as quiz_views
from result import views as result_views
from subscription import views as subscription_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wwcs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.home),
                       url(r'^register/$', views.render_register),
                       url(r'^login/$', views.user_login),
                       url(r'^home/$', views.user_home),
                       url(r'^account/$', views.user_account),
                       url(r'^logout/$', views.user_logout),
                       url(r'^attempt/$',quiz_views.attempt_quiz),
                       url(r'^submit/$',quiz_views.get_student_response),
                       url(r'^result/(\S+)/$', result_views.display_result),
                       url(r'^vpay/$', subscription_views.payment_voucher_ajax_request),
                       url(r'^vcreate/$', subscription_views.create_vouchers),
                       url(r'^pdf/$', result_views.pdf_try),

)
