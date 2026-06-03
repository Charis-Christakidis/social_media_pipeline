import os
import re
import pandas as pd


def clean_text(text):
    """Καθαρισμός κειμένου από links και ειδικούς χαρακτήρες."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = " ".join(text.split())
    return text


def calculate_reliability_v2(row):
    """Υπολογισμός Reliability Score (1-5) με βάση username και engagement."""
    score = 5
    username = str(row["user"])
    digit_ratio = sum(c.isdigit() for c in username) / (len(username) + 1)
    if digit_ratio > 0.4:
        score -= 2
    elif digit_ratio > 0.2:
        score -= 1
    total_engagement = row["likes"] + row["retweets"] + row["comments"]
    if total_engagement == 0:
        score -= 2
    if row["retweets"] > 0 and row["quotes"] / (row["retweets"] + 1) > 10:
        score -= 1
    return max(1, min(5, score))


def load_and_combine_raw_data(raw_dir):
    print("Loading and combining raw data...")
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Ο φάκελος δεν βρέθηκε: {raw_dir}")
    file_names = [f for f in os.listdir(raw_dir) if f.endswith(".csv")]
    if not file_names:
        raise FileNotFoundError(f"Δεν βρέθηκαν αρχεία .csv στον φάκελο: {raw_dir}")
    dataframes = []
    for file_name in sorted(file_names):
        file_path = os.path.join(raw_dir, file_name)
        print(f"Reading {file_name}...")
        df_part = pd.read_csv(file_path, low_memory=False)
        dataframes.append(df_part)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.drop_duplicates()
    print(f"Successfully combined data. Total rows: {len(combined_df)}")
    return combined_df


def transform_data(df):
    print("Starting data transformation...")
    df.columns = df.columns.str.lower().str.strip()
    metric_cols = ["likes", "quotes", "retweets", "comments"]
    for col in metric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0
    print("Cleaning post content...")
    df["cleaned_text"] = df["text"].apply(clean_text)
    df["hashtags"] = df["text"].apply(lambda x: " ".join(re.findall(r"#\w+", str(x))))
    df["mentions"] = df["text"].apply(lambda x: " ".join(re.findall(r"@\w+", str(x))))
    df["engagement_ratio"] = df.apply(
        lambda row: round(row["retweets"] / (row["comments"] + 1), 2), axis=1
    )
    print("Calculating user reliability scores...")
    df["reliability_score"] = df.apply(calculate_reliability_v2, axis=1)
    print("Score distribution:", df["reliability_score"].value_counts().to_dict())
    df["user_id"] = pd.factorize(df["user"])[0] + 1
    dim_users = df.groupby("user_id").agg(
        username=("user", "first"),
        reliability_score=("reliability_score", "mean")
    ).reset_index()
    df["engagement_id"] = range(1, len(df) + 1)
    fact_engagement = df[[
        "engagement_id", "user_id", "link", "text", "cleaned_text",
        "likes", "quotes", "retweets", "comments", "label",
        "hashtags", "mentions", "engagement_ratio"
    ]].copy()
    fact_engagement.columns = [
        "engagement_id", "user_id", "post_link", "post_content_raw", "post_content_clean",
        "likes_count", "quotes_count", "retweets_count", "comments_count", "label",
        "hashtags", "mentions", "engagement_ratio"
    ]
    print(f"Created dim_users with {len(dim_users)} unique users.")
    print(f"Created fact_engagement with {len(fact_engagement)} records.")
    return dim_users, fact_engagement


def save_processed_data(dim_users, fact_engagement, output_dir):
    print(f"Saving processed files to directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    dim_users.to_csv(os.path.join(output_dir, "dim_users.csv"), index=False)
    fact_engagement.to_csv(os.path.join(output_dir, "fact_engagement.csv"), index=False)
    print("ETL pipeline process completed successfully.")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == "data":
        BASE_DATA_DIR = current_dir
    else:
        BASE_DATA_DIR = os.path.join(current_dir, "data")
    RAW_DATA_DIR = os.path.join(BASE_DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(BASE_DATA_DIR, "processed")
    try:
        combined_raw_df = load_and_combine_raw_data(RAW_DATA_DIR)
        users_df, engagement_df = transform_data(combined_raw_df)
        save_processed_data(users_df, engagement_df, PROCESSED_DIR)
    except Exception as e:
        print(f"Pipeline execution failed: {e}")
