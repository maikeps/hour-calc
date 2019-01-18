import sys

from datetime import datetime


class Time:

	def __init__(self, timestr):
		self.hours = int(timestr.split(':')[0])
		self.minutes = int(timestr.split(':')[1])

	def __sub__(self, other):
		h = self.hours - other.hours
		m = (self.minutes - other.minutes) % 60

		if self.minutes - other.minutes < 0:
			h -= 1

		return Time(str(h)+':'+str(m))

	def __add__(self, other):
		h = self.hours + other.hours
		m = (self.minutes + other.minutes) % 60

		if self.minutes + other.minutes > 60:
			h += 1

		return Time(str(h)+':'+str(m))

	def __str__(self):
		return ('00'+str(self.hours))[-2:] + ':' + ('00'+str(self.minutes))[-2:]


class Calculator:

	def __init__(self, timearr):
		self.timearr = timearr

	def calculate(self):
		now = datetime.now().strftime('%H:%M')

		t1 = Time(self.timearr[0])

		try:
			t2 = Time(self.timearr[1])
		except IndexError:
			return Time(now) - t1

		try:
			t3 = Time(self.timearr[2])
		except IndexError:
			return t2-t1

		try:
			t4 = Time(self.timearr[3])
		except IndexError:
			return t2-t1 + Time(now)-t3

		return t2-t1 + t4-t3

	def predict(self, targetstr, lunchtime):
		time_worked = self.calculate()
		target = Time(targetstr)

		remaining = target - time_worked

		now = Time(datetime.now().strftime('%H:%M'))

		prediction = now + remaining

		# If there was no lunch time yet, add one our to the exit time
		if len(self.timearr) == 1:
			prediction = prediction + Time(lunchtime)

		return prediction


if __name__ == '__main__':
	args = []
	predict = False
	lunchtime = '01:00'
	targetstr = '08:00'

	# Interactive
	if len(sys.argv) == 1:
		argsstr = input('Type in the entry and exit times, formatted like this: hh:mm, hh:mm, [...]\n')
		args = argsstr.replace(' ', '').split(',')
		
		if len(args) < 4:
			predictstr = input('Do you want to predict the exit time at the end of the day? [Y/n]\n')
			predict = not predictstr or predictstr.upper() == 'Y'

		if predict and len(args) == 1:
			lunchtime = input('Type in how long you want your lunchtime to be, formatted like this: hh:mm.\n')

	else:		
		if sys.argv[1] == '-p':
			args = sys.argv[3:]
			targetstr = sys.argv[2]
			predict = True
		else:
			args = sys.argv[1:]

	calc = Calculator(args)

	print()
	print('Hours worked: ' + str(calc.calculate()))
	if predict:
		print('Exit at: ' + str(calc.predict(targetstr, lunchtime)))