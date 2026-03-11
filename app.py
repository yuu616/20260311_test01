import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="台積電股價分析", layout="wide")
st.title("📈 台積電 (2330.TW) 股價長條圖")

# 側邊欄設定
st.sidebar.header("日期篩選")
start = st.sidebar.date_input("開始日期", datetime.now() - timedelta(days=60))
end = st.sidebar.date_input("結束日期", datetime.now())

if start < end:
    # 抓取資料
    with st.spinner('正在從 Yahoo Finance 抓取資料...'):
        ticker = "2330.TW"
        df = yf.download(ticker, start=start, end=end)

    if not df.empty:
        # 重要：處理 yfinance 的新版 MultiIndex 欄位問題
        # 強制將欄位扁平化，確保 Streamlit 抓得到 'Close'
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # 建立繪圖專用的 DataFrame
        chart_df = pd.DataFrame(df['Close'])
        
        st.subheader(f"收盤價長條圖 ({start} 至 {end})")
        
        # 使用 Streamlit 原生長條圖，並指定 y 軸為 Close
        st.bar_chart(chart_df)

        # 顯示數值清單供檢查
        with st.expander("查看原始數據表"):
            st.write(df.sort_index(ascending=False))
    else:
        st.error("❌ 找不到數據。請檢查網路連線，或確認該日期區間是否有開盤。")
else:
    st.warning("⚠️ 開始日期必須早於結束日期。")
