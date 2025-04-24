import streamlit as st
import sqlite3
from markov_chain import MarkovChain
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Setup logging for better error handling
logging.basicConfig(level=logging.INFO)

# SQLite connection setup
conn = sqlite3.connect('lyrics.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_text TEXT,
                    output_text TEXT,
                    order_val INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Streamlit UI
st.title("🎶 Markov Chain Song Lyric Composer")
st.write("Welcome to the Markov Chain Song Lyric Composer! Paste your song lyrics and generate new lyrics based on the Markov model.")

# Input Section
order = st.slider("Select Markov Chain Order", 1, 5, 2, help="Higher order models generate more accurate predictions but require more training data.")
text_input = st.text_area("Paste song lyrics here", height=250)  # Text area for lyrics input

# Generate Button
if st.button("Generate Lyrics"):
    if text_input:
        try:
            # Initialize Markov Chain and train the model
            mc = MarkovChain(order=order)
            mc.train(text_input)
            generated_lyrics = mc.generate(length=50)  # Generate 50 words

            st.write("**Generated Lyrics:**")
            st.text(generated_lyrics)

            # Store the input/output in SQLite database
            cursor.execute("INSERT INTO history (input_text, output_text, order_val) VALUES (?, ?, ?)", 
                           (text_input, generated_lyrics, order))
            conn.commit()

            # Generate and display a WordCloud of the generated lyrics
            wordcloud = WordCloud(width=800, height=400).generate(generated_lyrics)
            plt.figure(figsize=(8, 4))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        except Exception as e:
            logging.error(f"Error generating lyrics: {e}")
            st.error("An error occurred while generating lyrics. Please try again.")
    else:
        st.warning("Please enter lyrics to train the model.")

# Display previously generated lyrics (History Section)
if st.checkbox("Show previous generations"):
    rows = cursor.execute("SELECT * FROM history ORDER BY date DESC").fetchall()
    for row in rows:
        st.markdown(f"**Generated on {row[4]} (Order {row[3]}):**")
        st.text(row[2])  # Show output text (generated lyrics)
