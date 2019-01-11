from bs4 import BeautifulSoup as bsoup
import requests as rq
import re

base_url = 'http://www.creationdentreprise.sn/rechercher-une-societe?field_rc_societe_value=&field_ninea_societe_value=&denomination=&field_localite_nid=All&field_siege_societe_value=&field_forme_juriduqe_nid=All&field_secteur_nid=All&field_date_crea_societe_value='
r = rq.get(base_url)

soup = bsoup(r.text, 'html.parser')

page_count_links = soup.find_all("a",href=re.compile(r".http://www.creationdentreprise.sn/rechercher-une-societe?field_rc_societe_value=&field_ninea_societe_value=&denomination=&field_localite_nid=All&field_siege_societe_value=&field_forme_juriduqe_nid=All&field_secteur_nid=All&field_date_crea_societe_value=&page=.*"))
try: 
    num_pages = int(page_count_links[-1].get_text())
except IndexError:
    num_pages = 1


url_list = ["{}&page={}".format(base_url, str(page)) for page in range(1, 3)]

with open("results.txt","w") as acct:
    for url_ in url_list:
        print("Processing {}...".format(url_))
        r_new = rq.get(url_)
        soup_new = bsoup(r_new.text)
        for tr in soup_new.find_all('tr'): 
            stack = []

            # set link_ext to None
            link_ext = None

            # try to get link in last column. If not present, pass
            try:
                link_ext = tr.select('a')[-1]['href']
            except:
                pass

            for td in tr.findAll('td'):
                stack.append(td.text.replace('\n', '').replace('\t', '').strip())

            # if a link was extracted from last column, use it to get html from link and parse wanted data
            if link_ext is not None:
                r_link = rq.get('http://creationdentreprise.sn' + link_ext)
                soup_link_ext = bsoup(r_link.text, 'html.parser')
                region = soup_link_ext.find(text=re.compile('Région:')).parent.nextSibling.text
                capital = soup_link_ext.find(text=re.compile('Capital:')).parent.nextSibling.text
                objet = soup_link_ext.find(text=re.compile('Objet social:')).parent.nextSibling.text

                stack = stack + [region, capital, objet]

            acct.write(", ".join(stack) + '\n') 
