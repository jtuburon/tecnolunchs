from django import template
from django.contrib.auth.decorators import login_required
from ..models import TransporterGroup, TransporterGroupMember, MainQueueMember, PunishmentQueueMember, GeneralConfiguration

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
