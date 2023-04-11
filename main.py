import pandas as pd
import streamlit as st

import data_fetcher
import sequence_searcher as proc

st.title('DNA Subsequence Finder')
st.subheader('Enter Genome Id and Subsequence Below')
st.write("using periods to denote 'don't care' bases, ex. T...C as a 5-base subsequence")

genome_id = st.text_input('Genome Id', '')
subsequence = st.text_input('Subsequence', '')

if st.button('Submit'):
    genome_seq = data_fetcher.fetch_genome_sequence_from_ncbi_nuccore(genome_id)
    matches = proc.find_matches(genome_seq, subsequence)

    st.subheader('Matches Found')
    df = pd.DataFrame.from_dict({'Start Positions in Genome': matches.keys(), 'Matched Subsequence': matches.values()})
    st.table(df)

    st.pyplot(proc.make_line_plot_of_matches(genome_seq, matches))

