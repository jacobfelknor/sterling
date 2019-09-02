from ajax_select import register, LookupChannel
from .models import Transaction

@register('categories')
class CategoryLookup(LookupChannel):

    model = Transaction

    def get_query(self, q, request):
        return self.model.objects.filter(category__icontains=q).order_by('category')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.category

    def format_match(self, item):
        return u"<span class='tag'>%s</span>" % item.category

    def get_result(self, item):
        return u"%s" % item.category

        