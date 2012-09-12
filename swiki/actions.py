from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from swiki.models import *
import json
from django import forms
from django.template import RequestContext

'''
create/edit swiki
'''
class SwikiDataForm(forms.Form):
	#not required because used with updaet_article()
	article_id = forms.IntegerField(required=False)

	article_title = forms.RegexField(
		min_length=2,
		max_length=40,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Title is Invalid.',
			'required': 'Title is Required',
			'min_length': 'Title is too short',
			'max_length': 'Title is too long',
		}
	)

	article_disambiguation = forms.RegexField(
		min_length=2,
		max_length=40,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Disambiguation is Invalid.',
			'required': 'Disambiguation is Required',
			'min_length': 'Disambiguation is too short',
			'max_length': 'Disambiguation is too long',
		}
	)

	article_body = forms.CharField(
		min_length=5,
		max_length=100000,
		error_messages={
			'invalid': 'Body is Invalid.',
			'required': 'Body is Required',
			'min_length': 'Body is too short',
			'max_length': 'Body is too long',
		}
	)

def action_create_article(request):

	form = SwikiDataForm(request.POST)

	if form.is_valid():
		response = SWiki.create(
			title=form.cleaned_data['article_title'],
			body=form.cleaned_data['article_body'],
			disambiguation=form.cleaned_data['article_disambiguation']
		)

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }

	return HttpResponse( json.dumps(response) )

def action_update_article(request):

	form = SwikiDataForm(request.POST)

	if form.is_valid():
		try:
			swiki = SWiki.objects.get(pk=form.cleaned_data['article_id'])

			response = swiki.update(
				title=form.cleaned_data['article_title'],
				body=form.cleaned_data['article_body'],
				disambiguation=form.cleaned_data['article_disambiguation']
			)
		except:
			response = {'success': False, 'message': 'error updating article'}

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

'''
add/remove reviews
'''
class AddReviewForm(forms.Form):
	article_id = forms.IntegerField(required=False)

	review_title = forms.RegexField(
		min_length=2,
		max_length=40,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Review Title is Invalid.',
			'required': 'Review Title is Required',
			'min_length': 'Review Title is too short',
			'max_length': 'Review Title is too long',
		}
	)

	review_body = forms.CharField(
		min_length=10,
		max_length=2000,
		error_messages={
			'invalid': 'Review Body is Invalid.',
			'required': 'Review Body is Required',
			'min_length': 'Review Body is too short',
			'max_length': 'Review Body is too long',
		}
	)

def action_add_review(request):

	form = AddReviewForm(request.POST)

	if form.is_valid():
		try:
			swiki = SWiki.objects.get(pk=form.cleaned_data['article_id'])

			response = swiki.add_review(
				title=form.cleaned_data['review_title'],
				body=form.cleaned_data['review_body']
			)
		except:
			response = {'success': False, 'message': 'error adding review'}

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

class RemoveReviewForm(forms.Form):
	review_id = forms.IntegerField(required=True)

def action_remove_review(request):

	form = RemoveReviewForm(request.POST)

	if form.is_valid():
		response = ReviewBox.remove(id=form.cleaned_data['review_id'])

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

'''
add/remove goals
'''
class AddGoalForm(forms.Form):
	article_id = forms.IntegerField(required=True)

	goal_action = forms.RegexField(
		min_length=2,
		max_length=40,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Goal Action is Invalid.',
			'required': 'Goal Action is Required',
			'min_length': 'Goal Action is too short',
			'max_length': 'Goal Action is too long',
		}
	)

	goal_object = forms.RegexField(
		min_length=2,
		max_length=40,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Goal Object is Invalid.',
			'required': 'Goal Object is Required',
			'min_length': 'Goal Object is too short',
			'max_length': 'Goal Object is too long',
		}
	)

	goal_reason = forms.CharField(
		min_length=5,
		max_length=1500,
		error_messages={
			'invalid': 'Body is Invalid.',
			'required': 'Body is Required',
			'min_length': 'Body is too short',
			'max_length': 'Body is too long',
		}
	)

	correlation_choices = (
		('positive', 'positive'),
		('negative', 'negative')
	)

	goal_correlation = forms.ChoiceField(choices=correlation_choices)

