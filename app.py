# Load libraries
import pandas as pd
from pandas.io.json import json_normalize 
import numpy as np
import requests
import urllib.request
import json
from datetime import datetime
import datetime as dt
import streamlit as st
import json
    

df_res = pd.DataFrame()
st.title("Lead Magic Email Loop")
st.markdown('---')

st.markdown('## Enter API Key')
lm_key = st.text_input('Enter your API Key Here')
st.markdown('---')

st.markdown('## Upload CSV')

uploaded_file = st.file_uploader("Upload Here")
if uploaded_file is not None:
#process and format csv 
    testdf = pd.read_csv(uploaded_file)

if 'selling_values' not in st.session_state:
    st.session_state.selling_values = None

st.markdown('---')
st.markdown('## Process with LeadMagic')

with st.form("step_3"):

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        all_res = []

        for index, row in testdf.iterrows():
            
            name = row['name']
            domain = row['domain']
            
            url = "https://api.leadmagic.io/qfn6986nsmxd6b79/api/search/name"

            p = {
              "name": name,
              "domain": domain
            }

            p = json.dumps(p)
            loaded_p = json.loads(p)

            headers = {
              "Content-Type": "application/json",
              "Accept": "application/json",
              "X-BLOBR-KEY": lm_key
            }

            response = requests.post(url, data=p, headers=headers)

            j = response.json()

            data = json_normalize(j)

            df = pd.DataFrame.from_dict(data)

            all_res.append(df)

            st.write(row['name']+" done")
            
        df_res = pd.concat(all_res)
    


def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

st.markdown('---')
st.markdown('## Download Enriched CSV')


st.download_button(
  label="Download data as CSV",
  data=convert_df_to_csv(df_res),
  file_name='lmemail.csv',
  mime='text/csv'
)
