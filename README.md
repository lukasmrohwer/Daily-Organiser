# Daily-Organiser

This script takes a plain-text message like “tomorrow, one hour work from home…” and automatically creates scheduled events in your Google Calendar.

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/lukasmrohwer/Daily-Organiser; cd Daily-Organiser
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Enable the Google Calendar API:
- Visit: https://console.developers.google.com/
- Create a project and enable the **Google Calendar API**
- Download `credentials.json` and place it in the project folder.

4. Run the script:

```bash
python main.py
```

## Notes
- The first time you run the script, a browser window will open for Google authentication.
- A new calendar called “Automated Schedule” will be created if it doesn’t exist.

## Example Input
```python
message = "tomorrow, one hour work from home, one hour apply to internship, one hour study for java, tutoring 5-6:30"
```

This is parsed and converted into calendar events automatically.