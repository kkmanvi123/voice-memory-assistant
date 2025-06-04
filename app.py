import os
import streamlit as st
from datetime import datetime
from utils.transcribe import transcribe_audio
from utils.embed import get_embedding, save_memory
from utils.search import MemorySearch

# Set page config
st.set_page_config(
    page_title="Voice Memory Assistant",
    page_icon="🎙️",
    layout="wide"
)

# Initialize session state
if 'memory_search' not in st.session_state:
    st.session_state.memory_search = MemorySearch()

# Create necessary directories
os.makedirs("data/audio_uploads", exist_ok=True)

# App title
st.title("🎙️ Voice Memory Assistant")

# File upload section
st.header("Upload Audio")
uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a'])

if uploaded_file is not None:
    # Save uploaded file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = uploaded_file.name.split('.')[-1]
    file_path = f"data/audio_uploads/{timestamp}.{file_extension}"
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Transcribe button
    if st.button("Transcribe + Save"):
        with st.spinner("Transcribing audio..."):
            # Transcribe audio
            transcript = transcribe_audio(file_path)
            
            # Generate embedding
            embedding = get_embedding(transcript)
            
            # Save to memory
            save_memory(transcript, embedding)
            
            # Reload search index
            st.session_state.memory_search.load_memories()
            
            st.success("Audio transcribed and saved!")
            st.write("Transcript:", transcript)

# Search section
st.header("Search Memories")
search_query = st.text_input("Enter your search query:")

if search_query:
    with st.spinner("Searching..."):
        results = st.session_state.memory_search.search(search_query)
        
        if results:
            st.subheader("Top 3 Matching Memories:")
            for i, result in enumerate(results, 1):
                with st.expander(f"Memory {i} - {result['timestamp']}"):
                    st.write(result['transcript'])
        else:
            st.info("No matching memories found.") 