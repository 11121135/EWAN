import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 【期末格式要求二】：st.header("你的命名：視覺化議題")
# ==============================================================================
st.header("⚾ 世紀傳奇大盤點：美國職棒歷史明星賽巨量數據之多維度動態視覺化分析")

# ==============================================================================
# 【期末格式要求三】：st.subheader("114-2 運動大數據與視覺化分析專題研究/姓名OOO")
# ==============================================================================
st.subheader("114-2 運動大數據與視覺化分析專題研究/姓名:詹育晴")

# 預設讀取的棒球數據檔案名稱
FILE_NAME = "AllstarFull.csv"

# ==============================================================================
# 【優化項目】：全域圖表動態過濾器 放置於左邊側邊欄（Sidebar）
# ==============================================================================
st.sidebar.header("🎛️ 全域圖表動態過濾器")

# 自動檢查並讀取檔案以初始化滑桿範圍
if os.path.exists(FILE_NAME):
    df_init = pd.read_csv(FILE_NAME)
    min_year, max_year = int(df_init['yearID'].min()), int(df_init['yearID'].max())
else:
    min_year, max_year = 1933, 2015

year_range = st.sidebar.slider("📅 調整歷史年份區間：", min_year, max_year, (min_year, max_year))
top_n = st.sidebar.slider("🔢 排行榜顯示數量：", 5, 25, 12)

st.sidebar.divider()

# ==============================================================================
# 【期末格式要求六】：側邊欄之「資料保護與隱私適度說明」
# ==============================================================================
with st.sidebar.expander("🔒 個人隱私與資料保護說明", expanded=True):
    st.write("根據中華民國《個人資料保護法》及學術倫理規範：")
    st.caption("1. 本專題所引用之數據皆為官方公開之歷史賽事客觀統計，完全不包含任何球員之私密敏感個資（如身分證字號、聯絡電話、醫療紀錄等）。")
    st.caption("2. 程式部署於雲端沙盒，所有互動查詢均屬即時運算，絕不留存或外洩使用者的瀏覽行為。")

# 主畫面自動檢查並讀取檔案
if not os.path.exists(FILE_NAME):
    st.error(f"❌ 系統找不到檔案：`{FILE_NAME}`。請確認該檔案已放置在與程式碼相同的資料夾。")
