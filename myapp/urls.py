from django.conf.urls import url
from . import views
from myapp.views import signup_view,login_view, post_view, feed_view, like_view, comment_view
urlpatterns = [
    url(r'post/$', post_view),
    url(r'login/$', login_view),
    url(r'feed/$', feed_view),
    url(r'like/$', like_view),
    url(r'comment/$', comment_view),
    url(r'^$', signup_view)


]