import streamlit as st
import requests


def build_prompt(topic, input_text):
    model_prompt = f"Message: {input_text} "
    model_prompt += f"Is this message about {topic}?"
    return model_prompt

model_req = requests.get('http://language-model.westeurope.cloudapp.azure.com/model').json()

st.header("text-classification-app")
st.markdown(f"Use language models to classify text. Currently powered by [{model_req['model_name']}]({model_req['source']}).")
st.markdown("Built with love by [NLRC 510](https://www.510.global/). See [the project on GitHub](https://github.com/rodekruis/text-generation-app).")
input_topic = st.text_area('Input topic', 'World')
input_text = st.text_area('Input text', 'Hello world!')
submit = st.button('Classify')
if submit:

    url = 'http://language-model.westeurope.cloudapp.azure.com/generate/'
    payload = {
        'text': build_prompt(input_topic.lower(), input_text),
        'length': 30
    }

    with st.spinner(text="This may take a moment..."):
        result = requests.post(url, json=payload).json()
        print(payload, result)
        if 'generated_text' in result.keys():
            text = result['generated_text']
        else:
            text = "An error occurred, please try again later or [contact us](mailto:support@510.global)!"

    st.text_area('Output', text)