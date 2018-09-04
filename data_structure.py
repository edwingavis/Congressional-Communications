#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 08:38:38 2018

@author: egavis
"""

import os
import csv

#delete data & rerun post-primaries

def build_file_structure():
    with open("lists/house_2018_sites_gov.csv", 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        for row in spamreader:
            state = row[0]
            race = row[1]
            name = row[3]
            os.makedirs("data"+"/" + state + "/" + race + "/" + name, exist_ok=True)

if __name__ == "__main__":
    build_file_structure()