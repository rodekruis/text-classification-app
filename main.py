import uvicorn
from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

# Initialize model
modelname = os.environ["MODEL_ORG"] + "/" + os.environ["MODEL_NAME"]
tokenizer = AutoTokenizer.from_pretrained(modelname)
model = AutoModelForSequenceClassification.from_pretrained(modelname)
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)


class ModelName(str, Enum):
    modelname = modelname

    @classmethod
    def exists(cls, key):
        return key in cls.__members__


class ClassifyPayload(BaseModel):
    text: str
    labels: list
    multi_label: Union[bool, None] = True


# load environment variables
port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="text-classification-app",
    description="Zero-shot text classification. \n"
                "Built with love by [NLRC 510](https://www.510.global/). See [the project on GitHub](https://github.com/rodekruis/text-classification-app).",
    version="0.0.1",
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)


@app.get("/")
def index():
    return {"data": "Welcome to text-classification-app!"}


@app.post("/classify/")
async def classify_text(payload: ClassifyPayload):
    output = {}
    try:
        output = classifier(
            sequences=payload.text,
            candidate_labels=payload.labels,
            multi_label=payload.multi_label
        )
    except:
        pass
    return output


@app.get("/model")
async def get_model():
    return {"model_name": modelname, "source": f"https://huggingface.co/{modelname}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)