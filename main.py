import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.title('BioRadish')

st.sidebar.write('''
# 日経バイオ系企業株価
こちらは株価可視化ツールです。
以下のオプションから表示日数を指定できます。
''')

st.file_uploader("ファイルアップロード", type='csv')