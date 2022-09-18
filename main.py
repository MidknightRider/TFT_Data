from riotwatcher import TftWatcher, ApiError

tft_watcher = TftWatcher('<API-KEY>')

my_region = 'na1'  # your region

me = tft_watcher.summoner.by_name(my_region, '<summoner_name>')
puuid = me['puuid']
print(me['name'])

# all objects are returned (by default) as a dict
my_ranked_stats = tft_watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats[0]['tier'], my_ranked_stats[0]['rank'])

# First we get the latest version of the game
versions = tft_watcher.match.by_puuid(my_region, puuid, 20)
latest_match_id = versions[0]

match = tft_watcher.match.by_id(my_region, latest_match_id)  # latest match

# Displaying the data for the most recent match
for i in range(len(match['info']['participants'])):
    if match['info']['participants'][i]['puuid'] == puuid:
        print("Augments:")
        for j in range(3):
            print((match['info']['participants'][i]['augments'])[j])
        print("Placement:", match['info']['participants'][i]['placement'])
        break

# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").

try:
    response = tft_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
