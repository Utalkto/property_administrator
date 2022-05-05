
from django.urls import path

from .views import candidates_form, send_invitation_to_candidate

urlpatterns = [
    path('candidate-form/<int:unit_id>', candidates_form, name='candidate_form'),
    path('send-invitation-to-candidate/<int:unit_id>/<int:minimun_score>', send_invitation_to_candidate, name='send_invitation_to_candidate'),
]