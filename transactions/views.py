from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import Account

from .forms import TransactionForm
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.

def transaction_ajax(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    transactions = Transaction.objects.filter(account__uuid=get('uuid'))
    response = TransactionSerializer(transactions, many=True)
    return JsonResponse(response.data, safe=False)


""" Server side processing example: """
# def drawing_list_ajax(request):
#     if request.method == "POST":
#         get = request.POST.get
#     else:
#         get = request.GET.get

#     start = int(get('start'))
#     length = int(get('length'))
#     end = start + length
#     search = get('search[value]')
#     order_column_index = int(get('order[0][column]'))
#     order_direction = get('order[0][dir]')
#     order_column_name = get('columns[{}][name]'.format(order_column_index))
#     # print('{}, {}'.format(order_column_name, order_direction))
#     if order_direction == "asc":
#         drawings = Drawing.objects.order_by('{}'.format(order_column_name))
#     else:
#         drawings = Drawing.objects.order_by('-{}'.format(order_column_name))
#     records_total = len(drawings)
    
#     if search:
#         query = (Q(number__icontains=search) | Q(description__icontains=search) | 
#                     Q(program_drawing__name__icontains=search) | Q(drawnby__name__icontains=search))
#         drawings = drawings.filter(query)

#     records_filtered = len(drawings)
#     drawings = drawings[start:end]
#     # drawing_qs = DrawingSerializer.setup_eager_load(drawings) # eager load is incompatible with serverside processing
#     serializer = DrawingSerializer(drawings, many=True)
#     response = {
#         "draw": int(get('draw')),
#         "recordsTotal": records_total,
#         "recordsFiltered": records_filtered,
#         "data": serializer.data,
#     }

#     return JsonResponse(response, safe=False)


class CreateTransaction(CreateView):
    # TODO
    # - Add autocomplete field for category section
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/edit_transaction.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['message'] = "Add Transaction"
        return ctx

    def form_valid(self, form):
        if self.request.method == 'POST':
            get = self.request.POST.get
        else:
            get = self.request.GET.get

        form.save(commit=False)
        uuid = self.request.GET['account']
        form.instance.account = Account.objects.get(uuid=uuid)
        form.instance.category = get('category')
        form.instance.date = datetime.strptime(get('date'), '%m/%d/%Y')
        form.instance.notes = get('notes')
        form.save()
        return redirect('accounts:view', slug=uuid)


class TransactionView(DetailView):
    model = Transaction
