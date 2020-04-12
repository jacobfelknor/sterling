from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    account = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=50)
    date = serializers.DateField()

    amount = serializers.SerializerMethodField()

    def __init__(self, instance=None, **kwargs):
        self.account_uuid = kwargs.pop("uuid")
        super().__init__(instance=instance, **kwargs)

    def get_amount(self, obj):
        ledgers = obj.ledgers.all()
        _sum = 0
        for ledger in ledgers:
            _sum += ledger.amount if str(ledger.account_id) == str(self.account_uuid) else 0

        return _sum

    def get_account(self, obj):
        return self.account_uuid
