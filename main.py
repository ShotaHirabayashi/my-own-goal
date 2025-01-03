import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection

# Define the application
st.set_page_config(
    page_title="カロリー消費トラッカー",
    page_icon="🍎",
    layout="centered"
)

conn = st.connection("supabase", type=SupabaseConnection)

st.markdown("<div style='padding-top: 2rem;'><h1 style='font-size:24px; margin-bottom: 0;'>🍎 カロリー消費トラッカー</h1></div>", unsafe_allow_html=True)

# Select date
date = st.date_input("日付を選んでください", datetime.date.today())

# Retrieve data from Supabase
response = conn.table("calories").select("*").eq("date", str(date)).execute()

if response.data:
    daily_calories = response.data[0]['allowed_calories']
    consumed_calories = response.data[0]['consumed_calories']
    remaining_calories = daily_calories - consumed_calories

    st.metric(label="許容カロリー", value=f"{daily_calories} kcal")
    remaining_calories_display = st.empty()
    remaining_calories_display.metric(
        label="残りの消費可能カロリー",
        value=f"{remaining_calories} kcal",
        delta=-consumed_calories
    )

    if remaining_calories < 0:
        st.error("カロリーを超過しています！")

    # Add calorie input field
    st.subheader("カロリー入力")
    new_calories = st.number_input("消費したカロリーを入力してください (kcal):", min_value=0, step=10)
    if st.button("カロリーを記録"):
        if isinstance(new_calories, (int, float)):
            updated_consumed = consumed_calories + new_calories
            updated_remaining = daily_calories - updated_consumed
            conn.table("calories").update({
                "consumed_calories": updated_consumed
            }).eq("date", str(date)).execute()
            st.success(f"{new_calories} kcal を記録しました！")
            remaining_calories_display.write(f"残りの消費可能カロリー: {updated_remaining} kcal")
        else:
            st.error("有効な数値を入力してください。")
else:
    # Insert a new row with default values
    conn.table("calories").insert({
        "allowed_calories": 2400,
        "consumed_calories": 2400,
        "date": str(date)
    }).execute()
    st.success("新しい日付のデータが作成されました。リロードしてください。")