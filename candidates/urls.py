
from django.urls import path

from .views import candidates_form, send_invitations_to_candidates, approve_candidate

urlpatterns = [
    path('candidate-form/<int:unit_id>', candidates_form, name='candidate_form'),
    path('send-invitation-to-candidates/<int:unit_id>/<int:minimun_score>', send_invitations_to_candidates, name='send_invitation_to_candidate'),
    path('aprove-candidate/<int:candidate_id>/<int:candidate_status>', approve_candidate, name='approve_candidate'),
]