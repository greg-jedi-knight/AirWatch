from django.db import models
from accounts.models import Account

class Project(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(Account, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name