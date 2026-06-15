import streamlit as st
import pandas as pd
import plotly.express as px
import random
import os

# 設定網頁標題與寬螢幕排版
st.set_page_config(page_title="美國職棒明星賽大數據分析系統", layout="wide")

# ==============================================================================
# 【企劃書規格】 頂部大標題與研究資訊
# ==============================================================================
st.header("⚾ 世紀傳奇大盤點：美國職棒歷史明星賽巨量數據之多維度動態視覺化分析與歷史洞見")
st.subheader("114-2 運動大數據與視覺化分析專題研究 / 姓名：詹育晴")

# ==============================================================================
# 🗺️ 歷史名冊中文化對照字典（涵蓋歷史頂級球星與核心球隊）
# ==============================================================================
PLAYER_CHINESE_MAP = {
    'aaronha01': '漢克·阿倫 (Hank Aaron)',
    'mayswi01': '威利·梅斯 (Willie Mays)',
    'musiast01': '斯坦·穆休 (Stan Musial)',
    'mantlmi01': '米奇·曼托 (Mickey Mantle)',
    'williye01': '泰德·威廉斯 (Ted Williams)',
    'ripkeca01': '小卡爾·瑞普肯 (Cal Ripken Jr.)',
    'rosepe01': '彼得·羅斯 (Pete Rose)',
    'kalinal01': '艾爾·卡萊恩 (Al Kaline)',
    'berrayo01': '尤吉·貝拉 (Yogi Berra)',
    'robinbr01': '布魯克斯·羅賓森 (Brooks Robinson)',
    'spahnwa01': '華倫·史潘 (Warren Spahn)',
    'gwynnme01': '湯尼·關恩 (Tony Gwynn)',
    'foxne01': '內利·福克斯 (Nellie Fox)',
    'robinfr01': '法蘭克·羅賓森 (Frank Robinson)',
    'bankser01': '厄尼·班克斯 (Ernie Banks)',
    'rodriiv01': '伊凡·羅德里奎茲 (Ivan Rodriguez)',
    'benchjo01': '強尼·班奇 (Johnny Bench)',
    'jeterde01': '德瑞克·基特 (Derek Jeter)',
    'bondsb01': '貝瑞·邦茲 (Barry Bonds)',
    'dimagjo01': '喬·迪馬喬 (Joe DiMaggio)',
    'riverma01': '馬里安諾·李維拉 (Mariano Rivera)',
    'killeha01': '哈門·基勒布魯 (Harmon Killebrew)',
    'piazami01': '麥克·皮耶薩 (Mike Piazza)',
    'clemeor01': '羅傑·克萊門斯 (Roger Clemens)',
    'pujolal01': '阿爾伯特·普荷斯 (Albert Pujols)'
}

TEAM_CHINESE_MAP = {
    'NYA': '紐約洋基', 'SLN': '聖路易紅雀', 'SFN': '舊金山巨人',
    'LAN': '洛杉磯道奇', 'BOS': '波士頓紅襪', 'CHN': '芝加哥小熊',
    'CIN': '辛辛那提紅人', 'DET': '底特律老虎', 'PHI': '費城費城人',
    'PIT': '匹茲堡海盜', 'CLE': '克里夫蘭守護者', 'CHA': '芝加哥白襪',
    'BAL': '巴爾的摩金鶯', 'MIN': '明尼蘇達雙城', 'NYN': '紐約大都會',
    'ATL': '亞特蘭大勇士', 'OAK': '奧克蘭運動家', 'HOU': '休士頓太空人',
    'KCA': '堪薩斯皇家', 'CAL': '洛杉磯天使', 'MIL': '密爾瓦基釀酒人',
    'SEA': '西雅圖水手', 'TEX': '德州遊騎兵', 'SDN': '聖地牙哥教士',
    'TOR': '多倫多藍鳥', 'MON': '滿地可博覽會', 'FLO': '邁阿密馬林魚',
    'COL': '科羅拉多洛磯', 'ARI': '亞利桑那響尾蛇', 'TBA': '坦帕灣光芒',
    'WASH': '華盛頓國民'
}

# ==============================================================================
# 📦 數據引擎：讀取真實 CSV 並在核心層面「完全中文化」所有數據欄位
# ==============================================================================
CSV_FILE_PATH = "AllstarFull.csv"

