import streamlit as st
import random

# Initialize session state variables if they don't exist
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(page_title="Number Guessing Game", page_icon="🎲")
st.title("Number Guessing Game 🎮")

# Game description
st.markdown("""
Try to guess the number between 1 and 100!
I'll tell you if your guess is too high or too low.
""")

# Input for guess
with st.form(key='guess_form'):
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
    submit_button = st.form_submit_button("Submit Guess")

# Game logic
if submit_button:
    st.session_state.attempts.append(guess)
    
    if guess == st.session_state.target_number:
        message = f"🎉 Congratulations! You found the number in {len(st.session_state.attempts)} attempts!"
        st.success(message)
        st.session_state.messages.append({"role": "assistant", "content": message})
        
        if st.button("Play Again"):
            st.session_state.target_number = random.randint(1, 100)
            st.session_state.attempts = []
            st.session_state.messages = []
            st.experimental_rerun()
            
    elif guess < st.session_state.target_number:
        message = "📈 Too low! Try a higher number."
        st.warning(message)
        st.session_state.messages.append({"role": "assistant", "content": message})
    else:
        message = "📉 Too high! Try a lower number."
        st.warning(message)
        st.session_state.messages.append({"role": "assistant", "content": message})

# Display chat messages
st.markdown("### Game History")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])