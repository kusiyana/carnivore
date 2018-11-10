from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
	    url(r'^lion/$', views.lion, name='lion'),
	    url(r'^lion/showPrides/$', views.showPrides, name='show_prides'),
	    url(r'^lion/showLions/$', views.showLions, name='show_lions'),
	    url(r'^lion/deleteAll/$', views.deleteAll, name='delete_all'),
	    url(r'^lion/initialise/$', views.initialise, name='initialise'),
	    url(r'^lion/initialise2/$', views.initialise2, name='initialise2'),
	    url(r'^lion/runSimulation/$', views.runSimulation, name='run_simulation'),
	    url(r'^lion/viewSimulation/$', views.viewSimulation, name='view_simulation'),
	    url(r'^lion/ajaxTrajectories/(?P<elapsedTime>\w+)$', views.ajaxTrajectories, name='ajax_trajectories'),

	    url(r'^lion/buildLionsFromShapefiles/(?P<shapefileIndex>\w+)$', views.buildLionsFromShapefiles, name='build_lions_from_shapefiles'),
	    url(r'^lion/viewTrajectories/(?P<elapsedTime>\w+)/$', views.viewTrajectories, name='view_trajectories'),
    	url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    	url(r'^add_page/$', views.add_page, name='add_page'), # NEW MAPPING!
    	url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'), # New!
        url(r'^add_page/(?P<category_name_url>\w+)', views.add_page, name='add_page')
#		url(r'^add_page/(?P<page_name_url>\w+)/$/$', views.add_page, name='add_page')
        )
        
