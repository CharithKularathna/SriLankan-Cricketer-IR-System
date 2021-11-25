import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
#from translate import Translator

_URL = "https://en.wikipedia.org/wiki/List_of_Sri_Lanka_ODI_cricketers"

data = {
    "name":[],   #text
    "bio":[],    #text
    "years":[],  #text
    "matches":[],
    "runs_scored":[],
    "highest_score":[],
    "bat_avg":[],
    "wickets":[],
    "runs_conceded":[],
    "best_figures":[], #text
    "ball_avg":[],
    "catches_taken":[]
}

#translator= Translator(to_lang="si")

#Call urlopen (this is the web client that helps to open the webpage)
#Opens the url, Grabs the page, close the connection
#Then soup can convert the HTML data to a certain useful format

def getUrl(name):
    suf = "_".join(list(name.split()))
    return ("https://en.wikipedia.org/wiki/" + suf)

uClient = uReq(_URL)
htmlPage = uClient.read()
uClient.close()

#HTML parsing with BeautifulSoup
webpage = soup(htmlPage, "html.parser")

table = webpage.find("table",{"class":"wikitable"})
rowArray = table.findAll('tr')

for i in range(2,len(rowArray)):
    name = rowArray[i].find("a").text
    values = rowArray[i].findAll("td")
    years = values[2].text
    matches = int(values[3].text)
    catches_taken = int(values[15].text)
    
    try:
        bat_avg = float(values[8].text)
        runs_scored = int(values[6].text)
        highest_score= values[7].text
    except:
        bat_avg = 0.00
        runs_scored = 0
        highest_score = "0"
    
    try:
        wickets = int(values[12].text)
        runs_conceded = int(values[11].text)
        best_figures = values[13].text
        ball_avg = float(values[14].text)
    except:
        wickets = 0
        runs_conceded = 0
        best_figures = "0/0"
        ball_avg = 0.00
    '''
    data["name"].append(name)
    data["years"].append(years)
    data["matches"].append(matches)
    data["runs_scored"].append(runs_scored)
    data["highest_score"].append(highest_score)
    data["bat_avg"].append(bat_avg)
    data["catches_taken"].append(catches_taken)
    data["wickets"].append(wickets)
    data["runs_conceded"].append(runs_conceded)
    data["best_figures"].append(best_figures)
    data["ball_avg"].append(ball_avg)
    '''
    
    bioUrl = getUrl(name)
    
    uClient1 = uReq(bioUrl)
    htmlPage1 = uClient1.read()
    uClient1.close()
    
    bioWebpage = soup(htmlPage1, "html.parser")
    bio = bioWebpage.find_all("p")[0].get_text()
    if (bio == "\n" or bio == ""):
        bio = bioWebpage.find_all("p")[1].get_text()
    #data["bio"].append(bio)
    
    temp = {
        "name":name,   #text
        "bio":bio,    #text
        "years":years,  #text
        "matches":matches,
        "runs_scored":runs_scored,
        "highest_score":highest_score,
        "bat_avg":bat_avg,
        "wickets":wickets,
        "runs_conceded":runs_conceded,
        "best_figures":best_figures, #text
        "ball_avg":ball_avg,
        "catches_taken":catches_taken
    }
    
    json_object = json.dumps(temp)
    file_name = str(i-1) + ".json"
    
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
    
    
    
    
#print(data)


