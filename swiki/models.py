from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Q
import json

'''
goal depreciated
'''
class Goal(models.Model):
	name = models.CharField(max_length=150, unique=True)

	'''
	end data fields
	'''
	
	@staticmethod
	def search(term):
		try:
			return Goal.objects.filter(name__istartswith=term)
		except:
			return []
	
	'''
	end static methods
	'''

	def get_all_swikis(self):
		return self.swiki_set.all().distinct()
		
	def times_used(self):
		return self.swiki_set.count()
	
	def __unicode__(self):
		return self.name
		
class Topic(models.Model):
	name = models.CharField(max_length=150, unique=True)

	'''
	end data fields
	'''

	@staticmethod
	def search(term):
		try:
			return Topic.objects.filter(name__istartswith=term)
		except:
			return []
					
	'''
	end static methods
	'''

	def get_all_swikis(self):
		return self.swiki_set.all()
		
	def times_used(self):
		return self.swiki_set.count()
		
	def __unicode__(self):
		return self.name
	
class SWiki(models.Model):
	#action
	title = models.CharField(max_length=150)
	#object
	disambiguation = models.CharField(max_length=150)

	body = models.TextField(max_length=10000)
	goals = models.ManyToManyField('SWiki', through='GoalSwikiRelationship', related_name='goaled')
	#goals_straight = models.ManyToManyField('SWiki', related_name='goaled_straight')
	goals_count = models.ManyToManyField('SWiki', through='GoalSwikiRelationshipCount', related_name='goaled_count')
	topics = models.ManyToManyField(Topic)

	'''
	end data fields
	'''

	@staticmethod
	def get_article(id):
		try:
			return SWiki.objects.get(pk=id)
		except:
			return None

	@staticmethod
	def get_article(action, obj):
		try:
			return SWiki.objects.get(title=action, disambiguation=obj)
		except:
			return None
	
	@staticmethod
	def create(title, body, disambiguation):
		try:
			sw = SWiki.objects.get(title=title, disambiguation=disambiguation)
		except:
			pass
		else:
			return {
				'success': False,
				'message': 'A Swiki with this name and disambiguation alread exists, you should probably check that one first.',
				'url': reverse('swiki_view_swiki', args=[sw.id])
			}

		sw = SWiki(title=title, body=body, disambiguation=disambiguation)
		sw.save()

		return {
			'success': True,
			'message': 'Swiki was created.',
			'url': sw.get_url(),
		}

	@staticmethod
	def search(term, goals=[], topics=[]):
		try:
			return SWiki.objects.filter(Q(goals__in=goals) | Q(topics__in=topics) | Q(title__istartswith=term) | Q(disambiguation__istartswith=term)).distinct()
			
		except:
			return []

	'''
	end static methods
	'''

	def get_display_title(self):
		return '%s %s' % (self.title, self.disambiguation)

	def get_url(self):
		return reverse('swiki_view_swiki', args=[self.id])
			
	def update(self, title, body, disambiguation):		
		self.title = title
		self.body = body
		self.disambiguation = disambiguation
		self.save()
		return {
			'success': True,
			'message': 'Article Body was Updated.'
		}
	
	def add_review(self, title, body):		
		review = ReviewBox(title=title, body=body)
		review.swiki = self
		review.save()

		return {
			'success': True,
			'message': 'Review was added.'
		}
			
	def add_topic(self, topic_text):
		try:
			topic = Topic.objects.get(name=topic_text)
			
		except:				
			topic = Topic(name=topic_text)
			topic.save()
			
		self.topics.add(topic)

		return {
			'success': True,
			'message': 'Topic Was added.',
			'topic': topic.name,
			'url': reverse('swiki_view_topic', args=[topic.name]),
		}

	def remove_topic(self, topic_id):
		try:
			topic = Topic.objects.get(pk=topic_id)
			self.topics.remove(topic)
		except:
			return {'success': False, 'message': 'Topic was not removed.'}
			
		else:
			return {'success': True, 'message': 'Topic was removed.'}
	
	def add_goal(self, goal_action, goal_object, body, correlation):
		try:
			goal = SWiki.objects.get(title=goal_action, disambiguation=goal_object)
		except:				
			goal = SWiki(title=goal_action, disambiguation=goal_object, body='')
			goal.save()
			
		relation = GoalSwikiRelationship(swiki=self, goal=goal, body=body, correlation=correlation)
		relation.save()

		try:
			relation_count = GoalSwikiRelationshipCount.objects.get(swiki=self, goal=goal, correlation=correlation)
			relation_count.count += 1
			relation_count.save()
		except:
			relation_count = GoalSwikiRelationshipCount(swiki=self, goal=goal, correlation=correlation, count=1)
			relation_count.save()

		return {
			'success': True,
			'message': 'Goal Was added.'
		}
		
	def get_goal_relations(self):
		return GoalSwikiRelationship.objects.filter(swiki=self)

	def get_positive_correlation_goal_relations(self):
		return GoalSwikiRelationship.objects.filter(swiki=self, correlation='positive')

	def get_negative_correlation_goal_relations(self):
		return GoalSwikiRelationship.objects.filter(swiki=self, correlation='negative')

	'''
	returns ways to achieve me
	'''
	def achieve_me(self):
		return GoalSwikiRelationshipCount.objects.filter(goal=self, correlation='positive').order_by('count')
	
	def __unicode__(self):
		return self.get_display_title()

class GoalSwikiRelationship(models.Model):
	swiki = models.ForeignKey(SWiki, related_name='swiki')
	goal = models.ForeignKey(SWiki, related_name='goal')
	body = models.CharField(max_length=1500)

	correlation_choices = (
		('positive', 'positive'),
		('negative', 'negative')
	)

	correlation = models.CharField(max_length=50, choices=correlation_choices)

	'''
	end data fields
	'''

	def get_goals_for_swiki(self, swiki):
		return GoalSwikiRelationship.objects.filter(swiki=swiki)

	@staticmethod
	def remove_relation(id):
		try:
			relation = GoalSwikiRelationship.objects.get(pk=id)
			relation.delete()
		except:
			return {
				'success':False,
				'message': 'Unable to remove goal relation'
			}

		else:
			return {
				'success':True,
				'message': 'Goal relation removed'
			}

	def __unicode__(self):
		return '%s -> %s' % (self.swiki.get_display_title(), self.goal.get_display_title())

class GoalSwikiRelationshipCount(models.Model):
	swiki = models.ForeignKey(SWiki, related_name='swiki_count')
	goal = models.ForeignKey(SWiki, related_name='goal_count')
	count = models.IntegerField()

	correlation_choices = (
		('positive', 'positive'),
		('negative', 'negative')
	)

	correlation = models.CharField(max_length=50, choices=correlation_choices)

	'''
	end data fields
	'''

	def __unicode__(self):
		return '%s -> %s (%s)' % (self.swiki.get_display_title(), self.goal.get_display_title(), self.count) 

		
class ReviewBox(models.Model):
	swiki = models.ForeignKey(SWiki, related_name='reviews')
	body = models.TextField()
	title = models.CharField(max_length=150)

	'''
	end data fields
	'''

	@staticmethod
	def remove(id):
		try:
			ReviewBox.objects.get(pk=id).delete()
			return {'success':True, 'message': 'Review was removed'}
		except:
			return {'success':False, 'message': 'Review was not removed'}

	'''
	end static fields
	'''

	def __unicode__(self):
		return self.title
