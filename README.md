# GemDiary




**GemDiary** is a comprehensive digital diary web application designed to empower individuals by providing detailed descriptions of their daily images and generating rich audio summaries of their activities. Leveraging advanced AI technologies, GemDiary not only enhances personal journaling but also fosters a seamless and immersive interaction between users and their recorded experiences. A standout feature of GemDiary is its **podcast generation capability**, which transforms daily summaries into engaging audio narratives. This innovative podcast functionality allows users to effortlessly revisit and reflect on their day-to-day lives, offering a unique and accessible way to cherish memories and track personal growth over time.

---

### Key Highlights:

- **Digital Diary Functionality:** Users can upload images from their daily lives, which GemDiary intelligently describes to capture essential details and contexts.
  
- **AI-Driven Descriptions:** Utilizing Google Generative AI (Gemini), the application generates clear and concise descriptions of uploaded images, making it easier for users to document their experiences.
  
- **Audio Summaries:** Beyond text descriptions, GemDiary converts daily entries into audio summaries using advanced Text-to-Speech technologies, providing an alternative medium for users to engage with their diary.
  
- **Podcast Generation:** The **podcast feature** stands out by compiling daily audio summaries into cohesive podcast episodes. This allows users to listen to their personal diaries on the go, offering a dynamic and accessible way to reflect on their daily lives.
  
- **Secure Data Management:** Integration with Firebase Firestore and Google Cloud Storage ensures that all diary entries and audio files are securely stored and easily accessible.
  
- **User-Friendly Interface:** A responsive and intuitive frontend built with Tailwind CSS ensures a seamless user experience, making diary management effortless and enjoyable.



## Table of Contents

