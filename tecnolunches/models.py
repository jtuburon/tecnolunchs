from django.db import models

class GeneralConfiguration(models.Model):
	group_size = models.IntegerField(default=1)
	final_time = models.TimeField(default='10:00:00')

class MenuItem(models.Model):
	name = models.CharField(max_length=200)
	assigned_date = models.DateField('date assigned', auto_now_add=True)
	MENU_ITEM_STATUSES = (		
		(0, 'NOT AVAILABE'),
		(1, 'AVAILABLE'),
	)
	status = models.IntegerField(choices=MENU_ITEM_STATUSES, default=0)

class QueueMember(models.Model):
	#user = models.ForeignKey('auth.user')	
	user= models.OneToOneField('auth.user', primary_key=True)
	USER_TYPES = (		
		(1, 'PERMANENT'),
		(2, 'TEMPORARY'),
	)
	member_type = models.IntegerField(choices=USER_TYPES, default=1)

class TransporterGroup(models.Model):
	name = models.CharField(max_length=200)
	assigned_date = models.DateField('date assigned', auto_now_add=True)
	TG_STATUSES = (
		(1, 'ASSIGNED'),
		(2, 'DONE')
	)
	status = models.IntegerField(choices=TG_STATUSES, default=1)

class TransporterGroupMember(models.Model):
	transport_group = models.ForeignKey('TransporterGroup', related_name='members')
	member = models.ForeignKey('QueueMember')
	TGM_STATUSES = (
		(1, 'ASSIGNED'),
		(2, 'CHECKED'),
		(3, 'DONE'),
		(4, 'UNDONE')
	)
	status = models.IntegerField(choices=TGM_STATUSES, default=1)
	checked_date = models.DateTimeField('datetime checked', auto_now_add=True)



class MainQueueMember(models.Model):	
	member= models.OneToOneField('QueueMember', primary_key=True)
	order = models.IntegerField()
	MQM_STATUSES = (		
		(0, 'FREE'),
		(1, 'BUSY'),
	)
	status = models.IntegerField(choices=MQM_STATUSES, default=0)
	registration_date = models.DateField('date registered', auto_now_add=True)

class ExtraQueueMember(models.Model):
	member = models.ForeignKey('QueueMember')	
	order = models.IntegerField()
	EQM_STATUSES = (		
		(0, 'FREE'),
		(1, 'BUSY'),
	)
	EQM_TYPES = (		
		(1, 'TEMPORARY'),
		(2, 'PUNISHMENT'),
	)	
	status = models.IntegerField(choices=EQM_STATUSES, default=1)
	member_type = models.IntegerField(choices=EQM_TYPES, default=1)
	registration_date = models.DateField('date registered', auto_now_add=True)