
from django.urls import path

from .views import CandidatesViewSet, send_invitations_to_candidates, approve_candidate

urlpatterns = [
    # root to create a new candiate
    path('candidate/<int:unit_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to get all or one candidate(s)
    path('candidate/<int:unit_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to update a candidate
    path('candidate/<int:candiate_id>', CandidatesViewSet.as_view(), name='candidates'),
    # root to delete candidate(s)
    path('candidate/<int:unit_id>/<int:candiate_id>', CandidatesViewSet.as_view(), name='candidates'),
    
    
    path('send-invitation-to-candidates/<int:unit_id>/<int:minimun_score>/<int:candidate_id>', send_invitations_to_candidates, name='send_invitation_to_candidate'),
    path('approve-candidate/<int:candidate_id>/<int:candidate_status>', approve_candidate, name='approve_candidate'),
]