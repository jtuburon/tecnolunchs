from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader
from django import template
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from models import GeneralConfiguration, MenuItem
from models import TransporterGroup, TransporterGroupMember
from models import QueueMember, MainQueueMember, ExtraQueueMember

from templatetags.tags_rendering import get_group_details, load_config
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

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
	try:
		qm= QueueMember.objects.get(user=user)
	except:
		qm = QueueMember(user= user);
		qm.save()
		mqm = MainQueueMember(member= qm)		
		mqm_busy_list =MainQueueMember.objects.filter(status = 1).order_by('order')
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
			mqm = TransporterGroupMember()
			mqm.transport_group= group
			mqm.member =assignables_list[i].member
			mqm.save();
	
def get_assignable_members_list():
	mqm_busy_list = MainQueueMember.objects.filter(status = 1) 
	mqm_busy_first= mqm_busy_list[0] if len(mqm_busy_list)>0 else None
	mqm_busy_last= mqm_busy_list[len(mqm_busy_list)-1] if len(mqm_busy_list)>0 else None
	print "first"
	print mqm_busy_first
	print "last"
	print mqm_busy_last
	if(mqm_busy_first!= None and mqm_busy_last!=None):
		first_list= MainQueueMember.objects.filter(order__gt= mqm_busy_last.order)
		last_list= MainQueueMember.objects.filter(order__lt= mqm_busy_first.order)
		return list(first_list) + list(last_list)
	else:		
		return list(MainQueueMember.objects.all());

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
	pqm_list=[]
	tqm_list=[]
	template = loader.get_template('queues_main.html')	
	context = RequestContext(request, {'mqm_list': mqm_list, 'pqm_list': pqm_list, 'tqm_list': tqm_list})
	return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunches/')
def menues(request):    	
	template = loader.get_template('menues_main.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

@login_required(login_url='/tecnolunches/')
def set_menu_availability(request, menu_id, menu_status):    	
	menu_status= json.loads(menu_status)	
	menu = MenuItem.objects.get(pk=menu_id);
	menu.status = menu_status
	menu.save();
	msg= "This menu is now available!" if menu_status else "This menu is now unavailable!"	
	response_data= {"status": True, "msg": msg}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/tecnolunches/')
@csrf_exempt
def save_menu(request):    	
	name = request.POST.get("name", "")
	menu_id = request.POST.get("menu_item", "")
	try:
		menu = MenuItem.objects.get(pk=menu_id);
		menu.name= name
		msg = "MenuItem was sucesfully created!!"
	except:
		menu = MenuItem(name= name);	
		msg = "MenuItem was sucesfully updated!!"
	menu.save();
	response_data= {"status": True, "msg": msg}
	return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url='/tecnolunches/')
def find_menu(request, menu_id):    		
	try:
		menu = MenuItem.objects.get(pk=menu_id);		
	except:		
		menu = None	
	template = loader.get_template('menu_item_form.html')
	context = RequestContext(request, {'menu': menu})
	return HttpResponse(template.render(context))


@login_required(login_url='/tecnolunches/')
def new_menu(request):    		
	template = loader.get_template('menu_item_form.html')
	context = RequestContext(request, {'menu': None})
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

@login_required(login_url='/tecnolunches/')
def set_groupmember_accomplishment(request, group_member_id, group_member_status):    	
	group_member_status= json.loads(group_member_status)	
	member = TransporterGroupMember.objects.get(pk=group_member_id);
	member.status = 3 if group_member_status else 4
	member.save();
	msg= "This member accomplished!" if group_member_status else "This member didn't acomplish!!"	
	response_data= {"status": True, "msg": msg}
	return HttpResponse(json.dumps(response_data), content_type="application/json")
