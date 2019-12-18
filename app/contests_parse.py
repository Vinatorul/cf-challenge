from secret import key, secret
from datetime import datetime
from random import randint
import requests
import hashlib
import time


class Parsing:
    def __init__(self, id):
        self.rand = str(randint(100000,1000000))
        self.t = str(int(time.time()))
        self.id = id

        self.hashed = f'{self.rand}/contest.standings?apiKey={key}&contestId={self.id}&time={self.t}#{secret}' 
        self.hashed = self.hashed.encode('utf-8')
        self.hashed = str(hashlib.sha512(self.hashed).hexdigest())

        self.ref = f'https://codeforces.com/api/contest.standings?contestId={self.id}&apiKey={key}&time={self.t}&apiSig={self.rand}{self.hashed}'
        try:
            self.response = requests.get(self.ref).json()['result']
        except:
            return None
            
    def status(self):
        return requests.get(self.ref).status_code
    
    def get_name(self):
        return self.response['contest']['name']

    def get_problems(self):

        self.problems = []
        for i in range(len(self.response['problems'])):
            self.problems.append(self.response['problems'][i])
        return self.problems


    def get_solutions(self):
        
        self.results = []
        self.handles = []
        
        for i in range(len(self.response['rows'])):
            self.handles.append(self.response['rows'][i]['party']['members'][0]['handle'])
   
        self.last_rating = get_rating(self.handles)
        
        for i in range(len(self.response['rows'])):
            self.points = int(self.response['rows'][i]['points'])
            self.penalty = self.response['rows'][i]['penalty']
            self.solutions = {}

            for j in range(len(self.response['rows'][i]['problemResults'])):

                if self.response['rows'][i]['problemResults'][j]['points'] != 0:

                    self.solutionsTime = self.response['rows'][i]['problemResults'][j]['bestSubmissionTimeSeconds']
                    self.solutionsTime = datetime.utcfromtimestamp(self.solutionsTime).strftime('%H:%M:%S')
                    self.tries = self.response['rows'][i]['problemResults'][j]['rejectedAttemptCount']
                    self.solutions[j] = [f'+{self.tries}' if self.tries > 0 else '+', self.solutionsTime] 
                else:
                    self.solutions[j] = [' ', ' '] 

            self.results.append([self.handles[i], self.last_rating[i], self.points, self.penalty, self.solutions])
            
        return self.results


def get_rating(handles):
    print(handles, len(handles))
    if len(handles) > 1:
        handles = ";".join(handles)
    else:
        handles = handles[0]
        
    last_rating = []
    
    ref = f'https://codeforces.com/api/user.info?handles={handles}'
    rating = requests.get(ref).json()
    for i in range(len(handles)):
        try:
            last_rating.append(rating['result'][i]['rating'])
        except:
            last_rating.append(0)
    print(ref)
    return last_rating