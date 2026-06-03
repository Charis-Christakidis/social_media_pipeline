-- ============================================================
-- ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ: Gaza War Twitter Dataset
-- Βάση: gazawar_analytics
-- ============================================================


-- ============================================================
-- 1. ΕΠΑΛΗΘΕΥΣΗ ΔΕΔΟΜΕΝΩΝ
-- Έλεγχος ότι οι πίνακες φορτώθηκαν σωστά
-- ============================================================
SELECT COUNT(*) AS total_users FROM dim_users;
SELECT COUNT(*) AS total_tweets FROM fact_engagement;


-- ============================================================
-- 2. ΑΞΙΟΠΙΣΤΙΑ ΧΡΗΣΤΩΝ (Reliability Score)
-- Εντοπισμός των πιο και λιγότερο αξιόπιστων χρηστών
-- βάσει του reliability score που υπολογίστηκε στο pipeline
-- ============================================================

-- Top 10 πιο αξιόπιστοι χρήστες
SELECT username, ROUND(reliability_score, 2) AS reliability_score
FROM dim_users
ORDER BY reliability_score DESC
LIMIT 10;

-- Top 10 λιγότερο αξιόπιστοι χρήστες (πιθανά bots)
SELECT username, ROUND(reliability_score, 2) AS reliability_score
FROM dim_users
ORDER BY reliability_score ASC
LIMIT 10;


-- ============================================================
-- 3. ENGAGEMENT ΑΝΑ LABEL
-- Σύγκριση του μέσου engagement (likes, retweets, comments)
-- ανά κατηγορία περιεχομένου (label)
-- 0: Ειρηνιστικά, 1: Pro-Palestine, 2: Γεωπολιτικά
-- 3: Pro-Peace, 4: Media/Links, 5: Pro-Israel
-- ============================================================
SELECT 
    label,
    COUNT(*) AS total_tweets,
    ROUND(AVG(likes_count), 2) AS avg_likes,
    ROUND(AVG(retweets_count), 2) AS avg_retweets,
    ROUND(AVG(comments_count), 2) AS avg_comments,
    ROUND(AVG(engagement_ratio), 2) AS avg_engagement_ratio
FROM fact_engagement
GROUP BY label
ORDER BY avg_likes DESC;


-- ============================================================
-- 4. ΕΝΤΟΠΙΣΜΟΣ ΠΙΘΑΝΩΝ BOT ACCOUNTS
-- Χρήστες με reliability score = 1, μηδενικό engagement
-- και bot-like usernames (αριθμοί, τυχαίοι χαρακτήρες)
-- ============================================================
SELECT 
    d.username,
    d.reliability_score,
    COUNT(f.engagement_id) AS total_tweets,
    SUM(f.likes_count) AS total_likes,
    SUM(f.retweets_count) AS total_retweets,
    SUM(f.comments_count) AS total_comments
FROM dim_users d
JOIN fact_engagement f ON d.user_id = f.user_id
WHERE d.reliability_score = 1
GROUP BY d.username, d.reliability_score
ORDER BY total_tweets DESC;


-- ============================================================
-- 5. TOP TWEETS ΒΑΣΕΙ LIKES
-- Τα πιο δημοφιλή tweets συνδυαστικά με τον χρήστη
-- και το reliability score για αξιολόγηση της πηγής
-- ============================================================
SELECT 
    f.post_content_raw,
    f.likes_count,
    f.retweets_count,
    f.comments_count,
    f.label,
    d.username,
    d.reliability_score
FROM fact_engagement f
JOIN dim_users d ON f.user_id = d.user_id
ORDER BY f.likes_count DESC
LIMIT 10;
