import streamlit as st
from openai import OpenAI
import random

# Define the list of animals globally
animals = ['elephant', 'penguin', 'giraffe', 'dolphin', 'kangaroo', 'tiger', 'koala', 'octopus']

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'target_animal' not in st.session_state:
    st.session_state.target_animal = random.choice(animals)
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'hint_given' not in st.session_state:
    st.session_state.hint_given = False

def reset_game():
    """Reset all game state variables"""
    st.session_state.target_animal = random.choice(animals)
    st.session_state.messages = []  # Reset chat history
    st.session_state.questions_asked = 0
    st.session_state.hint_given = False

def provide_hint(target_animal):
    """Provide a hint about the target animal."""
    hints = {
        'elephant': "It's the largest land animal.",
        'penguin': "It can't fly but swims well.",
        'giraffe': "It has a very long neck.",
        'dolphin': "It's a highly intelligent marine mammal.",
        'kangaroo': "It hops and has a pouch.",
        'tiger': "It's a big cat with stripes.",
        'koala': "It loves eucalyptus leaves.",
        'octopus': "It has eight arms."
    }
    return hints.get(target_animal, "No hint available.")

# Page config
st.set_page_config(page_title="Animal Guessing Game", page_icon="🦁")
st.title("Animal Guessing Game 🦁")

# Game instructions
st.markdown("""
Ask yes/no questions to guess the animal I'm thinking of! 
For example:
- Does it live in water?
- Is it a carnivore?
- Does it have fur?

When you're ready to guess, just say "Is it a [your guess]?"
""")

def analyze_question(question, target_animal):
    """Use OpenAI to analyze the question and provide only yes/no answers."""
    prompt = f"""
    You are helping with an animal guessing game. The target animal is a {target_animal}.
    The player asked: "{question}"
    
    IMPORTANT RESPONSE RULES:
    1. For yes/no questions: 
       - Answer must be EXACTLY "yes" or "no" (no explanation)
    2. For guesses:
       - Only treat "Is it a [animal]?" as a guess
       - Check if they guessed the exact animal
    
    YOU MUST RESPOND EXACTLY IN THIS FORMAT WITHOUT ANY DEVIATION:
    Type: [question/guess]
    Answer: [yes/no]
    IsCorrectGuess: [true/false, only if it's a guess]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return response.choices[0].message.content

def clean_response(response):
    """Ensures that only 'yes' or 'no' is provided in the response."""
    if response.startswith("yes"):
        return "yes"
    elif response.startswith("no"):
        return "no"
    else:
        # Fallback to trim any extra content
        return response.split('.')[0].strip()

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if question := st.chat_input("Ask a yes/no question about the animal..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get AI analysis
    response = analyze_question(question, st.session_state.target_animal)
    
    # Process the response
    response_lines = response.split('\n')
    response_dict = {}
    for line in response_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            response_dict[key.strip()] = value.strip()

    # Increment questions counter
    st.session_state.questions_asked += 1

    # Prepare assistant's response
    if response_dict.get('Type') == 'guess':
        if response_dict.get('IsCorrectGuess') == 'true':
            assistant_response = f"🎉 Congratulations! You got it right! It was a {st.session_state.target_animal}!\nYou took {st.session_state.questions_asked} questions to guess it."
            # Store game statistics
            st.session_state.game_history.append({
                'attempts': st.session_state.questions_asked,
                'target': st.session_state.target_animal
            })
        else:
            assistant_response = "No, that's not correct. Keep guessing!"
    else:
        # Strictly format the response
        answer = response_dict.get('Answer', '').strip().lower()
        answer = clean_response(answer)  # Ensure only 'yes' or 'no' is kept
        assistant_response = f"{answer}."

    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Display current progress
if st.session_state.questions_asked > 0:
    st.markdown(f"Questions asked: {st.session_state.questions_asked}")

# Provide a hint if requested
if st.button("Need a hint?"):
    if not st.session_state.hint_given:
        hint = provide_hint(st.session_state.target_animal)
        st.session_state.messages.append({"role": "assistant", "content": f"Hint: {hint}"})
        st.session_state.hint_given = True
        st.rerun()  # Rerun the app after hint is given
    else:
        st.warning("You've already received a hint for this game.")

# New Game Button
col1, col2, _ = st.columns([2,1,2])  # Create columns for better button placement
with col2:
    if st.button("New Game", key="new_game_button"):
        reset_game()
        st.rerun()  # Rerun the app to reflect changes