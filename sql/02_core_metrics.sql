-- 基于 user_behavior_sample 的核心指标查询

-- 1. 总行为数
SELECT COUNT(*) AS total_behaviors
FROM user_behavior_sample;

-- 2. 独立用户数 UV
SELECT COUNT(DISTINCT user_id) AS uv
FROM user_behavior_sample;

-- 3. 独立商品数
SELECT COUNT(DISTINCT item_id) AS unique_items
FROM user_behavior_sample;

-- 4. 独立类目数
SELECT COUNT(DISTINCT category_id) AS unique_categories
FROM user_behavior_sample;

-- 5-8. 浏览量、收藏数、加购数、购买数
SELECT
    SUM(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS pv_count,
    SUM(CASE WHEN behavior_type = 'fav' THEN 1 ELSE 0 END) AS fav_count,
    SUM(CASE WHEN behavior_type = 'cart' THEN 1 ELSE 0 END) AS cart_count,
    SUM(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS buy_count
FROM user_behavior_sample;

-- 9. 购买用户数
SELECT COUNT(DISTINCT user_id) AS buyer_count
FROM user_behavior_sample
WHERE behavior_type = 'buy';

-- 10. 用户购买转化率
SELECT
    buyer_count,
    uv,
    ROUND(1.0 * buyer_count / NULLIF(uv, 0), 4) AS user_purchase_conversion_rate
FROM (
    SELECT
        COUNT(DISTINCT CASE WHEN behavior_type = 'buy' THEN user_id END) AS buyer_count,
        COUNT(DISTINCT user_id) AS uv
    FROM user_behavior_sample
);

-- 11. 各行为类型占比
SELECT
    behavior_type,
    COUNT(*) AS behavior_count,
    ROUND(1.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS behavior_ratio
FROM user_behavior_sample
GROUP BY behavior_type
ORDER BY behavior_count DESC;

-- 12. 每日 PV、UV、购买数
SELECT
    date,
    SUM(CASE WHEN behavior_type = 'pv' THEN 1 ELSE 0 END) AS pv_count,
    COUNT(DISTINCT user_id) AS uv,
    SUM(CASE WHEN behavior_type = 'buy' THEN 1 ELSE 0 END) AS buy_count
FROM user_behavior_sample
GROUP BY date
ORDER BY date;

-- 13. 每小时活跃行为数
SELECT
    hour,
    COUNT(*) AS behavior_count,
    COUNT(DISTINCT user_id) AS active_users
FROM user_behavior_sample
GROUP BY hour
ORDER BY hour;
