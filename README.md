# Gaza War Twitter Analytics Pipeline

Ανάλυση tweets σχετικά με τη σύγκρουση Ισραήλ-Παλαιστίνης/Γάζα με χρήση Python και PostgreSQL.

## Dataset

Πηγή: [Kaggle - Tweets Israeli-Palestinian Conflict/Gaza War](https://www.kaggle.com/datasets/laidkahloul/tweets-sraeli-palestinian-conflict-gazawar)

Αποτελείται από 3 CSV αρχεία με συνολικά ~20.241 μοναδικά tweets από 4.910 χρήστες.

## Δομή Project

social_media_pipeline/
├── pipeline.py       # ETL pipeline
├── analysis.py       # Ανάλυση και γραφήματα
├── .env.example      # Παράδειγμα credentials
└── data/
├── raw/          # Αρχικά CSV
├── processed/    # Επεξεργασμένα CSV
└── outputs/      # Γραφήματα

## Απαιτήσεις

pandas
matplotlib
sqlalchemy
psycopg2-binary
python-dotenv

## Reliability Score

Κάθε χρήστης παίρνει score 1-5 βάσει:
- Username digit ratio (πιθανό bot)
- Μηδενικό engagement
- Ασυνήθιστο quote/retweet ratio

## Συμπεράσματα

### Κατανομή Tweets
Τα Pro-Palestine tweets αποτελούν τη μεγαλύτερη κατηγορία (27.8%), ακολουθούμενα από Media/Links (23%) και Ειρηνιστικά (19%).

### Engagement
Τα Pro-Palestine tweets έχουν το υψηλότερο μέσο engagement (10.46 likes, 5.38 retweets) ενώ τα Pro-Israel έχουν σημαντικά χαμηλότερο (2.64 likes, 0.79 retweets).

### Αξιοπιστία Χρηστών
- 46.3% Αξιόπιστοι (score 4-5)
- 53.5% Μέτρια Αξιοπιστία (score 2-3)
- 0.2% Πιθανά Bots (score 1)

### Bot Detection
Εντοπίστηκαν 10 πιθανά bot accounts με αριθμητικά usernames και μηδενικό engagement.

## Τεχνολογίες

- Python, pandas, matplotlib, sqlalchemy
- PostgreSQL, DBeaver
- JupyterLab
