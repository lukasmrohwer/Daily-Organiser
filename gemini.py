import os
import google.generativeai as genai
import json
from datetime import datetime

def get_schedule(message):

  # load api key from environment
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  # hard code api key
  # genai.configure(api_key="your-api-key-here")

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
  )

  date = datetime.today().strftime('%Y-%m-%d')

  chat_session = model.start_chat(
    history=[
        {
          "role": "user",
          "parts": [{ "text": 
            f"""
            You are an AI model created in order to help your user plan their day. They will come to you with a list of tasks that they need to complete throughout the day including any necessary timestamps, and you will need to provide them a plan for their day. The schedule should be designed in a way to encourage productivity by promoting a healthy workflow and appropriate breaks. 

            If they do not specify sleep times and/or meal times, schedule them in where most appropriate.
            If they don't have many tasks to complete that day, spread them out in a way to avoid physical and mental exhaustion.

            You should assume that your user is planning for today's date ({date}). They might instead say that they are planning for tomorrow, in which case you should assume that they are planning for the next day's date. 

            Your response must be formatted only in JSON. You will give your recommended schedule as a list of events (meaning the entire response is inside a []). There should not be any gaps between events, each minute should be account for. Each event should be formatted as the following:
            {{
            'summary': '[appropriate name for the task]',
            'location': '[appropriate location for the task]',
            'description': '[appropriate description for the task',
            'colorId': '[value based on criteria below e.g. 1]',
            'start': {{
              'dateTime': yyyy-mm-ddThh:mm:00+08:00,
              timeZone': 'Australia/Perth',
            }},
            'end': {{
              dateTime': yyyy-mm-ddThh:mm:00+08:00,
              'timeZone': 'Australia/Perth',
            }},
            }}
            Colour Criteria:
            1 - Events related to travelling between places e.g. transit to uni.
            2 - Everything related to uni work e.g. uni, study, lecture.
            3 - Events related to routine e.g. lunch, getting ready.
            4 - Events related to fun activities e.g. birthday party, surfing.
            6 - Miscellaneous events.
            7 - Events related to work e.g. tutoring, work from home.
            9 - Sleeping events.
            """
            }],
        },
        {
          "role": "model",
          "parts": [{ "text": "Understood."}],
        }
    ]
  )

  response = chat_session.send_message(message)

  schedule_data = json.loads(response.text.replace('```json', '').replace('```', '').strip())
  
  return schedule_data


if __name__ == '__main__':
    get_schedule()