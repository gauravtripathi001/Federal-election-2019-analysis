from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import json

def get_json_data(url):
    req = Request(url)
    while True:
        try:
            response = urlopen(req)

        except HTTPError as e:
            # print('The server couldn\'t fulfill the request.')
            # print('Error code: ', e.code)
            continue
        break

        # try:
        #     # response = urlopen(req)
        #     while True:
        #         response = urlopen(req)
        #         if (not (response.getcode() == 500)):
        #             break
        #         else:
        #             # Hope it won't 500 a little later
        #             time.sleep(1)
        # except HTTPError as e:
        #     print('The server couldn\'t fulfill the request.')
        #     print('Error code: ', e.code)
            
        # except URLError as e:
        #     print('We failed to reach a server.')
        #     print('Reason: ', e.reason)

    data = json.loads(response.read().decode())

    return data



url_ridings="https://electionsapi.cp.org/api/federal2019/Ridings"
ridings = get_json_data(url_ridings)
#print(ridings)

# riding_number
# english_name
# french_name
# total_votes
# turnout
# conservative_vote_share
# liberal_vote_share
# ndp_vote_share
# green_vote_share
# bloc_quebecois_vote_share
# peoples_party_vote_share

url_parties="https://electionsapi.cp.org/api/federal2019/Parties"
parties=get_json_data(url_parties)
vote_share=[]

for r in ridings:
    riding=str(r['RidingNumber'])
    url_r="https://electionsapi.cp.org/api/federal2019/Candidates_For_Riding?ridingnumber="+riding
    
    
    
    candidates_for_riding=get_json_data(url_r)
    
    #Prepopulating party vote counts with 0
    for party in parties:
        r[party['ShortName_En']]=0

    for candidate in candidates_for_riding:
        party=candidate['PartyShortName_En']
        votes=candidate['Votes']
        r[party]=votes
    print(r)
    vote_share.append(r)
    # conservative_vote_share=r[']
    # liberal_vote_share
    # ndp_vote_share
    # green_vote_share
    # bloc_quebecois_vote_share
    # peoples_party_vote_share
print(vote_share)



