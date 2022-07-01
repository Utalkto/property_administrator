from django.db import models

from register.models import CustomUser
from properties.models import Unit


class Candidate(models.Model):
    # foreign keys
    
    property_manager = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=False, blank=False, on_delete=models.CASCADE)
    
    # ---------------------------------
    # fields
    
    availability_date = models.JSONField(null=False) 
    adults_information = models.JSONField(null=False) # there can be more than one adult 
    
    current_address = models.CharField(max_length=400, null=False)
    current_landlord_name = models.CharField(max_length=100, null=False)
    current_landlord_phone = models.CharField(max_length=100, null=False)
    
    duration_of_lease = models.CharField(max_length=25, null=False)
    
    expected_renting_duration = models.CharField(null=False, max_length=100)
    
    family_income = models.CharField(max_length=50)
    facebook_account = models.CharField(max_length=500, default='')
    
    length_of_time_at_current_address = models.CharField(max_length=400)
    link_to_schedule_view_sent = models.BooleanField(default=False)
    
    max_score = models.IntegerField(default=80)
    manual_questions_reviewed = models.BooleanField(default=False)
    number_of_adults = models.IntegerField(null=False)
    number_of_children = models.IntegerField(null=False)

    pets = models.CharField(max_length=100) 
    previous_unit_time = models.CharField(max_length=255)
    preferred_move_in_date = models.DateField(null=False)

    reason_for_moving = models.TextField(null=False)
    reason_for_rejection = models.CharField(max_length=250, default='')
    rejected = models.BooleanField(default=False)
    relevant_information = models.TextField(null=False)
    
    work_references_checked = models.BooleanField(default=False)
    work_references_passed = models.BooleanField(default=False)
    
    living_references_checked = models.BooleanField(default=False)
    living_references_passed = models.BooleanField(default=False)
    
    score = models.IntegerField()
    status = models.IntegerField(default=0)
    
    viewing_date = models.DateTimeField(null=True, default=None)
    viewing_id = models.CharField(max_length=200, null=True, default=None)
    
    viewing_score = models.IntegerField(null=True)
    viewing_comments = models.JSONField(null=True)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.score}'


class CandidateStatus(models.Model):
    status = models.IntegerField()
    string = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.string}'


