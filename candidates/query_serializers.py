from rest_framework import serializers, fields

class CandidateQuerySerializer(serializers.Serializer):
    unit_id = fields.CharField(default='all')
    have_viewing_appoinments = fields.BooleanField(default=False)
    pending_payments = fields.BooleanField(default=False)
    rejected = fields.BooleanField(default=False)
    minimun_score = fields.IntegerField(default=0)
