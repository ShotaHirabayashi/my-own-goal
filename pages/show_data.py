import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection
import matplotlib.pyplot as plt
import pandas as pd

# Connect to Supabase
conn = st.connection("supabase", type=SupabaseConnection)


st.markdown("<div style='padding-top: 2rem;'><h1 style='font-size:24px; margin-bottom: 0;'>📊 グラフ表示</h1></div>",
            unsafe_allow_html=True)


# Retrieve last 7 days of data
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)
response = conn.table("calories").select("date, consumed_calories").gte("date", str(seven_days_ago)).lte("date",
                                                                                                         str(today)).order(
    "date").execute()

if response.data:
    data = pd.DataFrame(response.data)
    data["date"] = pd.to_datetime(data["date"])
    data.set_index("date", inplace=True)

    st.write("直近7日間のカロリー消費グラフ:")

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["consumed_calories"], marker="o", linestyle="-", color="b")
    plt.title("calories (for 7 days)")
    plt.xlabel("日付")
    plt.ylabel("calories (kcal)")
    plt.grid(True)
    st.pyplot(plt)
else:
    st.warning("直近7日間のデータが見つかりませんでした。")