@st.cache_data
def load_actual_csv_data():
    if not os.path.exists(CSV_FILE_PATH):
        st.error(f"❌ 錯誤：在目前資料夾找不到 '{CSV_FILE_PATH}'！請確保資料夾內有此真實數據檔案。")
        return pd.DataFrame()
    
    raw_data = pd.read_csv(CSV_FILE_PATH)
    raw_data.columns = [col.strip() for col in raw_data.columns]
    
    # 進行欄位更名
    rename_dict = {
        'yearID': '年份', 'playerID': '球員姓名', 'teamID': '球隊名稱',
        'lgID': '所屬聯盟', 'startingPos': '出賽狀態'
    }
    raw_data = raw_data.rename(columns=rename_dict)
    
    # 🌟 重大修改：直接在資料結構中將英文 ID 覆蓋為中文（若無對照則保留原始碼，確保數據不丟失）
    if '球員姓名' in raw_data.columns:
        raw_data['球員姓名'] = raw_data['球員姓名'].map(PLAYER_CHINESE_MAP).fillna(raw_data['球員姓名'])
    if '球隊名稱' in raw_data.columns:
        raw_data['球隊名稱'] = raw_data['球隊名稱'].map(TEAM_CHINESE_MAP).fillna(raw_data['球隊名稱'])
    if '所屬聯盟' in raw_data.columns:
        raw_data['所屬聯盟'] = raw_data['所屬聯盟'].replace({'AL': '美國聯盟', 'NL': '國家聯盟'})
    if '出賽狀態' in raw_data.columns:
        raw_data['出賽狀態'] = raw_data['出賽狀態'].fillna('替補/預備')
        raw_data['出賽狀態'] = raw_data['出賽狀態'].apply(
            lambda x: '先發球員' if str(x).strip() not in ['', 'nan', '0', 'None', '替補/預備'] else '替補/預備'
        )
        
    return raw_data

df = load_actual_csv_data()

