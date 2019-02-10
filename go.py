import gspread
from oauth2client.service_account import ServiceAccountCredentials
def getAll(user):
	scope = ['https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('robotics-754c481f15d8.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1SR8wfO0b1b8wK5avQ0tLWPAYFPRcGPyczoJECl9EclI/edit#gid=0").sheet1

	membersList = {}
	person = ""
	i = 0
	members = wks.col_values(1)
	# if user not in members:
	# 	return "not a user in the spreadsheet"
	for person in members:
		if(person not in membersList):
			membersList[person] = i
			i += 1
	if(user not in membersList):
		return "Not a user in the spreadsheet"

	userRow = wks.row_values(int(membersList[user])+1)
	print(userRow)
	return(userRow)