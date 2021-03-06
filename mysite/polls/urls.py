from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^(?P<question_id>[0-9]+)/$", views.detail, name='detail'),
    url(r"^(?P<question_id>[0-9]+)/results/$",views.results, name='results'),
    url(r"^(?P<question_id>[0-9]+)/vote/$", views.vote, name='vote'),
    url(r"^get_data/$", views.get_data, name='get_data'),
    url(r"^get_sr_data/$",views.get_sr_data,name='get_sr_data'),
]
