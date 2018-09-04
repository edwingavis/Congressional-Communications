import urllib3 
import time
#import progressbar
import bs4
import random
import os

#USE BREHM->SEARCHES TO PULL TWITTER ACCOUNTS!!!

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()    

def scrape(site, state, race, name):
    checked = {}
    remaining = [site] #may use another data structure (collections.)
    while remaining:
        url = remaining.pop() #LIFO
        if url in checked:
            continue
        checked.add(url)
        html = get_html(url)
        if not html:
            continue #may not be necessary 
        soup, links = get_soup_links(html, site)
        for link in links: 
            remaining.append(link)
        #write str(soup) to file
        write_file(soup)
      
def write_file(site, state, race, soup):
    '''
    '''
    file_path = 'propublica/' + state + '_' + str(race)
    with open(file_path, 'w') as f: 
        #print("Writing FILE %s" % file_path)
        f.write(str(soup))

        
def get_html(url):
    '''
    '''
    #put try/except in here 
    rv = "" #may be wrong datatype
    try:
        r = http.request('GET', url)
        rv = r.data
    except:
        print("Error scraping %s" % url)
    return rv 

def get_soup_links(html, site):
    '''
    '''
    #finish
    soup = bs4.BeautifulSoup(html, 'lxml')
    new_links = soup.find_all("a")
    links = {} #need to make it only links to same site (+relative)
    for l in new_links:
        if site in l: 
        #p needs something like l.data / l.html etc. 
        #plus account for relative links
        #could speedup w/ regex search?
            links.add(l)
    return soup, links

###############################
     
def main():
    '''
    deprecated, kept for time.sleep(random) examples
    '''
    #i = 0
    bar = progressbar.ProgressBar()
    for state in bar(elections.states[5:]):
        for race in range(elections.races[state]):
            url = build_url(state, race + 1) 
            html = get_html(url)
            write_file(html, state, race)
            sleep_time = random.randint(4,7)
            time.sleep(sleep_time)
        time.sleep(sleep_time * max(random.random() * 2, 1))
    
if __name__ == '__main__':
	pass
