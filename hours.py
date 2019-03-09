import gspread
from oauth2client.service_account import ServiceAccountCredentials
def getHours(user):
	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('robotics-754c481f15d8.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1SR8wfO0b1b8wK5avQ0tLWPAYFPRcGPyczoJECl9EclI/").sheet1

	membersDict = {}
	person = ""
	i = 0
	members = wks.col_values(1)
	hours = wks.col_values(2)

	for person in members:
		membersDict[person] = hours[i]
		i += 1		



	print(membersDict[user])
	return(membersDict[user])