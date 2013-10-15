from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.views.home', name='home'),
                       url(r'^query/get/$', 'middletier.views.get', name='middletierget'),
                       url(r'^query/put/$', 'middletier.views.put', name='middletierput'),
                       url(r'^toilet/(\d+)$', 'main.views.single_toilet_view', name='single_toilet_view'),
		       url(r'^signin$', 'main.views.signin', name='signin'), 
		       url(r'^create$', 'main.views.create', name='create'),
                       url(r'^gmap$', 'main.views.gmap', name='gmap test'),
		       url(r'^addrestroom$', 'main.views.add_restroom', name='add_restroom'),


    # Examples:
    # url(r'^$', 'toilet_mapper.views.home', name='home'),
    # url(r'^toilet_mapper/', include('toilet_mapper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
