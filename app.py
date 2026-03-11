import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 設定網頁標題
st.title("台積電 (2330.TW) 股價走勢圖")

# 側邊欄：輸入日期區間
st.sidebar.header("查詢條件")
start_date = st.sidebar.date_input("開始日期", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("結束日期", datetime.now())

if start_date < end_date:
    # 下載台積電數據
    ticker = "2330.TW"
    df = yf.download(ticker, start=start_date, end=end_date)

    if not df.empty:
        # 顯示原始數據摘要
        st.subheader(f"{ticker} 歷史數據 (收盤價)")
        
        # Streamlit 顯示長條圖 (以收盤價 Close 為主)
        # 注意：yfinance 回傳的 columns 可能是 MultiIndex，需視情況處理
        chart_data = df['Close']
        st.bar_chart(chart_data)
        
        # 顯示詳細資料表
        st.write(df.tail())
    else:
        st.warning("在此日期區間內找不到數據，請嘗試更換日期。")
else:
    st.error("錯誤：開始日期必須早於結束日期。")
