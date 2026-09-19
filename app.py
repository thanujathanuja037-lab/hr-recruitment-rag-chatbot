"""Streamlit chat page. Run with: streamlit run app.py"""
import streamlit as st

import config
import rag_core

st.set_page_config(page_title="HR Assistant", page_icon="💼")
st.title("💼 HR & Recruitment Assistant")
st.caption("Answers only from the HR documents in the knowledge base.")

max_dist = st.sidebar.slider(
    "Relevance cutoff (lower = stricter)",
    0.3, 1.5, float(config.MAX_DISTANCE), 0.05
)
debug = st.sidebar.checkbox("Show scores (debug)")

if st.sidebar.button("Clear chat"):
    st.session_state.msgs = []
    st.rerun()

if debug:
    st.sidebar.write(
        "Scores of last question:",
        st.session_state.get("last_scores", [])
    )


@st.cache_resource
def load():
    return rag_core.load_db(), rag_core.get_llm()


try:
    db, llm = load()
except Exception as e:
    st.error(f"Could not start: {e}")
    st.stop()

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.write(m["text"])
        if m.get("sources"):
            with st.expander("Sources"):
                for s in m["sources"]:
                    st.write("•", s)

q = st.chat_input("Ask an HR or recruitment question...")

if q:
    st.session_state.msgs.append(
        {"role": "user", "text": q}
    )

    with st.chat_message("user"):
        st.write(q)

    with st.chat_message("assistant"):
        with st.spinner("Searching the HR documents..."):
            res = rag_core.answer_question(
                q, db, llm, max_distance=max_dist
            )

        st.write(res["answer"])

        if res["sources"]:
            with st.expander("Sources"):
                for s in res["sources"]:
                    st.write("•", s)

        if debug:
            st.write("Retrieval scores:", res["scores"])
            st.write("Reason:", res["reason"])

    st.session_state.msgs.append({
        "role": "assistant",
        "text": res["answer"],
        "sources": res["sources"]
    })

    st.session_state.last_scores = res["scores"]