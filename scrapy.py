from bs4 import BeautifulSoup as bsoup
import requests as rq
import re

base_url = 'http://www.creationdentreprise.sn/rechercher-une-societe?field_rc_societe_value=&field_ninea_societe_value=&denomination=&field_localite_nid=All&field_siege_societe_value=&field_forme_juriduqe_nid=All&field_secteur_nid=All&field_date_crea_societe_value='
r = rq.get(base_url)

soup = bsoup(r.text)
# Use regex to isolate only the links of the page numbers, the one you click on.
page_count_links = soup.find_all("a",href=re.compile(r".http://www.creationdentreprise.sn/rechercher-une-societe?field_rc_societe_value=&field_ninea_societe_value=&denomination=&field_localite_nid=All&field_siege_societe_value=&field_forme_juriduqe_nid=All&field_secteur_nid=All&field_date_crea_societe_value=&page=.*"))
try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[-1].get_text())
except IndexError:
    num_pages = 1

# Add 1 because Python range.
url_list = ["{}&page={}".format(base_url, str(page)) for page in range(1, 3)]

# Open the text file. Use with to save self from grief.
with open("results.txt","w") as acct:
    for url_ in url_list:
        print("Processing {}...".format(url_))
        r_new = rq.get(url_)
        soup_new = bsoup(r_new.text)
        for tr in soup_new.find_all('tr'): 
            stack = []
            for td in tr.findAll('td'):
                stack.append(td.text.replace('\n', '').replace('\t', '').strip())
            acct.write(", ".join(stack) + '\n')
