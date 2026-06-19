import streamlit as st
import requests

st.title("AWS Agreement RAG Chatbot")

question = st.text_input(
    "Ask a Question"
)

if st.button("Ask"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={
            "question": question
        }
    )

    result = response.json()

    st.write("### Answer")
    st.write(result["answer"])

    st.write("### Sources")

    for source in result["sources"]:
        st.write(source)




import pandas as pd

if st.button("Show Analytics"):

    response = requests.get(
        "http://127.0.0.1:8000/analytics"
    )

    data = response.json()

    st.subheader("Average Latency")
    st.metric(
        "Latency (seconds)",
        round(data["average_latency"], 2)
    )

    st.subheader("Most Frequent Questions")

    df1 = pd.DataFrame(
        data["most_frequent_questions"],
        columns=["Question", "Count"]
    )

    st.dataframe(df1, use_container_width=True)

    st.subheader("Questions With No Answer")

    df2 = pd.DataFrame(
        data["no_answer_queries"],
        columns=["Question"]
    )

    st.dataframe(df2, use_container_width=True)