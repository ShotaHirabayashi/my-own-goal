import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection

conn = st.connection("supabase", type=SupabaseConnection)


st.markdown("<div style='padding-top: 2rem;'><h1 style='font-size:24px; margin-bottom: 0;'>🍎 商品登録</h1></div>",
            unsafe_allow_html=True)

product_name = st.text_input("商品名を入力してください")
product_calories = st.number_input("商品カロリーを入力してください (kcal):", min_value=0, step=10)

if st.button("商品を登録"):
    if product_name and isinstance(product_calories, (int, float)):
        conn.table("products").insert({
            "name": product_name,
            "calories": product_calories
        }).execute()
        st.success(f"商品 '{product_name}' を登録しました！")
    else:
        st.error("商品名とカロリーを正しく入力してください。")