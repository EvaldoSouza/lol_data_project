from riotwatcher import LolWatcher, ApiError
import pandas as pd

# golbal variables
api_key = 'CHAVE_DA_API'
watcher = LolWatcher(api_key)
my_region = 'br1'

me = watcher.summoner.by_name(my_region, 'SiriusPuroMalte')
print(me)

#my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
#print(my_ranked_stats)

#my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
my_matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'])
# fetch last match detail
last_match = my_matches[0]
match_detail = watcher.match.by_id(my_region, last_match)
#participants é uma list de dicts, os dicts tem todas as informações que preciso
print(match_detail)


