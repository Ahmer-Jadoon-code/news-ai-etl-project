import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Root folder se .env load karna taake API key mil sake
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env'))

# Gemini AI ko configure karna
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def enrich_silver_data(silver_data):
    """Silver data ko AI se parhwaya jata hai taake Sentiment aur Summary mil sake."""
    
    if not silver_data:
        print("No silver data to enrich.")
        return []

    enriched_data = []
    print(f"Total {len(silver_data)} news articles AI processing ke liye aayi hain...")

    for i, item in enumerate(silver_data):
        print(f"AI Processing {i+1}/{len(silver_data)}: {item['title'][:40]}...")
        
        # AI ko instruction dena
        prompt = f"""
        Neeche di gayi news ko parhein:
        Title: {item['title']}
        Summary: {item['summary']}
        
        Sirf 2 cheezein batayen:
        1. Sentiment (Positive, Negative, ya Neutral)
        2. Ek choti summary (Sirf 1 line mein)
        
        Jawab hamesha is format mein dein: Sentiment | Summary
        """
        
        try:
            response = model.generate_content(prompt)
            result = response.text.split('|')
            
            # AI ke jawab ko alag alag karna
            sentiment = result[0].strip() if len(result) > 0 else "Neutral"
            ai_summary = result[1].strip() if len(result) > 1 else "No AI Summary"
            
        except Exception as e:
            print(f"❌ AI Error: {e}")
            sentiment = "Error"
            ai_summary = "Error"
            
        # Purane data mein naya AI ka data shamil karna
        enriched_item = item.copy()
        enriched_item['sentiment'] = sentiment
        enriched_item['ai_summary'] = ai_summary
        
        enriched_data.append(enriched_item)
        
        # API ki speed limit se bachne ke liye 2 second ka gap
        time.sleep(2)
        
    print("✅ Gold Layer AI Processing Complete!")
    return enriched_data