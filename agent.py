import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_KEY"))


def plan_trip(destination,day,preferences):
    """
    Generate a detailed AI-powered day-by-day trip plan.
    
    Parameters:
        destination (str): City or country to visit.
        days (int): Number of days for the trip.
        preferences (str): User preferences (food, adventure, museums, etc.)
    
    Returns:
        str: Formatted trip itinerary with recommendations.
    """
    
    prompt = f"""
    I am planning a {day}-day trip to {destination}.
    my preferance : {preferences if preferences else 'no specific prefrences'}.
    
    
    please create a detailed and create day-by-day itinerary including:
    - Morning ,afternoon, and evening activities
    - recommended  restaurant OR local foods
    - travel tips , local transportation suggestions 
    - optional hidden games and unique experiences
    - Estimate budget if possible
    - give chepest current flight and train name and sources of link for booking that tickets 
    
    Format th eoutput clearly using heading and bullet points

    """

    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text

    
if __name__ == "__main__":
    print("--Wellcom to AI Trip planner")
    dest = input("Enter the Destination : ")
    day = int(input("Enter the numbers of days : "))
    prefs = input("Enter your preference (food, adventure ,culture) : ")
    
    print("\n Generating Your AI powered Trip plan...\n")
    trip_plan = plan_trip(dest,day,prefs)
    
    print("\n -- Your Detailed AI Trip Plan")
    print(trip_plan)    
    