else:
    df = pd.read_csv(FILE_NAME)
    
    # ─── 球員純中文姓名對照表（全面移除英文） ───
    player_name_map = {
        'aaronto01': '漢克·阿倫', 'musiast01': '斯坦·穆休',
        'mayswi01': '威利·梅斯', 'mantlmi01': '米奇·曼托',
        'bropebr01': '布魯克斯·羅賓森', 'aparili01': '路易斯·阿帕里西奧',
        'yastrca01': '卡爾·雅澤姆斯基', 'carewro01': '羅德·卡魯',
        'rosepe01': '彼得·羅斯', 'benchjo01': '強尼·班奇',
        'schmimi01': '麥克·舒密特', 'ripkeca01': '小卡爾·瑞普肯',
        'gwynnto01': '湯尼·關恩', 'rodrial01': '羅德里奎茲',
        'ruthba01': '貝比·魯斯', 'gehrilo01': '盧·賈里格',
        'williye01': '泰德·威廉斯', 'jeterde01': '德瑞克·基特',
        'ortizda01': '大衛·歐提茲', 'pujolal01': '阿爾伯特·普荷斯',
        'mayerwi01': '威利·梅斯', 'mayerwi02': '威利·梅斯'
    }
    
    # ─── 球隊純中文名稱對照表（全面移除英文） ───
    team_map = {
        'NYA': '紐約洋基', 'SLN': '聖路易紅雀', 'CHN': '芝加哥小熊',
        'BOS': '波士頓紅襪', 'LAN': '洛杉磯道奇', 'CIN': '辛辛那提紅人',
        'DET': '底特律老虎', 'SFN': '舊金山巨人', 'PIT': '匹茲堡海盜',
        'CHA': '芝加哥白襪', 'CLE': '克里夫蘭守護者', 'PHI': '費城費城人',
        'BAL': '巴爾的摩金鶯', 'MIN': '明尼蘇達雙城', 'HOU': '休士頓太空人',
        'NYN': '紐約大都會', 'OAK': '奧克蘭運動家', 'ATL': '亞特蘭大勇士',
        'SFG': '舊金山巨人', 'SDN': '聖地牙哥教士', 'WAS': '華盛頓國民'
    }
    
    # 資料結構與純繁體中文化轉換
    df['聯盟'] = df['lgID'].map({'AL': '美國聯盟', 'NL': '國家聯盟'}).fillna('未知聯盟')
    df['球隊'] = df['teamID'].map(team_map).fillna(df['teamID'])
    df['年份'] = df['yearID']
    df['球員姓名'] = df['playerID'].map(player_name_map).fillna('未知球員')

    # 依據左側過濾器條件篩選數據
    filtered_df = df[(df['年份'] >= year_range[0]) & (df['年份'] <= year_range[1])]
    
    # 頂部核心大數據摘要 (KPI卡片)
    st.write("### 📊 當前篩選區間之數據規模總覽")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚾ 歷史總入選人次", f"{len(filtered_df):,} 人次")
    col2.metric("⭐ 傳奇明星球員總數", f"{filtered_df['球員姓名'].nunique():,} 位")
    col3.metric("🏢 曾參與球隊總數", f"{filtered_df['球隊'].nunique():,} 支")
    
    st.divider()
    
    # 主畫面分頁標籤設計
    tab1, tab2, tab3 = st.tabs([
        "🏆 傳奇球星人氣王排行", 
        "🏢 球隊歷史貢獻度排行", 
        "📈 參賽規模歷史演變趨勢"
    ])
    
    # ===== Tab 1: 球員純中文姓名排行 (繽紛撞色、粗體黑色大字) =====
    with tab1:
        st.write(f"#### 🏆 指定年份區間內入選明星賽次數最高的前 {top_n} 名傳奇巨星")
        player_counts = filtered_df[filtered_df['球員姓名'] != '未知球員']['球員姓名'].value_counts().reset_index(name='入選次數').head(top_n)
        
        # 配色：使用高飽和度 Dark24 強烈撞色，完全中文化標籤
        fig_player = px.bar(
            player_counts, x="入選次數", y="球員姓名", orientation='h', color="球員姓名", 
            color_discrete_sequence=px.colors.qualitative.Dark24, text="入選次數",
            labels={"入選次數": "入選次數（次）", "球員姓名": "傳奇球員姓名"}
        )
        fig_player.update_traces(textposition='inside', textfont=dict(size=14, color='black', family="Arial Black"))
        fig_player.update_layout(yaxis={'categoryorder':'total ascending'}, height=500, showlegend=False)
        st.plotly_chart(fig_player, use_container_width=True)
        
    # ===== Tab 2: 球隊歷史貢獻度 (噴射彩虹強烈漸層) =====
    with tab2:
        st.write(f"#### 🏢 貢獻最多明星賽球員的球隊排行 (前 {top_n} 名)")
        team_counts = filtered_df['球隊'].value_counts().reset_index(name='總入選人次').head(top_n)
        
        # 配色：使用對比度極高的 Jet 霓虹彩虹漸層，完全中文化標籤
        fig_team = px.bar(
            team_counts, x="球隊", y="總入選人次", color="總入選人次", color_continuous_scale="Jet", text="總入選人次",
            labels={"球隊": "球隊名稱", "總入選人次": "歷史入選總人次（人次）"}
        )
        fig_team.update_traces(textposition='outside', textfont=dict(size=13, color='black', family="Arial Black"))
        fig_team.update_layout(height=450)
        st.plotly_chart(fig_team, use_container_width=True)
        
    # ===== Tab 3: 歷年參賽人數趨勢 (粗線亮點) =====
    with tab3:
        st.write("#### 📈 歷年明星賽入選總人數之時代演變趨勢")
        yearly_counts = filtered_df.groupby('年份').size().reset_index(name='入選人數')
        
        # 配色：高飽和度螢光紅粗線 + 亮藍色圓點，完全中文化標籤
        fig_line = px.line(
            yearly_counts, x="年份", y="入選人數", line_shape="spline", markers=True,
            labels={"年份": "舉辦年份（年）", "入選人數": "當屆入選總人數（人）"}
        )
        fig_line.update_traces(line=dict(color="#FF0000", width=4), marker=dict(color="#0000FF", size=8))
        fig_line.update_layout(height=450)
        st.plotly_chart(fig_line, use_container_width=True)
