# import necessary libraries

import os
from google import genai
import pandas as pd
from dotenv import load_dotenv
import json


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# library of pmids and pdfs to be used for the extraction

papers = [
    {"pmid": "25483931", "pdf": "PMID-25483931.pdf"},
    {"pmid": "32777331", "pdf": "PMID-32777331.pdf"},
    {"pmid": "19377993", "pdf": "PMID-19377993.pdf"},
]

pdfs_dir = os.path.join(os.getcwd(), "part2_gemini", "pdfs")

EXTRACTION_PROMPT = """You are analyzing a scientific research paper about aptamers. Extract all aptamers described in the paper and return a JSON array where each element represents one aptamer.

Use exactly these keys for each object:
- paper_id: the PMID of the paper, provided below
- aptamer_name: the name or identifier given to the aptamer in the paper
- target: the molecule the aptamer binds to
- sequence: the nucleotide sequence of the aptamer
- pool_type: the type of nucleic acid used (e.g. ssDNA, RNA, modified DNA)
- kd: the dissociation constant reported for the aptamer
- source: a single string summarizing where all fields were found in the paper

Rules:
- Do not infer, estimate, or assume any value
- If a field is not explicitly stated in the paper, output "not reported" for that field and "not reported" for its source
- Only extract information directly present in the paper text
- Return only the JSON array, no extra text, no markdown backticks

The PMID of this paper is: {pmid}"""

# create a list to hold all extracted rows

all_rows = []


for paper in papers:
    pdf_path = os.path.join(pdfs_dir, paper["pdf"])
    print(pdf_path)
    uploaded_file = client.files.upload(file=pdf_path, config={"mime_type": "application/pdf"})
    print(uploaded_file)
    prompt = EXTRACTION_PROMPT.replace("{pmid}", paper["pmid"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file, prompt]
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    print(raw)
    rows = json.loads(raw)
    all_rows.extend(rows)

# import to excel

df = pd.DataFrame(all_rows)
df.to_excel("part2_gemini/results.xlsx", index=False)
print(f"Exported {len(df)} rows to results.xlsx")