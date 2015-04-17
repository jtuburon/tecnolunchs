from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader
from django import template
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import TransporterGroup, TransporterGroupMember, MainQueueMember, PunishmentQueueMember, GeneralConfiguration
from templatetags.group_main import get_group_details 
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import F
from django.utils import timezone

register = template.Library()

def index(request):    
    template = loader.get_template('tecnolunchs/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunchs/')
def welcome(request):    
	user=request.user
	update_main_queue(user)
	generate_new_group()
	template = loader.get_template('tecnolunchs/myprofile.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def update_main_queue(user):
	mqm_list = MainQueueMember.objects.filter(user=user) 
	mqm = mqm_list[0] if len(mqm_list) >0 else None
	if mqm == None:
		mqm = MainQueueMember()
		mqm.user = user;
		mqm_busy_list = MainQueueMember.objects.filter(status = 1) 
		mqm_first= mqm_busy_list[0] if len(mqm_busy_list)>0 else None
		if mqm_first != None:
			mqm.order= mqm_first.order 
			MainQueueMember.objects.filter(id__gte= mqm_first.id).update(order= F('order') +1)
		else:
			mqm.order= 1			
		mqm.save()

def generate_new_group():
	mqm_list = TransporterGroup.objects.filter(assigned_date=timezone.now())
	if len(mqm_list)==0:
		config = load_config()
		group= TransporterGroup()
		group.name = "TransportGroup #" + str(len(mqm_list) + 1)
		group.save()		
		assignables_list= get_assignable_members_list()
		assignables_count = config.group_size if len(assignables_list) >= config.group_size else len(assignables_list)
		release_busy();
		for i in range(assignables_count):
			assignables_list[i].status=1;
			assignables_list[i].save();
	
def get_assignable_members_list():
	mqm_busy_list = MainQueueMember.objects.filter(status = 1) 
	mqm_busy_first= mqm_busy_list[0] if len(mqm_busy_list)>0 else None
	mqm_busy_last= mqm_busy_list[len(mqm_busy_list)-1] if len(mqm_busy_list)>0 else None
	print "first"
	print mqm_busy_first
	print "last"
	print mqm_busy_last
	if(mqm_busy_first!= None and mqm_busy_last!=None):
		first_list= MainQueueMember.objects.filter(id__gt= mqm_busy_last.id)
		last_list= MainQueueMember.objects.filter(id__lt= mqm_busy_first.id)
		return list(first_list) + list(last_list)
	else:
		return MainQueueMember.objects.all();
	

def release_busy():
	MainQueueMember.objects.filter(status=1).update(status=2) 

def load_config():
	config = GeneralConfiguration.objects.get(pk=1)
	if config == None:
		config = GeneralConfiguration();
		config.id=1
		config.save()
	return config


@login_required(login_url='/tecnolunchs/')
def groups(request):    
	template = loader.get_template('groups_main.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunchs/')
def queues(request):    
	mqm_list = MainQueueMember.objects.all() 
	template = loader.get_template('queues_main.html')
	context = RequestContext(request, {'mqm_list': mqm_list})
	return HttpResponse(template.render(context))


def logout(request):
    auth_logout(request)
    return redirect('/tecnolunchs/')

@login_required(login_url='/tecnolunchs/')
def show_group_details(request, group_id):   
	return render_to_response('group_detail.html', get_group_details(group_id), context_instance=RequestContext(request));
	