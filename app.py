import streamlit as st
import requests
import urllib.parse
import html

# =========================================
# SONGLINK 1.0
# =========================================

st.set_page_config(
    page_title="SONGLINK",
    page_icon="🎵",
    layout="wide"
)

# =========================================
# STYLING
# =========================================

st.markdown("""
<style>

.stApp {
    background-color: #080b10;
    color: #ffffff;
}

[data-testid="stHeader"] {
    background-color: #080b10;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1 {
    color: #00e5a0;
    font-size: 55px !important;
    font-weight: 900;
}

h2, h3 {
    color: white;
}

.stTextInput input {
    background-color: #151a23;
    color: white;
    border-radius: 12px;
}

.stButton button {
    background-color: #00e5a0;
    color: #08110d;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    min-height: 45px;
}

.stButton button:hover {
    background-color: #00bb82;
    color: white;
}

.song-card {
    background-color: #151a23;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    border: 1px solid #252d38;
}

.small-text {
    color: #a0aab8;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.markdown("# 🎵 SONGLINK")

st.markdown(
    "### Discover music. Find artists. Explore sounds."
)

st.caption("A free music discovery platform.")

st.divider()

# =========================================
# SESSION STATE
# =========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "results" not in st.session_state:
    st.session_state.results = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# =========================================
# MUSICBRAINZ SEARCH
# =========================================

def search_music(query):

    endpoint = "https://musicbrainz.org/ws/2/recording/"

    params = {
        "query": query,
        "fmt": "json",
        "limit": 15
    }

    headers = {
        "User-Agent": "SONGLINK/1.0 (music discovery application)"
    }

    try:

        response = requests.get(
            endpoint,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return data.get("recordings", [])

    except requests.RequestException as error:

        st.error(f"Music search failed: {error}")

        return []

# =========================================
# MUSIC INFORMATION
# =========================================

def get_artist(recording):

    artist_credits = recording.get("artist-credit", [])

    artists = []

    for credit in artist_credits:

        if isinstance(credit, dict):

            artist = credit.get("name")

            if artist:
                artists.append(artist)

    return ", ".join(artists) or "Unknown artist"


def get_album(recording):

    releases = recording.get("releases", [])

    if releases:

        return releases[0].get(
            "title",
            "Unknown album"
        )

    return "Unknown album"


def get_year(recording):

    releases = recording.get("releases", [])

    if releases:

        date = releases[0].get("date", "")

        if date:
            return date[:4]

    return "Unknown year"


# =========================================
# SEARCH
# =========================================

search_query = st.text_input(
    "Search for a song or artist",
    placeholder="Try Adele, Drake, Sauti Sol..."
)

search_col, clear_col = st.columns([3, 1])

with search_col:

    search_button = st.button(
        "🔎 SEARCH MUSIC",
        use_container_width=True
    )

with clear_col:

    clear_button = st.button(
        "🗑️ CLEAR",
        use_container_width=True
    )

if clear_button:

    st.session_state.results = []

    st.session_state.last_query = ""

    st.rerun()

if search_button:

    if search_query.strip():

        with st.spinner("Searching the music database..."):

            results = search_music(search_query.strip())

        st.session_state.results = results

        st.session_state.last_query = search_query.strip()

        st.session_state.history.insert(
            0,
            search_query.strip()
        )

        st.session_state.history = (
            st.session_state.history[:10]
        )

    else:

        st.warning("Enter a song or artist name.")

# =========================================
# RESULTS
# =========================================

if st.session_state.results:

    st.markdown(
        f"## Search results for: "
        f"{html.escape(st.session_state.last_query)}"
    )

    for index, music in enumerate(
        st.session_state.results
    ):

        title = music.get(
            "title",
            "Unknown title"
        )

        artist = get_artist(music)

        album = get_album(music)

        year = get_year(music)

        recording_id = music.get("id", "")

        st.markdown(
            f"""
            <div class="song-card">
                <h3>🎵 {html.escape(title)}</h3>
                <p>👤 {html.escape(artist)}</p>
                <p>💿 {html.escape(album)}</p>
                <p>📅 {html.escape(year)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            search_web_url = (
                "https://archive.org/advancedsearch.php?"
                + urllib.parse.urlencode({
                    "q": title + " " + artist,
                    "fl[]": ["identifier", "title"],
                    "output": "json"
                })
            )

            st.link_button(
                "🌐 Explore music sources",
                "https://archive.org/search?"
                + urllib.parse.urlencode({
                    "query": title + " " + artist
                }),
                use_container_width=True
            )

        with col2:

            st.link_button(
                "🔍 Find song information",
                "https://musicbrainz.org/recording/"
                + recording_id,
                use_container_width=True
            )

        st.divider()

# =========================================
# EMPTY RESULTS
# =========================================

elif st.session_state.last_query:

    st.info("No music results found.")

# =========================================
# SEARCH HISTORY
# =========================================

st.markdown("## 🕘 Recent searches")

if st.session_state.history:

    for item in st.session_state.history:

        st.write("🔎", item)

else:

    st.caption("Your recent searches will appear here.")

# =========================================
# FOOTER
# =========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#8491a1;">
        <h3>SONGLINK</h3>
        <p>Music discovery made simple.</p>
        <p>Built with Python.</p>
    </div>
    """,
    unsafe_allow_html=True
)
