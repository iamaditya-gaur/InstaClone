from django.conf.urls import url
from . import views
from myapp.views import signup_view,login_view
urlpatterns = [
    url(r'login/$', login_view),
    url(r'$', signup_view),

]