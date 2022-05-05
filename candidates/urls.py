
from django.urls import path

from .views import candiates_form, send_invitation_to_candidate

urlpatterns = [
    path('candidate-form/<int:unit_id>', candiates_form, name='candidate_form'),
    path('send-invitation-to-candidate/<int:unit_id>/<int:minimun_score>', send_invitation_to_candidate, name='send_invitation_to_candidate'),
]