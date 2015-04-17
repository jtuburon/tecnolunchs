from django.db import models

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
	user = models.ForeignKey('auth.user')
	TGM_STATUSES = (
		(1, 'ASSIGNED'),
		(2, 'CHECKED'),
		(3, 'DONE'),
		(4, 'UNDONE')
	)
	status = models.IntegerField(choices=TGM_STATUSES, default=1)
	checked_date = models.DateTimeField('datetime checked', auto_now_add=True)

class MainQueueMember(models.Model):
	user = models.ForeignKey('auth.user')
	order = models.IntegerField()
	MQM_STATUSES = (		
		(0, 'FREE'),
		(1, 'BUSY'),
	)
	status = models.IntegerField(choices=MQM_STATUSES, default=0)
	registration_date = models.DateField('date registered', auto_now_add=True)

class PunishmentQueueMember(models.Model):
	user = models.ForeignKey('auth.user')
	order = models.IntegerField()
	PQM_STATUSES = (		
		(0, 'RELEASED'),
		(1, 'PUNISHED'),
	)
	status = models.IntegerField(choices=PQM_STATUSES, default=1)
	registration_date = models.DateField('date registered', auto_now_add=True)
	
	USER_TYPES = (		
		(1, 'PERMANENT'),
		(2, 'TEMPORARY'),
	)
	member_type = models.IntegerField(choices=USER_TYPES, default=1)

class GeneralConfiguration(models.Model):
	group_size = models.IntegerField(default=3)