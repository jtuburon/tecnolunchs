from django.db import models

class TransporterGroup(models.Model):
	name = models.CharField(max_length=200)
	assigned_date = models.DateField('date assigned')
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
	checked_date = models.DateTimeField('datetime checked')
