import email
import json
from select import select
import time
from unicodedata import name
import streamlit as st
import requests
import pandas as pd
import datetime as dt

# set page config
st.set_page_config(page_title="LearnApp", page_icon="favicon.png")

# hide streamlit branding and hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# set today's date and time
curr_time_dec = time.localtime(time.time())
date = time.strftime("%Y-%m-%d", curr_time_dec)

# get learnapp's content data
f = open("content.json")
content_data = json.load(f)
f.close()

# functions for getting user specific course progress
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2YjliODBkMC0yNDMyLTExZWItYjI2NS0zYjBiYWNkOGE1ZjYiLCJpcCI6IjQ5LjI0OS42OS4yMiwgMTMwLjE3Ni4xODguMjM5IiwiY291bnRyeSI6IklOIiwiaWF0IjoxNjY5MzY5MTY0LCJleHAiOjE2Njk5NzM5NjQsImF1ZCI6ImxlYXJuYXBwIiwiaXNzIjoiaHlkcmE6MC4wLjEifQ.APE2ARFntcL3UuItG5H4tneFCYJaIH4XySvjJyKQCQg"


def fetch_userid(email):
    email = email.replace("@", "%40")
    url = "https://hydra.prod.learnapp.com/kraken/users/search?q=" + email

    payload = {}
    headers = {
        "authorization": token,
        "x-api-key": "u36jbrsUjD8v5hx2zHdZNwqGA6Kz7gsm",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    try:
        data = json.loads(response.text)["users"][0]
        try:
            return data["userId"]
        except:
            return -1
    except:
        return -1


def course_progress(email_id, course_id):
    try:
        user_id = fetch_userid(email_id)
        url = f"https://census.prod.learnapp.com/kraken/users/{user_id}/courses/{course_id}"
        payload = {}
        headers = {
            "authorization": token,
            "x-api-key": "Ch2rqJp3rxH8ZVccQT8ywV7zMR3Ac8fQ",
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        progress = data["courseDetailData"]["percentage"]
    except:
        progress = 0

    return progress


# function for creating the genericcourse cards
def course_container(day_no, date, course_key):
    #
    st.subheader(f"📘 {day_no}: {content_data[course_key]['title']}")
    st.write(f"📅 {date}")
    st.write("✍️ Task: Watch the recorded course and share your learnings!")

    canonical_title = content_data[course_key]["canonicalTitle"]
    course_id = content_data[course_key]["id"]
    progress = course_progress(email_id, course_id)
    if progress >= 85:
        progress_str = f"✅ {progress}"
    else:
        progress_str = f"📖 {progress}"
    course_url = (
        f"https://learnapp.com/courses/{canonical_title}/topics/trailer?locale=en-us"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.image(content_data[course_key]["assetUrl"], width=300)

    with col2:

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(
            f"[![Play Now](https://s3.ap-south-1.amazonaws.com/messenger.prod.learnapp.com/emails/newsLetters-15-nov-22-la-announcement-akriti-singh/5e7bcdd4-039a-4a0f-a255-7c48d3993eaa.png)]({course_url})"
        )
        st.caption(f"{progress_str}% completed")

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.write("")
    # with col2:
    #     st.write("|")
    #     st.write("|")
    #     st.write("|")
    # with col3:
    #     st.write("")

    st.write("")
    st.write("")


# function for creating the genericcourse cards
def workshop_container(day_no, date, workshop_name, workshop_jpeg):
    #
    st.subheader(f"📘 {day_no}: {workshop_name}")
    st.write(f"📅 {date}")
    st.write(f"🕒 09:00 AM")
    st.write("🚨 Task: Attend the live class and share your learnings!")

    col1, col2 = st.columns(2)
    with col1:
        st.image(workshop_jpeg, width=300)

    with col2:

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(
            f"[![Register](https://s3.ap-south-1.amazonaws.com/messenger.prod.learnapp.com/emails/newsLetters-17-nov-22-options-course-email/d1fe4b84-9661-4a70-b06d-d7431b8a5799.png)](https://www.google.com)"
        )
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.write("")
    # with col2:
    #     st.write("|")
    #     st.write("|")
    #     st.write("|")
    # with col3:
    #     st.write("")

    st.write("")
    st.write("")


# Frontend
col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    st.image("logo.png", width=225)
    st.write("")
with col3:
    st.write("")

st.markdown(
    "<h2 style='text-align: center; color: white;'>Learn Trading From Scratch</h2>",
    unsafe_allow_html=True,
)
st.write("-----")

try:
    email_id = st.experimental_get_query_params()["email"][0]
except:
    email_id = (
        st.text_input(
            "Enter your LearnApp Registered Email Address to know your progress"
        )
        .strip()
        .lower()
    )
st.write("---")

course_key = "basics-of-personal-finance"
course_container("Day 01", "29 Nov'22", course_key)

workshop_container(
    "Day 02",
    "30 Nov'22",
    "Create your own Personal Budget",
    "workshop/basics-of-personal-finance.jpeg",
)

course_key = "basics-of-trading"
course_container("Day 03", "01 Dec'22", course_key)

workshop_container(
    "Day 04",
    "02 Dec'22",
    "How to use trading terminal?",
    "workshop/basics-of-trading.jpeg",
)

course_key = "intro-to-technical-analysis"
course_container("Day 05", "05 Dec'22", course_key)

workshop_container(
    "Day 06",
    "06 Dec'22",
    "Using technical analysis in Live Markets",
    "workshop/learn-technical-analysis.jpeg",
)

course_key = "learn-intraday-strategy"
course_container("Day 07", "07 Dec'22", course_key)

workshop_container(
    "Day 08",
    "08 Dec'22",
    "How to trade systems in Live Markets?",
    "workshop/mean-reversion-strategy.jpeg",
)
