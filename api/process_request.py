from os import walk
import csv
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
import sys
import json
import string
import urllib2
from BeautifulSoup import BeautifulSoup
import ConfigParser

LOG_PRODUCTION  = 0
LOG_WARNING     = 1
LOG_ALL_MESSAGE = 10

# LOGLEVEL = LOG_ALL_MESSAGE
LOGLEVEL = LOG_WARNING


class process_request:

    def __init__(self):
        self.load_skill_mapping("../model/skillname_to_skilltags.tsv")
        self.load_stop_words("../model/skill_stop_words.txt")
        
    def load_skill_mapping(self, filename):
        self.skill_map = {} 
        f = open(filename, "r")
        reader = csv.reader(f, delimiter=':')
        for row in reader:
            # print "len", len(row)
            # print "row", row
            # print "row contents %s: %s"%(row[0], row[1])
            self.skill_map[row[0]] = row[1]
            
        f.close()
        print self.skill_map

    def load_stop_words(self, filename):
        stop_words = []
        f = open(filename,"r")
        stop_words += eval(f.readline())

        self.stop_words = stop_words
        # print "stop",  self.stop_words

    def get_job_text(self, job_id, method = 'local'):
        data = None
        #print 'method',method, job_id
        if method == 'local':
            #print "local"
            data = json.load(open("../model/job_desc.json","r"))
            #print "data", data
        elif method == 'mongo':
            data = None
            pass
        if job_id in data.keys():
            job_text = data['%s'%job_id]['job_text']
        else:
            print "Job id not found"
            job_text = None
        return job_text

    def map_skill_to_job_id(self, job_id, method='local'):

        all_matched_skills  = {}

        jobtext = self.get_job_text(job_id, method=method)
        # print "job_text", jobtext
        # print self.stop_words

        tx = CountVectorizer(ngram_range=[1,3],stop_words=None)
        vx = tx.fit_transform([jobtext])
        job_set = set(tx.get_feature_names())
        i  = 0
        for skill, ft in self.skill_map.items():
            matched_skills = {}
            skill_set = set(ft.split(","))
            intersect = job_set.intersection(skill_set)
            score = len(intersect)
            if score >0:
                matched_skills['skill'] = skill
                matched_skills['score'] = score
                matched_skills['matched_tags'] = list(intersect)
                all_matched_skills[i] =  matched_skills
                i += 1

        return all_matched_skills

    def process(self, req, method='local'):

        request = json.loads(req)

        # Test if job text could be loaded
        job_id = request["job_id"]
        if not self.get_job_text(job_id, method=method):
            msg = "ERROR: job text could not be retrieved"
            print msg
            return msg
        else:
            response = self.map_skill_to_job_id(job_id, method=method)
            return response




    def clean_string(self, input=""):
        output = input.replace(':','%3A')
        output = output.replace(',','%2C')
        output = output.replace(' ','+')
        return output


def main():
    pr = process_request()
    test = {"job_id": "12323323"}
    #test = {"job_id": "1232332333"}
    # test = {"keyword": "retail sales","location":"Washington, DC","context": []}
    # test = {"keyword": "retail sales","location":"Washington, DC","context": [{"question":"Can you use devices like scanners?","answer": 1}]}
    #test = {"keyword": "retail sales","location":"Modesto, CA","context": [{"question":"Can you use devices like scanners?","answer": 1}]}
    #print pr.process(json.dumps(test))
    print pr.process(json.dumps(test))
    

if __name__ == '__main__':
    main()
