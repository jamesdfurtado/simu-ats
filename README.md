# simu-ats
SimuATS is an app that allows users to generate what a certain job's ATS acts like.
The user uploads a job description, where it will then extract hard skills, and assign each one with an importance level of 1-3.
The user can then upload their resume, and the "ATS" will provide a rating of 0-100 to see how highly they score.
It also can provide the user with a suggested revision of their resume.

## Setup Instructions

1. Open up your terminal and clone the repository

```git clone https://github.com/jamesdfurtado/simu-ats.git```

2. Navigate into simu-ats file:

``` cd simu-ats```

3. Create a virtual environment:

```python -m venv env```

4. Activate the environment:

```env\Scripts\activate```

5. Install PyTorch manually:

*IMPORTANT: This must be done before installed requirements.txt, or else app will not work.*

```pip install torch --index-url https://download.pytorch.org/whl/cu121```


6. Install required packages:

```pip install -r requirements.txt```


7. Create a `.env` file:

for powershell (VScode uses this), ```New-Item -Path ".env" -ItemType "file"``` 

for most other terminals, ```touch .env``` 

8. Inside `.env`, add:
```OPENAI_API_KEY="your-openai-key-here"```
Replace your-openai-api-key-here with your own OpenAI API key.

9. Run the app:
```streamlit run app.py```
