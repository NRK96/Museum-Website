from django import forms
from django.contrib.auth.models import User
from scheduling.models import Reservation, Request, CustomerProfile, Docent
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Reservation
        fields = ['customer',
                  'group_size',
                  'date',
                  'start_time',
                  'end_time',
                  'docent',
                  'info_text',
                  ]

    # def clean(self):
    #     cleaned_data = super(ReservationForm, self).clean()
    #     start_time = cleaned_data.get('start_time')
    #     end_time = cleaned_data.get('end_time')
    #     date = cleaned_data.get('date')
    #     docent = cleaned_data.get('docent')
    #     present = timezone.now()
    #     # Check to make sure that the start and end times are valid.
    #     if end_time <= start_time:
    #         raise forms.ValidationError('End time cannot be set to before start time')
    #     # Check to make sure that the reservation isn't being made for a past date.
    #     if date < timezone.now().date():
    #         raise forms.ValidationError('Cannot make a reservation in the past.')
    #     if Reservation.objects.all().count() != 0:
    #         res_set = Reservation.objects.exclude(id__exact=.pk)
    #         # Check that this reservation doesn't overlap with any of the assigned docent's other reservations.
    #         for res in res_set:  # for each reservation already stored
    #             if date == res.date:  # if the potential date matches a reservations date
    #                 if (start_time == res.end_time or end_time == res.start_time) and docent.name == res.docent.name:
    #                     # if the start time lines up with the end time or vice-versa, ignore
    #                     break
    #                 if (start_time == res.start_time or end_time == res.end_time) and docent.name == res.docent.name:
    #                     # if the start time overlaps with another or the end time does, fail.
    #                     raise forms.ValidationError('Can\'t have two reservations with the same start or end time '
    #                                                 'assigned to the same docent.')
    #                 if (res.start_time < start_time < res.end_time and docent.name == res.docent.name) or (res.start_time < end_time < res.end_time and docent.name == res.docent.name):
    #                     # if the start time is in between another reservation or the end time is, fail.
    #                     raise forms.ValidationError('That docent is already assigned to a reservation during that time,'
    #                                                 ' please assign another')
    #
    #         # Don't allow a docent to be assigned more than 3 reservations in a day.
    #         count = 0
    #         res_set = Reservation.objects.filter(date__exact=date)  # filter reservations to this day
    #         for res in res_set:
    #             if res.docent.name == docent.name:  # if the docent name matches another reservation's docent name
    #                 count += 1  # increment count
    #         if count >= 3:  # if the count is 3 or higher, fail
    #             raise forms.ValidationError('This docent is already assigned 3 reservations for that date, '
    #                                         'please choose another docent.')


class ReservationUpdateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Reservation
        fields = ['customer',
                  'group_size',
                  'actual_group_size',
                  'date',
                  'start_time',
                  'end_time',
                  'docent',
                  'info_text',
                  ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name',
                  'email',
                  'group_size',
                  'reserved_date',
                  'start_time',
                  'end_time',
                  'info_text'
                  ]


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['name',
                  'email',
                  ]


class DocentForm(forms.ModelForm):
    class Meta:
        model = Docent
        fields = ['name',
                  'email',
                  ]


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
