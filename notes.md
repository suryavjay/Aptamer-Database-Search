# Notes

I noticed when i built the pubmed search the 10 it chose to return were all 2026 publications. To fix this i decided to add a sort by relevance parameter which then showed papers ranging from 2009 - 2025. Things I had to fix were the fact that some parameters were differentiated by their ability to use either the find() function or the findall() function. This is because some things, like year and article title, needed only to be found once, whereas the abstract might have had multiple parts to it and required this difference to correctly capture the full abstract.

For the 3 papers, I decided to choose PMIDs 32777331, 19377993, and 25483931.

For PMID 19377993, it is an entire book, but the aptamer section is focused only on pages 209-22

For gemini extraction, I created a prompt I best believed would cover extracting the different fields as accurately as possible. I noticed that for paper 3 it extracted a 18-mer sequence instead of the actual 15-mer sequence shown in the paper. In my output excel sheet there is a false positive aptamer in row 33 as it reported a pool as an aptamer.

The extraction didn't correctly capture the underlines for PMID 25483931 which would show differences in the resulting excel sheet for different "alph anomers" (not exactly sure what they are). 

for PMID 32777331, it says for TBA HD1 Kd is 1.4nM which is seemingly hallucinated as the paper says TBA. Additionally, NU172 is also seemingly hallucinating the Kd, as i was not able to physically find it in the paper.

Bullets of what Gemini did incorrectly:

- Lost alpha-anomer position information from PMID-25483931 due to underline formatting
- Read the entire textbook for PMID-19377993 instead of just the target chapter, producing 26 rows of mostly         irrelevant aptamers
- Hallucinated Kd values for TBA (1.4 nM) and NU172 (0.38 nM)
- Misattributed the TBA row to PMID-19377993 instead of PMID-25483931

Things to improve:

For one of the PDFs, the PMID referred to a specific chapter in an entire textbook but gemini read the entire book instead of the chapter, so feed only the chapter. Improve the prompt that blocks value inferencing, as the prompt I had used clearly did not work to the best ability.

Using the field Kd seems to be too broad and allows values that are not Kds into the column.