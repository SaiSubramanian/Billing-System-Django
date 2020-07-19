from django.conf.urls import url
from bPay import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^adminLogin/$', views.AdminLoginPageView.as_view()),
    url(r'^accountantCreation/$', views.AccountantCreationPageView.as_view()),
    url(r'^adminAuth', views.adminAuth, name='authAdmin'),
    url(r'^accountantAuth', views.accountantAuth, name='authAccountant'),
    url(r'^adminHome', views.route2adminHome, name='adminHome'),
    url(r'^accountantHome', views.route2accountantHome, name='accountantHome'),
    url(r'^createAccountant', views.createAccountant, name='createAccountant'),
    url(r'^adminGetDetails', views.adminGetDetails, name='getDetailsA1')
]