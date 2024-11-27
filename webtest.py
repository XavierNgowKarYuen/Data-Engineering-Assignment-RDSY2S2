import streamlit as st
from bs4 import BeautifulSoup
import requests

# Define the GIF paths and labels
gifs = [
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action1.gif", "label": "Bagus"},
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action2.gif", "label": "Marah"},
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action3.gif", "label": "Terkejut"},
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action4.gif", "label": "Sedih"},
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action5.gif", "label": "Lawak"},
    {"path": "C:/Degree Year 2 Semester 2/Data Engineering/Assignment/action6.gif", "label": "Bosan"},
]

# ScrapedData Class
class ScrapedData:
    def __init__(self, aid, title, date, publisher, views, comments_count, content):
        self.aid = aid
        self.title = title
        self.date = date
        self.publisher = publisher
        self.views = views
        self.comments_count = comments_count
        self.content = content

    def __str__(self):
        return f"""
        Aid: {self.aid}
        Title: {self.title}
        Date: {self.date}
        Publisher: {self.publisher}
        Views: {self.views}
        Comments Count: {self.comments_count}
        Content:
        {self.content}
        """

def remove_cari_dot_my(text):
    """Removes '-CariDotMy' from the given text and trims leading/trailing spaces."""
    return text.replace("- CariDotMy", "").strip()

def scrape_article(url, aid):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('title').text if soup.find('title') else "Unknown"
    title = remove_cari_dot_my(title)

    date_tag = soup.find('p', class_='xg1')
    date = date_tag.text.split('|')[0].strip() if date_tag else "Unknown"

    publisher_tag = date_tag.find('a') if date_tag else None
    publisher = publisher_tag.text if publisher_tag else "Unknown"

    views_tag = soup.find('em', id='_viewnum')
    views = views_tag.text if views_tag else "0"

    comments_tag = soup.find('em', id='_commentnum')
    comments_count = comments_tag.text if comments_tag else "0"

    content_tag = soup.find('td', id='article_content')
    content = content_tag.get_text(strip=True) if content_tag else ""

    return ScrapedData(aid, title, date, publisher, views, comments_count, content)

# Title
st.title("Scraping Integration")

# Scraping Section
st.header("Scrape Data from Articles")
base_url = "https://b.cari.com.my/portal.php?mod=view&aid="
aid = st.number_input("Enter Article ID to Scrape:", min_value=1, value=1, step=1)

if st.button("Scrape Article"):
    url = f"{base_url}{aid}"
    try:
        scraped_data = scrape_article(url, aid)
        st.write(scraped_data)
    except Exception as e:
        st.error(f"Error scraping {url}: {e}")

# Divider
st.write("---")

# GIF Section
st.header("Interactive GIF")


# Initialize session state for counters
if "counters" not in st.session_state:
    st.session_state.counters = {gif["label"]: 0 for gif in gifs}

cols = st.columns(len(gifs))

# Display GIFs with buttons
for col, gif in zip(cols, gifs):
    if col.button(f"{gif['label']}"):
        st.session_state.counters[gif["label"]] += 1
    col.image(gif["path"], width=100, caption=f"{gif['label']} ({st.session_state.counters[gif['label']]})")
