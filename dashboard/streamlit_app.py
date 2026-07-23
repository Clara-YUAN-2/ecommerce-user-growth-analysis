"""淘宝电商用户行为分析与增长优化 Dashboard。"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# 页面基础配置
st.set_page_config(
    page_title="淘宝电商用户行为分析与增长优化 Dashboard",
    page_icon="Dashboard",
    layout="wide",
)

# 使用相对路径定位 processed 数据，便于部署到 GitHub
BASE_DIR = Path(__file__).resolve().parents[1]
processed_path = BASE_DIR / "data" / "processed"

# 统一配色：参考图中的奶油白、雾面卡片、暖橙强调和深色文字
COLOR_BG = "#efe7dc"
COLOR_PANEL = "rgba(255, 255, 255, 0.66)"
COLOR_TEXT = "#211f1d"
COLOR_MUTED = "#7d756d"
COLOR_ORANGE = "#ff8a2a"
COLOR_ORANGE_LIGHT = "#ffd5ad"
COLOR_DARK = "#1f1f1f"
COLOR_GRID = "rgba(94, 80, 66, 0.14)"
PLOT_COLORS = ["#ff8a2a", "#222222", "#b9aaa0", "#f2bc7d", "#81756c"]


def apply_custom_style() -> None:
    """注入页面样式，让 Dashboard 呈现柔和玻璃拟态风格。"""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: "Noto Sans SC", "Microsoft YaHei", Arial, sans-serif;
        }}

        .stApp {{
            color: {COLOR_TEXT};
            background:
                radial-gradient(circle at 18% 12%, rgba(255, 255, 255, 0.72), transparent 28%),
                radial-gradient(circle at 78% 20%, rgba(255, 138, 42, 0.22), transparent 22%),
                radial-gradient(circle at 72% 82%, rgba(255, 255, 255, 0.55), transparent 26%),
                linear-gradient(135deg, #f5eee6 0%, {COLOR_BG} 48%, #ded2c7 100%);
        }}

        .block-container {{
            max-width: 1280px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }}

        [data-testid="stSidebar"] {{
            background: rgba(245, 238, 230, 0.78);
            border-right: 1px solid rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(22px);
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {{
            color: {COLOR_TEXT};
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label {{
            min-height: 42px;
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 999px;
            color: {COLOR_TEXT};
            background: rgba(255, 255, 255, 0.34);
            border: 1px solid rgba(255, 255, 255, 0.54);
        }}

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: rgba(255, 255, 255, 0.72);
        }}

        h1, h2, h3 {{
            color: {COLOR_TEXT};
            letter-spacing: 0;
        }}

        h1 {{
            font-size: 2.55rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }}

        h2 {{
            margin-top: 1.35rem;
            font-weight: 750;
        }}

        h3 {{
            font-weight: 700;
        }}

        p, .stCaption, [data-testid="stMarkdownContainer"] {{
            color: {COLOR_MUTED};
        }}

        .hero-panel {{
            position: relative;
            padding: 34px 38px 32px;
            margin-bottom: 28px;
            overflow: hidden;
            border-radius: 30px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.74), rgba(255, 255, 255, 0.42));
            border: 1px solid rgba(255, 255, 255, 0.78);
            box-shadow: 0 28px 70px rgba(79, 60, 44, 0.18);
            backdrop-filter: blur(24px);
        }}

        .hero-panel::after {{
            content: "";
            position: absolute;
            right: 9%;
            top: 24%;
            width: 180px;
            height: 180px;
            border-radius: 999px;
            background: linear-gradient(180deg, #ffb164 0%, #ff7f1f 100%);
            box-shadow: 0 32px 60px rgba(255, 122, 24, 0.32);
            z-index: 0;
        }}

        .hero-panel::before {{
            content: "";
            position: absolute;
            right: 17%;
            top: 8%;
            width: 260px;
            height: 260px;
            border-radius: 999px;
            border: 2px solid rgba(255, 255, 255, 0.76);
            background: rgba(255, 255, 255, 0.16);
            z-index: 0;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 780px;
        }}

        .hero-kicker {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 13px;
            margin-bottom: 18px;
            border-radius: 999px;
            color: {COLOR_TEXT};
            background: rgba(255, 255, 255, 0.58);
            border: 1px solid rgba(255, 255, 255, 0.72);
            font-size: 0.86rem;
            font-weight: 600;
        }}

        .hero-title {{
            margin: 0;
            color: {COLOR_TEXT};
            font-size: 2.75rem;
            line-height: 1.14;
            font-weight: 800;
        }}

        .hero-subtitle {{
            max-width: 760px;
            margin-top: 14px;
            color: #615850;
            font-size: 1.03rem;
            line-height: 1.8;
        }}

        .section-card {{
            padding: 24px;
            margin: 18px 0 22px;
            border-radius: 24px;
            background: {COLOR_PANEL};
            border: 1px solid rgba(255, 255, 255, 0.78);
            box-shadow: 0 18px 48px rgba(75, 58, 43, 0.12);
            backdrop-filter: blur(20px);
        }}

        .note-card {{
            padding: 18px 20px;
            margin: 18px 0;
            border-radius: 20px;
            color: #4c4037;
            background: rgba(255, 213, 173, 0.52);
            border: 1px solid rgba(255, 255, 255, 0.74);
        }}

        [data-testid="stMetric"] {{
            min-height: 126px;
            padding: 18px 18px 16px;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.64);
            border: 1px solid rgba(255, 255, 255, 0.78);
            box-shadow: 0 14px 34px rgba(77, 58, 42, 0.10);
        }}

        [data-testid="stMetricLabel"] p {{
            color: {COLOR_MUTED};
            font-size: 0.92rem;
            font-weight: 500;
        }}

        [data-testid="stMetricValue"] {{
            color: {COLOR_TEXT};
            font-size: 1.78rem;
            font-weight: 800;
        }}

        [data-testid="stDataFrame"] {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.72);
            box-shadow: 0 12px 30px rgba(77, 58, 42, 0.09);
        }}

        [data-testid="stPlotlyChart"] {{
            padding: 12px;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.78);
            box-shadow: 0 16px 40px rgba(77, 58, 42, 0.10);
        }}

        .stAlert {{
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.68);
            background: rgba(255, 255, 255, 0.56);
        }}

        hr {{
            border-color: rgba(78, 63, 50, 0.14);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_csv(file_name: str) -> pd.DataFrame | None:
    """读取 processed 目录下的 CSV；文件不存在时返回 None。"""
    file_path = processed_path / file_name
    if not file_path.exists():
        return None
    return pd.read_csv(file_path)


def show_missing_module(file_name: str) -> None:
    """展示缺失数据提示，避免页面中断。"""
    st.warning(f"{file_name} 该模块数据暂未生成")


def format_number(value) -> str:
    """将大数字格式化为千分位。"""
    if pd.isna(value):
        return "-"
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    if numeric_value.is_integer():
        return f"{int(numeric_value):,}"
    return f"{numeric_value:,.2f}"


def format_percent(value) -> str:
    """将比例字段格式化为百分比。"""
    if pd.isna(value):
        return "-"
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    if numeric_value <= 1:
        numeric_value *= 100
    return f"{numeric_value:.2f}%"


def metric_value(metrics_df: pd.DataFrame, metric_name: str):
    """从核心指标表中按中文指标名取数。"""
    matched = metrics_df.loc[metrics_df["指标"] == metric_name, "数值"]
    if matched.empty:
        return None
    return matched.iloc[0]


def metric_card(label: str, value, is_percent: bool = False) -> None:
    """统一展示指标卡片。"""
    display_value = format_percent(value) if is_percent else format_number(value)
    st.metric(label=label, value=display_value)


def style_plot(fig):
    """统一设置图表的视觉样式。"""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.42)",
        font=dict(family="Microsoft YaHei, Noto Sans SC, Arial", color=COLOR_TEXT, size=13),
        title=dict(font=dict(size=18, color=COLOR_TEXT), x=0),
        colorway=PLOT_COLORS,
        height=420,
        margin=dict(l=24, r=24, t=58, b=24),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=COLOR_GRID)
    fig.update_yaxes(gridcolor=COLOR_GRID, zeroline=False)
    return fig


def simple_bar(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    """生成简洁柱状图。"""
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        text_auto=True,
        title=title,
        color_discrete_sequence=PLOT_COLORS,
    )
    fig = style_plot(fig)
    fig.update_traces(
        marker_line_width=0,
        marker_color=COLOR_ORANGE if color is None else None,
        textposition="outside",
        cliponaxis=False,
    )
    return fig


def simple_line(df: pd.DataFrame, x: str, y, title: str):
    """生成简洁趋势图。"""
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title,
        color_discrete_sequence=PLOT_COLORS,
    )
    fig = style_plot(fig)
    fig.update_traces(line_width=3, marker_size=7)
    return fig


def note(text: str) -> None:
    """展示业务解释卡片。"""
    st.markdown(f'<div class="note-card">{text}</div>', unsafe_allow_html=True)


def show_page_header() -> None:
    """展示全局标题和副标题。"""
    st.markdown(
        """
        <div class="hero-panel">
            <div class="hero-content">
                <div class="hero-kicker">淘宝电商分析项目 · Growth Dashboard</div>
                <h1 class="hero-title">淘宝电商用户行为分析与增长优化 Dashboard</h1>
                <div class="hero-subtitle">
                    基于淘宝用户行为数据，分析平台流量规模、转化漏斗、用户留存、
                    用户分群、商品类目机会，并提出增长优化策略。
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_project_overview() -> None:
    """项目概览模块。"""
    st.header("项目概览")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.write(
        "本项目基于淘宝用户行为数据，模拟电商平台数据分析师视角，围绕浏览、"
        "收藏、加购、购买等行为，识别用户转化瓶颈、用户分层价值和商品类目"
        "增长机会，为平台提升购买转化率和用户运营效率提供数据支持。"
    )

    st.subheader("数据字段说明")
    field_df = pd.DataFrame(
        [
            {"字段": "user_id", "说明": "用户 ID"},
            {"字段": "item_id", "说明": "商品 ID"},
            {"字段": "category_id", "说明": "商品类目 ID"},
            {"字段": "behavior_type", "说明": "行为类型，包含 pv、fav、cart、buy"},
            {"字段": "timestamp", "说明": "行为时间戳"},
        ]
    )
    st.dataframe(field_df, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def show_core_metrics() -> None:
    """核心指标模块。"""
    st.header("核心指标")
    metrics_df = load_csv("full_core_metrics.csv")
    if metrics_df is None:
        show_missing_module("full_core_metrics.csv")
        return

    metric_items = [
        ("总行为数", "总行为数", False),
        ("独立用户数", "独立用户数", False),
        ("独立商品数", "独立商品数", False),
        ("独立类目数", "独立类目数", False),
        ("pv 浏览量", "pv 浏览量", False),
        ("fav 收藏数", "fav 收藏数", False),
        ("cart 加购数", "cart 加购数", False),
        ("buy 购买数", "buy 购买数", False),
        ("购买用户数", "购买用户数", False),
        ("用户购买转化率", "用户购买转化率", True),
    ]

    for row_start in range(0, len(metric_items), 5):
        cols = st.columns(5)
        for col, (label, metric_name, is_percent) in zip(cols, metric_items[row_start : row_start + 5]):
            with col:
                metric_card(label, metric_value(metrics_df, metric_name), is_percent)

    st.subheader("核心指标明细")
    st.dataframe(metrics_df, width="stretch", hide_index=True)


def show_funnel() -> None:
    """转化漏斗模块。"""
    st.header("转化漏斗")
    behavior_df = load_csv("behavior_funnel_metrics.csv")
    user_df = load_csv("user_funnel_metrics.csv")

    if behavior_df is None:
        show_missing_module("behavior_funnel_metrics.csv")
    else:
        st.subheader("行为层面漏斗表")
        st.dataframe(behavior_df, width="stretch", hide_index=True)
        st.plotly_chart(
            simple_bar(behavior_df, "behavior_name", "behavior_count", "行为数量柱状图"),
            width="stretch",
        )

    if user_df is None:
        show_missing_module("user_funnel_metrics.csv")
    else:
        st.subheader("用户层面漏斗表")
        st.dataframe(user_df, width="stretch", hide_index=True)
        st.plotly_chart(
            simple_bar(user_df, "behavior_name", "user_count", "用户数量柱状图"),
            width="stretch",
        )

    note(
        "浏览行为占绝大多数，购买行为明显少于浏览行为。平台后续应重点关注"
        "浏览到加购、加购到购买之间的转化流失。"
    )


def show_activity_retention() -> None:
    """活跃与留存模块。"""
    st.header("活跃与留存")
    daily_df = load_csv("daily_activity.csv")
    hourly_df = load_csv("hourly_activity.csv")
    weekday_df = load_csv("weekday_activity.csv")
    retention_df = load_csv("user_retention.csv")

    if daily_df is None:
        show_missing_module("daily_activity.csv")
    else:
        st.plotly_chart(
            simple_line(daily_df, "date", "total_behavior_count", "每日行为趋势图"),
            width="stretch",
        )

    col_left, col_right = st.columns(2)
    with col_left:
        if hourly_df is None:
            show_missing_module("hourly_activity.csv")
        else:
            st.plotly_chart(
                simple_line(hourly_df, "hour", "total_behavior_count", "每小时活跃趋势图"),
                width="stretch",
            )
    with col_right:
        if weekday_df is None:
            show_missing_module("weekday_activity.csv")
        else:
            x_col = "weekday_name" if "weekday_name" in weekday_df.columns else "weekday"
            st.plotly_chart(
                simple_bar(weekday_df, x_col, "total_behavior_count", "每周活跃趋势图"),
                width="stretch",
            )

    if retention_df is None:
        show_missing_module("user_retention.csv")
    else:
        retention_cols = [
            "day_1_retention_rate",
            "day_3_retention_rate",
            "day_7_retention_rate",
        ]
        st.plotly_chart(
            simple_line(retention_df, "cohort_date", retention_cols, "次日、3 日、7 日留存率趋势图"),
            width="stretch",
        )

    note("用于识别用户活跃高峰，为推荐触达、优惠券发放、活动推送时间提供依据。")


def show_user_segments() -> None:
    """用户分群模块。"""
    st.header("用户分群")
    segment_df = load_csv("user_segment_summary.csv")
    if segment_df is None:
        show_missing_module("user_segment_summary.csv")
        return

    st.subheader("用户分群汇总表")
    st.dataframe(segment_df, width="stretch", hide_index=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(
            simple_bar(segment_df, "用户群体", "用户数", "各用户群体数量柱状图"),
            width="stretch",
        )
    with col_right:
        st.plotly_chart(
            simple_bar(segment_df, "用户群体", "平均购买数", "各用户群体平均购买次数柱状图"),
            width="stretch",
        )

    st.plotly_chart(
        simple_bar(segment_df, "用户群体", "平均活跃天数", "各用户群体平均活跃天数柱状图"),
        width="stretch",
    )
    note(
        "不同用户群体具有不同运营价值。高价值用户适合复购和会员运营，高潜力用户"
        "适合优惠券刺激，低活跃用户适合召回。"
    )


def show_category_opportunity() -> None:
    """类目机会模块。"""
    st.header("类目机会")
    category_df = load_csv("category_opportunity.csv")
    if category_df is None:
        show_missing_module("category_opportunity.csv")
        return

    if "opportunity_type" in category_df.columns:
        opportunity_count = (
            category_df.groupby("opportunity_type", as_index=False)
            .agg(category_count=("category_id", "nunique"))
            .sort_values("category_count", ascending=False)
        )
        st.plotly_chart(
            simple_bar(
                opportunity_count,
                "opportunity_type",
                "category_count",
                "不同机会类型类目数量柱状图",
            ),
            width="stretch",
        )

    opportunity_map = [
        ("高浏览低购买类目 Top 20", "高浏览低购买类目", "pv_count"),
        ("高加购低购买类目 Top 20", "高加购低购买类目", "cart_count"),
        ("高收藏低购买类目 Top 20", "高收藏低购买类目", "fav_count"),
        ("高转化优势类目 Top 20", "高转化优势类目", "user_buy_rate"),
    ]

    for title, opportunity_type, sort_col in opportunity_map:
        st.subheader(title)
        if "opportunity_type" not in category_df.columns:
            st.warning("category_opportunity.csv 缺少 opportunity_type 字段，该模块数据暂未生成")
            continue
        filtered_df = category_df[category_df["opportunity_type"] == opportunity_type].copy()
        if filtered_df.empty:
            st.warning(f"{opportunity_type} 该模块数据暂未生成")
            continue
        display_cols = [
            "category_id",
            "opportunity_type",
            "pv_count",
            "fav_count",
            "cart_count",
            "buy_count",
            "user_buy_rate",
        ]
        existing_cols = [col for col in display_cols if col in filtered_df.columns]
        st.dataframe(
            filtered_df.sort_values(sort_col, ascending=False).head(20)[existing_cols],
            width="stretch",
            hide_index=True,
        )

    note(
        "类目机会分析用于识别平台中流量高但购买弱、加购强但临门转化不足、"
        "收藏多但决策慢的商品类目，从而制定差异化运营策略。"
    )


def show_growth_strategy() -> None:
    """增长策略模块。"""
    st.header("增长策略")
    strategy_df = load_csv("category_strategy_recommendations.csv")
    if strategy_df is None:
        show_missing_module("category_strategy_recommendations.csv")
    else:
        strategy_cols = [
            "category_id",
            "opportunity_type",
            "business_problem",
            "strategy_recommendation",
        ]
        existing_cols = [col for col in strategy_cols if col in strategy_df.columns]
        st.subheader("类目增长策略建议表")
        st.dataframe(strategy_df[existing_cols], width="stretch", hide_index=True)

    st.subheader("策略总结")
    st.markdown(
        """
1. **高浏览低购买类目**：优化详情页、价格展示、评价内容和推荐精准度。
2. **高加购低购买类目**：推送限时优惠券、降价提醒、库存提醒和满减活动。
3. **高收藏低购买类目**：推送买家秀、评价内容、相似商品推荐和收藏降价提醒。
4. **高转化优势类目**：面向高价值用户做复购推荐、搭配推荐和会员专属活动。
        """
    )


apply_custom_style()
show_page_header()

# 侧边栏导航
st.sidebar.title("导航")
selected_module = st.sidebar.radio(
    "请选择模块",
    [
        "项目概览",
        "核心指标",
        "转化漏斗",
        "活跃与留存",
        "用户分群",
        "类目机会",
        "增长策略",
    ],
)

st.sidebar.divider()
st.sidebar.caption(f"数据目录：{processed_path}")

if selected_module == "项目概览":
    show_project_overview()
elif selected_module == "核心指标":
    show_core_metrics()
elif selected_module == "转化漏斗":
    show_funnel()
elif selected_module == "活跃与留存":
    show_activity_retention()
elif selected_module == "用户分群":
    show_user_segments()
elif selected_module == "类目机会":
    show_category_opportunity()
elif selected_module == "增长策略":
    show_growth_strategy()
