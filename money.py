import gspread
from oauth2client.service_account import ServiceAccountCredentials
def getMoney(user):
	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('robotics-754c481f15d8.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1SR8wfO0b1b8wK5avQ0tLWPAYFPRcGPyczoJECl9EclI/").sheet1

	membersList = {}
	person = ""
	i = 0
	members = wks.col_values(1)
	money = wks.col_values(9)
	# if user not in members:
	# 	return "not a user in the spreadsheet"
	for person in members:
		if(person not in membersList):
			memMon = money[i]
			if(memMon=="-"):
				memMon = "0"
			memMonlen = len(memMon)
			membersList[person] = memMon[0:memMonlen-4]
			i += 1
	if(user not in membersList):
		return "Not a user in the spreadsheet"

	return(membersList[user])