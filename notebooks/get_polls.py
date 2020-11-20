import urllib.request
import pandas as pd
import datetime
from urllib.error import URLError
import os.path
if not os.path.isfile('president_polls.csv') :
    url = "https://projects.fivethirtyeight.com/polls-page/president_polls.csv"
    try:
        with urllib.request.urlopen(url) as request:
            data = request.read().decode('utf-8')
            with open('president_polls.csv','w',encoding='utf-8') as f:
                f.write(data)
    except URLError:
        print('Erreur de téléchargement! Télécharger manuellement:\n'+url)
electoral_votes = pd.read_csv('electoral_votes.csv',header=None,names=['state','votes'],index_col=0)
polls = pd.read_csv('president_polls.csv',low_memory=False)
polls.start_date = pd.to_datetime(polls.start_date,format='%m/%d/%y')
polls = polls[polls.start_date > datetime.datetime(2020,7,1)]
polls = polls[polls.answer.isin(['Biden','Trump'])]
polls = polls[~polls.state.isna()]
polls = polls[['state','sample_size','answer','pct']]
polls = polls.reset_index(drop=True)
polls['votes']=electoral_votes.loc[polls.state].reset_index(drop=True)

with open('president_polls_parsed.csv','w') as f:
    polls.to_csv(f, index=False)