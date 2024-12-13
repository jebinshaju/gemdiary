from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import io
import google.generativeai as genai
from gtts import gTTS
import uuid
import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from pydub import AudioSegment
from google.cloud import storage
from fastapi.middleware.cors import CORSMiddleware



cred = credentials.Certificate("echosight-firebase-adminsdk-h0bdv-2738befc2a.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

GOOGLE_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# GOOGLE_API_KEY = "XXXXXXXXXXXX"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
# model = genai.GenerativeModel('gemini-2.0-flash-exp')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
# Initialize the Google Cloud Storage client using the same service account
storage_client = storage.Client.from_service_account_json("XXXXXXXXXXXXXXXXX.json")
bucket_name = "echosight.firebasestorage.app"  # Replace with your actual Firebase Storage bucket name
bucket = storage_client.bucket(bucket_name)

def describe_image(image_content):
    try:
        image = Image.open(io.BytesIO(image_content))

        prompt = """
        You are a helpful assistant for a blind person, and you are assisting them to see through a camera.
        You will be provided with an image. Your task is to describe this image with clear and concise natural language. 
        Focus on the most relevant objects, people, and any significant details that might be of interest to someone who cannot see the image. 
        Avoid technical or overly complex vocabulary.

        Keep the description short and simple. 
        Prioritize information about:
        - Primary objects present
        - People, if any (describe their general appearance)
        - Text, if any (read the text if it's legible)
        - Action, if any (what is happening?)
        - Environment (indoor, outdoor, nature, urban?)
        - Important colors

        If the scene is not clear, state that it's unclear and you can't interpret. also dont start the response with "the image"
        """

        # Pass the image and the prompt to the Gemini API
        response = model.generate_content([prompt, image])
        response.resolve()

        description = response.text.strip()
        return description
    except Exception as e:
        print(f"Error generating description: {e}")
        return "Sorry, I could not describe the scene."

def text_to_speech(text, voice_type="default"):
    try:
        # Choose different TLDs for simulated voice differences
        if voice_type == "good_person":
            tld = "co.uk"   # Attempt female/British accent
        elif voice_type == "normal_person":
            tld = "com.au"  # Attempt male/Australian accent
        else:
            tld = "com"

        audio_file = f"audio/audio_{uuid.uuid4()}.mp3"
        os.makedirs("audio", exist_ok=True)
        tts = gTTS(text=text, lang='en', tld=tld, slow=False)
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"Error converting to speech: {e}")
        return None

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        if not image_data:
            return JSONResponse(content={"description": "No image content provided."})
        
        description = describe_image(image_data)
        if description:
            audio_file = text_to_speech(description)
            if audio_file:
                # Upload the audio file to Firebase Storage
                blob = bucket.blob(os.path.basename(audio_file))
                blob.upload_from_filename(audio_file)
                blob.make_public()
                audio_url = blob.public_url

                # Save the description and audio URL to Firestore
                description_ref = db.collection('image_descriptions').document(str(uuid.uuid4()))
                description_ref.set({
                    'description': description,
                    'audio_url': audio_url,
                    'timestamp': datetime.utcnow()
                })

                # Remove local audio file
                if os.path.exists(audio_file):
                    os.remove(audio_file)

                return JSONResponse(content={
                    "description": description,
                    "audio_url": audio_url
                })
            else:
                raise HTTPException(status_code=500, detail="Failed to generate audio.")
        else:
            return JSONResponse(content={"description": "Failed to generate description."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# @app.get("/audio/{file_name}")
# async def get_audio(file_name: str):
#     file_path = os.path.join("audio", file_name)
#     try:
#         return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Audio file not found.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
#     finally:
#         # Optionally remove the file after serving
#         if os.path.exists(file_path):
#             os.remove(file_path)

@app.get("/daily_summary/")
async def daily_summary():
    try:
        # Define the current day range
        today = datetime.utcnow().date()
        start_of_day = datetime(today.year, today.month, today.day)
        end_of_day = start_of_day + timedelta(days=1)

        entries = db.collection('image_descriptions').where(
    field_path='timestamp', op_string='>=', value=start_of_day
).where(
    field_path='timestamp', op_string='<', value=end_of_day
).stream()

        descriptions = []
        for entry in entries:
            data = entry.to_dict()
            description = data['description']
            timestamp = data['timestamp']

            time_of_day = "in the morning" if 5 <= timestamp.hour < 12 else \
                          "in the afternoon" if 12 <= timestamp.hour < 17 else \
                          "in the evening" if 17 <= timestamp.hour < 21 else \
                          "at night"

            descriptions.append(f"{description.capitalize()} {time_of_day}.")

        if descriptions:
            combined_text = " ".join(descriptions)
            prompt = f"""
            Write a positive diary entry summarizing the following events that happened today in a concise and cheerful tone:
            {combined_text}
            """
            response = model.generate_content(prompt)
            response.resolve()
            diary_summary = response.text.strip()

            today_datetime = datetime(today.year, today.month, today.day)
            diary_ref = db.collection('daily_diaries').document(today.isoformat())
            diary_ref.set({
                'date': today_datetime,
                'summary': diary_summary,
                'last_updated': datetime.utcnow()
            }, merge=True)

            # Persona-based conversation
            good_person_persona = "You are a helpful, optimistic, and caring person."
            normal_person_persona = "You are neutral and slightly curious."

            # Good Person speaks first
            prompt_good = f"{good_person_persona}\nHere's the summary of the day: {diary_summary}\nPlease comment."
            good_response = model.generate_content(prompt_good).text.strip()

            # Normal Person responds
            prompt_normal = f"{normal_person_persona}\nThe good person said: {good_response}\nPlease respond as the normal person."
            normal_response = model.generate_content(prompt_normal).text.strip()

            # Good Person responds again
            prompt_good_2 = f"{good_person_persona}\nThe normal person said: {normal_response}\nReply as the good person again."
            good_response_2 = model.generate_content(prompt_good_2).text.strip()

            # Create the podcast script
            podcast_script = [
                f"Good Person: {good_response}",
                f"Normal Person: {normal_response}",
                f"Good Person: {good_response_2}"
            ]

            # Convert the conversation to speech
            audio_files = []
            for line in podcast_script:
                # Determine the voice type
                if line.startswith("Good Person:"):
                    voice_type = "good_person"
                    # Remove the "Good Person:" prefix from the text
                    text_to_say = line.replace("Good Person:", "").strip()
                else:
                    voice_type = "normal_person"
                    # Remove the "Normal Person:" prefix from the text
                    text_to_say = line.replace("Normal Person:", "").strip()

                audio_file = text_to_speech(text_to_say, voice_type=voice_type)
                if audio_file:
                    audio_files.append(audio_file)

            # Combine all audio segments into one podcast file
            combined = None
            for f in audio_files:
                segment = AudioSegment.from_mp3(f)
                if combined is None:
                    combined = segment
                else:
                    combined += segment

            podcast_file = f"audio/podcast_{uuid.uuid4()}.mp3"
            if combined:
                combined.export(podcast_file, format="mp3")

            # Clean up individual line files
            for f in audio_files:
                if os.path.exists(f):
                    os.remove(f)

            # Upload the podcast file to Firebase Storage
            blob = bucket.blob(os.path.basename(podcast_file))
            blob.upload_from_filename(podcast_file)
            # Make the file publicly accessible, or manage via security rules
            blob.make_public()
            podcast_url = blob.public_url

            # Update Firestore with podcast_url
            diary_ref.update({'podcast_url': podcast_url, 'last_updated': datetime.utcnow()})

            # Remove local podcast file after upload
            if os.path.exists(podcast_file):
                os.remove(podcast_file)

            # Return the summary and the public podcast URL from Firebase Storage
            return JSONResponse(content={
                "summary": diary_summary,
                "podcast_url": podcast_url
            })
        else:
            return JSONResponse(content={"summary": "No entries found for today."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
@app.get("/fetch_all_diaries/")
async def fetch_all_diaries(page: int = Query(default=1, ge=1, description="Page number"),
                            page_size: int = Query(default=10, ge=1, le=100, description="Number of diaries per page")):
    """
    Fetch all diary entries with pagination.
    """
    try:
        diaries_ref = db.collection('daily_diaries').order_by('date', direction=firestore.Query.DESCENDING)
        
        # Firestore does not support offset efficiently. Using cursor-based pagination.
        # To implement cursor-based pagination, you need to keep track of the last document from the previous page.
        # For simplicity, we'll use a basic approach here.

        # Calculate the number of documents to skip
        skip = (page - 1) * page_size

        # Since Firestore's Python client doesn't support offset, we fetch all diaries and slice them.
        # Note: This is not efficient for large datasets.
        all_diaries = list(diaries_ref.stream())
        total_diaries = len(all_diaries)

        # Slice the list for pagination
        paginated_diaries = all_diaries[skip:skip + page_size]

        diary_list = []
        for diary in paginated_diaries:
            data = diary.to_dict()
            diary_list.append({
                'date': data['date'].strftime("%Y-%m-%d"),
                'summary': data['summary'],
                'podcast_url': data.get('podcast_url', '')
            })

        return JSONResponse(content={
            "total_diaries": total_diaries,
            "page": page,
            "page_size": page_size,
            "diaries": diary_list
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
