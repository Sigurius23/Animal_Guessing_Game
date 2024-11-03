import streamlit as st

st.set_page_config(page_title="Game Statistics", page_icon="📊")
st.title("Game Statistics 📊")

if 'attempts' in st.session_state:
    st.markdown(f"### Current Game")
    st.markdown(f"Number of attempts: {len(st.session_state.attempts)}")
    
    if st.session_state.attempts:
        st.markdown("### Guess History")
        st.line_chart([{"attempt": i+1, "guess": guess} 
                      for i, guess in enumerate(st.session_state.attempts)],
                     x="attempt", y="guess")
else:
    st.info("No game statistics available yet. Start playing to see your stats!")