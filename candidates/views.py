# python

import validators
import requests

# django

from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from register.models import CustomUser

# serializers 
from .serializers import CandiatesSerializer, CandiatesGetSerializer

# models
from properties.models import Unit, Links
from .models import Candidate

# modules created for the app
from app_modules.send_email import SendEmail

# swagger
from drf_yasg.utils import swagger_auto_schema


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
    '0': 0, # exceds number of rooms in unit
    '1': 3, # equal to number of rooms in unit
    '2': 6, # equal to number of rooms - 1 
    '3': 8, # equal to number of rooms - 2
    '4': 10 # equal to number of rooms - 3 or less
}


STATIC_FORM_MAX_SCORE = 80


CALENDLY_ACCESS_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjUxODYzNzc5LCJqdGkiOiIzZDA2ZWJhNy02MmI0LTQwZjQtOTg2NC05MDVhMTNkMWIyYjkiLCJ1c2VyX3V1aWQiOiI1YzljOGZhOS0zODZkLTQxZWUtOWRkYi1jOGNlMGMzMzU4OWEifQ.2WNLz3DYgd8vq-FXg7RiECGnL5lON879bOgVVnLApMk'
CALENDLY_USER_ID = '5c9c8fa9-386d-41ee-9ddb-c8ce0c33589a'

# functions  ------------------------------------------

def get_candidate_score_from_form(unit_capacity:int, form_data:dict) -> int: 
    
    """
    
    takes the data from the form that is send to candidates calculate the total score 

    Returns:
        int: total score a candidate get
    """
    
    total_score:int = 0
    
    total_score += DATA_FOR_HOUSEHOLD[form_data['family_income']]['score']
    total_score += DATA_FOR_CANDIDATE_PET[form_data['pets']]['score']   
    total_score += DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[form_data['length_of_time_at_current_address']]['score']   
    total_score += DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[form_data['expected_renting_duration']]['score']  
    

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
   

def get_candidates_with_viewing(unit_id:int) -> list:
    
    candidates_to_event = []
    
    # first get the event that were set in calendly 
    list_event_url = "https://api.calendly.com/scheduled_events"
    querystring = {"user":f"https://api.calendly.com/users/{CALENDLY_USER_ID}","count":"40"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjUxODYzNzc5LCJqdGkiOiIzZDA2ZWJhNy02MmI0LTQwZjQtOTg2NC05MDVhMTNkMWIyYjkiLCJ1c2VyX3V1aWQiOiI1YzljOGZhOS0zODZkLTQxZWUtOWRkYi1jOGNlMGMzMzU4OWEifQ.2WNLz3DYgd8vq-FXg7RiECGnL5lON879bOgVVnLApMk"
    }

    event_response = requests.request("GET", list_event_url, headers=headers, params=querystring).json()['collection']
    
    candidates = list(Candidate.objects.filter(unit=unit_id))
    
    # iterate through each event to get info
    for event in event_response:
        
        event_id = event['uri'][42:]
        event_id_url = f"https://api.calendly.com/scheduled_events/{event_id}/invitees"
        
        date = event['start_time']
        
        # we get the invitee email and look for it in the database
        invitee_email = requests.request("GET", event_id_url, headers=headers).json()['collection'][0]['email']
        
        found = False
        
        for index, candidate in enumerate(candidates):
            for adult in candidate.adults_information:
                if invitee_email == candidate.adults_information[adult]['email']:
                    candidate_to_event = {
                    'date': date,
                    'candidate': CandiatesSerializer(candidate).data
                    }
                    candidates_to_event.append(candidate_to_event)
                    candidates.pop(index)
                    found = True
                    break
                
            if found:
                break
        
        if not found:
            candidate_to_event = {
                'date': None,
                'candidate': f'the following email {invitee_email} is not associeted with no candidates'
                }
        
            candidates_to_event.append(candidate_to_event)
    
    return candidates_to_event
   
