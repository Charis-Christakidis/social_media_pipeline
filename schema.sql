-- ============================================================
-- SCHEMA: Gaza War Twitter Dataset
-- Δημιουργία πινάκων στη βάση gazawar_analytics
-- ============================================================

DROP TABLE IF EXISTS fact_engagement CASCADE;
DROP TABLE IF EXISTS dim_users CASCADE;

CREATE TABLE dim_users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    reliability_score NUMERIC(5,2)
);

CREATE TABLE fact_engagement (
    engagement_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES dim_users(user_id),
    post_link TEXT,
    post_content_raw TEXT,
    post_content_clean TEXT,
    likes_count INTEGER,
    quotes_count INTEGER,
    retweets_count INTEGER,
    comments_count INTEGER,
    label VARCHAR(50),
    hashtags TEXT,
    mentions TEXT,
    engagement_ratio NUMERIC(10,2)
);
