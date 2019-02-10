import requests
def getCommits(organ, repoName):
	repositoryName = repoName
	organization = organ 
	r = requests.get('https://github.com/' + organization + '/' + repositoryName)
	results = (r.text[r.text.find('<span class="num text-emphasized">') : r.text.find('<a data-pjax href="/' + organization+'/'  + repositoryName + '/branches">')])
	results2 = results.split('<span class="num text-emphasized">')
	results3 = results2[1]
	results4 = str(results3[0:results3.find("</span>")])
	resultsFinal = results4.strip()
	return(resultsFinal)