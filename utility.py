from google import genai

api_key="AQ.Ab8RN6JuwI_OjKIwuKRbbPl1V05X3SB18NhQdDUQpmclZ4Qj2w"

#step1: authenticate

client=genai.Client(api_key=api_key)


prompt="what is ai agent in simple words"

response=client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)