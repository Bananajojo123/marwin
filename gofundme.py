import requests
def getDonations():
	r = requests.get('https://www.gofundme.com/help-missoula-robotics-team-get-to-calgary')
	results = (r.text[r.text.find('<h2 class="goal">') : r.text.find('<span class="smaller">')])
	results2 = results.replace('<h2 class="goal">', "")
	results3 = results2.replace('<strong>', "")
	resultsFinal = str(results3.replace('</strong>', "").strip())
	print(resultsFinal)
	return(resultsFinal)