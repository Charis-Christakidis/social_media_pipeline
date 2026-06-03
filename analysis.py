import os
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Φόρτωση του password από το .env αρχείο
load_dotenv()
password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/gazawar_analytics")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_plot(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, bbox_inches="tight", dpi=150)
    print(f"Αποθηκεύτηκε: {path}")

label_names = {0: "Ειρηνιστικά", 1: "Pro-Palestine", 2: "Γεωπολιτικά", 3: "Pro-Peace", 4: "Media/Links", 5: "Pro-Israel"}

# 1. Πίτα: Κατανομή tweets ανά κατηγορία
query1 = "SELECT label, COUNT(*) AS total_tweets, ROUND(AVG(likes_count), 2) AS avg_likes, ROUND(AVG(retweets_count), 2) AS avg_retweets, ROUND(AVG(comments_count), 2) AS avg_comments FROM fact_engagement GROUP BY label ORDER BY avg_likes DESC"
df1 = pd.read_sql(query1, engine)
df1["label_name"] = df1["label"].astype(int).map(label_names)

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df1["total_tweets"], labels=df1["label_name"], autopct="%1.1f%%", startangle=140,
    colors=["#4C72B0","#55A868","#C44E52","#8172B2","#CCB974","#64B5CD"])
ax.set_title("Κατανομή Tweets ανά Κατηγορία", fontsize=13, fontweight="bold")
plt.tight_layout()
save_plot("1_tweets_per_label_pie.png")
plt.show()

# 2. Bars: Engagement ανά κατηγορία
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Engagement ανά Κατηγορία Περιεχομένου", fontsize=14, fontweight="bold")
for ax, col, color, title in zip(axes,
    ["avg_likes", "avg_retweets", "avg_comments"],
    ["#4C72B0", "#55A868", "#C44E52"],
    ["Μέσος Αριθμός Likes", "Μέσος Αριθμός Retweets", "Μέσος Αριθμός Comments"]):
    ax.barh(df1["label_name"], df1[col], color=color)
    ax.set_title(title)
    ax.set_xlabel("Μέσος Αριθμός")
    ax.invert_yaxis()
plt.tight_layout()
save_plot("2_engagement_per_label.png")
plt.show()

# 3. Πίτα: Κατηγοριοποίηση χρηστών βάσει αξιοπιστίας
query3 = "SELECT CASE WHEN reliability_score = 1 THEN 'Πιθανά Bots' WHEN reliability_score <= 3 THEN 'Μέτρια Αξιοπιστία' ELSE 'Αξιόπιστοι' END AS category, COUNT(*) AS total FROM dim_users GROUP BY category"
df3 = pd.read_sql(query3, engine)
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(df3["total"], labels=df3["category"], autopct="%1.1f%%", startangle=140,
    colors=["#C44E52", "#CCB974", "#55A868"])
ax.set_title("Κατηγοριοποίηση Χρηστών βάσει Αξιοπιστίας", fontsize=13, fontweight="bold")
plt.tight_layout()
save_plot("3_user_categories.png")
plt.show()

# 4. Top tweets βάσει likes
query4 = "SELECT DISTINCT ON (f.likes_count) SUBSTRING(f.post_content_clean, 1, 80) AS tweet_preview, f.post_link, f.likes_count FROM fact_engagement f JOIN dim_users d ON f.user_id = d.user_id ORDER BY f.likes_count DESC LIMIT 10"
df4 = pd.read_sql(query4, engine)
df4["label"] = df4.apply(lambda row: "\n".join(textwrap.wrap(str(row["tweet_preview"]), width=40)) + "\n>> " + str(row["post_link"]), axis=1)

fig, ax = plt.subplots(figsize=(12, 10))
ax.barh(df4["label"], df4["likes_count"], color="#4C72B0")
ax.set_title("Top Tweets βάσει Likes", fontsize=13, fontweight="bold")
ax.set_xlabel("Αριθμός Likes")
ax.invert_yaxis()
plt.tight_layout()
save_plot("4_top_tweets.png")
plt.show()

engine.dispose()
print("Ανάλυση ολοκληρώθηκε! Τα γραφήματα αποθηκεύτηκαν στον φάκελο outputs/")
