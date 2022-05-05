
from django.urls import path

from .views import candidates_form, send_invitations_to_candidates, pre_aprove_candidates

urlpatterns = [
    path('candidate-form/<int:unit_id>', candidates_form, name='candidate_form'),
    path('send-invitation-to-candidate/<int:unit_id>/<int:minimun_score>', send_invitations_to_candidates, name='send_invitation_to_candidate'),
    path('pre-aprove-candidates/<int:candidate_id>/<int:candidate_status>', pre_aprove_candidates, name='pre_aprove_candidates'),
]