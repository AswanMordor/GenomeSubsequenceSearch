import requests


class NCBI:
    DEFAULT_DATABASE = 'nuccore'
    BASE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=' + DEFAULT_DATABASE + '&id='
    DEFAULT_PARAMS = '&rettype=fasta&retmode=text'


def fetch_genome_sequence_from_ncbi_nuccore(ncbi_id: str) -> str:
    url = NCBI.BASE_URL + ncbi_id + NCBI.DEFAULT_PARAMS
    try:
        response = requests.get(url)
        content = str(response.content, 'utf-8')
        return content[content.find('\n') + 1:]
    except requests.exceptions.HTTPError as err:
        print("HTTP error: " + str(err))