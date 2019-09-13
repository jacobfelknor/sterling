from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField(max_length=50)
    amount = serializers.FloatField()
    category= serializers.CharField()
    date = serializers.DateField()