def action_add_goal(request):

	form = AddGoalForm(request.POST)

	if form.is_valid():
		try:
			swiki = SWiki.objects.get(pk=form.cleaned_data['article_id'])
			response = swiki.add_goal(form.cleaned_data['goal_action'], form.cleaned_data['goal_object'], form.cleaned_data['goal_reason'], form.cleaned_data['goal_correlation'])
		except:
			response = {'success': False, 'message': 'error adding goal'}

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))


class RemoveGoalRelationForm(forms.Form):
	relation_id = forms.IntegerField(required=True)

def action_remove_goal_relation(request):

	form = RemoveGoalRelationForm(request.POST)

	if form.is_valid():
		response = GoalSwikiRelationship.remove_relation(form.cleaned_data['relation_id'])

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

'''
add/remove topic
'''
class AddTopicForm(forms.Form):
	article_id = forms.IntegerField(required=True)

	topic_title = forms.RegexField(
		min_length=2,
		max_length=30,
		regex=r'^[a-zA-Z0-9-_ ]+$',
		error_messages={
			'invalid': 'Topic is Invalid.',
			'required': 'Topic is Required',
			'min_length': 'Topic is too short',
			'max_length': 'Topic is too long',
		}
	)

def action_add_topic(request):

	form = AddTopicForm(request.POST)

	if form.is_valid():
		try:
			swiki = SWiki.objects.get(pk=form.cleaned_data['article_id'])
			response = swiki.add_topic(form.cleaned_data['topic_title'])
		except:
			response = {'success': False, 'message': 'error adding topic'}

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

class RemoveTopicForm(forms.Form):
	topic_id = forms.IntegerField(required=True)
	article_id = forms.IntegerField(required=True)

def action_remove_topic(request):

	form = RemoveTopicForm(request.POST)

	if form.is_valid():
		try:
			swiki = SWiki.get_article(form.cleaned_data['article_id'])
			response = swiki.remove_topic(form.cleaned_data['topic_id'])
		except:
			response = {'success': False, 'message': 'Unable to remove topic'} 

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }
		
	return HttpResponse(json.dumps(response))

'''
search
'''
class SubmitSearchForm(forms.Form):
	query = forms.CharField(max_length=150)

def action_submit_search(request):
	form = SubmitSearchForm(request.POST)

	if form.is_valid():
		response = {'success': True, 'url': reverse('swiki_view_swiki_search', args=[form.cleaned_data['query']])}

	else:
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }

	return HttpResponse(json.dumps(response))

'''
achieve query
'''

class AchieveQueryForm(forms.Form):

	action = forms.CharField(
		min_length=1,
		max_length=100,
		error_messages={
			'invalid': 'Action is Invalid.',
			'required': 'Action is Required',
			'min_length': 'Action is too short',
			'max_length': 'Action is too long',
		}
	)

	object = forms.CharField(
		min_length=1,
		max_length=100,
		error_messages={
			'invalid': 'Object is Invalid.',
			'required': 'Object is Required',
			'min_length': 'Object is too short',
			'max_length': 'Object is too long',
		}
	)

def action_submit_achieve_query(request):
	form = AchieveQueryForm(request.POST)

	if not form.is_valid():
		first_error_message = form.errors.items()[0][1][0]
		response = {'success': False, 'message': first_error_message }

	else:
		base_article = SWiki.get_article(action=form.cleaned_data['action'], obj=form.cleaned_data['object'])

		if base_article is None:
			response = {'success': False, 'message': 'Aticle not found.'}

		else:
			relations = base_article.achieve_me()
			print relations

			response = {
				'success': True,
				'message': 'successful',
				'article_title': base_article.get_display_title(),
				'article_url': base_article.get_url(), 
			} 

			response['paths'] = [
				{
					'title': relation.swiki.get_display_title(),
					'action': relation.swiki.title,
					'object': relation.swiki.disambiguation,
					'url': relation.swiki.get_url(),
					'count': relation.count,
				}
				for relation in relations] 


	return HttpResponse(json.dumps(response))