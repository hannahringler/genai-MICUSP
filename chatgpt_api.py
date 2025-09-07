from openai import OpenAI
import os
client = OpenAI(api_key="KEY")

os.chdir('MICUSP/pdfs')
for f in os.listdir():
    pdfname=str(f)+'.txt'
    file = client.files.create(
        file=open(f, "rb"),
        purpose="user_data"
    )

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file.id,
                    },
                    {
                        "type": "input_text",
                        "text": "Can you give me feedback on this paper?",
                    },
                ]
            }
        ]
    )
    with open("chatgpt_feedback/"+str(f)+".txt","w") as outputfile:
        outputfile.write(response.output_text)
    outputfile.close()