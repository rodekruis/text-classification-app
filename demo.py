import streamlit as st
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
sns.set_theme(style="whitegrid")

model_req = requests.get('http://language-model.westeurope.cloudapp.azure.com/model').json()

st.header("text-classification-app")
st.markdown(f"Use language models to classify text. Currently powered by [{model_req['model_name']}]({model_req['source']}).")
st.markdown("Built with love by [NLRC 510](https://www.510.global/). See [the project on GitHub](https://github.com/rodekruis/text-generation-app).")
input_text = st.text_area('Text', 'I have a problem with my iphone that needs to be resolved asap!!')
input_labels = st.text_area('Class labels (comma-separated)', 'urgent, not urgent, phone, tablet, computer')
submit = st.button('Classify')
if submit:

    url = 'http://language-model.westeurope.cloudapp.azure.com/classify/'
    payload = {
        'text': input_text,
        'labels': input_labels.split(','),
        'multi_label': True
    }
    with st.spinner(text="This may take a moment..."):
        results = requests.post(url, json=payload).json()
        fig, ax = plt.subplots()
        scores = [x*100. for x in results['scores']]
        sns.barplot(x=scores, y=results['labels'], label="Total", color="b")
        ax.set(xlabel='score (%)', ylabel='class labels')
        st.pyplot(fig)