# ------------------------------------------------------

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_invitations_to_candidates(request, unit_id):
    
    """
    
    summary: send invation to one or more candiate to view the unit
    
    unit_id <int> : the united id the candidate is applying to 
    
    
    body : { 
        calendar_link <str> <required> : the link provided by the property manager that is going to use to send
        to the candidates, this str has to be a valid url, in case it is not a valid url, it must be a
        number indicating the id of the link previously provided and is stored in the data base (CutsomUser.Links) 
        
        
        save_link <bool> <optional> : field in case the user wants to save the link in the database
        
        minimun_score <int> <optional> : when the property manager wants to invite more than one candidate at the same time,
        the minimun score of the candidates that will receive the invitation must be provided
        
        candidate_id <int> <optional> : it must be provided to invitate one specific candidate

        }
    """
    
    # link test : 'https://calendly.com/amelendes-1/viewing-test'
    
    calendar_link = request.data['calendar_link']
    
    if not validators.url(str(calendar_link)):
        try:
            calendar_link = Links.objects.get(id=int(calendar_link))
        except ObjectDoesNotExist:
            return Response(
                {
                    'error': True,
                    'message':'the selected link does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
        
    if 'save_link' in request.data.keys():
        new_link = Links(
            owner=CustomUser.objects.get(id=request.user.id),
            link=calendar_link, 
            link_name=request.data['link_name'], 
            link_type='invitation_link')
        new_link.save()
            
    # getting just one candiate to invitate to the viewing
    # used filter here to be able to perform the for loop without changing so much 
    if 'candidate_id' in request.data.keys():
        candidates = Candidate.objects.filter(id=int(request.data['candidate_id']))
    
    # getting more than one candidate to invitate to the viewing 
    else:
        candidates = Candidate.objects.filter(unit=unit_id, score__gte=int(request.data['minimun_score']))
        
    emails_sent_to:dict = {}
    
    # (O n time)
    for candidate_index, candidate in enumerate(candidates):  
        emails_sent_to[f'candidate{candidate_index}'] = {}
        for index, adult in enumerate(candidate.adults_information):
            
            emails_sent_to[f'candidate{candidate_index}'][f'adult{index}'] = candidate.adults_information[adult]['email']

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
def approve_candidate(request, candidate_id:int, candidate_status:int):
    
    """
    
    Documentation here
    
    """
    
    candidate = Candidate.objects.get(id=candidate_id)
    candidate.status = candidate_status
    candidate.save()
    
    emails_sent_to:dict = {}
        
    
    # (O n time)
    for index, adult in enumerate(candidate.adults_information):
        
        emails_sent_to[f'adult{index}'] = candidate.adults_information[adult]['email']
        
        if candidate_status == 1:
            attach_file = None
            
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
        elif candidate_status == 3:
            attach_file = 'test.pdf'
            
            email_subject = 'Congratulations'
            email_html = f"""
                        <html>
                            <body>
                                <h1>Dear {candidate.adults_information[adult]['name']}, you have been approved to live in our unit</h1>
                                <p>Now the next step is to pay the necessary stuff to continue</p>
                            </body>
                        </html>
                    """

        SendEmail(
            send_to= candidate.adults_information[adult]['email'],
            subject= email_subject,
            html=email_html,
            attach_file=attach_file
            )
    
    return Response(
        {
            'message': 'email(s) sent successfully',
            'sent_to': emails_sent_to
        },status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def manual_information_review(request, candidate_id, candidate_score):
    
    candidate = Candidate.objects.get(id=candidate_id)
    candidate.manual_questions_reviewed = True
    candidate.score += candidate_score 
    candidate.save()
    
    return Response(
        {
            'message': 'successfull'
        }, status=status.HTTP_200_OK)


class CandidatesViewSet(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: CandiatesSerializer()})
    def get(self, request, unit_id):

        if unit_id == 'all':

            candidates = Candidate.objects.filter(property_manager=request.user.id)

        else:
        
            if 'have_viewing_appoinments' in request.data.keys():
                candidates = get_candidates_with_viewing(unit_id=unit_id)
                return Response({'candidates': candidates})
            
            if 'pending_payments' in request.data.keys():
                candidates = Candidate.objects.filter(unit=unit_id, status=3)
                return Response({'candidates': candidates.data})
            else:
                
                if 'rejected' in request.data.keys():
                    candidates = Candidate.objects.filter(unit=unit_id, score__gte=request.data['minimun_score'], rejected=True)
                else:
                    candidates = Candidate.objects.filter(unit=unit_id, score__gte=request.data['minimun_score'])

            if not candidates:
                return Response(
                    {
                        'message': 'no candidates meet the provided requirements'
                    }, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CandiatesGetSerializer(candidates, many=True)
        return Response({'candidates': serializer.data}, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
    responses={200: CandiatesSerializer()})
    def post(self, request, unit_id):
        """
        
        note: the optional fields that are sent to this view must have a number associated with them 
        
        """
        try:
            current_unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return Response(
                {
                    'error': True,
                    'message': f'unit with id {unit_id} does not exist'
                }, status=status.HTTP_404_NOT_FOUND
                )
            
        # calculating the score a candidate has gotten
        request.data['score'] = get_candidate_score_from_form(unit_capacity=current_unit.rooms * 2, form_data=request.data)
        
        # converting the data from the form to string so that it can be saved in the databse
        request.data['family_income'] = DATA_FOR_HOUSEHOLD[request.data['family_income']]['str_part']
        request.data['pets'] = DATA_FOR_CANDIDATE_PET[request.data['pets']]['str_part']
        
        request.data['expected_renting_duration'] = DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[request.data['expected_renting_duration']]['str_part']
        request.data['length_of_time_at_current_address'] = DATA_FOR_TIME_AT_CURRENT_ADDRESS_AND_RENTAL_DURATION[request.data['length_of_time_at_current_address']]['str_part']
        request.data['max_score'] = STATIC_FORM_MAX_SCORE
        
        # setting the candidate status to default 0
        request.data['status'] = 0
        
        serializer = CandiatesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            property_manager_email = current_unit.property_manager.email 
            
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
    
    
    def put(self, request, candidate_id):
        
        """
        
        _summary_ : function to update a candidate
        Returns:
            _type_: _description_
        """
        
        candidate = Candidate.objects.get(id=candidate_id)

        if 'score' in request.data.keys():
            request.data['score'] += candidate.score
        
        
        serializer = CandiatesSerializer(candidate, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {
                    'error': True, 
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST)
            
            
    def delete(self, request, unit_id, candidate_id):
        if int(candidate_id) == 0:
            Candidate.objects.filter(unit=unit_id).delete()
        else:
            c = Candidate.objects.get(id=candidate_id)
            c.delete()
        
        return Response({'message: candidate(s) deleted successfully'}, status=status.HTTP_200_OK)
        
        