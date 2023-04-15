import pandas as pd
import streamlit as st
import extra_streamlit_components as stx
import datetime

from dateutil.relativedelta import relativedelta

import data_fetcher
import sequence_searcher as proc

SUBSEQUENCES = 'subsequences'


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()
cookies = cookie_manager.get_all()
st.write(cookies)

st.title('DNA Subsequence Finder')
st.write('(v0.4.2-beta (Note: this version uses cookies to save sessions)')
st.subheader('Enter Genome Id and Subsequence Below')
st.write("using periods to denote 'don't care' bases, ex. T...C as a 5-base subsequence")

genome_id = st.text_input('Genome Id', '' if not cookie_manager.get(SUBSEQUENCES)
else cookie_manager.get(SUBSEQUENCES)[0]).upper().strip()
subsequence = st.text_input('Subsequence', '' if not cookie_manager.get(SUBSEQUENCES)
else cookie_manager.get(SUBSEQUENCES)[1]).upper().strip()

button_container = st.container()
results_container = st.container()


def update_cookies(subseq: str, g_id: str):
    cookie_manager.set(SUBSEQUENCES, [g_id, subseq], key='0',
                       expires_at=(datetime.date.today() + relativedelta(months=+6)))


def show_results(final_subsequence: str):
    with results_container:
        update_cookies(subsequence, genome_id)
        genome_seq = data_fetcher.fetch_genome_sequence_from_ncbi_nuccore(genome_id)
        if genome_seq.strip() != '':
            matches = proc.find_matches(genome_seq, final_subsequence)

            st.subheader('Matches Found for Subsequence: ' + final_subsequence)
            df = pd.DataFrame.from_dict(
                {'Start Positions in Genome': matches.keys(), 'Matched Subsequence': matches.values()})
            st.table(df)

            st.pyplot(proc.make_line_plot_of_matches(genome_seq, matches))


def valid_subsequence():
    global subsequence
    subsequence = str.replace(subsequence, "…", "...")
    for c in subsequence:
        if c not in proc.COMPLIMENTS.keys():
            with results_container: st.error('Please use only A T G C or . in your subsequence input')
            return False
    return True


with button_container:
    if st.button('Search for Subsequence'):
        if valid_subsequence(): show_results(subsequence)
    if st.button('Search for Complement'):
        if valid_subsequence(): show_results(proc.create_compliment(subsequence))
    if st.button('Search for the Reverse'):
        if valid_subsequence(): show_results((proc.create_reverse(subsequence)))
