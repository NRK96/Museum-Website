from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from scheduling.models import CustomerProfile, Reservation, Docent


def create_profile(name, email):
    """
    Helper method that creates a customer profile with the given name
    and email and uses the current time for dateCreated and lastUpdated
    """

    return CustomerProfile.objects.create(name=name, email=email)

def create_docent(name, email):
    """
    creates a Docent model instance for use in testing
    :param name: name for the docent
    :param email: email for the docent (must be unique)
    :return: Docent object
    """
    return Docent.objects.create(name=name, email=email)

def create_reservation(customer, group_size, date, start_time, end_time, info_text, docent):
    """
    Creates Reservation model instance for use in testing
    :param customer: customer model to be mapped to
    :param group_size: int - size of group
    :param date: datetime - date of the reservation
    :param start_time: int - start time of the reservation
    :param end_time: int - end time of the reservation
    :param info_text: char - extra info for the reservation
    :param docent: docent model to be mapped to
    :return: a reservation instance
    """
    return Reservation.objects.create(customer=customer, group_size=group_size, date=date, start_time=start_time,
                                      end_time=end_time, info_text=info_text, docent=docent)

class CustomerProfileTestCase(TestCase):

    def setUp(self):
        """
        Create a profile to manipulate during testing
        """
        createTime = timezone.now()
        self.customerProfile= CustomerProfile.objects.create(
            name= 'Team Woogity',
            email= 'woogity@email.com',
            date_created= createTime,
            last_updated= createTime
        )

    def test_customer_profile_basic(self):
        """
        Tests basic model functionality
        """
        self.assertEqual(self.customerProfile.name, 'Team Woogity')
        self.assertEqual(self.customerProfile.email, 'woogity@email.com')

    def test_profile_naming_conflict(self):
        """
        Tests that two profiles aren't allowed to have the same name
        """
        self.cust1 = create_profile('Bob', 'bob1@email.com')
        with self.assertRaises(ValidationError):
            self.cust2 = create_profile('Bob', 'bob2@email.com')

    def test_profile_email_conflict(self):
        """
        Tests that two profiles aren't allowed to have the same email
        """
        self.cust1 = create_profile('name1', 'bob@email.com')
        with self.assertRaises(IntegrityError):
            self.cust2 = create_profile('name2', 'bob@email.com')


class ReservationTestCase(TestCase):
    def setUp(self):
        self.cust1 = create_profile('cust1', 'cust1@email.com')
        self.doce1 = create_docent('doce1', 'doce1@emai.com')
        self.doce2 = create_docent('doce2', 'doce2@email.com')

        def test_reservation_basic(self):
            """
            Test basic functionality of reservation model
            """
        res = create_reservation(self.cust1, 1, '2018-08-08', '0:00', '1:00', ',', self.doce1)
        self.assertEqual(res.customer, self.cust1)
        self.assertEqual(res.group_size, 1)
        self.assertEqual(res.date, '2018-08-08')
        self.assertEqual(res.start_time, '0:00')
        self.assertEqual(res.end_time, '1:00')
        self.assertEqual(res.info_text, ',')
        self.assertEqual(res.docent, self.doce1)

    def test_reservation_cant_be_made_in_the_past(self):
       self.assertRaises(ValidationError,
                         res=create_reservation(self.cust1, 1, '2017-08-08', '0:00', '0:01', '.', self.doce1))

    def test_reservation_cant_set_end_time_to_before_start_time(self):
        self.assertRaises(ValidationError,
                          res=create_reservation(self.cust1, 1, '2018-08-08', '2:00', '1:00', '.', self.doce1))

    def test_reservation_times_cant_overlap_for_same_docent(self):
        res = create_reservation(self.cust1, 1, '2018-08-08', '1:00', '2:00', '.', self.doce1)
        self.assertRaises(ValidationError,
                          res2=create_reservation(self.cust1, 1, '2018-08-08', '1:00', '2:00', '.', self.doce1))

    def test_docent_cant_be_mapped_to_more_than_max_number_of_reservations_a_day(self):
        res0 = create_reservation(self.cust1, 1, '2018-08-08', '1:00', '2:00', '.', self.doce1)
        res1 = create_reservation(self.cust1, 1, '2018-08-08', '2:00', '3:00', '.', self.doce1)
        res2 = create_reservation(self.cust1, 1, '2018-08-08', '3:00', '4:00', '.', self.doce1)
        self.assertRaises(ValidationError,
                          res3=create_reservation(self.cust1, 1, '2018-08-08', '4:00', '5:00', '.', self.doce1))



