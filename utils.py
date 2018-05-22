from calendar import HTMLCalendar
import datetime as date
from scheduling.models import Reservation

class ReservationCalendar(HTMLCalendar):
	
	def __init__(self, reservations=None):
		super(ReservationCalendar, self).__init__()
		self.reservations = reservations

	def format_day(self, day, weekday, reservations):
		"""
		Return a day as a table cell.
		"""
		reservations_from_day = reservations.filter(date__day=day)
		reservations_html = "<ul>"
		for res in reservations_from_day:
			reservations_html += res.get_absolute_url() + "<br>"
		reservations_html += "</ul>"

		if date == 0:
			return '<td class="noday">&nbsp;</td>' 
		else:
			return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, reservations_html)

	def format_week(self, theweek, reservations):
		"""
		Return a complete week as a table row
		"""
		s = ''.join(self.format_day(d, wd, reservations) for (d, wd) in theweek)
		return '<tr>%s</tr>' % s

	def format_month(self, theyear, themonth, withyear=True):
		"""
		Return a formatted month as a table.
		"""
		reservations = Reservation.objects.filter(date__month=themonth)

		v = []
		a = v.append
		a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
		a('\n')
		a(self.formatmonthname(theyear, themonth, withyear=withyear))
		a('\n')
		a(self.formatweekheader())
		a('\n')
		for week in self.monthdays2calendar(theyear, themonth):
			a(self.formatweek(week, reservations))
			a('\n')
		a('</table>')
		a('\n')
		return ''.join(v)
