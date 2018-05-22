from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from scheduling.models import Request, Reservation, CustomerProfile, Docent
from scheduling.forms import ReservationForm, CustomerProfileForm, RequestForm, DocentForm, ReservationUpdateForm


# ------------------------------------------------------------- #
# Header Views
# ------------------------------------------------------------- #

# View for the home landing page
def home(request):
    # getting our template
    template = loader.get_template('directlinks/home.html')
    # rendering the template in HttpResponse
    return HttpResponse(template.render({"user": request.user}), request)


# View for the confirmation page displayed when submitting a request.
def confirmation(request):
    # getting our template
    template = loader.get_template('scheduling/confirmation.html')
    # rendering the template in HttpResponse
    return HttpResponse(template.render(), request)


# View for our Contact page
def contact(request):
    # getting our template
    template = loader.get_template('directlinks/contact.html')
    # rendering the template in HttpResponse
    return HttpResponse(template.render({"user": request.user}), request)


# View for our scheduling page
@login_required
def scheduling(request):
    template = loader.get_template('directlinks/scheduling.html')
    return HttpResponse(template.render({"user": request.user}), request)


def request_confirm(request):
    template = loader.get_template('directlinks/request/request_confirmation.html')
    return HttpResponse(template.render(), request)


# View for the statistics page.
class statistics(LoginRequiredMixin, generic.ListView):
    context_object_name = 'stat_list'
    template_name = 'scheduling/statistics.html'
    
    def get_queryset(self):
        return Reservation.objects.all()

# ------------------------------------------------------------- #
# Request Views
# ------------------------------------------------------------- #


# View for submitting a new request (The form page)
class RequestCreate(CreateView):
    model = Request
    # the fields mentioned below become the entry rows in the generated form
    template_name = 'directlinks/request/request_index.html'
    form_class = RequestForm
    success_url = reverse_lazy('req_confirm')


class RequestIndex(LoginRequiredMixin, generic.ListView):
    """
    Class for our view displaying all current requests.
    """
    template_name = 'scheduling/request/request_list.html'
    context_object_name = 'req_list'

    def get_queryset(self):
        return Request.objects.all().order_by('reserved_date')

    def get_context_data(self, **kwargs):
        context = super(RequestIndex, self).get_context_data(**kwargs)
        context['customers'] = CustomerProfile.objects.all()
        customers = CustomerProfile.objects.values_list('name', flat=True)
        profile_exist_list = []
        for name in Request.objects.values_list('name', flat=True):
            for cust in customers:
                if name == cust:
                    profile_exist_list.append(name)
        print(profile_exist_list)
        context['profile_exist_list'] = profile_exist_list
        return context


# View for updating a request
class RequestUpdate(UpdateView):
    model = Request
    # the fields mentioned below become the entry rows in the update form
    fields = '__all__'


# View for deleting a request
class RequestDelete(DeleteView):
    model = Request
    # the delete button forwards to the url mentioned below.
    template_name = 'scheduling/request/request_confirm_delete.html'
    success_url = reverse_lazy('scheduling:req_index')

# ------------------------------------------------------------- #
# Reservation Views
# ------------------------------------------------------------- #


class ReservationIndex(LoginRequiredMixin, generic.ListView):
    """
    Class for our view displaying the list of all current reservations
    """
    template_name = 'scheduling/reservation/reservation_index.html'
    context_object_name = 'res_list'

    def get_queryset(self):
        return Reservation.objects.all().order_by('date')

    def get_context_data(self, **kwargs):
        context = super(ReservationIndex, self).get_context_data(**kwargs)
        context['today'] = datetime.today()
        context['a_week'] = datetime.today()+timedelta(days=7)
        if Reservation.objects.filter(date__range=(datetime.today(), datetime.today()+timedelta(days=7))).count() > 0:
            context['recent'] = Reservation.objects.filter(date__range=
                                                       (datetime.today(), datetime.today()+timedelta(days=7)))
        return context


class ReservationDetail(LoginRequiredMixin, generic.DetailView):
    model = Reservation
    template_name = 'scheduling/reservation/reservation_detail.html'


