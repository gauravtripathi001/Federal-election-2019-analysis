DROP TABLE IF EXISTS vote_share; 

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
  ); 

DROP TABLE IF EXISTS candidates; 

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
  ); 