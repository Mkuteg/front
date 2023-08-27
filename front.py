import logging
import random
import time
from typing import List, Tuple, Any
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox
from urllib3.util import url

logging.getLogger("streamlit_searchbox").setLevel(logging.DEBUG)


st.set_page_config(page_title="Поиск по документации", layout="wide", initial_sidebar_state="auto", page_icon="📖")

st.title = "Поиск по документации"

st.markdown("---")

def search_test(question: str) -> list[Tuple[Any, Any]]:
    response = requests.post(
            "https://al-dente.serveo.net/answer",
            timeout=15,
            json={"question": question}
        ).json()
    print(response)
    candidates = response['candidates']['candidate']
    return [
            (
                candidate['question'],
                candidate['answer']
            )
            for candidate in candidates

        ]

def search_docs_ids(question: str) -> List[Tuple[str, str]]:

    # you can use a nice default here
    if not question:
        return []
    # with information on title, id, etc
    response = requests.post(
        "https://al-dente.serveo.net/answer",
        timeout=15,
        json={"question": question}
    ).json()
    print(response)
    candidates = response['candidates']
    # first element will be shown in search, second is returned from component
    return [
        (
            candidate["candidate"]['question'] + " " + str(candidate['similarity']),
            candidate["candidate"]['answer']
        )
        for candidate in candidates

    ]

def search_empty_list(_: str):
    if not st.session_state.get("search_empty_list_n", None):
        st.session_state["search_empty_list_n"] = 1
        return ["a", "b", "c"]

    return []

#################################
#### application starts here ####
#################################


st.markdown("---")

with st.container():
    selected_value = st_searchbox(
        search_function=search_docs_ids,
        placeholder="Поиск... ",
        label="Поиск по доке на главной странице",
        default="Нет ответа",
        clear_on_submit=False,
        clearable=True,
        key="docs_search_main",
    )
    st.info(selected_value)
    st.info(selected_value)

with st.container():
    value = search_test("search")

