from google import genai
from google.genai import types
import httpx
import urllib
import bleach
import pandas as pd
import time

#Install certificate (if needed)
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

#Get paper metadata
papers = pd.read_csv('https://elicorpora.info/browse?mode=download&start=1&sort=dept&direction=asc')
papers.head()

#Add relevant metadata to lists
pids = papers['PAPER ID'].tolist()

#setup client
client = genai.Client(api_key="KEY")

for p in pids:
  print(p)
  doc_url = 'https://elicorpora.info/static/search/pdf/'+str(p)+'.pdf'

  # Retrieve and encode the PDF byte
  doc_data = httpx.get(doc_url).content

  prompt = "Can you give me feedback on this paper?"
  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(
          data=doc_data,
          mime_type='application/pdf',
        ),
        prompt])
  file=open("gemini_feedback/"+str(p)+".txt","w")
  file.write(response.text)
  file.close()
  time.sleep(5)