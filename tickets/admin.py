from django.contrib import admin
from .models import SupplierWorkArea, Suppliers, TicketAppoinment, TicketPriority, TicketType, MaintanenceType, MaintanenceIssueType, TicketAction, Ticket, MaintanenceSubIssueType, MaintanenceIssueDescription, TicketSteps, TicketComments


admin.site.register(TicketType)
admin.site.register(MaintanenceType)
admin.site.register(MaintanenceIssueType)
admin.site.register(MaintanenceSubIssueType)
admin.site.register(MaintanenceIssueDescription)
admin.site.register(TicketAction)
admin.site.register(TicketPriority)
admin.site.register(Ticket)
admin.site.register(TicketSteps)
admin.site.register(Suppliers)
admin.site.register(TicketComments)
admin.site.register(SupplierWorkArea)
admin.site.register(TicketAppoinment)




