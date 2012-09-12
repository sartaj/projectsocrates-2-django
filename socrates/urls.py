from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

'''
I know I could distribute urls among apps,
but really thats just more files to deal with.
put all url's in the main urls.py file.
'''

admin.autodiscover()

urlpatterns = patterns('',
	
	#admin
	url(r'^admin/', include(admin.site.urls)),

	#dev static content
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

#socrates urls
urlpatterns += patterns('socrates.views',
	url(r'^changelog/$', 'view_changelog', name='socrates_view_changelog'),
	url(r'^$', 'root_redirect', name='socrates_root_redirect'),
)

#swiki view urls
urlpatterns += patterns('swiki.views',
	url(r'^view/(?P<swiki_id>\d+)/$', 'view_swiki', name='swiki_view_swiki'),
	url(r'^edit/(?P<swiki_id>\d+)/$', 'view_edit_swiki', name='swiki_view_edit_swiki'),
	url(r'^goal/(?P<goal>[\w ]+)/$', 'view_goal', name='swiki_view_goal'),
	url(r'^topic/(?P<topic>[\w ]+)/$', 'view_topic', name='swiki_view_topic'),
	url(r'^create/$', 'view_create_swiki', name='swiki_view_create_swiki'),
	url(r'^all/$', 'view_all_swiki', name='swiki_view_all_swiki'),
	url(r'^search/(?P<term>.+)/$', 'view_search', name='swiki_view_swiki_search'),
	url(r'^achieve/$', 'view_achieve', name='swiki_view_achieve'),
)

#swiki action urls
urlpatterns += patterns('swiki.actions',
	url(r'^swiki/action/create_article/$', 'action_create_article', name='swiki_action_create_article'),
	url(r'^swiki/action/update_article/$', 'action_update_article', name='swiki_action_update_article'),
	url(r'^swiki/action/add_review/$', 'action_add_review', name='swiki_action_add_review'),
	url(r'^swiki/action/remove_review/$', 'action_remove_review', name='swiki_action_remove_review'),
	url(r'^swiki/action/add_goal/$', 'action_add_goal', name='swiki_action_add_goal'),
	url(r'^swiki/action/remove_goal_relation/$', 'action_remove_goal_relation', name='swiki_action_remove_goal_relation'),
	url(r'^swiki/action/add_topic/$', 'action_add_topic', name='swiki_action_add_topic'),
	url(r'^swiki/action/remove_topic/$', 'action_remove_topic', name='swiki_action_remove_topic'),
	url(r'^swiki/action/submit_search/$', 'action_submit_search', name='swiki_action_submit_search'),
	url(r'^swiki/action/submit_achieve_query/$', 'action_submit_achieve_query', name='swiki_action_submit_achieve_query'),
)