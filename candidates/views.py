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

# CONSTANTS

DATA_FOR_HOUSEHOLD = {
        '0': {'score': 0, 'str_part': '<$2,000'},
        '1': {'score': 3, 'str_part': '$2,000 - $2,500'},
        '2': {'score': 6, 'str_part': '$2,500 - $3,000'},
        '3': {'score': 8, 'str_part': '$3,000 - $4,500'},
        '4': {'score': 10, 'str_part': '>$4,500'}
    }


DATA_FOR_CANDIDATE_PET = {
        '0': {'score': 0, 'str_part': '>= 2 dogs'},
        '1': {'score': 4, 'str_part': '1 dog'},
        '2': {'score': 0, 'str_part': '>= 3 cats'},
        '3': {'score': 4, 'str_part': '2 cats'},
        '4': {'score': 7, 'str_part': '1 cat'},
        '5': {'score': 10, 'str_part': '0'} 
    }


DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION  = {
        '0': {'score': 0, 'str_part': '0 to 6 months'},
        '1': {'score': 2, 'str_part': '6 months to 1 year'},
        '2': {'score': 5, 'str_part': '1 to 2 years'},
        '3': {'score': 8, 'str_part': '2 to 5 years'},
        '4': {'score': 10, 'str_part': 'More than 5 years'},
    }


SCORE_FOR_NUMBER_OF_RESIDENTS = {
    '0': {'score': 0 }, # exceds number of rooms in unit
    '1': {'score': 3 }, # equal to number of rooms in unit
    '2': {'score': 6 }, # equal to number of rooms - 1 
    '3': {'score': 8 }, # equal to number of rooms - 2
    '4': {'score': 10 } # equal to number of rooms - 3 or less
}


STATIC_FORM_MAX_SCORE = 80

# functions  ------------------------------------------

def get_candidate_score(unit_capacity:int, form_data:dict) -> int: 
    
    """
    
    takes the data from the form that is send to candidates calculate the total score 

    Returns:
        int: total score a candidate get
    """
    
    total_score:int = 0
    
    total_score += DATA_FOR_HOUSEHOLD[form_data['family_income']['score']]
    total_score += DATA_FOR_CANDIDATE_PET[form_data['pets']['score']]    
    total_score += form_data['length_of_time_at_current_address']
    total_score += form_data['expected_rent_duration']
    

    number_of_residents = int(form_data['number_of_adults']) + int(form_data['number_of_children']) 
    
    if number_of_residents > unit_capacity:
        # just a formality 
        # pass here since the total score will not change
        pass
    
    elif number_of_residents == unit_capacity:
        total_score += SCORE_FOR_NUMBER_OF_RESIDENTS['1']
        
    elif number_of_residents == unit_capacity - 1: 
        total_score += SCORE_FOR_NUMBER_OF_RESIDENTS['2']
        
    elif number_of_residents == unit_capacity - 2:
        total_score += SCORE_FOR_NUMBER_OF_RESIDENTS['3']
    
    elif number_of_residents <= unit_capacity - 3:
        total_score += SCORE_FOR_NUMBER_OF_RESIDENTS['4']
        
    return total_score 
    

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def candidates_form(request, unit_id):
    
    """
    
    Documentation here     
    
    
    note: the optional fields that are sent to this view must have a number associated with them 
    
    """
    
    current_unit = Units.objects.get(id=unit_id)
        
    # calculating the score a candidate has gotten
    request.data['score'] = get_candidate_score(unit_capacity= current_unit.rooms * 2, form_data=request.data)
    
    # converting the data from the form to string so that it can be saved in the databse
    
    request.data['family_income'] = DATA_FOR_HOUSEHOLD[request.data['family_income']['str_part']]
    request.data['pets'] = DATA_FOR_CANDIDATE_PET[request.data['pets']['str_part']]
    
    request.data['expected_renting_duration'] = DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[request.data['expected_renting_duration']['str_part']]
    request.data['length_of_time_at_current_address'] = DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[request.data['length_of_time_at_current_address']['str_part']]
    request.data['max_score'] = STATIC_FORM_MAX_SCORE
    
    # setting the candidate status to default 0
    request.data['status'] = 0
    
    
    serializer = FormForCandiatesSerializer(request.data)
    
    if serializer.is_valid():
        serializer.save()
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
            }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_invitations_to_candidates(request, unit_id, minimun_score, calendar_link):
    
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


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def approve_candidates(request, candidate_id:int, candidate_status:int):
    
    """
    
    Documentation here
    
    """
    
    candidate = Candidate.objects.get(id=candidate_id)
    candidate.status = candidate_status
    candidate.save()
    
    emails_sent_to:dict = {}
    
    if candidate_status == 1:
        email_subject = 'References'
        email_html = f"""
                    <html>
                        <body>
                            <h1>Dear {candidate.adults_information[adult]['name']}, please send the following references:</h1>
                            <p>reference 1</p>
                            <p>reference 2</p>
                        </body>
                    </html>
                    """
                    
    # the payment info must be attached 
    elif candidate_status == 2:
        email_subject = 'Congratulations'
        
        email_html = f"""
                    <html>
                        <body>
                            <h1>Dear {candidate.adults_information[adult]['name']}, you have been approved to live in our unit</h1>
                            <p>Now the next step is to pay the necessary stuff to continue</p>
                            <p>Payment info</p>
                        </body>
                    </html>
                    """
        
    
    # (O n time)
    for index, adult in enumerate(candidate.adults_information):
        
        emails_sent_to[f'adult{index}'] = candidate.adults_information[adult]['email']

        SendEmail(
            send_to= candidate.adults_information[adult]['email'],
            subject= email_subject,
            html=email_html)
    
    return Response(
        {
            'message': 'email(s) sent successfully',
            'sent_to': emails_sent_to
        },status=status.HTTP_200_OK)