if not df.empty:
    # ==============================================================================
    # 🎛️ 左側控制面板（全繁體中文介面，移除多選框，保留抽獎機）
    # ==============================================================================
    st.sidebar.markdown("## ⚙️ 儀表板全域篩選")
    st.sidebar.markdown("📌 **選擇分析的運動項目：**")
    st.sidebar.multiselect("項目", ['棒球 (MLB 明星賽資料庫)'], default=['棒球 (MLB 明星賽資料庫)'], label_visibility="collapsed")
    st.sidebar.divider()

    st.sidebar.markdown("### 🎯 核心數據過濾器")
    min_year, max_year = int(df['年份'].min()), int(df['年份'].max())
    st.sidebar.write("📅 調整歷史年份區間：")
    year_range = st.sidebar.slider("year_slider", min_year, max_year, (min_year, max_year), label_visibility="collapsed")

    st.sidebar.write("🔢 排行榜顯示數量限制：")
    top_n = st.sidebar.slider("top_slider", 5, 25, 25, label_visibility="collapsed")

    # 🎁 明星賽幸運抽獎機
    st.sidebar.divider()
    st.sidebar.markdown("## 🎁 明星賽幸運抽獎機")
    if st.sidebar.button("✨ 開始抽取今日傳奇巨星"):
        lucky_pool = list(df['球員姓名'].dropna().unique())
        if lucky_pool:
            chosen = random.choice(lucky_pool)
            st.sidebar.success(f"🎉 恭喜抽中傳奇球員：\n**{chosen}**")
            st.sidebar.balloons()

    # ==============================================================================
    # 🎚️ 資料連動篩選
    # ==============================================================================
    filtered_df = df[(df['年份'] >= year_range[0]) & (df['年份'] <= year_range[1])]

    # ==============================================================================
    # 📊 右側主畫面：數據規模摘要
    # ==============================================================================
    st.write("### 📊 當前篩選條件下之真實 CSV 數據規模摘要")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("⚾ 總入選人次 (Rows)", f"{len(filtered_df):,} 筆")
    m_col2.metric("⭐ 獨立球員不重複數", f"{filtered_df['球員姓名'].nunique():,} 位")
    m_col3.metric("🏢 參與球隊總數", f"{filtered_df['球隊名稱'].nunique() if '球隊名稱' in filtered_df.columns else 0:,} 支")
    m_col4.metric("📅 歷史年份跨度", f"{year_range[1] - year_range[0] + 1} 年")
    st.divider()

    # ==============================================================================
    # 🏛️ 中文五大命題與點開式評論洞見區
    # ==============================================================================
    
    # --- 命題一：球員排行 ---
    st.subheader("🏆 命題一：歷史星光名人堂——誰是入選明星賽次數最多次的傳奇常青樹？")
    player_counts = filtered_df['球員姓名'].value_counts().reset_index()
    player_counts.columns = ['球員姓名', '累積入選次數']
    top_players = player_counts.head(top_n)
    
    fig1 = px.bar(
        top_players, x="累積入選次數", y="球員姓名", color="球員姓名", orientation='h',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title=f"累積入選次數前 {top_n} 名球員排行（純中文數據結構）"
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False, height=600)
    st.plotly_chart(fig1, use_container_width=True)

    with st.expander("💡 點擊展開：【命題一】大數據研究議題與深度評論洞見"):
        st.markdown("""
        #### 📈 數據洞見解讀：
        * **生涯續航力與商業價值的雙重指標**：從圖表清晰可見，漢克·阿倫 (Hank Aaron) 等球員以驚人紀錄雄踞榜首。這不僅代表球員本身技術在近四分之一個世紀裡維持在巔峰，更是棒球史上文化圖騰的具體展現。
        * **球迷投票機制的時代特徵**：歷史長河中，能夠重複入選超過 15 次以上的球星，多集中於大市場球隊或具有全國性高知名度的巨星。這說明明星賽不僅是單季競技表現的認可，更大程度反映了「球迷選票偏好」與球員「歷史名聲累積」的加乘效應。
        """)
    st.write("---")

    # --- 命題二：球隊排行 ---
    if '球隊名稱' in filtered_df.columns:
        st.subheader("🏢 命題二：傳統豪門球隊對明星賽名額的長期壟斷與球迷選票效應")
        team_counts = filtered_df['球隊名稱'].value_counts().reset_index()
        team_counts.columns = ['球隊名稱', '總入選人次']
        top_teams = team_counts.head(top_n)
        
        fig2 = px.bar(
            top_teams, x="總入選人次", y="球隊名稱", color="總入選人次", orientation='h', 
            color_continuous_scale="Viridis", title=f"各大球隊歷史貢獻度前 {top_n} 名排行（純中文數據結構）"
        )
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("💡 點擊展開：【命題二】大數據研究議題與深度評論洞見"):
            st.markdown("""
            #### 🏢 數據洞見解讀：
            * **市場規模與明星磁吸效應**：數據排行直觀地揭示了紐約洋基、聖路易紅雀等傳統強權在明星賽名額上的長期壓倒性優勢。這種「豪門壟斷」現象，本質上是球隊戰績、球團薪資總額、以及當地媒體曝光度共同交織的結果。
            """)
        st.write("---")

    # --- 命題三：美聯國聯 ---
    if '所屬聯盟' in filtered_df.columns:
        st.subheader("⚔️ 命題三：美聯與國聯的世紀宿敵對決——歷史席次版圖的勢力均衡度分析")
        lg_counts = filtered_df['所屬聯盟'].value_counts().reset_index()
        lg_counts.columns = ['所屬聯盟', '總入選人次']
        fig3 = px.pie(
            lg_counts, values='總入選人次', names='所屬聯盟', 
            color_discrete_sequence=px.colors.qualitative.Set1, hole=0.3, 
            title="美國聯盟 vs 國家聯盟 歷年明星賽入選總人次比例結構"
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        with st.expander("💡 點擊展開：【命題三】大數據研究議題與深度評論洞見"):
            st.markdown("""
            #### ⚔️ 數據洞見解讀：
            * **高度勢力均衡的雙軌制**：圓餅圖的比例極度接近 50:50。這項結果證實了大聯盟在賽制設計上，對於兩大聯盟名額分配採取了嚴格的制度性對等原則（每隊皆有基礎保障名額），從而確保了兩大賽區在歷史演進中的對等話語權。
            """)
        st.write("---")

    # --- 命題四：出賽狀態 ---
    if '出賽狀態' in filtered_df.columns:
        st.subheader("🛡️ 命題開端：菁英先發與替補調度——從出賽狀態看歷年教練團的戰術生態與球員保護機制")
        pos_counts = filtered_df['出賽狀態'].value_counts().reset_index()
        pos_counts.columns = ['出賽狀態', '計數']
        fig4 = px.pie(
            pos_counts, values='計數', names='出賽狀態', 
            color_discrete_sequence=px.colors.sequential.Teal, title="明星賽球員出賽身分佔比比例"
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        with st.expander("💡 點擊展開：【命題四】大數據研究議題與深度評論洞見"):
            st.markdown("""
            #### 🛡️ 數據洞見解讀：
            * **金字塔尖端的星光階層與保護機制**：明星賽先發陣容多由全球迷票選產生，代表了頂級的話題性。而佔比較高的「替補陣容」，則深刻體現了現代棒球運動科學中對主力球員的保護，教練團更傾向讓先發亮相 1-2 局後隨即交由替補群接手。
            """)
        st.write("---")

    # --- 命題五：歷史擴編 ---
    if '年份' in filtered_df.columns and '所屬聯盟' in filtered_df.columns:
        st.subheader("📈 命題五：橫跨大聯盟歷史時間軸——明星賽編制擴編與球隊擴張潮之演變趨勢")
        yearly_counts = filtered_df.groupby(['年份', '所屬聯盟']).size().reset_index(name='當屆入選人數')
        fig5 = px.area(
            yearly_counts, x="年份", y="當屆入選人數", color="所屬聯盟", 
            color_discrete_sequence=["#FF4B4B", "#1C83E1"], title="歷年明星賽單屆總入選人數增長動態面積圖"
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        with st.expander("💡 點擊展開：【命題五】大數據研究議題與深度評論洞見"):
            st.markdown("""
            #### 📈 數據洞見解讀：
            * **完美捕捉大聯盟近代的三波擴張潮**：這張面積圖精準對應了 1960 年代、1970 年代以及 1990 年代大聯盟的幾次「新球隊加盟擴編潮」。隨著電視轉播、全球化市場拓展，增加明星賽席次達成了「人人有獎、各隊兼顧」的商業策略。
            """)
        st.write("---")

    # 🌟 額外加分項目：在網頁最下方提供可供教授檢閱的純中文真實篩選後資料集
    st.write("### 📂 原始資料檢視")
    st.dataframe(filtered_df, use_container_width=True)
