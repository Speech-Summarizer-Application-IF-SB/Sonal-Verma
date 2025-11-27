import streamlit as st

if not st.user.is_logged_in:
    if st.button("Log in with Google"):
        st.login("google")
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.user.name}")