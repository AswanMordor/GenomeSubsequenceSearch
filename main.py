import pandas as pd
import streamlit as st
import re

import data_fetcher
import sequence_searcher as proc

st.title('DNA Subsequence Finder')
st.subheader('Enter Genome Id and Subsequence Below')
st.write("using periods to denote 'don't care' bases, ex. T...C as a 5-base subsequence")

genome_id = st.text_input('Genome Id', '').upper().strip()
subsequence = st.text_input('Subsequence', '').upper().strip()

button_container = st.container()
results_container = st.container()


def show_results(final_subsequence: str):
    with results_container:
        genome_seq = data_fetcher.fetch_genome_sequence_from_ncbi_nuccore(genome_id)
        if genome_seq.strip() != '':
            matches = proc.find_matches(genome_seq, final_subsequence)

            st.subheader('Matches Found for Subsequence: ' + final_subsequence)
            df = pd.DataFrame.from_dict(
                {'Start Positions in Genome': matches.keys(), 'Matched Subsequence': matches.values()})
            st.table(df)

            st.pyplot(proc.make_line_plot_of_matches(genome_seq, matches))


def valid_subsequence(subseq: str):
    if not re.search('^[ATGC.]+$', subseq):
        with results_container: st.error('Please use only A T G C or . in your subsequence input')
        return False
    return True


with button_container:
    if st.button('Search for Subsequence'):
        if valid_subsequence(subsequence): show_results(subsequence)
    if st.button('Search for Complement'):
        if valid_subsequence(subsequence): show_results(proc.create_compliment(subsequence))
    if st.button('Search for the Reverse'):
        if valid_subsequence(subsequence): show_results((proc.create_reverse(subsequence)))
