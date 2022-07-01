
from django.urls import path

from .views import CandidatesViewSet, send_invitations_to_candidates, approve_candidate

urlpatterns = [
    # root to create a new candiate
    path('candidates/<str:unit_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to get all or one candidate(s)
    path('candidates/<str:unit_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to update a candidate
    path('candidate-update/<int:candidate_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to delete candidate(s)
    path('candidate/<int:unit_id>/<int:candidate_id>', CandidatesViewSet.as_view(), name='candidates'),
    
    
    path('send-invitation-to-candidates/<int:unit_id>', send_invitations_to_candidates, name='send_invitation_to_candidate'),
    path('approve-candidate/<int:candidate_id>/<int:candidate_status>', approve_candidate, name='approve_candidate'),
]