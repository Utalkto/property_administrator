from django.db import models
from properties.models import Tenants, Units, PropertyCities

from register.models import CustomUser

# ID OF EACH TABLE (EXCEPT FOR TICKET) WILL BE THE VALUE IN THE OPTIONS DISPLAYED IN FRONT 

class TicketType(models.Model):
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'

   
# tables for maintanence 
   
class MaintanenceType(models.Model):
    ticket_type = models.ForeignKey(TicketType, null=False, on_delete=models.CASCADE)
    
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return self.string_part
    

class MaintanenceIssueType(models.Model):
    maintanence_type = models.ForeignKey(MaintanenceType, null=False, on_delete=models.CASCADE)
    
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return self.string_part
    

# here would be the part of the appliance that is failing 
class MaintanenceSubIssueType(models.Model):
    maintanence_issue_type = models.ForeignKey(MaintanenceIssueType, null=False, on_delete=models.CASCADE)
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return self.string_part   
    
    
class MaintanenceIssueDescription(models.Model):
    maintanence_issue_sub_type = models.ForeignKey(MaintanenceSubIssueType, null=False, on_delete=models.CASCADE)
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return self.string_part

# ----------------------------------------

class TicketAction(models.Model):
    issue_description = models.ForeignKey(MaintanenceIssueDescription, null=False, on_delete=models.CASCADE, default=1)
    action_to_do = models.JSONField()
    
    

# class TicketIssue(models.Model):
#     issue = models.CharField(max_length=120)
    
class TicketPriority(models.Model):
    string_part = models.CharField(max_length=120)


class TicketSteps(models.Model):
    
    # foreign keys 
    
    ticket_type = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE, default=1)
    
    # --------------------------------------------
    # fields
    
    string_part = models.CharField(max_length=120)
    info = models.CharField(max_length=1000, default='', null=True)
    action_link = models.URLField(max_length=120, default='', null=True)


class Ticket(models.Model):
    # foreignKeys 
    created_by = models.ForeignKey(Tenants, null=False, blank=False, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE)
    unit =  models.ForeignKey(Units, null=False, blank=False, on_delete=models.CASCADE)
    priority =  models.ForeignKey(TicketPriority, null=False, blank=False, on_delete=models.CASCADE)
    ticket_status =  models.ForeignKey(TicketSteps, null=False, blank=False, on_delete=models.CASCADE)
    action_to_do = models.ForeignKey(TicketAction, null=True, blank=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, default=1)


    # ------------------------------------
    # fields 
    
    approved = models.BooleanField(default=False)
    actual_price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=True)
    action_log = models.TextField(null=True)
    
    followed_up = models.BooleanField(default=False)
    followed_up_commnets = models.CharField(max_length=250, null=True)
    
    contractor_availability = models.DateField(null=True)
    contractors_contacted = models.JSONField(default=dict)
    comments_for_approval = models.TextField(null=True)
    
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    
    photo = models.ImageField(upload_to='tickets', null=True)    
    
    proposed_contractor= models.IntegerField(null=True)
    contractor_solution = models.CharField(max_length=200, null=True)
    
    quoted_price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=True)
    
    stimated_time_for_solution = models.IntegerField(null=True)
    specialty = models.CharField(max_length=50, null=True)
    
    reparation_day = models.DateField(null=True)
    
    target_completion_date = models.DateField(null=True)
    
    # def __str__(self) -> str:
    #     return self.status



class Suppliers(models.Model):
    # foreign keys
    
    city = models.ForeignKey(PropertyCities, null=False, blank=False, on_delete=models.CASCADE)
    role = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE)
    
    # --------------------------
    # fields

    email = models.CharField(max_length=100)
    
    last_time_hired = models.DateField(null=True, default=None)
    
    name = models.CharField(max_length=50)
    
    phone = models.CharField(max_length=100)
    
    rating = models.IntegerField()
    
    times_hired = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f'{self.name} - {self.id}'
    
    
   