class ReservationCreate(LoginRequiredMixin, CreateView):
    """
    Class for handling creation of new reservations
    """
    model = Reservation
    template_name = 'scheduling/reservation/reservation_form.html'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        context = super(ReservationCreate, self).get_context_data(**kwargs)
        context['customer'] = CustomerProfile.objects.all()
        context['reservation_list'] = Reservation.objects.all()
        return context


class ReservationCreateFromRequest(LoginRequiredMixin, CreateView):
    """
    Class used to confirm request details when converting request to a reservation
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'scheduling/reservation/reservation_from_request_form.html'

    def get_initial(self):
        initial = super(ReservationCreateFromRequest, self).get_initial()
        req = Request.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        cp = CustomerProfile.objects.get(name__exact=req.name)
        initial['customer'] = cp
        initial['group_size'] = req.group_size
        initial['date'] = req.reserved_date
        initial['start_time'] = req.start_time
        initial['end_time'] = req.end_time
        initial['info_text'] = req.info_text
        return initial


class ReservationUpdate(LoginRequiredMixin, UpdateView):
    """
    Class for handling updating current reservations
    """
    model = Reservation
    template_name = 'scheduling/reservation/reservation_update.html'
    form_class = ReservationUpdateForm

    def get_success_url(self):
        return str(self.object.pk) + '/detail'


class ReservationDelete(LoginRequiredMixin, DeleteView):
    """
    Class for handling deleting current reservations
    """
    model = Reservation
    template_name = 'scheduling/reservation/reservation_confirm_delete.html'
    success_url = reverse_lazy('scheduling:res_index')


# ------------------------------------------------------------- #
# CustomerProfile Views
# ------------------------------------------------------------- #

class CustomerProfileIndex(LoginRequiredMixin, generic.ListView):
    """
    Class for our view displaying the list of all customer profiles
    """
    template_name = 'scheduling/customerprofile/customerprofile_index.html'
    context_object_name = 'prof_list'

    def get_queryset(self):
        return CustomerProfile.objects.all()


class CustomerProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = CustomerProfile
    template_name = 'scheduling/customerprofile/customerprofile_detail.html'


class CustomerProfileCreate(LoginRequiredMixin, CreateView):
    """
    Class for handling creation of new profiles
    """
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'scheduling/customerprofile/customerprofile_form.html'


class CustomerProfileCreateFromRequest(LoginRequiredMixin, CreateView):
    """
    Class used for creating a profile from a request
    """
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'scheduling/customerprofile/customerprofile_form.html'

    def get_initial(self):
        initial = super(CustomerProfileCreateFromRequest, self).get_initial()
        cp = Request.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        initial['name'] = cp.name
        initial['email'] = cp.email
        return initial

    def get_success_url(self):
        pass

class CustomerProfileUpdate(LoginRequiredMixin, UpdateView):
    """
    Class for updating existing profiles
    """
    model = CustomerProfile
    fields = '__all__'


class CustomerProfileDelete(LoginRequiredMixin, DeleteView):
    """
    Class for deleting existing profiles
    """
    model = CustomerProfile
    success_url = reverse_lazy('prof_index')

# ------------------------------------------------------------- #
# Docent Views
# ------------------------------------------------------------- #


class DocentIndex(LoginRequiredMixin, generic.ListView):
    """
    Class for our view displaying the list of all docents
    """
    template_name = 'scheduling/docent/docent_index.html'
    context_object_name = 'doc_list'

    def get_queryset(self):
        return Docent.objects.all()


class DocentDetail(LoginRequiredMixin, generic.DetailView):
    model = Docent
    template_name = 'scheduling/docent/docent_detail.html'


class DocentCreate(LoginRequiredMixin, CreateView):
    """
    Class for handling creation of new docents
    """
    model = Docent
    form_class = DocentForm
    template_name = 'scheduling/docent/docent_form.html'


class DocentUpdate(LoginRequiredMixin, UpdateView):
    """
    Class for updating existing docents
    """
    model = Docent
    fields = '__all__'


class DocentDelete(LoginRequiredMixin, DeleteView):
    """
    Class for deleting existing docents
    """
    model = Docent
    success_url = reverse_lazy('doc_index')