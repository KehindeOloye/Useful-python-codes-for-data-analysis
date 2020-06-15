from __future__ import division
import os, json, ast
import pandas as pd
import math
from collections import Counter
import csv

def pad(l, content, width):
    l.extend([content] * (width - len(l)))
    return l

def controlmaximum(list,maxsize):
    size = len(list)
    if size > maxsize:
        difference = size - maxsize
        del list[-difference:]
    return list

def controlminimum(list,maxsize):
    size = len(list)
    if size < maxsize:
        difference = maxsize - size
        for x in range(difference):
            list.append(0)
    return list

def controlmaxmin(list,maxsize):
    size = len(list)
    if maxsize > size:
        controlminimum(list,maxsize)
    elif maxsize < size:
        controlmaximum(list,maxsize)
    return list

def thejson(path):
    json_file = path
    with open(json_file, 'r') as f:
        json_text = json.load(f)
        maxapi = 5
        maxcontentresolve = 5
        maxtheerror = 3
        maxdex = 5
        maxfileexistx = 5
        thedex = json_text['droidmon']['DexFile']
        thedex = controlmaxmin(thedex, maxdex)
        fileexist = json_text['droidmon']['api']['java_io_File_exists']
        contentresolve = json_text['droidmon']['ContentResolver_queries']
        contentresolve = ast.literal_eval(json.dumps(contentresolve))
        contentresolve = controlmaxmin(contentresolve, maxcontentresolve)
        theerror = json_text['droidmon']['error']
        theerror = ast.literal_eval(json.dumps(theerror))
        theerror = controlmaxmin(theerror, maxtheerror)
        the_list = []
        #the_list + contentresolve
        the_list.append(tuple(contentresolve))
        #the_list.extend(contentresolve)
        #the_list + [theerror]
        the_list.append(tuple(theerror))
        #the_list.extend(theerror)
        #the_list + [thedex]
        the_list.append(tuple(thedex))
        #the_list + [fileexist]
        the_list.append(fileexist)
    return the_list

def tocsv(path):
    mylist=thejson(path)
    with open('jsonfile', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(mylist)

def counter_cosine_similarity(path1,path2):
    list1 = thejson(path1)
    list2 = thejson(path2)
    c1= Counter(list1)
    c2 = Counter(list2)
    terms = set(list1).union(list2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def myjson():
    path_to_json = '~/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    jsons_data = pd.DataFrame(columns=['contentresolve', 'theerror', 'thedex', 'fileexist'])
    # both the json and an index number are needed to use enumerate()
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            maxapi=5
            maxcontentresolve=5
            maxtheerror=3
            maxdex=5
            maxfileexistx=5
            thedex = json_text['droidmon']['DexFile']
            thedex = controlmaxmin(thedex, maxdex)
            fileexist=json_text['droidmon']['api']['java_io_File_exists']
            contentresolve = json_text['droidmon']['ContentResolver_queries']
            contentresolve = controlmaxmin(contentresolve, maxcontentresolve)
            theerror = json_text['droidmon']['error']
            theerror=controlmaxmin(theerror,maxtheerror)
            # here I push a list of data into a pandas DataFrame at row given by 'index'
            jsons_data.loc[index] = [contentresolve, theerror, thedex, fileexist]
    print(jsons_data)
