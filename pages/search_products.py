import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection

conn = st.connection("supabase", type=SupabaseConnection)

st.markdown("<div style='padding-top: 2rem;'><h1 style='font-size:24px; margin-bottom: 0;'>🍎 商品検索</h1></div>",
            unsafe_allow_html=True)

search_query = st.text_input("商品名を検索してください")
if search_query:
    results = conn.table("products").select("*").ilike("name", f"%{search_query}%").execute()
    if results.data:
        st.write("検索結果:")
        for item in results.data:
            st.write(f"- {item['name']}: {item['calories']} kcal")
    else:
        st.warning("該当する商品が見つかりませんでした。")
