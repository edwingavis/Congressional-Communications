import requests
import time
import progressbar
import bs4
import random
import csv
import os

#USE BREHM->SEARCHES TO PULL TWITTER ACCOUNTS!!!

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#http = urllib3.PoolManager()    

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
#pretending to be chrome

CAMPAIGNS = True
HOUSE = False

STOPPED = ("CA", "28")
#issues:
#tabitha isner -- AL2 -- some kind of SPA
#PROBABLY MISSED A FEW OTHERS IN FIRST 42, 
#could just filter for len(os.listdir)==1 
#greg stanton, not sure why campaign not work: stantonforarizona.com
#jared huffman CA2 - campaign site
#DALE MENSING CA2 - campaign site
#salud carbajal - error every page
#mark reed ca30

def main():
    with open("../lists/house_2018_sites_gov.csv") as csvfile:
        spamreader = csv.reader(csvfile)
        for _ in range(0): 
            next(spamreader)
            #skip don young... mike rogers
        bar = progressbar.ProgressBar()
        cont = True
        for row in bar(spamreader):
            state, race= row[0:2]
            name, c_site, g_site = row[3:6]
            #house site:
            if (state, race) == STOPPED:
                cont = False
                #continue #if second candidate
            if cont:
                continue
            print("\nScraping %s %s %s" % (state, race, name))
            if HOUSE and g_site:
                house_folder = "../data/%s/%s/%s/house_site" % (state, race, name)
                os.makedirs(house_folder, exist_ok = True)
                scrape(g_site, house_folder)
            if CAMPAIGNS and c_site:
                camp_folder = "../data/%s/%s/%s/elect_site" % (state, race, name)
                os.makedirs(camp_folder, exist_ok = True)
                scrape(c_site, camp_folder)  

def scrape(site, folder):#, state, race, name):
    checked = set()
    remaining = [site] #may use another data structure (collections.)
    while remaining:
        url = remaining.pop() #LIFO
        if url.lower().strip() in checked or check_url(url):
            continue
        checked.add(url.lower().strip())
        html = get_html(url)
        if not html:
            continue #may not be necessary 
        soup, links = get_soup_links(html, site)
        for link in links: 
            remaining.append(link)
        #write str(soup) to file
        write_file(folder, url, soup)#, state, race, name)
        sleep_time = 3 * random.random()
        time.sleep(sleep_time)
      
def check_url(url):
    known = {"watch", "youtube", ".aspx", "#", ".pdf", 
             "user", "twitter", "facebook", "mailto",
             ".jpg", ".png", ".bmp", ".jpeg", ".xls", "tel:",
             "ical", "javascript", "action", "gallery", ".mp4"}
    lowered = url.lower()
    for v in known:
        if v in lowered:
            return True
    return False
        
def write_file(folder, url, soup):
    '''
    '''
    fname = "/" + url.strip("https: ").replace(
                       "//","").replace("/","_").replace(".","_")
    if len(fname) > 150:
        fname = fname[:150]
    print("Scraped:\t%s" % fname)
    with open(folder + fname + '.html', 'w') as f: 
        f.write(str(soup))
        
def get_html(url):
    '''
    '''
    #put try/except in here 
    rv = "" #may be wrong datatype
    try:
        header = {'User-Agent':UA}
        rv = requests.get(url, headers=header).text
    except:
        print("Error scraping %s" % url)
    return rv 

def get_soup_links(html, site):
    '''
    '''
    #finish
    soup = bs4.BeautifulSoup(html, 'lxml')
    new_links = soup.find_all("a", href=True)
    links = set() #need to make it only links to same site (+relative)
    #print(new_links)
    for l in new_links:
        if site in l['href']: 
        #p needs something like l.data / l.html etc. 
        #plus account for relative links
        #could speedup w/ regex search?
            links.add(l['href'])
        elif "/" not in l['href'] or l['href'][0] == "/":
            relative = l['href'].strip("/")
            combined = site + relative
            links.add(combined)
    return soup, links

#time.sleep(sleep_time * max(random.random() * 2, 1))

if __name__ == '__main__':
	main()
