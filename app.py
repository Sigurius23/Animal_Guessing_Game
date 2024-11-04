import streamlit as st
import random

# Initialize session state variables
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'game_history' not in st.session_state:
    st.session_state.game_history = []

# Page configuration
st.set_page_config(page_title="Number Guessing Game", page_icon="🎲")
st.title("Number Guessing Game 🎮")

# Game description
st.markdown("""
Try to guess the number between 1 and 100!
I'll tell you if your guess is too high or too low.
""")

def validate_input(guess):
    """Validate user input to ensure it's a number between 1 and 100."""
    try:
        guess = int(guess)
        if 1 <= guess <= 100:
            return True, guess
        return False, "Please enter a number between 1 and 100"
    except ValueError:
        return False, "Please enter a valid number"

# Input form for guess
with st.form(key='guess_form'):
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
    submit_button = st.form_submit_button("Submit Guess")

# Game logic
if submit_button:
    # Validate input
    is_valid, result = validate_input(guess)
    
    if is_valid:
        st.session_state.attempts.append(guess)
        
        # Check guess against target number
        if guess == st.session_state.target_number:
            attempts = len(st.session_state.attempts)
            message = f"🎉 Congratulations! You found the number in {attempts} attempts!"
            st.success(message)
            st.session_state.messages.append({"role": "assistant", "content": message})
            
            # Store game statistics
            st.session_state.game_history.append({
                'attempts': attempts,
                'target': st.session_state.target_number
            })
            
            # Play again button
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
    else:
        # Display error message if input is invalid
        st.error(result)

# Display chat messages
st.markdown("### Game History")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display current game progress
if st.session_state.attempts:
    st.markdown(f"### Current Game Progress")
    st.markdown(f"Number of attempts so far: {len(st.session_state.attempts)}")