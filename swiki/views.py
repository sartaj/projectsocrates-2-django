from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from swiki.models import *
import json
from django import forms
from django.template import RequestContext
	
def view_search(request, term):
	goals = Goal.search(term)
	topics = Topic.search(term)
	swikis = SWiki.search(term, goals, topics)
	empty = not goals and not topics and not swikis
	
	render_vars = {
		'term': term,
		'goals': goals,
		'topics': topics,
		'swikis': swikis, 
		'empty': empty,
	}
	
	return render_to_response('swiki/search.html', render_vars, context_instance=RequestContext(request))

def view_swiki(request, swiki_id):
	article = get_object_or_404(SWiki, pk=swiki_id)
	
	render_vars = {
		'article': article,
		'editable': False,
	}
	
	return render_to_response('swiki/view.html', render_vars, context_instance=RequestContext(request))

def view_edit_swiki(request, swiki_id):
	article = get_object_or_404(SWiki, pk=swiki_id)
	
	render_vars = {
		'article': article,
		'editable': True,
	}
	
	return render_to_response('swiki/view.html', render_vars, context_instance=RequestContext(request))
		
def view_create_swiki(request):
	return render_to_response('swiki/create.html', {}, context_instance=RequestContext(request))

def view_achieve(request):
	return render_to_response('swiki/achieve.html', {}, context_instance=RequestContext(request))

def view_all_swiki(request):
	render_vars = {
		'articles': SWiki.objects.all(),
	}

	return render_to_response('swiki/view_all.html', render_vars, context_instance=RequestContext(request))
	
def view_goal(request, goal):
	
	try:
		goal = Goal.objects.get(name=goal)
		goal_exists = True
	except:
		goal_exists = False
		swikis = None
		
	render_vars = {
		'goal': goal,
		'goal_exists': goal_exists,
	}
	
	return render_to_response('swiki/goal.html', render_vars, context_instance=RequestContext(request))

'''
depreciated
'''
def view_topic(request, topic):
	
	try:
		topic = Topic.objects.get(name=topic)
		topic_exists = True
	except:
		topic_exists = False
		swikis = None
		
	render_vars = {
		'topic': topic,
		'topic_exists': topic_exists,
	}
	
	return render_to_response('swiki/topic.html', render_vars, context_instance=RequestContext(request))