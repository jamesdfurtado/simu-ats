# simu-ats

This is a work in progress!
- The app is in an MVP state at the moment. Many things need to be overhauled and functionalities need to be expanded upon
- The end goal is to create the SimuATS fully locally and free, without leveraging paid tools like OpenAI API.

SimuATS is an app that allows users to generate what a certain job's ATS acts like.
The user uploads a job description, where it will then extract hard skills, and assign each one with an importance level of 1-3.
The user can then upload their resume, and the "ATS" will provide a rating of 0-100 to see how highly they score.
It also can provide the user with a suggested revision of their resume.

Currently, the app is largely powered by OpenAI API, however I plan to entirely overhaul this system to have a local model do the heavy lifting. I am doing this to minimize costs and create my OWN tool-- not a GPT wrapper. :)

## Setup Instructions

1. Open up your terminal and clone the repository

```git clone https://github.com/jamesdfurtado/simu-ats.git```

2. Navigate into simu-ats file:

``` cd simu-ats```

3. Create a virtual environment:

```python -m venv env```

4. Activate the environment:

```env\Scripts\activate```


5. Install required packages:

```pip install -r requirements.txt```


6. Create a `.env` file:

for powershell (VScode uses this), ```New-Item -Path ".env" -ItemType "file"``` 

for most other terminals, ```touch .env``` 

7. Inside `.env`, add:
```OPENAI_API_KEY="your-openai-key-here"```
Replace your-openai-api-key-here with your own OpenAI API key.

8. Run the app:
```streamlit run app.py```
