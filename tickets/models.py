from django.db import models
from properties.models import Tenants, Units

# ID OF EACH TABLE (EXCEPT FOR TICKET) WILL BE THE VALUE IN THE OPTIONS DISPLAYED IN FRONT 

class TicketType(models.Model):
    ticket_type = models.CharField(max_length=120)

   
class SubTicketType(models.Model):
    sub_ticket_type = models.CharField(max_length=120)
    
    
class TicketIssue(models.Model):
    issue = models.CharField(max_length=120)
    

class TicketAction(models.Model):
    action = models.CharField(max_length=120)
    

class Ticket(models.Model):
    # foreignKeys 
    created_by = models.ForeignKey(Tenants, null=False, blank=False ,on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, null=False, blank=False ,on_delete=models.CASCADE)
    unit =  models.ForeignKey(Units, null=False, blank=False ,on_delete=models.CASCADE)
    
    
    # ------------------------------------
    # fields 
    
    approved = models.BooleanField(default=False)
    actual_price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
    action_log = models.TextField(null=True)
    
    followed_up = models.BooleanField(default=False)
    followed_up_commnets = models.CharField(max_length=250, default='')
    
    contractor_availability = models.DateField()
    comments_for_approval = models.TextField()
    
    date_opened = models.DateTimeField()
    date_close = models.DateTimeField(null=True)
    description = models.TextField()
    
    photo = models.ImageField(upload_to='tickets')    
    
    proposed_contractor= models.IntegerField(null=True)
    priority = models.CharField(max_length=50)
    contractor_solution = models.CharField(max_length=200, default='')
    
    quoted_price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
    
    status = models.CharField(max_length=50)
    stimated_time_for_solution = models.IntegerField()
    specialty = models.CharField(max_length=50)
    
    reparation_day = models.DateField()
    
    target_completion_date = models.DateField(null=True)
    
    def __str__(self) -> str:
        return self.status

    
    