#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:41:40 2018

@author: egavis
"""

import os
import json
import csv
import re
import collections

import progressbar
import jellyfish

SITE_REGEX = re.compile("[a-z]*://[a-z0-9\.\-]*/")


def main():
    '''
    '''
    #this currently finds all house.gov web addresses heuristically 
    rep_sites = pull_house_urls("house.gov")
    with open("lists/house_2018_websites.csv", 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        labels = next(spamreader) #may be able to just give column titles...
        with open("lists/house_2018_sites_gov.csv", 'w') as csvfile2:
            spamwriter = csv.writer(csvfile2)
            spamwriter.writerow(labels[:-1] + ["GOV_SITE"] + [labels[-1]])
            bar = progressbar.ProgressBar()
            for row in bar(spamreader):
                if "I" not in row[2]:
                    spamwriter.writerow(row[:-1] + [""] + [row[-1]])                        
                    continue
                match = [get_match(row[0], row[3], rep_sites)]
                spamwriter.writerow(row[:-1] + match + [row[-1]])                        

def get_match(state, name, r_sites):
    best = (0, "")
    names = name.split(" ")
    for possible in r_sites[state]:
        scores = []
        possibles = possible.split(" ")
        for p in possibles:
            for n in names:
                score = jellyfish.jaro_winkler(p, n.upper())
                if len(scores) < 2:
                    scores.append(score)
                else:
                    scores.sort()
                    if score >= scores[0]: 
                        scores[0] = score
        total = sum(scores)
        if total > best[0]:
            url = re.findall(SITE_REGEX, r_sites[state][possible])[0]
            best = (total, url)
    return best[1]

def pull_house_urls(term):
    reps = collections.defaultdict(dict)
    f_names = os.listdir("searches") #mkdir and fill
    for name in f_names:
        try:
            with open("searches/%s" % name) as f:
                data = json.load(f)
                state = name[2:4]
                query = data['queryContext']['originalQuery']
                name = query.strip("for congress")
                for v in data["webPages"]["value"]:
                    url = v["url"]
                    if term in url:
                        reps[state][name] = url
                        break #heuristic 
        except Exception as e:
            print(e)
    return reps
        
if __name__ == "__main__":
    main()