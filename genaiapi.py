# pip install google-genai
# pip install python-dotenv
from google import genai
#api_key="AIzaSyAcUCZCCU-5mVy_qZyHeq4yzw6_qPZuuAE"
client = genai.Client(api_key="AIzaSyDqLwpoJgo0FDsjuSplwJvMuYJV4l5r7C8")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Tell me a story in 100 words.'
)
print(response.text)