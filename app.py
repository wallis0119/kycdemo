import streamlit as st
import time

# 頁面設定
st.set_page_config(page_title="投信客審 AI 助理 Demo", layout="wide", page_icon="🛡️")

# 自定義 CSS 讓介面更專業
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; }
    .stStatus { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 投信客審 AI 自動化助理 (Demo Concept)")
st.caption("數位業務專案提案：利用 LLM 代理提升 KYC/CDD 審查效率與精準度")

# --- 第一區：輸入與上傳 ---
with st.sidebar:
    st.header("👤 1. 客戶基準資料")
    subject_name = st.text_input("客戶姓名", "王小明")
    birth_year = st.number_input("出生年份 (民國)", value=70)
    residence = st.selectbox("居住地區", ["台北市", "新北市", "台中市", "高雄市", "其他"])
    job_type = st.text_input("職業背景", "金融從業人員")
    
    st.divider()
    st.header("📂 2. 資料上傳")
    tdcc_file = st.file_uploader("上傳 TDCC 查詢檔", type=["pdf", "png", "jpg"])
    news_files = st.file_uploader("上傳預查之網路新聞 (可多選)", type=["pdf"], accept_multiple_files=True)

# --- 第二區：自動搜尋與比對 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🌐 3. 自動化聯網查核")
    search_keywords = st.multiselect("搜尋引擎關鍵字組合：", ["詐欺", "洗錢", "掏空", "判決書", "裁罰"], default=["詐欺", "洗錢"])
    
    if st.button("🚀 執行自動查核與去識別化"):
        with st.status("正在執行作業...", expanded=True) as status:
            st.write("🔍 正在檢索 Google News 與 司法院裁判書系統...")
            time.sleep(1.5)
            st.write(f"🛡️ 去識別化處理中：已將『{subject_name}』替換為標籤 `{{{{SUBJECT_NAME}}}}`...")
            time.sleep(1)
            st.write("🤖 AI 代理進行特徵比對中 (年齡、職業、地域)...")
            time.sleep(1)
            status.update(label="查核完成！", state="complete", expanded=False)
        
        st.success("✅ 掃描完畢：共發現 3 則相關報導，AI 已自動排除 2 則雜訊。")

    # 模擬搜尋結果卡片
    st.markdown("---")
    st.write("**AI 預選結果：**")
    
    # 卡片 1
    with st.container(border=True):
        st.write("📰 **新聞：{{SUBJECT_NAME}} 涉嫌違反銀行法...**")
        st.caption("來源：中時電子報 | 日期：2023-11-20")
        st.error("🔴 警示：特徵高度吻合 (年齡約 45 歲、居住地一致)")
        st.checkbox("採納此項並納入報告", value=True, key="c1")

    # 卡片 2
    with st.container(border=True):
        st.write("📰 **公告：{{SUBJECT_NAME}} 獲頒傑出青年獎**")
        st.caption("來源：市府新聞稿 | 日期：2024-01-15")
        st.success("🟢 排除：正面訊息且非本人 (年齡不符)")
        st.checkbox("採納 AI 排除建議", value=True, key="c2")

# --- 第三區：交互確認與產出 ---
with col2:
    st.subheader("⚖️ 4. 交互式確認與初稿生成")
    
    st.info("💡 **AI 綜合摘要：** 經比對，網路搜尋結果中有一則 2023 年之銀行法案件，其人物特徵與客戶本人高度重合。其餘搜尋結果皆為同名同姓之雜訊，已自動過濾。")
    
    final_decision = st.select_slider(
        "人工覆核判定：",
        options=["正常", "注意", "高風險"],
        value="注意"
    )
    
    manual_notes = st.text_area("審查人員補充意見：", placeholder="例如：經電話訪談，該案件為誤用帳戶，目前已獲不起訴處分...")

    if st.button("📄 生成客審報告初稿", type="primary"):
        st.divider()
        report_text = f"""
【客審報告初稿 - 僅供參考】
客戶姓名：{subject_name}
審查日期：2026-02-27
查核項目：網路負面新聞、TDCC、司法院系統

一、自動化查核結果：
- AI 掃描總數：5 份資料
- 自動排除：4 份 (原因：年齡不符、無關情事)
- 警示項目：1 份 (涉及 2023 年銀行法報導)

二、人工覆核意見：
- 判定等級：{final_decision}
- 專業註記：{manual_notes if manual_notes else "無"}

三、合規建議：
[自動生成] 建議列入「{final_decision}」等級監控，並要求客戶提供相關判決書證明文件。
        """
        st.code(report_text, language="markdown")
        st.download_button("📥 下載 Word 格式 (.txt)", data=report_text, file_name="KYC_Draft.txt")
