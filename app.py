import pandas as pd
import requests
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="NVF Dashboard",
    layout="wide"
)

@st.cache_data(ttl=3600)
def hent_ranking():
    url = "https://nvf-backend.herokuapp.com/api/public/ranking/"
    r = requests.get(url)
    r.raise_for_status()
    return pd.DataFrame(r.json())

@st.cache_data(ttl=3600)
def hent_stevner():
    url = (
        "https://nvf-backend.herokuapp.com/api/public/stevner"
        "?fra-dato=2021-01-01&til-dato=2026-12-31"
    )
    r = requests.get(url)
    r.raise_for_status()
    return pd.DataFrame(r.json())

st.title("NVF Analyseportal")

fane1, fane2 = st.tabs(["Ranking", "Stevner"])

with fane1:

    df = hent_ranking()

    st.subheader("Ranking")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.write(f"Antall utøvere: {len(df)}")

    numeriske = df.select_dtypes(include="number").columns

    if len(numeriske) > 0:

        valgt = st.selectbox(
            "Velg poengkolonne",
            numeriske
        )

        fig = px.histogram(
            df,
            x=valgt,
            title=f"Fordeling av {valgt}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with fane2:

    stevner = hent_stevner()

    st.subheader("Stevner")

    st.dataframe(
        stevner,
        use_container_width=True,
        hide_index=True
    )

    st.write(f"Antall stevner: {len(stevner)}")

    if "dato" in stevner.columns:

        stevner["dato"] = pd.to_datetime(
            stevner["dato"],
            errors="coerce"
        )

        stevner["år"] = stevner["dato"].dt.year

        årsstat = (
            stevner
            .groupby("år")
            .size()
            .reset_index(name="Antall")
        )

        fig = px.bar(
            årsstat,
            x="år",
            y="Antall",
            title="Stevner per år"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )