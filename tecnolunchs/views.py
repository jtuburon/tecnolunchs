from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader
from django import template
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
register = template.Library()

def index(request):    
    template = loader.get_template('tecnolunchs/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunchs/')
def welcome(request):    
    template = loader.get_template('tecnolunchs/myprofile.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def logout(request):
    auth_logout(request)
    return redirect('/tecnolunchs/')

