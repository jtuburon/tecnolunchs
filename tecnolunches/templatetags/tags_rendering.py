from django import template
from django.contrib.auth.decorators import login_required
from ..models import GeneralConfiguration, MenuItem
from ..models import TransporterGroup, TransporterGroupMember
from ..models import QueueMember, MainQueueMember, ExtraQueueMember

register = template.Library()

@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('groups_main.html', takes_context=True)
def show_groups_main(context):    
	return {}


@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('groups_list.html', takes_context=True)
def show_groups_list(context):
	groups = TransporterGroup.objects.order_by('-assigned_date')[:5]    
	return {'groups': groups}

@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('group_detail.html', takes_context=True)
def show_group_details(context, group_id):   
	return get_group_details(group_id)

def get_group_details(group_id):
	if group_id == -1:
		groups = TransporterGroup.objects.order_by('-assigned_date')		
		group = groups[0] if len(groups)>0 else None
	else:
		group = TransporterGroup.objects.get(pk=group_id)
	members_list = group.members.all() if group !=None else None
	return {'members_list': members_list}

@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('menues_list.html', takes_context=True)
def show_menues_list(context):
	menues = MenuItem.objects.order_by('-status', 'name')    
	return {'menues': menues}

@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('menu_item_form.html', takes_context=True)
def show_menu_form(context, menu):		
	return {"menu": menu}

def load_config():
	try:
		config = GeneralConfiguration.objects.get(pk=1)
	except:
		config = GeneralConfiguration();
		config.id=1
		config.save()
	return config


@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('general_settings.html', takes_context=True)
def show_general_settings(context):	
	config= load_config()
	print config
	return {'config': config}


@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('members_list.html', takes_context=True)
def show_members_list(context):
	print "Helllo"
	members = QueueMember.objects.order_by('member_type', 'user')    
	return {'members': members}

@login_required(login_url='/tecnolunches/')
@register.inclusion_tag('reqs_menues_list.html', takes_context=True)
def show_reqs_menues_list(context):
	menues = MenuItem.objects.order_by('-status', 'name')    
	return {'menues': menues}