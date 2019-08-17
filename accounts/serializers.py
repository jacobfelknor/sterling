from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    number = serializers.IntegerField()
    account_type = serializers.CharField(max_length=10)
    bank = serializers.CharField(max_length=20)
    # notes = serializers.CharField()