# django

from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

# serializers 
from .serializers import FormForCandiatesSerializer

# modules
from properties.models import Units
from .models import Candidate

# modules created for the app
from app_modules.send_email import SendEmail


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def candiates_form(request, unit_id):
    
    serializer = FormForCandiatesSerializer(request.data)
    
    # TODO: CONVERT SCORE HERE 
    
    if serializer.is_valid():
        serializer.save()
        
        current_unit = Units.objects.get(id=unit_id)
        property_manager_email = current_unit.property_manager # this returns the email of the property manager
        
        SendEmail(
            send_to= property_manager_email,
            subject= f'There is a new canditate interested in {current_unit.name}',
            html = f"""
                    <html>
                        <body>
                            <h1>New candidate interested to rent a unit</h1>
                        </body>
                    </html>
                    """
            )
            
        return Response(
            {
                'message': 'Form received'
            }, 
            status=status.HTTP_200_OK
            )
            
    else:
        return Response({
            'error': True,
            'message': 'serializer is not valid',
            'serializer_error': serializer.errors
            })
        

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_invitation_to_candidate(request, unit_id, minimun_score, calendar_link):
    
    """
    
    Documentation here 
    
    """
    
    candidates = Candidate.objects.filter(unit=unit_id, score__gte=minimun_score)
    emails_sent_to:dict = {}
    
    # (O n time)
    for candidate in candidates:  
        for index, adult in enumerate(candidate.adults_information):
            
            emails_sent_to[f'adult{index}'] = candidate.adults_information[adult]['email']

            SendEmail(
                send_to= candidate.adults_information[adult]['email'],
                subject= f'Invitation to view the unit',
                html= f"""
                        <html>
                            <body>
                                <h1>Dear {candidate.adults_information[adult]['name']}, you have been invited to view the unit</h1>
                                <p>Now you can <a href={calendar_link}> schedule </a> a visit to the unit</p>
                            </body>
                        </html>
                        """
                )
    
    return Response(
        {
            'message': 'invitations sent successfully',
            'sent_to': emails_sent_to
        },status=status.HTTP_200_OK)
    