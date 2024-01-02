from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class dataSesion:
    def __init__(self, legislatureName, sesionName, topic, sesionDate, boletin, quantityYes, quantityNo, quantityAbs, quantityPareo):
        self.legislature = legislatureName
        self.name = sesionName
        self.topic = topic
        self.date = sesionDate
        self.boletin = boletin
        self.quantityYes = quantityYes
        self.quantityNo = quantityNo
        self.quantityAbs = quantityAbs
        self.quantityPareo = quantityPareo
        self.votesSesions = []

    def addVote(self, vote):
        self.votesSesions = vote

def parsedUrl(url):
    urlParsed = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    page = urlopen(urlParsed).read().decode()
    soup =  BeautifulSoup(page, features="html.parser")

    return soup

def getSalary(url):
    soup = parsedUrl(url)
    section = soup.find('section', {'class':'seccion2 sans'})
    table_trs = section('tr')
    salaryData = []

    for tr in table_trs:
        myData = []
        td_data = tr.findAll('td')

        if(len(td_data) != 0 ):
            #print('----------')

            for data in td_data:
                myData.append(data.text)

            salaryData.append(myData)
            #print(myData)
    
    allData.append(salaryData)
    return allData

def getSupportSenadores(url):
    soup = parsedUrl(url)
    names = soup.findAll('h1')
    mySupportData = []

    for name in names:
        #NAME - [#asesor - #funcion - #c.juridica - #monto - #consejero regional - #concejal - #otro parlamentario - #Contrato]
        mySupport = [name.text]
        supports = soup.find('table', id=name.text).findAll('tr')
        
        #print("------")
        for support in supports:
            dataSupport = []

            if(len(support.attrs) != 1):
                tds = support.findAll('td')
                for td in tds:
                    dataSupport.append(td.text)
                    
                mySupport.append(dataSupport)
        
        mySupportData.append(mySupport)
        #print(mySupport)
    
    #print(mySupportData)
    return mySupportData

def getExternalConsults(url):
    soup = parsedUrl(url)
    names = soup.findAll('h1')
    myExternalAsesor = []

    for name in names:
        myAsesor = [name.text]
        asesorConsult = soup.find('table', id=name.text).findAll('tr')

        #print("------")
        for asesor in asesorConsult:
            #0 NombreAsesor - 1 Materia - 2 Monto - 3 Observaciones - 4 Consejero Regional - 5 Consejal - 6 Otro Parlamentario - 7 Contrato/Informes
            dataAsesor = []
            
            if(len(asesor.attrs) != 1):
                tds = asesor.findAll('td')
                for td in tds:
                    dataAsesor.append(td.text)
                    
                myAsesor.append(dataAsesor)

        myExternalAsesor.append(myAsesor)
        #print(myAsesor)
    
    #print(myExternalAsesor)
    return myExternalAsesor

def getOperationalExpenses(url):
    soup = parsedUrl(url)
    tables = soup.findAll('table')
    myOperationalExpenses = []

    for table in tables:
        #print("-----")
        tds = table.findAll('td')
        myOperational= []
        myAuxOperational = []

        for td in tds:
            if(len(td.attrs) == 0):
                if(len(td.text) != 0):
                    myAuxOperational = []
                    myAuxOperational.append((td.text).strip())
            if(len(td.attrs) == 1):
                if(td.attrs != {"colspan": "12"}):
                    myAuxOperational.append((td.text).strip())
                    myOperational.append(myAuxOperational)
                else:
                    myOperational.append(td.text.strip())
        
        if(len(myOperational) != 0):
            myOperationalExpenses.append(myOperational)
    return myOperationalExpenses

def getVotesInSesions(url):
    urlx = url + "index.php?mo=sesionessala&ac=votacionSala&legiini=462"
    soup = parsedUrl(urlx)
    legislature = soup.find('select', attrs={"name":"legislaturas"})
    legislatureOptions = legislature('option')
    sesionsData = []

    for option in legislatureOptions:
        urlLegislature = urlx + "&legiid=" + option['value']
        soupOption = parsedUrl(urlLegislature)
        sesions = soupOption.find('select', attrs={"name":"sesionessala"})
        sesionsOptions = sesions('option')
        #print(sesionsOptions)

        for optionS in sesionsOptions:
            countAux = 0
            countVotes = 0
            soupTopics = parsedUrl(urlLegislature + "&sesiid=" + optionS['value'])
            topics = soupTopics.findAll('td', attrs={"class": "clase_td", "style": "background-color: #EEEEEE"})
            resumeData = soupTopics.findAll('td', attrs={"class": "clase_td", "style": "background-color: #FFFFFF"})
            votes = soupTopics.findAll('a', attrs={"style": "background-color: #2A335D; color: #FFFFFF; border-radius: .5em; padding: 6px"})

            if(len(topics) > 0):
                for topic in topics:
                    print("-----")
                    print(urlLegislature + "&sesiid=" + optionS['value'])
                    this = dataSesion(option.text, optionS.text, topic.text.strip(), resumeData[countAux].text, resumeData[countAux + 1].text,
                                      resumeData[countAux + 2].text, resumeData[countAux + 3].text, resumeData[countAux + 4].text,
                                      resumeData[countAux + 5].text)
                    #print(topic.text)
                    urlVotation = url + votes[countVotes]['href']
                    print(urlVotation)
                    soupVotation = parsedUrl(urlVotation)
                    trs = soupVotation.findAll('tr')
                    
                    attrs = []
                    for tr in trs:
                        tds = tr.findAll('td')
                        countAttrs = 0

                        for td in tds:
                            if(countAttrs == 0 ):
                                attrs.append(td.text)
                            elif(td.img != None):
                                if(countAttrs == 1):
                                    attrs.append("Si")
                                elif(countAttrs == 2):
                                    attrs.append("No")
                                if(countAttrs == 3):
                                    attrs.append("Abstención")
                                elif(countAttrs == 4):
                                    attrs.append("Pareo")

                            countAttrs += 1

                    this.addVote(attrs)

                    countAux += 6
                    countVotes += 1
                    sesionsData.append(this)

                    print(this.topic)
                    print(this.votesSesions)
        



def getDataSenadores():
    print("TRANSAPARENCIA")
    print("Cargando salarios")
    #salaries = getSalary(links[0])
    print("Cargando Personal de apoyo")
    #supports = getSupportSenadores(links[1])
    print("Cargando Asesorias Externas")
    #asesorExternal = getExternalConsults(links[2])
    print("Cargando Gastos Operacionales")
    #opExpenses = getOperationalExpenses(links[3])
    print("Cargando Votaciones de Senadores")
    votes = getVotesInSesions(links[4])
    print("END TRANSAPARENCIA")
    

#RECORDATORIO, ANTES DE EJECUTAR LA ACTUALIZACION, VACIAR LA BD POR CONSOLA
links = ["https://www.senado.cl/appsenado/index.php?mo=transparencia&ac=informeTransparencia&tipo=7&anno=2023&mesid=0",
         "https://www.senado.cl/appsenado/index.php?mo=transparencia&ac=informeTransparencia&tipo=15&anno=2023&mesid=0",
         "https://www.senado.cl/appsenado/index.php?mo=transparencia&ac=informeTransparencia&tipo=16&anno=2023&mesid=0",
         'https://www.senado.cl/appsenado/index.php?mo=transparencia&ac=informeTransparencia&tipo=20&anno=2023&mesid=9',
         "https://www.senado.cl/appsenado/"]

# 0 Salary - 1 Gastos - 
allData = []
getDataSenadores()