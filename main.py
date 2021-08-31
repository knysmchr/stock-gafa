import pandas as pd
import altair as alt
import yfinance as yf
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

@st.cache
def get_data(days,tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲の指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix':'NFLX',
        'amazon': 'AMZN',
        'amgen': 'AMGN',
        'american express': 'AXP',
        'boeing': 'BA',
        'caterpillar': 'CAT',
        'cisco systems': 'CSCO',
        'salesforce.com': 'CRM',
        'chevron': 'CVX',
        'dow': 'DOW',
        'walt disney': 'DIS',
        'goldman sachs': 'GS',
        'home depo': 'HD',
        'honeywell international': 'HON',
        'ibm': 'IBM',
        'intel': 'INTC',
        'johnson and johnson': 'JNJ',
        'jp morgan chase': 'JPM',
        'coca cola': 'KO',
        'mcdonalds': 'MCD',
        '3m company': 'MMM',
        'merck & co': 'MRK',
        'nike': 'NKE',
        'P&G': 'PG',
        'travelers': 'TRV',
        'united health': 'UNH',
        'visa': 'V',
        'verizzon commu': 'VZ',
        'walgreens boots': 'WBA',
        'walmart': 'WMT',
        'raytheon tech': 'RTX',
        'costco': 'COST',
        'oracle': 'ORCL',
        'starbucks': 'SBUX',
        'at&t': 'T',
        'lockheed martin': 'LMT',
        'micron tech': 'MU',
        'deere': 'DE',
        'zoetis': 'ZTS',
        'altria group': 'MO',
        'duke energy': 'DUK',
        'southern co': 'SO',
        'bank of america': 'BAC',
        'city group': 'C',
        'wells fargo': 'WFC',
        'adobe': 'ADBE',
        'qualcomm': 'QCOM',
        'alibaba': 'BABA',
        'pfizer': 'PFE',
        'abbvie': 'ABBV',
        'exxonmobil': 'XOM',
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        default=['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write('### 株価 (USD)', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x='Date:T', 
                y=alt.Y('Stock Prices(USD):Q', stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        'おっと！何かエラーが起きているようです。'
    )