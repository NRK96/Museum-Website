from django.test import TestCase
from scheduling.forms import ReservationForm
from scheduling.models import Reservation, Docent, CustomerProfile
from django import forms
from django.core.exceptions import ValidationError



class ReservationFormTestCase(TestCase):

    def setUp(self):
        self.cust = CustomerProfile.objects.create(name='cust', email='cust@email.com')
        self.doce1 = Docent.objects.create(name='doce1', email='doce1@email.com')
        self.doce2 = Docent.objects.create(name='doce2', email='doce2@email.com')
        self.res1 = Reservation.objects.create(customer=self.cust, group_size='1', date="2018-10-11", start_time="0:00",
                                               end_time="1:00", docent=self.doce1, info_text='.')
        self.res1.save()
        self.res2 = Reservation.objects.create(customer=self.cust, group_size='1', date="2018-10-11", start_time="1:00",
                                               end_time="2:00", docent=self.doce1, info_text='.')
        self.res2.save()

    def test_form_basic(self):
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '2:00',
                'end_time': '3:00',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data)
        self.res3 = form.save()
        self.assertEqual(self.res3.customer, self.cust)

    def test_form_cant_create_a_reservation_with_conflicting_times(self):
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '0:00',
                'end_time': '1:00',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '1:30',
                'end_time': '2:30',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '3:30',
                'end_time': '2:30',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2017-10-11',
                'start_time': '1:30',
                'end_time': '2:30',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data)
        self.assertFalse(form.is_valid())

    def test_form_cant_create_a_reservation_for_a_docent_with_3_or_more_reservations_on_the_same_day(self):
        data = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '3:00',
                'end_time': '4:00',
                'docent': self.doce1,
                'info_text': '.',
                }
        res3 = ReservationForm(data)
        print(res3.errors)
        data2 = {'customer': self.cust,
                'group_size': 1,
                'date': '2018-10-11',
                'start_time': '4:00',
                'end_time': '5:00',
                'docent': self.doce1,
                'info_text': '.',
                }
        form = ReservationForm(data2)
        self.assertRaises(ValidationError, res=form.save())



