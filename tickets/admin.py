from django.contrib import admin
from .models import TicketType, MaintanenceType, MaintanenceIssueType, TicketAction, Ticket, MaintanenceSubIssueType, MaintanenceIssueDescription


admin.site.register(TicketType)
admin.site.register(MaintanenceType)
admin.site.register(MaintanenceIssueType)
admin.site.register(MaintanenceSubIssueType)
admin.site.register(MaintanenceIssueDescription)
admin.site.register(TicketAction)
admin.site.register(Ticket)


