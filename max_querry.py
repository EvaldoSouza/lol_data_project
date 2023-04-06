from riotwatcher import LolWatcher, ApiError
import csv
import pandas as pd


# golbal variables
api_key = 'RGAPI-5397e491-17a3-4184-9659-06c7c51825ff'
watcher = LolWatcher(api_key)
my_region = 'br1'
summoner = 'SiriusPuroMalte'

me = watcher.summoner.by_name(my_region, summoner)
my_matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'], count= 100)

filename = summoner + '_matches.csv'
df = pd.DataFrame(my_matches)
#salvando para csv
df.to_csv(str(filename))
