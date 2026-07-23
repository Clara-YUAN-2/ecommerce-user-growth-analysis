-- 07_sql_business_metrics_validation.sql
-- SQL 业务查询与指标验证

-- 1. 核心指标查询
SELECT *
FROM full_core_metrics;

-- 2. 漏斗指标查询
SELECT *
FROM behavior_funnel_metrics;

SELECT *
FROM user_funnel_metrics;

-- 3. 用户分群查询
SELECT *
FROM user_segment_summary;

SELECT
    user_segment,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM user_segmentation), 4) AS user_ratio
FROM user_segmentation
GROUP BY user_segment
ORDER BY user_count DESC;

SELECT
    user_segment,
    ROUND(AVG(total_behavior_count), 2) AS avg_total_behavior,
    ROUND(AVG(pv_count), 2) AS avg_pv,
    ROUND(AVG(fav_count), 2) AS avg_fav,
    ROUND(AVG(cart_count), 2) AS avg_cart,
    ROUND(AVG(buy_count), 2) AS avg_buy,
    ROUND(AVG(active_days), 2) AS avg_active_days
FROM user_segmentation
GROUP BY user_segment
ORDER BY avg_buy DESC;

SELECT
    COUNT(*) AS cart_no_buy_user_count
FROM user_segmentation
WHERE cart_count > 0 AND buy_count = 0;

SELECT
    COUNT(*) AS fav_no_buy_user_count
FROM user_segmentation
WHERE fav_count > 0 AND buy_count = 0;

SELECT
    user_id,
    pv_count,
    fav_count,
    cart_count,
    buy_count,
    total_behavior_count,
    active_days
FROM user_segmentation
WHERE buy_count = 0
ORDER BY pv_count DESC
LIMIT 20;

-- 4. 活跃趋势查询
SELECT *
FROM daily_activity
ORDER BY date
LIMIT 20;

SELECT *
FROM hourly_activity
ORDER BY hour;

-- 5. 类目机会查询
SELECT
    opportunity_type,
    COUNT(DISTINCT category_id) AS category_count
FROM category_opportunity
GROUP BY opportunity_type
ORDER BY category_count DESC;

SELECT
    category_id,
    opportunity_type,
    cart_count,
    buy_count,
    cart_user_count,
    buy_user_count,
    cart_no_buy_user_gap,
    cart_no_buy_rate
FROM category_opportunity
WHERE opportunity_type = '高加购低购买类目'
ORDER BY cart_no_buy_user_gap DESC
LIMIT 20;

SELECT
    category_id,
    opportunity_type,
    pv_count,
    buy_count,
    pv_user_count,
    buy_user_count,
    pv_no_buy_user_gap,
    pv_no_buy_rate
FROM category_opportunity
WHERE opportunity_type = '高浏览低购买类目'
ORDER BY pv_no_buy_user_gap DESC
LIMIT 20;

-- 6. 策略建议查询
SELECT
    category_id,
    opportunity_type,
    business_problem,
    strategy_recommendation
FROM category_strategy_recommendations
LIMIT 20;
