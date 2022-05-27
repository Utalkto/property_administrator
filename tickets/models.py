from django.db import models
from properties.models import Tenants, Units, PropertyCities

from register.models import CustomUser

# ID OF EACH TABLE (EXCEPT FOR TICKET) WILL BE THE VALUE IN THE OPTIONS DISPLAYED IN FRONT 


class SupplierWorkArea(models.Model):
    
    work_area = models.CharField(max_length=120)
    # work_area = models.CharField(max_length=120, default='120')
    
    
    def __str__(self) -> str:
        return f'{self.work_area} - {self.id}'
    

class Suppliers(models.Model):
    # foreign keys
    
    city = models.ForeignKey(PropertyCities, null=False, blank=False, on_delete=models.CASCADE)
    # role = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE)
    
    work_area = models.ForeignKey(SupplierWorkArea, null=False, blank=False, on_delete=models.CASCADE, default=None)
    
    # --------------------------
    # fields

    email = models.CharField(max_length=100)
    
    last_time_hired = models.DateField(null=True, default=None)
    
    name = models.CharField(max_length=50)
    
    phone = models.CharField(max_length=100)
    
    rating = models.IntegerField(null=True, default=None)
    
    times_hired = models.IntegerField(null=True, default=None)
    
    
    def __str__(self) -> str:
        return f'{self.name} - {self.id}'


class TicketType(models.Model):
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'

   
# tables for maintanence 
   
class MaintanenceType(models.Model):
    ticket_type = models.ForeignKey(TicketType, null=False, on_delete=models.CASCADE)
    
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'
    

class MaintanenceIssueType(models.Model):
    maintanence_type = models.ForeignKey(MaintanenceType, null=False, on_delete=models.CASCADE)
    
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'
    

# here would be the part of the appliance that is failing 
class MaintanenceSubIssueType(models.Model):
    maintanence_issue_type = models.ForeignKey(MaintanenceIssueType, null=False, on_delete=models.CASCADE)
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'
    
    
class MaintanenceIssueDescription(models.Model):
    maintanence_issue_sub_type = models.ForeignKey(MaintanenceSubIssueType, null=False, on_delete=models.CASCADE)
    work_area = models.ForeignKey(SupplierWorkArea, null=False, on_delete=models.CASCADE, default=5)

    string_part = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'

# ----------------------------------------

class TicketAction(models.Model):
    issue_description = models.ForeignKey(MaintanenceIssueDescription, null=False, on_delete=models.CASCADE, default=1)
    action_to_do = models.JSONField()
    

# class TicketIssue(models.Model):
#     issue = models.CharField(max_length=120)

class TicketPayment(models.Model):
    
    amount = models.IntegerField()
    payment_date = models.DateField()
    reference_code = models.CharField(max_length=120)
    notes = models.TextField(null=True)
    
    
class TicketPriority(models.Model):
    string_part = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'


class TicketSteps(models.Model):
    
    # foreign keys 
    
    ticket_type = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE, default=1)
    
    # --------------------------------------------
    # fields
    
    string_part = models.CharField(max_length=120)
    info = models.CharField(max_length=1000, default='', null=True)
    action_link = models.URLField(max_length=120, default=None, null=True)
    
    second_action_link = models.URLField(max_length=120, null=True, default=None)
    name_second_action_link= models.CharField(max_length=120, null=True, default=None)
    
    
    def save(self, *args, **kwargs):
        if self.action_link == 'http://localhost:8000/None':
            self.action_link = None
            self.second_action_link = None
            self.name_second_action_link = None
        if self.second_action_link == 'http://localhost:8000/None':
            self.second_action_link = None
            self.name_second_action_link = None
            
        super(TicketSteps, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return f'{self.string_part} - {self.id}'
    
 
class Ticket(models.Model):
    # foreignKeys 
    created_by = models.ForeignKey(Tenants, null=False, blank=False, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, null=False, blank=False, on_delete=models.CASCADE)
    unit =  models.ForeignKey(Units, null=False, blank=False, on_delete=models.CASCADE)
    priority =  models.ForeignKey(TicketPriority, null=False, blank=False, on_delete=models.CASCADE)
    ticket_status =  models.ForeignKey(TicketSteps, null=False, blank=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, default=1)
    
    contractor = models.ForeignKey(Suppliers, null=True, blank=False, on_delete=models.CASCADE, default=None)
    action_to_do = models.ForeignKey(TicketAction, null=True, blank=False, on_delete=models.CASCADE, default=None)       
    problem = models.ForeignKey(MaintanenceIssueDescription, null=True, on_delete=models.CASCADE, default=None)
    payment = models.ForeignKey(TicketPayment, null=True, on_delete=models.CASCADE, default=None)

    # ------------------------------------
    # fields 
    
    approved = models.BooleanField(default=False)
    
    followed_up = models.BooleanField(default=False)
    
    contractors_contacted = models.JSONField(default=dict)
    comments_for_approval = models.TextField(null=True)
    
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(null=True)
    
    last_date_ticket_change = models.DateTimeField(null=True, default=None)
    
    max_for_approval = models.IntegerField(default=250)
    
    photo = models.ImageField(upload_to='tickets', null=True)
    
    contractor_solution = models.TextField(null=True)
    
    quoted_price = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=True)
    
    stimated_time_for_solution = models.IntegerField(null=True)
    solution_date = models.DateField(null=True)
    

class TicketComments(models.Model):
    # foreignKeys 
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)
    made_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)

    # ------------------------------------
    # fields 
    
    date = models.DateTimeField()
    comment = models.TextField()


class TicketAppoinment(models.Model):
    
    # Foreign keys  
    created_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=models.CASCADE)
    # ------------------------------------------------------------
    # Fields
    
    date = models.DateTimeField(null=False)
    completed = models.BooleanField(default=False)
    supplier_attendance = models.BooleanField(default=False)
    
    
    
    
    
    
    






