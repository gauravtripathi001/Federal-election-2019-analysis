from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import psycopg2
import json

def get_json_data(url):
    req = Request(url)

    while True:
        try:
            response = urlopen(req)

        except HTTPError as e:
            #Will retry
            continue
        break

    data = json.loads(response.read().decode())

    return data

def insert_into_table(postgres_insert_query,record_to_insert,table):
    try:
        connection = psycopg2.connect(
        database='postgres', user='gtripathi', password='QJdYWGAA6XqqU7bnF.PUr', host='hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com', port= '5432')
        cursor = connection.cursor()

        
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into table", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def create_table(create_table_query,table):
    try:
    
        connection = psycopg2.connect(database='postgres', user='gtripathi', password='QJdYWGAA6XqqU7bnF.PUr', host='hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com', port= '5432')

        cursor = connection.cursor()
        
        cursor.execute(create_table_query)
        connection.commit()
        print(table,"table created successfully in PostgreSQL ")

    except (Exception, psycopg2.Error) as error :
        print("Failed to insert record into table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()

def main():
    url_ridings="https://electionsapi.cp.org/api/federal2019/Ridings"
    ridings = get_json_data(url_ridings)

    url_parties="https://electionsapi.cp.org/api/federal2019/Parties"
    parties=get_json_data(url_parties)
    vote_share=[]


    create_table_query='''DROP TABLE IF EXISTS vote_share; 

    CREATE TABLE vote_share 
    ( 
        riding_number             INT NOT NULL, 
        english_name              TEXT, 
        french_name               TEXT, 
        total_votes               INT, 
        turnout                   REAL, 
        conservative_vote_share   REAL, 
        liberal_vote_share        REAL, 
        ndp_vote_share            REAL, 
        green_vote_share          REAL, 
        bloc_quebecois_vote_share REAL, 
        peoples_party_vote_share  REAL, 
        PRIMARY KEY (riding_number) 
    ); '''

    create_table(create_table_query,"vote_share")

    create_table_query='''DROP TABLE IF EXISTS candidates; 

    CREATE TABLE candidates 
    ( 
        riding_number            INT NOT NULL, 
        liberal_candidate        TEXT, 
        conservative_candidate   TEXT, 
        ndp_candidate            TEXT, 
        green_candidate          TEXT, 
        bloc_quebecois_candidate TEXT, 
        peoples_party_candidate  TEXT, 
        PRIMARY KEY (riding_number) 
    ); '''

    create_table(create_table_query,"candidates")
    count=0
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

            first_name=candidate['First']
            
            if(party=='LIB'):
                r['liberal_candidate']=first_name
            elif(party=='CON'):
                r['conservative_candidate']=first_name
            elif(party=='GRN'):
                r['green_candidate']=first_name
            elif(party=='NDP'):
                r['ndp_candidate']=first_name
            elif(party=='BQ'):
                r['bloc_quebecois_candidate']=first_name
            elif(party=='PPC'):
                r['peoples_party_candidate']=first_name
        
        postgres_insert_query = '''INSERT INTO vote_share(riding_number,english_name,french_name,total_votes,turnout,conservative_vote_share,liberal_vote_share,ndp_vote_share,green_vote_share,bloc_quebecois_vote_share,peoples_party_vote_share) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        riding_number=r['RidingNumber'];english_name=r['Name_En'];french_name=r['Name_Fr'];total_votes=r['TotalVotes'];turnout=(r['TotalVotes']/r['TotalVoters']);conservative_vote_share=r['CON']/total_votes;liberal_vote_share=r['LIB']/total_votes;ndp_vote_share=r['NDP']/total_votes;green_vote_share=r['GRN']/total_votes;bloc_quebecois_vote_share=r['BQ']/total_votes;peoples_party_vote_share=r['PPC']/total_votes
        record_to_insert = (riding_number,english_name,french_name,total_votes,turnout,conservative_vote_share,liberal_vote_share,ndp_vote_share,green_vote_share,bloc_quebecois_vote_share,peoples_party_vote_share)
        
        insert_into_table(postgres_insert_query,record_to_insert,"vote_share")
        
        postgres_insert_query = '''INSERT INTO candidates(riding_number,liberal_candidate,conservative_candidate,ndp_candidate,green_candidate,bloc_quebecois_candidate,peoples_party_candidate) VALUES(%s,%s,%s,%s,%s,%s,%s);'''
        liberal_candidate=r.get('liberal_candidate');conservative_candidate=r.get('conservative_candidate');ndp_candidate=r.get('ndp_candidate');green_candidate=r.get('green_candidate');bloc_quebecois_candidate=r.get('bloc_quebecois_candidate');peoples_party_candidate=r.get('peoples_party_candidate')
        record_to_insert=(riding_number,liberal_candidate,conservative_candidate,ndp_candidate,green_candidate,bloc_quebecois_candidate,peoples_party_candidate)
        insert_into_table(postgres_insert_query,record_to_insert,"candidates")
        
        count+=1
        print(count,"records inserted in vote_share and candidates tables")
    print("All records inserted succesfully")

main()