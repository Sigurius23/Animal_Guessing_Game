import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Game Statistics", page_icon="📊")
st.title("Game Statistics 📊")

# Initialize game history if not exists
if 'game_history' not in st.session_state:
    st.session_state.game_history = []

# Calculate statistics
if st.session_state.game_history:
    games_played = len(st.session_state.game_history)
    avg_guesses = sum(game['attempts'] for game in st.session_state.game_history) / games_played
    
    st.markdown(f"### Overall Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Games Played", games_played)
    with col2:
        st.metric("Average Guesses", f"{avg_guesses:.1f}")
    
    # Create DataFrame for visualization
    df = pd.DataFrame(
        [{'Game': i+1, 'Attempts': game['attempts']} 
         for i, game in enumerate(st.session_state.game_history)]
    )
    
    # Bar chart
    st.markdown("### Guesses per Game")
    fig = px.bar(df, x='Game', y='Attempts')
    st.plotly_chart(fig)
    
    # Recent games table
    st.markdown("### Recent Games")
    st.dataframe(df.tail(5))
else:
    st.info("No games completed yet. Start playing to see your statistics!")