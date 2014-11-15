from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^geckoboard/arpu', 'output.views.geckoboard_arpu', name='geckoboard_arpu'),
)
