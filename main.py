from bs4 import BeautifulSoup
import urllib.request
import html2text
import json

listaubicaciones = []
Eventos = {}
Eventos['Eventos'] = []

def localizacion(URL): 
    onURL = urllib.request.urlopen(URL)
    if(onURL.getcode == 404):
        print("FIN")
    else:
        soup = BeautifulSoup(onURL, 'html.parser')
        review2=[]

        for i in soup.find_all('div', {'class':'bloque-info-caption bloque-info-link text-uppercase bloque-info-caption-on'}):
            cada_uno2=i.find_all('a')
            #print(per_review)
            review2.append(cada_uno2)

        new_review2 = []
        h = html2text.HTML2Text()
        h.ignore_links = True

        

        for each2 in review2:
            new_each2 = str(each2).replace('<a class="pull-left">', '')
            new_each2 = h.handle(new_each2)
            ubicacion = new_each2.split(",")[1]
            ubicacion = ubicacion.strip()
            ubicacion = ubicacion.replace(']','')
            listaubicaciones.append(ubicacion)
            new_review2.append(ubicacion)

def paginas(URL):
    onURL = urllib.request.urlopen(URL)
    if(onURL.getcode == 404):
        print("FIN")
    else:
        soup = BeautifulSoup(onURL, 'html.parser')
        review=[]

        for i in soup.find_all('div', {'class':'bloque-info-caption bloque-info-caption-main'}):
            cada_uno=i.find('a')
            review.append(cada_uno)

        new_review = []
        h = html2text.HTML2Text()
        h.ignore_links = True
        i = 0
        for each in review:
            new_each = str(each).replace('<span class="fecha_evento">', '')
            new_each = str(each).replace('<a href="*" title="*">','')
            new_each = h.handle(new_each)
            new_each = new_each.replace('\n\n', '')
            fecha = new_each[0:6]
            titulo = new_each[8:len(new_each)]
            print(new_each)
            localizacion(URL)
            print(listaubicaciones[i])
            i = i+1
            Eventos['Eventos'].append({
                'Fecha' : fecha,
                'Nombre' : titulo, 
                'Localización' : listaubicaciones[i]
            })
            with open('Eventos.json', 'w') as file:
                json.dump(Eventos, file, indent=4)
        

for i in range (1,8):
    i = str(i)
    paginas("https://www.andalucialab.org/eventos/page/"+i+"/")
    i = int(i)