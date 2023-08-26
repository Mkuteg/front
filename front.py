import enum
import logging
import random
import time
from typing import List, Tuple
import wikipedia
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox

logging.getLogger("streamlit_searchbox").setLevel(logging.DEBUG)
st.title = "Поиск по документации"

st.set_page_config(page_title="Поиск по документации", layout="wide", initial_sidebar_state="auto", page_icon="📖")

concat_string = ""

def search_wikipedia_ids(searchterm: str) -> List[Tuple[str, any]]:
    """
    function with list of tuples (label:str, value:any)
    """

    # you can use a nice default here
    if not searchterm:
        return []

    # search that returns a list of wiki articles in dict form
    # with information on title, id, etc
    response = requests.get(
        "http://en.wikipedia.org/w/api.php",
        params={
            "list": "search",
            "format": "json",
            "action": "query",
            "srlimit": 10,
            "limit": 10,
            "srsearch": searchterm,
        },
        timeout=5,
    ).json()["query"]["search"]

    # first element will be shown in search, second is returned from component
    return [
        (
            str(article["title"]),
            article["pageid"],
        )
        for article in response
    ]




def search_docs_ids(question: str) -> List[Tuple[str, str]]:
    """
    function with list of tuples (label:str, value:any)
    """
    # you can use a nice default here

    if not question:
        return []

    # with information on title, id, etc
    response = requests.post(
        "http://0.0.0.0:8000/answer",
         timeout=15,
         json={"question": question}
    ).json()
    print(response)
    # first element will be shown in search, second is returned from component
    return [
        (
            str(qa["question"]),
            str(qa["answer"])
        )
        for qa in response

    ]




def search_rnd_delay(question: str) -> List[str]:
    print(f"searching... {question}")
    time.sleep(random.randint(1, 5))
    return [f"{question}_{i}" for i in range(10)]


def search_fancy_return(_: str):
    e = enum.Enum("FancyEnum", {"a": 1, "b": 2, "c": 3})
    return [e.a, e.b, e.c]


def search_empty_list(_: str):
    if not st.session_state.get("search_empty_list_n", None):
        st.session_state["search_empty_list_n"] = 1
        return ["a", "b", "c"]

    return []


#################################
#### application starts here ####
#################################


c2, c3 = st.columns(2)


with st.sidebar:
    selected_value = st_searchbox(
        search_function=search_wikipedia_ids,
        placeholder="Поиск... ",
        label="Поиск на wikipedia",
        default="SOME DEFAULT",
        clear_on_submit=False,
        clearable=False,
        key="docs_search_sidebar",
    )
    st.write(f"{selected_value}")
    st.info(f"{selected_value}")


with st.container():
    selected_value = st_searchbox(
        search_rnd_delay,
        default=None,
        clear_on_submit=False,
        clearable=True,
        label="Поиск с задержкой",
        key="search_rnd_delay",
    )
    st.info(f"{selected_value}")


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



