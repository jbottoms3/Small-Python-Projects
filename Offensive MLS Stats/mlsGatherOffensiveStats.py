import requests
import bs4
import sys
import json

# Webpage to access MLS Player data from page "page"
def getURL(page):
    return 'http://www.mlssoccer.com/stats/alltime?page=%s' % (str(page))

# Scraping offensive stats for each player and keeping data in dictionary 
def gatherStats():
    url = ''
    playerList = []

    outputFile = open('OffensiveOutput.txt', 'w')
    playerFile = open('OffensivePlayers.txt', 'w')
    
    playersDict = dict()

    pageNum = 0

    #New players stop appearing at page 102 due to webpage bug
    while (pageNum < 102):

            print('Working on Page' + str(pageNum))

            url = getURL(pageNum)

            mlsPage = requests.get(url).text
            soup = bs4.BeautifulSoup(mlsPage, "html.parser")

            result = soup.body.find_all('td', {"data-title" : "Player"})

            numPlayersOnPage = len(result)


            for playerTag in result:
                playerName = playerTag.getText()
                GP = playerTag.parent.find_all('td', {"data-title" : "GP"})[0].getText()
                GS = playerTag.parent.find_all('td', {"data-title" : "GS"})[0].getText()
                MINS = playerTag.parent.find_all('td', {"data-title" : "MINS"})[0].getText()
                G = playerTag.parent.find_all('td', {"data-title" : "G"})[0].getText()
                A = playerTag.parent.find_all('td', {"data-title" : "A"})[0].getText()
                SHTS = playerTag.parent.find_all('td', {"data-title" : "SHTS"})[0].getText()
                SOG = playerTag.parent.find_all('td', {"data-title" : "SOG"})[0].getText()
                GWG = playerTag.parent.find_all('td', {"data-title" : "GWG"})[0].getText()
                PKGbyAttempts = playerTag.parent.find_all('td', {"data-title" : "PKG/A"})[0].getText()
                HmG = playerTag.parent.find_all('td', {"data-title" : "HmG"})[0].getText()
                RdG = playerTag.parent.find_all('td', {"data-title" : "RdG"})[0].getText()
                GperNinetyMin = playerTag.parent.find_all('td', {"data-title" : "G/90min"})[0].getText()
                ScoringPct = playerTag.parent.find_all('td', {"data-title" : "SC%"})[0].getText()

                if (playerName not in playersDict):
                    playersDict[playerName] = dict()
                    playersDict[playerName]['Games Played'] = GP
                    playersDict[playerName]['Games Started'] = GS
                    playersDict[playerName]['Minutes Played'] = MINS
                    playersDict[playerName]['Goals'] = G
                    playersDict[playerName]['Assists'] = A
                    playersDict[playerName]['Shots'] = SHTS
                    playersDict[playerName]['Shots on Goal'] = SOG
                    playersDict[playerName]['Game Winning Goals'] = GWG
                    playersDict[playerName]['Penalty Kicks / Attempts'] = PKGbyAttempts
                    playersDict[playerName]['Home Goals'] = HmG
                    playersDict[playerName]['Road Goals'] = RdG
                    playersDict[playerName]['Goals per 90 min'] = GperNinetyMin
                    playersDict[playerName]['Scoring %'] = ScoringPct

                    playerFile.write(playerName.encode('utf-8') + '\n')


            pageNum += 1

    outputFile.write(json.dumps(playersDict, indent=4, sort_keys=True) + '\n')

    outputFile.close()


# Convert json formed above to an excel csv file
def convertToExcel():

    with open('output.txt') as data_file:    
        data = json.load(data_file)

    excelFile = open('mls-excel.csv', 'wb')
    excelFile.write('Player,Games Played,Games Started,Minutes Played,Goals,Assists,Shots,Shots on Goal,Game Winning Goals,Penalty Kicks / Attempts,Home Goals,Road Goals,Goals per 90 min,Scoring %'.encode('utf-8'))
    excelFile.write('\n'.encode('utf-8'))
    for player in data.keys():
        excelFile.write(player.encode('utf-8'))
        excelFile.write(','.encode('utf-8'))

        excelFile.write((data[player]['Games Played']+',').encode('utf-8'))
        excelFile.write((data[player]['Games Started']+',').encode('utf-8'))
        excelFile.write((data[player]['Minutes Played']+',').encode('utf-8'))
        excelFile.write((data[player]['Goals']+',').encode('utf-8'))
        excelFile.write((data[player]['Assists']+',').encode('utf-8'))
        excelFile.write((data[player]['Shots']+',').encode('utf-8'))
        excelFile.write((data[player]['Shots on Goal']+',').encode('utf-8'))
        excelFile.write((data[player]['Game Winning Goals']+',').encode('utf-8'))
        excelFile.write(("'"+data[player]['Penalty Kicks / Attempts']+',').encode('utf-8'))
        excelFile.write((data[player]['Home Goals']+',').encode('utf-8'))
        excelFile.write((data[player]['Road Goals']+',').encode('utf-8'))
        excelFile.write((data[player]['Goals per 90 min']+',').encode('utf-8'))
        excelFile.write((data[player]['Scoring %']+',').encode('utf-8'))
        
        excelFile.write('\n'.encode('utf-8'))

    excelFile.close()

gatherStats()  
convertToExcel()
