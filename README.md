# Aptamer Database Search

A lab research project exploring automated extraction of aptamer data from scientific literature using PubMed's API and Google Gemini AI.

## Overview

This project investigates whether large language models can reliably extract structured aptamer data — sequences, targets, binding affinities, and pool types — from published research papers. It consists of four parts, progressing from automated literature retrieval to AI-assisted extraction and manual validation.

## Project Structure

```
aptamer-test/
├── part1_pubmed/
│   └── script.py          # PubMed API search and data retrieval
├── part2_gemini/
│   ├── extract.py         # Gemini-based aptamer extraction from PDFs
│   └── results.xlsx       # Extracted aptamer data (56 rows across 3 papers)
├── notes.md               # Project notes and observations
├── pubmed_apta...xlsx     # PubMed search results
└── .env                   # API keys (not tracked)
```

## Parts

### Part 1 — PubMed Retrieval ✓
Queries PubMed for thrombin-targeting aptamer papers using the NCBI Entrez API. Retrieves the top 10 results by relevance, extracts titles, abstracts, PMIDs, and publication years, and exports to Excel.

**Query used:**
```
(aptamer[Title/Abstract] OR aptamers[Title/Abstract]) AND thrombin[Title/Abstract] AND ("1990"[Date - Publication] : "2026"[Date - Publication])
```

### Part 2 — Gemini Extraction ✓
Feeds three PDFs into Gemini 2.5 Flash via the File API and extracts structured aptamer data using a prompted extraction pipeline. Outputs a clean JSON-structured Excel file with one row per aptamer.

**Papers used:**
- PMID-25483931 — Kolganova et al. 2014, *Anomeric DNA quadruplexes: Modified thrombin aptamers*
- PMID-32777331 — Riccardi et al. 2021, *G-quadruplex-based aptamers targeting human thrombin*
- PMID-19377993 — Gronewold 2009, *Aptamers and Biosensors* (chapter in Methods in Molecular Biology vol. 535)

**Fields extracted:** `paper_id`, `aptamer_name`, `target`, `sequence`, `pool_type`, `kd`

### Part 3 — Manual Validation ✓
Manual reading of all three papers to extract the same fields, followed by a systematic comparison against Gemini's output.

**Key findings:**
- Gemini lost alpha-anomer position data from PMID-25483931 due to underline formatting not surviving PDF parsing
- Gemini read the entire 406-page textbook for PMID-19377993 instead of the target chapter, producing 26 rows of mostly irrelevant aptamers
- Gemini hallucinated Kd values for TBA (1.4 nM) and NU172 (0.38 nM) despite a hallucination safeguard
- The `kd` field conflated true Kd, IC50, and EC50 values with no distinction

**How to improve:**
- Crop PDFs to relevant pages before input
- Strengthen safeguard to block implicit calculation from relative comparisons
- Split `kd` into `binding_metric` and `binding_value` fields
- Add a `modifications` field for chemically modified aptamers
- Define ambiguous field names explicitly in the prompt

### Part 4 — Not Started

## Setup

### Requirements
- Python 3.9+
- Dependencies: `python-dotenv`, `requests`, `pandas`, `openpyxl`, `google-genai`

```bash
pip install python-dotenv requests pandas openpyxl google-genai
```

### Environment Variables
Create a `.env` file in the project root:
```
NCBI_API_KEY=your_ncbi_api_key
NCBI_EMAIL=your_email
GEMINI_API_KEY=your_gemini_api_key
```

### Running Part 1
```bash
cd part1_pubmed
python3 script.py
```

### Running Part 2
Add PDFs to `part2_gemini/pdfs/` then:
```bash
cd part2_gemini
python3 extract.py
```

## Notes
- Gemini free tier: `gemini-2.5-flash` works; `gemini-2.0-flash` and `gemini-2.0-flash-lite` have zero quota on free tier
- PubMed API requires registration for an API key at https://www.ncbi.nlm.nih.gov/account/
