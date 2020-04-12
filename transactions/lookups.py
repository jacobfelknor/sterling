from ajax_select import register, LookupChannel
from .models import Transaction
from accounts.models import Account


@register("categories")
class CategoryLookup(LookupChannel):

    model = Transaction

    def get_query(self, q, request):
        objects = self.model.objects.filter(category__icontains=q).order_by("category")
        return set([obj.category for obj in objects])

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

    def format_match(self, item):
        return u"<span class='tag'>%s</span>" % item

    def get_result(self, item):
        return u"%s" % item

    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        else:
            return False


@register("accounts")
class AccountLookup(LookupChannel):
    model = Account

    def get_query(self, q, request):
        objects = self.model.objects.filter(name__icontains=q).order_by("name")
        return [obj.name for obj in objects]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

    def format_match(self, item):
        return u"<span class='tag'>%s</span>" % item

    def get_result(self, item):
        return u"%s" % item

    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        else:
            return False
