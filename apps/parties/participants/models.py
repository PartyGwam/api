from django.db import models


class Participant(models.Model):
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'participants'
