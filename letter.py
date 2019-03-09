import gspread
from hours import getHours
from go import getAll
from oauth2client.service_account import ServiceAccountCredentials
def lettering(user):
	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('robotics-754c481f15d8.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1SR8wfO0b1b8wK5avQ0tLWPAYFPRcGPyczoJECl9EclI/").sheet1

	person = ""
	i = 0
	lettered = False

	members = wks.col_values(1)
	hours = wks.col_values(2)
	fundraisingHours = wks.col_values(5)
	FIRSTEvent = wks.col_values(8)
	volHours = wks.col_values(8)
	money = wks.col_values(9)

	membersHours = {}
	membersFundraisingHours = {}
	membersFIRSTEventHours = {}
	membersVolHours = {}
	membersMoney = {}


	for person in members:
		membersHours[person] = hours[i]
		membersFundraisingHours[person] = fundraisingHours[i]
		membersFIRSTEventHours[person] = FIRSTEvent[i]
		membersVolHours[person] = volHours[i]
		membersMoney[person] = money[i]

		i += 1

	# Code below fixes money
	membersMoney[user] = str(membersMoney[user]).replace("$", "").replace(".", "").strip()

	

	theirHoursSplit = getHours(user).strip().split(":")
	theirHoursSplitCoverted = round(((int(theirHoursSplit[0]) * 60) + int(theirHoursSplit[1]))/60)
	
	# code below gets hours and converts to minutes
	usersHours = theirHoursSplitCoverted
	usersFundraisingHours = int(membersFundraisingHours[user].split(".")[0])
	usersVolHours = int(membersVolHours[user])
	usersMoney = int(membersMoney[user])
	# Code below gets how far away you are from lettering
	hoursLeft = (round(5400 - (usersHours * 60)))/60
	fundraisingHoursLeft = 5-int(usersFundraisingHours)
	volHoursLeft = int(3 - usersVolHours)
	moneyLeft = int(400 - usersMoney)

	if(hoursLeft + fundraisingHoursLeft + volHoursLeft + moneyLeft < 0):
		return "Good job " + user + " you have lettered! I am also sending your currrent overview"
	else:
		return "You are close to lettering. I am sending your stuff to you so that you know how far away you are." 