from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.text import slugify

import os, os.path

# Create your models here.
from django.urls import reverse


# sends the email
def send_email(self, message):
    send_mail(
        'Reservation Confirmation',
        message,
        'MuseumOfSouthTexas@gmail.com',
        [str(self.customer.email)],
        fail_silently=False,
    )

# saves the emails to a folder
def save_letters(self, message):
    # current directory
    path = os.getcwd()
    # if the ConfirmationLetters directory doesn't exist, make it
    if not os.path.exists('ConfirmationLetters'):
        os.makedirs('ConfirmationLetters')
    # path to the ConfirmationLetters directory
    letterpath = path + '/ConfirmationLetters'
    filename = str(self.customer.name) + '_Reservation_' + str(self.date) + '.txt'
    # move to the ConfirmationLetters directory and create a file containing the confirmation letter
    os.chdir(letterpath)
    file = open(filename, 'w')
    file.write(message)
    file.close()
    # go back to the original directory so we don't keep creating subdirectories.
    os.chdir(path)

# whenever a new reservation is created, sends and saves an email
def email_handler(self):
    message = 'Hello ' + str(
        self.customer.name) + ',\n\nYour reservation request has been accepted. The details of your visit are listed below.\n\nParty size: ' + str(
        self.group_size) + '\nDate of visit: ' + str(self.date) + '\nTime: ' + str(self.start_time) + ' to ' + str(
        self.end_time) + '\nDocent assigned: ' + str(
        self.docent) + '\n\n If you have any questions feel free to contact us by calling 555-5555 or through email at MuseumOfSouthTexas@gmail.com, thank you for your interest and enjoy your visit!\n\n- The MOST Staff!'
    send_email(self, message)
    save_letters(self, message)


class Request(models.Model):
    """
    Model tracking customer reservation requests. Keeps track of names, emails,
    group sizes, start/end times, reservation dates, publication dates and 
    additional info so an employee might be able to add their reservation 
    and/or customer profile to the database
    """
    name = models.CharField('Organization/Name', max_length=100, )
    email = models.EmailField(max_length=50, default='n/a')
    group_size = models.PositiveIntegerField(default=1)
    reserved_date = models.DateField('Reservation Date', help_text='Date to Reserve')
    start_time = models.TimeField('Start of the Tour', help_text='Tour Time Slot', )
    end_time = models.TimeField('End of the Tour', help_text='End time of Tour')
    pub_date = models.DateTimeField('Date Published', auto_now=True)
    info_text = models.TextField('Additional Info.', max_length=256, default='Other')

    def __str__(self):
        return self.name

    # on submit click on the Request entry page, it redirects to the url below. 
    def get_absolute_url(self):
        return reverse('scheduling:req_index')

    def clean(self):
        for res in Reservation.objects.filter(date__exact=self.reserved_date):
            if res.start_time < self.start_time < res.end_time:
                pass

class Docent(models.Model):
    """
    Profile used to keep track of Docents. Keeps track of their name and 
    email information. Lists date created aswell as the date
    the profile was last updated.
    """
    name = models.CharField('Name', primary_key=True, unique=True, max_length=100, )
    email = models.EmailField(max_length=50, unique=True, default='n/a')
    date_created = models.DateTimeField('Date Created', auto_now=True)
    last_updated = models.DateTimeField('Last updated', auto_now=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scheduling:doc_index')

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Docent.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()


class CustomerProfile(models.Model):
    """
    Profile used to keep track of Customers. Keeps track of their name and 
    email information for contact. Lists date created aswell as the date
    the profile was last updated.
    """
    name = models.CharField('Organization/Name', primary_key=True, unique=True, max_length=100)
    email = models.EmailField(max_length=50, unique=True, default='n/a')
    date_created = models.DateTimeField('Date Created', auto_now=True)
    last_updated = models.DateTimeField('Last updated', auto_now=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scheduling:prof_index')

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while CustomerProfile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()


class Reservation(models.Model):
    """
    Model for tracking reservations. Mapped to a Customer Profile.
    Keeps track of date of reservation, start and end times, the docent 
    assigned to give the tour, and any additional information given at the
    time of creation
    """
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    group_size = models.PositiveIntegerField(default=1)
    actual_group_size = models.PositiveIntegerField(default = 0)
    date = models.DateField('Day of the Reservation', help_text='Date to Reserve')
    start_time = models.TimeField('Start of the Tour', help_text='Tour Time Slot', )
    end_time = models.TimeField('End of the Tour', help_text='End time of Tour')
    pub_date = models.DateTimeField('Date Published', auto_now=True)
    info_text = models.TextField('Additional Info.', max_length=256, default='None')
    docent = models.ForeignKey(Docent, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name

    # redirect URL used after saving a new reservation model
    def get_absolute_url(self):
        return reverse('scheduling:res_index')

    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("Cannot create a reservation in the past.")
        if self.end_time < self.start_time:
            raise ValidationError("Cannot set the end time to before the start time.")
        if Reservation.objects.all().count() != 0:
            for res in Reservation.objects.filter(date__exact=self.date):
                if res.start_time < self.start_time < res.end_time and res.docent.name == self.docent.name:
                    raise ValidationError('Start time overlaps with another reservation assigned to this docent.'
                                          ' Correct the time or choose another docent.')
                if res.start_time < self.end_time < res.end_time and res.docent.name == self.docent.name:
                    raise ValidationError('End time overlaps with another reservation assigned to this docent.'
                                          ' Correct the time or choose another docent.')
                if res.start_time == self.start_time or res.end_time == self.end_time and res.docent.name == self.docent.name:
                    raise ValidationError('Cannot have a reservation with the same start or end time assigned to the '
                                          'same docent, correct the time or choose another docent.')
            filtered = Reservation.objects.filter(date__exact=self.date)
            count = 0
            for res in filtered:
                if res.docent.name == self.docent.name:
                    count += 1
            if count >= 3:
                raise ValidationError('This docent has already been assigned the max amount of reservations for this'
                                      ' day, choose another docent to assign.')


# sends email whenever a new reservation is created
def model_created(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        email_handler(instance)


post_save.connect(model_created, sender=Reservation)
