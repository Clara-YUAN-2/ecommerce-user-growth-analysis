-- SQLite 建表脚本：用户行为样本表
-- 数据来源：data/processed/UserBehavior_sample_cleaned.csv

DROP TABLE IF EXISTS user_behavior_sample;

CREATE TABLE user_behavior_sample (
    user_id INTEGER,
    item_id INTEGER,
    category_id INTEGER,
    behavior_type TEXT,
    timestamp INTEGER,
    datetime TEXT,
    date TEXT,
    hour INTEGER,
    weekday INTEGER
);

CREATE INDEX IF NOT EXISTS idx_user_behavior_sample_user_id
ON user_behavior_sample (user_id);

CREATE INDEX IF NOT EXISTS idx_user_behavior_sample_behavior_type
ON user_behavior_sample (behavior_type);

CREATE INDEX IF NOT EXISTS idx_user_behavior_sample_date
ON user_behavior_sample (date);

CREATE INDEX IF NOT EXISTS idx_user_behavior_sample_hour
ON user_behavior_sample (hour);
