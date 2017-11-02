from django.conf.urls import url

from .views import LoginView, CheckTokenView, logout_view, ProfileView

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^(?P<token>[a-z0-9\-]+)$', CheckTokenView.as_view(), name='token'),
    url(r'logout/$', logout_view, name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]