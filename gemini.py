from google import genai

# client = genai.Client(api_key="YOUR_API_KEY")

print("Client initialized successfully.")
response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)