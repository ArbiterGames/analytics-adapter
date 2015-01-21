from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^yesterdays-dau', 'output.views.yesterdays_dau', name='yesterdays_dau'),
    url(r'^geckoboard/arpu', 'output.views.geckoboard_arpu', name='geckoboard_arpu'),
    url(r'^geckoboard/dau', 'output.views.geckoboard_dau', name='geckoboard_dau'),
    url(r'^geckoboard/revenue-total', 'output.views.geckoboard_total_revenue', name='geckoboard_total_revenue'),
    url(r'^geckoboard/revenue', 'output.views.geckoboard_revenue', name='geckoboard_revenue'),
    url(r'^geckoboard/pool-impact', 'output.views.geckoboard_pool_impact', name='geckoboard_pool_impact'),
    url(r'^geckoboard/algorithm-arpu', 'output.views.geckoboard_algorithm_arpu', name='geckoboard_algorithm_arpu'),
)