1. [Motivation](#motivation)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Technologies Used](#technologies-used)
5. [Setup and Installation](#setup-and-installation)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
   - [Backend Configuration](#backend-configuration)
   - [Frontend Configuration](#frontend-configuration)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
   - [POST /process_image/](#post-process_image)
   - [GET /daily_summary/](#get-daily_summary)
   - [GET /fetch_all_diaries/](#get-fetch_all_diaries)
8. [Code Snippets Explained](#code-snippets-explained)
   - [Image Description Generation](#image-description-generation)
   - [Text-to-Speech Conversion](#text-to-speech-conversion)
   - [Daily Summary and Podcast Generation](#daily-summary-and-podcast-generation)
9. [Configuration and API Enabling](#configuration-and-api-enabling)
   - [Google Cloud APIs](#google-cloud-apis)
   - [Firebase Setup](#firebase-setup)
10. [Deployment](#deployment)
11. [Contributing](#contributing)
12. [License](#license)
13. [Acknowledgements](#acknowledgements)

## Motivation

In today's fast-paced world, individuals often seek effective ways to document and reflect on their daily activities and experiences. Traditional journaling methods can be time-consuming and may lack the multimedia integration that modern users desire. GemDiary aims to revolutionize personal journaling by offering a seamless blend of image descriptions and audio summaries. By leveraging advanced AI technologies, GemDiary enhances the journaling experience, making it more interactive, accessible, and engaging. A standout feature of GemDiary is its podcast generation capability, which transforms daily summaries into dynamic audio narratives, allowing users to effortlessly revisit and reflect on their day-to-day lives in an innovative and personalized manner.
- **Enhancing Accessibility:** Providing detailed and accurate descriptions of images to assist visually impaired users in understanding their surroundings.
- **Promoting Independence:** Enabling users to interact with visual content without relying heavily on external assistance.
- **Facilitating Daily Reflections:** Allowing users to maintain a diary of their daily activities through audio summaries, fostering self-reflection and memory enhancement.

## Features

- **Image Upload and Description:**
  - Upload images and receive clear, concise descriptions.
  - Utilizes AI to focus on primary objects, people, text, actions, environment, and colors.

- **Text-to-Speech Conversion:**
  - Converts generated descriptions into audio files with varied voice types for a personalized experience.

- **Daily Diary Summaries:**
  - Aggregates daily image descriptions to create a positive diary entry.
  - Generates podcast-style audio summaries for easy listening.

- **Firestore Integration:**
  - Stores descriptions, audio URLs, and diary summaries for persistent data management.

- **Google Cloud Storage Integration:**
  - Manages storage of audio files with secure and scalable solutions.

- **Responsive Frontend:**
  - User-friendly interface built with Tailwind CSS.
  - Real-time feedback with loaders and image previews.

## Architecture

GemDiary follows a modular architecture, separating concerns between the frontend and backend:

- **Frontend:** 
  - Built with HTML, CSS (Tailwind), and JavaScript.
  - Handles user interactions, image uploads, and displays results.

- **Backend:**
  - Powered by FastAPI, serving RESTful APIs.
  - Integrates with Google Generative AI (Gemini) for image description.
  - Utilizes Google Cloud Storage and Firebase Firestore for data management.
  - Implements Text-to-Speech conversion using gTTS and pydub.



## Technologies Used

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/) - Web framework for building APIs.
  - [Google Generative AI (Gemini)](https://cloud.google.com/generative-ai) - For image description generation.
  - [gTTS](https://pypi.org/project/gTTS/) - Google Text-to-Speech for audio generation.
  - [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) - For Firestore and Storage management.
  - [Pillow](https://python-pillow.org/) - Image processing.
  - [pydub](https://github.com/jiaaro/pydub) - Audio manipulation.
  - [Google Cloud Storage](https://cloud.google.com/storage) - Cloud storage solution.
  - ![image](https://github.com/user-attachments/assets/7a2fe0d7-0fe4-42ff-96c0-067b507f0a56)


- **Frontend:**
  - [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework.
  - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - For interactivity.
  - [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML) - Markup language.
  - ![image](https://github.com/user-attachments/assets/7740e4db-d795-4750-8196-da3da963e183)



## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **Node.js and npm** (for frontend, if further development is required)
- **Google Cloud Account**
- **Firebase Project**
- **API Keys and Service Account Credentials**

### Clone the Repository

```bash
git clone https://github.com/yourusername/GemDiary.git
cd GemDiary
```

### Backend Configuration

1. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Setup:**

   - Obtain the Firebase Admin SDK JSON credentials from your Firebase project.
   - Place the `echosight-firebase-adminsdk-h0bdv-2738befc2a.json` file in the root directory.

4. **Google Cloud API Setup:**

   - Ensure the following APIs are enabled in your Google Cloud project:
     - **Generative AI API**
     - **Cloud Storage API**
   - Obtain the API key and update it in the `GOOGLE_API_KEY` variable in `main.py`.

5. **Environment Variables:**

   - Create a `.env` file (optional) to securely manage your API keys and credentials.

### Frontend Configuration

1. **Navigate to the Frontend Directory:**

   ```bash
   cd frontend
   ```

2. **Install Dependencies:**

   Since the frontend uses plain HTML, CSS, and JavaScript, additional dependencies may not be necessary. However, if you plan to extend functionalities using frameworks like React or Vue, set up accordingly.

## Running the Application

### Start the Backend Server

Ensure you are in the virtual environment and run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be accessible at `http://localhost:8000`.

### Access the Frontend

Open the `index.html` file located in the `frontend` directory in your preferred web browser.

## API Endpoints

### POST `/process_image/`

**Description:**  
Uploads an image, generates a description using Gemini AI, converts the description to speech, and stores the data in Firestore.

**Request:**

- **Method:** POST
- **URL:** `/process_image/`
- **Form Data:**
  - `file` (UploadFile): Image file to be processed.

**Response:**

- **Status 200:**
  ```json
  {
    "description": "A description of the image.",
    "audio_url": "https://storage.googleapis.com/your-bucket/audio_file.mp3"
  }
  ```
- **Status 400/500:**
  ```json
  {
    "detail": "Error message."
  }
  ```

### GET `/daily_summary/`

**Description:**  
Generates a daily summary of all image descriptions and creates a podcast-style audio summary.

**Request:**

- **Method:** GET
- **URL:** `/daily_summary/`

**Response:**

- **Status 200:**
  ```json
  {
    "summary": "Today's positive diary summary.",
    "podcast_url": "https://storage.googleapis.com/your-bucket/podcast_file.mp3"
  }
  ```
- **Status 400/500:**
  ```json
  {
    "detail": "Error message."
  }
  ```

### GET `/fetch_all_diaries/`

**Description:**  
Fetches all diary entries with pagination support.

**Request:**

- **Method:** GET
- **URL:** `/fetch_all_diaries/`
- **Query Parameters:**
  - `page` (int, default=1): Page number.
  - `page_size` (int, default=10): Number of diaries per page.

**Response:**

- **Status 200:**
  ```json
  {
    "total_diaries": 50,
    "page": 1,
    "page_size": 10,
    "diaries": [
      {
        "date": "2024-04-27",
        "summary": "Summary text.",
        "podcast_url": "https://storage.googleapis.com/your-bucket/podcast_file.mp3"
      },
      ...
    ]
  }
  ```
- **Status 400/500:**
  ```json
  {
    "detail": "Error message."
  }
  ```

## Code Snippets Explained

### Image Description Generation

The `describe_image` function leverages Google Generative AI (Gemini) to generate a description of the uploaded image.

```python
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
        response = model.generate_content([prompt, image])
        response.resolve()
        description = response.text.strip()
        return description
    except Exception as e:
        print(f"Error generating description: {e}")
        return "Sorry, I could not describe the scene."
```

**Explanation:**

- **Image Loading:** Utilizes Pillow to open and process the uploaded image.
- **Prompt Construction:** A detailed prompt guides the AI to generate a user-friendly description tailored for visually impaired users.
- **AI Interaction:** Sends the prompt and image to the Gemini model to receive a descriptive text.
- **Error Handling:** Ensures that any issues during the process are caught and an appropriate message is returned.

### Text-to-Speech Conversion

The `text_to_speech` function converts generated text descriptions into audio files using gTTS.

```python
def text_to_speech(text, voice_type="default"):
    try:
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
```

**Explanation:**

- **Voice Customization:** Alters the Top-Level Domain (TLD) to simulate different accents and voice types.
- **Audio File Management:** Saves the generated audio in the `audio` directory with a unique filename.
- **Error Handling:** Catches and logs any errors during the conversion process.

### Daily Summary and Podcast Generation

The `/daily_summary/` endpoint aggregates daily descriptions and generates a podcast-style summary.

```python
@app.get("/daily_summary/")
async def daily_summary():
    try:
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

            prompt_good = f"{good_person_persona}\nHere's the summary of the day: {diary_summary}\nPlease comment."
            good_response = model.generate_content(prompt_good).text.strip()

            prompt_normal = f"{normal_person_persona}\nThe good person said: {good_response}\nPlease respond as the normal person."
            normal_response = model.generate_content(prompt_normal).text.strip()

            prompt_good_2 = f"{good_person_persona}\nThe normal person said: {normal_response}\nReply as the good person again."
            good_response_2 = model.generate_content(prompt_good_2).text.strip()

            podcast_script = [
                f"Good Person: {good_response}",
                f"Normal Person: {normal_response}",
                f"Good Person: {good_response_2}"
            ]

            audio_files = []
            for line in podcast_script:
                if line.startswith("Good Person:"):
                    voice_type = "good_person"
                    text_to_say = line.replace("Good Person:", "").strip()
                else:
                    voice_type = "normal_person"
                    text_to_say = line.replace("Normal Person:", "").strip()

                audio_file = text_to_speech(text_to_say, voice_type=voice_type)
                if audio_file:
                    audio_files.append(audio_file)

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

            for f in audio_files:
                if os.path.exists(f):
                    os.remove(f)

            blob = bucket.blob(os.path.basename(podcast_file))
            blob.upload_from_filename(podcast_file)
            blob.make_public()
            podcast_url = blob.public_url

            diary_ref.update({'podcast_url': podcast_url, 'last_updated': datetime.utcnow()})

            if os.path.exists(podcast_file):
                os.remove(podcast_file)

            return JSONResponse(content={
                "summary": diary_summary,
                "podcast_url": podcast_url
            })
        else:
            return JSONResponse(content={"summary": "No entries found for today."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
```

**Explanation:**

- **Data Aggregation:** Retrieves all image descriptions for the current day from Firestore.
- **Summary Generation:** Uses Gemini AI to create a positive and concise diary entry based on the aggregated descriptions.
- **Persona-Based Conversation:** Simulates a conversation between two personas to create a dynamic podcast script.
- **Audio Generation:** Converts each line of the conversation into speech and combines them into a single podcast file.
- **Storage and Retrieval:** Uploads the podcast to Google Cloud Storage and updates Firestore with the podcast URL.
- **Error Handling:** Manages exceptions and ensures the system remains robust.

## Configuration and API Enabling

### Google Cloud APIs

To ensure GemDiary functions correctly, the following APIs must be enabled in your Google Cloud project:

1. **Generative AI API:**
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Go to **APIs & Services** > **Library**.
   - Search for **Generative AI** and enable it.

2. **Cloud Storage API:**
   - In the **APIs & Services** > **Library**, search for **Cloud Storage**.
   - Enable the **Cloud Storage API**.

3. **Service Account Creation:**
   - Navigate to **IAM & Admin** > **Service Accounts**.
   - Create a new service account with permissions for **Firestore** and **Cloud Storage**.
   - Download the JSON key file and place it in the root directory as `echosight-firebase-adminsdk-h0bdv-2738befc2a.json`.

### Firebase Setup

1. **Create a Firebase Project:**
   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Click on **Add project** and follow the prompts.

2. **Firestore Database:**
   - In your Firebase project, navigate to **Firestore Database**.
   - Create a new Firestore database in **Native Mode**.

3. **Storage Bucket:**
   - Navigate to **Storage** in the Firebase Console.
   - Set up a new storage bucket (e.g., `echosight.firebasestorage.app`).

4. **Firebase Admin SDK:**
   - Generate a new private key for your service account.
   - Download the JSON file and save it as `echosight-firebase-adminsdk-h0bdv-2738befc2a.json` in the project root.

5. **Firestore Rules:**
   - Ensure that your Firestore and Storage have appropriate security rules to protect user data.

## Deployment

For deploying GemDiary to production, consider the following steps:

1. **Backend Deployment:**
   - Use platforms like **Google App Engine**, **AWS EC2**, or **Heroku**.
   - Ensure environment variables and secrets are securely managed.
   - Set up HTTPS for secure communication.

2. **Frontend Deployment:**
   - Host the frontend on platforms like **Netlify**, **Vercel**, or **GitHub Pages**.
   - Configure CORS to allow requests from the frontend to the backend.

3. **Domain and SSL:**
   - Obtain a custom domain for your application.
   - Configure SSL certificates to secure data transmission.

4. **Continuous Integration/Continuous Deployment (CI/CD):**
   - Implement CI/CD pipelines using tools like **GitHub Actions**, **Travis CI**, or **Jenkins** to automate testing and deployment.

## Contributing

Contributions are welcome! Whether it's reporting bugs, suggesting features, or improving documentation, your input is valuable.

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

[MIT License](LICENSE)

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://cloud.google.com/generative-ai)
- [Firebase](https://firebase.google.com/)
- [gTTS](https://pypi.org/project/gTTS/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pydub](https://github.com/jiaaro/pydub)

---

*Made with ❤️ by the GemDiary Team*
