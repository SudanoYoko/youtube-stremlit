import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write(
    """
    # GAFA株価
    こちらは株価可視化ツールです。以下のオプションから表示日数を設定してください。
    """
)

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFAの株価
""")

@st.cache
def get_data(days, tickers):

    df = pd.DataFrame()

    for company in tickers.keys():
        # 辞書型より、指定した会社名のTickerを取得
        tkr = yf.Ticker(tickers[company])
        # appleの5日間の株価を取得
        hist = tkr.history(period=f'{days}d')
        # 日付の表示形式を、日 月 年 とする
        hist.index = hist.index.strftime('%d %B %Y')
        # 終値のみを取得
        hist = hist[['Close']]
        # カラム名を「close」から「apple」に変更
        hist.columns = [company]
        # 表の向きを横方向に変更
        hist = hist.T
        # インデックス名を「Name」に変更
        hist.index.name = 'Name'
        # 上記で作成したデータをdfに追加する
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。', 
        0.0, 3500.0, (0.0, 3500.0)
    )

        # TickerNameを辞書型でまとめる
    tickers = {
        'apple': 'AAPL',
        'facebook': 'FB',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '会社名を選択してください',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('少なくとも１社は選んでください。')
    else:
        # 取得した株価より、指定した会社名のもののみ取得
        data = df.loc[companies]
        st.write('### 株価（USD）', data.sort_index())
        # 表の向きを変更
        data = data.T.reset_index()
        # Dateを基準に表を再度崩す
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラーが発生しました"
    )