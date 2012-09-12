from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse


def view_changelog(request):
	return render_to_response('socrates/changelog.html', {}, context_instance=RequestContext(request))

def root_redirect(request):
	return HttpResponseRedirect( reverse('swiki_view_all_swiki', args=[]) )