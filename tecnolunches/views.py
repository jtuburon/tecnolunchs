from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader
from django import template
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import TransporterGroup, TransporterGroupMember, MainQueueMember, PunishmentQueueMember, GeneralConfiguration
from templatetags.group_main import get_group_details, load_config
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import F
from django.utils import timezone

register = template.Library()

def index(request):    
    template = loader.get_template('tecnolunches/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunchs/')
def welcome(request):    
	user=request.user
	update_main_queue(user)
	generate_new_group()
	template = loader.get_template('tecnolunches/myprofile.html')
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
		group.name = "TransportGroup #" + str(TransporterGroup.objects.count() + 1)
		group.save()		
		assignables_list= get_assignable_members_list()
		assignables_count = config.group_size if len(assignables_list) >= config.group_size else len(assignables_list)
		release_busy();
		for i in range(assignables_count):
			assignables_list[i].status=1;
			assignables_list[i].save();
			member = TransporterGroupMember()
			member.transport_group= group
			member.user =assignables_list[i].user
			member.save();
	
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

def get_busy_members_list():
	return list(MainQueueMember.objects.filter(status = 1))
	
def get_current_queue():	
	return get_busy_members_list() + get_assignable_members_list()

def release_busy():
	MainQueueMember.objects.filter(status=1).update(status=0) 


@login_required(login_url='/tecnolunches/')
def groups(request):    
	template = loader.get_template('groups_main.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunches/')
def queues(request):    
	mqm_list = get_current_queue()
	template = loader.get_template('queues_main.html')
	context = RequestContext(request, {'mqm_list': mqm_list})
	return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunches/')
def admin(request):    
	config= load_config()
	template = loader.get_template('admin_main.html')
	context = RequestContext(request, {'config': config})
	return HttpResponse(template.render(context))

@login_required(login_url='/tecnolunches/')
def save_gral_settings(request, group_size):    
	config= load_config()
	config.group_size= group_size
	config.save()
	template = loader.get_template('general_settings.html')
	context = RequestContext(request, {'config': config})
	return HttpResponse(template.render(context))

def logout(request):
    auth_logout(request)
    return redirect('/tecnolunches/')

@login_required(login_url='/tecnolunches/')
def show_group_details(request, group_id):   
	return render_to_response('group_detail.html', get_group_details(group_id), context_instance=RequestContext(request));
	
@login_required(login_url='/tecnolunches/')
def today(request):    
	config= load_config()
	list = TransporterGroup.objects.filter(assigned_date=timezone.now())

	group = list[0] if len(list)>0 else None
	if group!= None:
		members = group.members.all()
		print members
	template = loader.get_template('today_main.html')
	context = RequestContext(request, {'group': group , 'members': members})
	return HttpResponse(template.render(context))