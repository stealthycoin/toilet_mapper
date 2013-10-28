from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.home', name='home'),
                       url(r'^query/get/$', 'middletier.views.get', name='middletierget'),
                       url(r'^query/put/$', 'middletier.views.put', name='middletierput'),
                       url(r'^toilet/(\d+)$', 'toilet.views.single_toilet_view', name='single_toilet_view'),
                       url(r'^nearby$', 'toilet.views.list_toilet_view', name='list_restroom'),
                       url(r'^signin$', 'main.views.signin', name='signin'), 
                       url(r'^signup$', 'main.views.create_user', name='create'),
                       url(r'^signed-up$', 'main.views.signed_up', name='create'),
                       url(r'^gmap$', 'main.views.gmap', name='gmap_test'),
                       #url(r'^profile$', 'main.views.profile', name='user_profile'),
                       url(r'^profile/(\w+)$', 'main.views.profile', name='user_profile'),
                       url(r'^addrestroom$', 'main.views.add_restroom', name='add_restroom'),
                       
# API Section
               # Toilet API
                       url(r'^api/toilet/create/$', 'toilet.middletier.add', name='api_toilet_create'),
                       url(r'^api/toilet/retrieve/$', 'toilet.middletier.listing', name='api_toilet_retrieve'),

               # Review API
                       url(r'^api/review/create/$', 'review.middletier.add', name='api_review_create'),
                       url(r'^api/review/upvote/$', 'review.middletier.upvote', name='api_review_upvote'),
                       url(r'^api/review/downvote/$', 'review.middletier.downvote', name='api_review_downvote'),
                       url(r'^api/review/retrieve/$', 'review.middletier.get', name='api_review_retrieve'),

               # User API
                       url(r'^api/user/login/$', 'common.middletier.login', name='signin'), 
                       url(r'^api/user/logout/$', 'common.middletier.logout', name='signin'), 
                       url(r'^api/user/create/$', 'common.middletier.create_user', name='signin'), 

               # Flag API
                       url(r'^api/flag/retrieve_rankings/$', 'toilet.middletier.flag_retrieve_rankings', name='api_flag_rankings'),
                       url(r'^api/flag/retrieve_flags/$', 'toilet.middletier.flag_retrieve_flags', name='api_flag_flags'),
                       url(r'^api/flag/upvote/$', 'toilet.middletier.flag_upvote', name='api_flag_upvote'),
                       url(r'^api/flag/downvote/$', 'toilet.middletier.flag_downvote', name='api_flag_downvote'),

    # Examples:
    # url(r'^$', 'toilet_mapper.views.home', name='home'),
    # url(r'^toilet_mapper/', include('toilet_mapper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
