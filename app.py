import streamlit as st

# -------------------------------
# SONGLINK CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="SONGLINK",
    page_icon="🎵",
    layout="wide"
)

# -------------------------------
# DESIGN
# -------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0b0b0b;
    color: white;
}

h1 {
    color: #00ff99;
    text-align: center;
}

.search-box {
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------

st.title("🎵 SONGLINK")

st.markdown(
    "<h3 style='text-align:center;'>Music, one search away.</h3>",
    unsafe_allow_html=True
)

st.write("")

# -------------------------------
# SEARCH
# -------------------------------

song = st.text_input(
    "Search for a song",
    placeholder="Enter song name or artist..."
)

search_button = st.button("🔎 SEARCH")

# -------------------------------
# SEARCH FUNCTION
# -------------------------------

if search_button:

    if song.strip():

        st.success(f"You searched for: {song}")

        st.info("Our music search engine will be connected in the next stage.")

    else:

        st.warning("Please enter a song name.")

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>SONGLINK • Built with Python</p>",
    unsafe_allow_html=True
)
