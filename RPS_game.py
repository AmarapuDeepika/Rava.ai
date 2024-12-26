import streamlit as st
import random

st.title("Rock, Paper, Scissors")
choices = ["Rock", "Paper", "Scissors"]
user_choice = st.selectbox("Your choice:", choices)
if st.button("Play"):
    comp_choice = random.choice(choices)
    result = "It's a tie!"
    if (user_choice == "Rock" and comp_choice == "Scissors") or \
       (user_choice == "Paper" and comp_choice == "Rock") or \
       (user_choice == "Scissors" and comp_choice == "Paper"):
        result = "You win!"
    elif user_choice != comp_choice:
        result = "You lose!"
    st.success(f"Computer chose {comp_choice}. {result}")
