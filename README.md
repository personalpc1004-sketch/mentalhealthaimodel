# Mental Health AI Model API

A Flask-based REST API for experimental PHQ-9 severity classification using an XGBoost model. The API accepts the nine PHQ-9 responses together with the response time for each question and returns a predicted severity category, confidence, and class probabilities.

> **Important:** This model is an experimental screening/classification component. It is **not an autonomous medical diagnostic system** and should not be used as a substitute for assessment by a qualified mental-health professional.

---

# 🚀 API Integration — Start Here

## Base URL

```text
https://mentalhealthaimodel.onrender.com/
```

You can integrate the API from any frontend, mobile app, backend service, Postman, or other HTTP client.

### Available endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API health/status check |
| `GET` | `/test` | Browser-based PHQ-9 model testing page |
| `POST` | `/predict` | Submit PHQ-9 responses and response times for prediction |

---

## 1. Check API Status

### Request

```http
GET https://mentalhealthaimodel.onrender.com/
```

### Example response

```json
{
  "status": "success",
  "message": "Mental Health AI API is running",
  "model": "XGBoost",
  "model_version": "v1"
}
```

Use this endpoint as a health check. It is also the recommended endpoint for uptime monitoring because it does not perform model inference.

---

# 2. Prediction API

## Endpoint

```http
POST https://mentalhealthaimodel.onrender.com/predict
```

### Headers

```http
Content-Type: application/json
```

### Request body

The API requires exactly these 18 input fields:

- `question1` through `question9`
- `time1` through `time9`

### Question response values

Each PHQ-9 question uses the following numeric mapping:

| Value | Response |
|---:|---|
| `0` | Not at all |
| `1` | Several days |
| `2` | More than half the days |
| `3` | Nearly every day |

### Response time fields

`time1` through `time9` represent the number of seconds the user took to answer the corresponding question.

For example:

```text
question1 -> time1
question2 -> time2
...
question9 -> time9
```

The response times are used as behavioral features by the model.

---

## Example Request

```json
{
  "question1": 1,
  "question2": 1,
  "question3": 1,
  "question4": 0,
  "question5": 1,
  "question6": 0,
  "question7": 1,
  "question8": 0,
  "question9": 0,

  "time1": 8.5,
  "time2": 10.2,
  "time3": 7.8,
  "time4": 6.4,
  "time5": 9.1,
  "time6": 5.8,
  "time7": 8.2,
  "time8": 6.7,
  "time9": 7.5
}
```

## Example cURL

```bash
curl -X POST "https://mentalhealthaimodel.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "question1": 1,
    "question2": 1,
    "question3": 1,
    "question4": 0,
    "question5": 1,
    "question6": 0,
    "question7": 1,
    "question8": 0,
    "question9": 0,
    "time1": 8.5,
    "time2": 10.2,
    "time3": 7.8,
    "time4": 6.4,
    "time5": 9.1,
    "time6": 5.8,
    "time7": 8.2,
    "time8": 6.7,
    "time9": 7.5
  }'
```

---

# 3. Example JavaScript / React / Next.js Integration

```javascript
const API_URL = "https://mentalhealthaimodel.onrender.com";

const assessmentData = {
  question1: 1,
  question2: 1,
  question3: 1,
  question4: 0,
  question5: 1,
  question6: 0,
  question7: 1,
  question8: 0,
  question9: 0,

  time1: 8.5,
  time2: 10.2,
  time3: 7.8,
  time4: 6.4,
  time5: 9.1,
  time6: 5.8,
  time7: 8.2,
  time8: 6.7,
  time9: 7.5
};

const response = await fetch(`${API_URL}/predict`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(assessmentData)
});

const result = await response.json();

console.log(result);
```

---

# 4. Flutter Integration

The API can be consumed from Flutter using `http` or `dio`.

## Using `http`

Add the package to `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.0.0
```

Example:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> predictMentalHealth() async {
  const apiUrl =
      'https://mentalhealthaimodel.onrender.com/predict';

  final body = {
    'question1': 1,
    'question2': 1,
    'question3': 1,
    'question4': 0,
    'question5': 1,
    'question6': 0,
    'question7': 1,
    'question8': 0,
    'question9': 0,

    'time1': 8.5,
    'time2': 10.2,
    'time3': 7.8,
    'time4': 6.4,
    'time5': 9.1,
    'time6': 5.8,
    'time7': 8.2,
    'time8': 6.7,
    'time9': 7.5,
  };

  final response = await http.post(
    Uri.parse(apiUrl),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode(body),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);

    print(data['data']['predicted_severity']);
    print(data['data']['confidence']);
    print(data['data']['probabilities']);
  } else {
    print('API Error: ${response.body}');
  }
}
```

---

# 5. Prediction Response

A successful prediction returns:

```json
{
  "status": "success",
  "data": {
    "model_version": "v1",
    "predicted_severity": "Mild",
    "confidence": 0.7993830442428589,
    "probabilities": {
      "Mild": 0.7993830442428589,
      "Minimal": 0.1982,
      "Moderate": 0.0022,
      "Moderately Severe": 0.0001,
      "Severe": 0.0001
    }
  }
}
```

The exact probability values depend on the submitted answers and response times.

## Response fields

| Field | Type | Description |
|---|---|---|
| `status` | string | `success` when prediction succeeds |
| `data.model_version` | string | Model version used for prediction |
| `data.predicted_severity` | string | Predicted PHQ-9 severity category |
| `data.confidence` | number | Highest predicted class probability |
| `data.probabilities` | object | Probability for each severity class |

---

# 6. Severity Categories

The current model uses these PHQ-9 severity categories:

| PHQ-9 Score | Category |
|---:|---|
| `0–4` | Minimal |
| `5–9` | Mild |
| `10–14` | Moderate |
| `15–19` | Moderately Severe |
| `20–27` | Severe |

The API returns the category name rather than the raw PHQ-9 score.

---

# 7. Error Responses

## Missing request body

### Response

```json
{
  "status": "error",
  "message": "Request body is required"
}
```

HTTP status:

```text
400 Bad Request
```

## Missing required fields

For example, if `question5` is missing:

```json
{
  "status": "error",
  "message": "Missing required fields: ['question5']"
}
```

HTTP status:

```text
400 Bad Request
```

## Server/internal error

```json
{
  "status": "error",
  "message": "Internal server error"
}
```

HTTP status:

```text
500 Internal Server Error
```

---

# 8. PHQ-9 Questions

The API expects nine responses corresponding to these questions:

1. Little interest or pleasure in doing things
2. Feeling down, depressed, or hopeless
3. Trouble falling or staying asleep, or sleeping too much
4. Feeling tired or having little energy
5. Poor appetite or overeating
6. Feeling bad about yourself — or that you are a failure or have let yourself or your family down
7. Trouble concentrating on things, such as reading the newspaper or watching television
8. Moving or speaking so slowly that other people could have noticed, or the opposite — being so fidgety or restless that you have been moving around a lot more than usual
9. Thoughts that you would be better off dead or of hurting yourself in some way

Each question is answered using:

```text
0 = Not at all
1 = Several days
2 = More than half the days
3 = Nearly every day
```

For production use, the wording and administration of a validated questionnaire should be handled carefully and consistently.

---

# 9. Project Overview

## Project Name

**Mental Health AI Model API**

## Purpose

This project provides an HTTP API around an XGBoost-based experimental model that classifies PHQ-9 assessment responses into severity categories.

The model combines:

1. PHQ-9 question responses
2. Per-question response times
3. Derived behavioral timing features

The API is designed so that a frontend, mobile application, or another backend can submit an assessment and receive a structured prediction response.

---

# 10. Technology Stack

### Backend

- Python
- Flask
- Flask-CORS
- Gunicorn

### Machine Learning

- XGBoost
- scikit-learn
- NumPy
- Pandas
- Joblib

### Model

- XGBoost classifier
- Model version: `v1`
- 36 input features

### Deployment

- Render Web Service
- Gunicorn production server

---

# 11. Project Folder Structure

```text
mental-health-ai-api/
│
├── app.py
├── requirements.txt
├── .python-version
├── .gitignore
├── README.md
│
├── model/
│   ├── xgboost_model.json
│   ├── label_encoder.pkl
│   └── metadata.json
│
├── services/
│   ├── __init__.py
│   └── prediction_service.py
│
├── utils/
│   ├── __init__.py
│   └── feature_engineering.py
│
└── templates/
    └── test.html
```

---

# 12. File-by-File Explanation

## `app.py`

Main Flask application.

Responsibilities:

- Creates the Flask application
- Enables CORS
- Defines API routes
- Receives JSON prediction requests
- Calls the prediction service
- Returns JSON responses
- Provides the health endpoint
- Serves the browser testing page

Main routes:

```text
GET  /
GET  /test
POST /predict
```

---

## `requirements.txt`

Contains Python dependencies required to run the application.

Current dependencies:

```txt
Flask==3.1.2
flask-cors==6.0.1
xgboost==3.0.5
scikit-learn==1.7.1
joblib==1.5.1
numpy==2.3.2
pandas==2.3.2
gunicorn==23.0.0
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## `.python-version`

Specifies the Python version used by the deployment environment.

Current value:

```text
3.13
```

Python 3.13 is used to provide compatible pre-built wheels for the ML dependencies.

---

# 13. Model Files

## `model/xgboost_model.json`

Contains the trained XGBoost model.

The API loads this file during application startup.

---

## `model/label_encoder.pkl`

Contains the scikit-learn label encoder used during training.

It converts between the encoded model classes and their human-readable severity names.

---

## `model/metadata.json`

Contains model metadata such as:

- Model version
- Model type
- Feature count
- Target classes
- Model parameters
- Validation metrics
- Test metrics
- Calibration information
- Model purpose

The API uses the metadata to expose the model version in the prediction response.

---

# 14. `services/` Directory

## `services/prediction_service.py`

Contains the prediction logic.

Responsibilities:

1. Load the XGBoost model.
2. Load the label encoder.
3. Load model metadata.
4. Generate the 36 model features.
5. Run XGBoost prediction.
6. Generate class probabilities.
7. Convert encoded prediction into a severity label.
8. Return structured prediction data.

The main public function is:

```python
predict(data)
```

---

# 15. `utils/` Directory

## `utils/feature_engineering.py`

Responsible for converting the API request into the 36 features expected by the trained model.

### Question features

9 features:

```text
question1
question2
question3
question4
question5
question6
question7
question8
question9
```

### Raw timing features

9 features:

```text
time1
time2
time3
time4
time5
time6
time7
time8
time9
```

### Statistical timing features

```text
time_mean
time_median
time_std
time_min
time_max
time_range
time_total
fast_response_count
slow_response_count
```

### Log-transformed timing features

```text
log_time1
log_time2
log_time3
log_time4
log_time5
log_time6
log_time7
log_time8
log_time9
```

Total:

```text
9 question features
+ 9 raw timing features
+ 9 statistical/behavioral features
+ 9 log timing features
= 36 features
```

---

# 16. `templates/test.html`

Browser-based testing interface for the model.

The page provides:

- One PHQ-9 question at a time
- Actual question text
- Four answer choices
- `OK` button to continue
- Automatic response-time measurement
- Progress indicator
- Final prediction request
- Predicted severity
- Confidence
- Class probabilities
- Restart functionality
- Experimental-model disclaimer

The page communicates with:

```text
POST /predict
```

When deployed, it can be opened at:

```text
https://mentalhealthaimodel.onrender.com/test
```

---

# 17. How Response Time Is Calculated

The browser test page records the time from when a question is displayed until the user selects/continues with an answer.

For example:

```text
Question 1 shown
        ↓
User reads question
        ↓
User selects answer
        ↓
Elapsed time = time1
```

This process is repeated for all nine questions.

The API does not calculate the user's reading/answer time itself. The client application must send the `time1`–`time9` values.

For another frontend or mobile app, implement the same timing concept before calling `/predict`.

---

# 18. Complete API Contract

## Base URL

```text
https://mentalhealthaimodel.onrender.com
```

## Health Check

```http
GET /
```

## Web Test Page

```http
GET /test
```

## Prediction

```http
POST /predict
Content-Type: application/json
```

### Required request schema

```json
{
  "question1": 0,
  "question2": 0,
  "question3": 0,
  "question4": 0,
  "question5": 0,
  "question6": 0,
  "question7": 0,
  "question8": 0,
  "question9": 0,

  "time1": 0.0,
  "time2": 0.0,
  "time3": 0.0,
  "time4": 0.0,
  "time5": 0.0,
  "time6": 0.0,
  "time7": 0.0,
  "time8": 0.0,
  "time9": 0.0
}
```

### Successful response schema

```json
{
  "status": "success",
  "data": {
    "model_version": "v1",
    "predicted_severity": "Mild",
    "confidence": 0.7993830442428589,
    "probabilities": {
      "Mild": 0.7993830442428589,
      "Minimal": 0.1982,
      "Moderate": 0.0022,
      "Moderately Severe": 0.0001,
      "Severe": 0.0001
    }
  }
}
```

---

# 19. Integration Flow

A typical frontend integration should follow this flow:

```text
User opens assessment
        ↓
Question 1
        ↓
Record response + response time
        ↓
Question 2
        ↓
Record response + response time
        ↓
...
        ↓
Question 9
        ↓
Record response + response time
        ↓
Build JSON request
        ↓
POST /predict
        ↓
Flask API
        ↓
Feature Engineering
        ↓
XGBoost Model
        ↓
Prediction + Probabilities
        ↓
JSON Response
        ↓
Frontend displays result
```

---

# 20. Example Integration Architecture

```text
┌─────────────────────────────┐
│       Frontend / App        │
│                             │
│  React / Next.js / Flutter  │
└──────────────┬──────────────┘
               │
               │ POST /predict
               │ JSON
               ▼
┌─────────────────────────────┐
│       Flask REST API        │
│                             │
│   mentalhealthaimodel...    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Feature Engineering     │
│                             │
│  18 input values → 36       │
│  model features             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      XGBoost Model v1       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Prediction           │
│                             │
│ Severity + Confidence +     │
│ Class Probabilities         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Frontend           │
│       Result Screen         │
└─────────────────────────────┘
```

---

# 21. Running the Project Locally

## Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd mental-health-ai-api
```

## Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start Flask

```bash
python app.py
```

The application will normally run at:

```text
http://127.0.0.1:5000
```

Check:

```text
http://127.0.0.1:5000/
```

Test UI:

```text
http://127.0.0.1:5000/test
```

---

# 22. Testing with Postman

## Health check

Method:

```text
GET
```

URL:

```text
https://mentalhealthaimodel.onrender.com/
```

## Prediction

Method:

```text
POST
```

URL:

```text
https://mentalhealthaimodel.onrender.com/predict
```

Headers:

```text
Content-Type: application/json
```

Body:

```text
raw → JSON
```

Paste:

```json
{
  "question1": 1,
  "question2": 1,
  "question3": 1,
  "question4": 0,
  "question5": 1,
  "question6": 0,
  "question7": 1,
  "question8": 0,
  "question9": 0,
  "time1": 8.5,
  "time2": 10.2,
  "time3": 7.8,
  "time4": 6.4,
  "time5": 9.1,
  "time6": 5.8,
  "time7": 8.2,
  "time8": 6.7,
  "time9": 7.5
}
```

---

# 23. Deployment

The API is deployed as a Render Web Service.

## Render build command

```bash
pip install -r requirements.txt
```

## Render start command

```bash
gunicorn app:app
```

The Flask application reads the Render-provided `PORT` environment variable and binds to:

```text
0.0.0.0
```

The model files are packaged with the application and loaded when the service starts.

---

# 24. Render URLs

Production base URL:

```text
https://mentalhealthaimodel.onrender.com/
```

Health check:

```text
https://mentalhealthaimodel.onrender.com/
```

Browser test:

```text
https://mentalhealthaimodel.onrender.com/test
```

Prediction:

```text
https://mentalhealthaimodel.onrender.com/predict
```

---

# 25. Render Free-Tier Consideration

The API is deployed on Render's free web-service infrastructure.

Free services can spin down after a period of inactivity. The first request after the service has spun down may therefore take longer while the service starts again.

For an uptime/health monitor, use:

```text
GET https://mentalhealthaimodel.onrender.com/
```

Do not continuously call `/predict` just to keep the service active, because `/` is sufficient as a lightweight health endpoint.

---

# 26. CORS

The Flask application currently enables CORS:

```python
CORS(app)
```

This allows browser-based frontend applications hosted on different origins to call the API.

For a production environment with known frontend domains, CORS can later be restricted to specific origins.

---

# 27. Security Considerations

Before using this API with real users, additional production security controls should be considered.

Recommended areas include:

- HTTPS
- Authentication/authorization where required
- Rate limiting
- Request validation
- Logging and audit controls
- Secure storage of assessment data
- PII minimization
- Access control
- Monitoring
- Abuse protection
- Appropriate clinical safety workflows

Do not place secrets, API keys, passwords, or private credentials inside the source code.

---

# 28. Data Privacy

The current prediction endpoint is designed to receive assessment inputs and return a prediction.

The current API code does not define a database for storing user assessment history.

If user-identifiable or sensitive assessment data is later stored, the application should implement appropriate privacy, security, retention, access-control, and governance requirements before production use.

---

# 29. Model Information

## Model

```text
XGBoost Classifier
```

## Version

```text
v1
```

## Input features

```text
36
```

## Output classes

```text
Minimal
Mild
Moderate
Moderately Severe
Severe
```

The model was developed as an experimental PHQ-9 severity classification benchmark.

Because the target severity categories are derived from PHQ-9 responses and the model receives those responses as inputs, high classification performance should not be interpreted as independent clinical diagnostic validation.

---

# 30. Model Performance — V1

The current experimental model was evaluated using a stratified train/validation/test split.

### Test metrics

```text
Accuracy:       0.9827
Macro Precision: 0.9194
Macro Recall:    0.8088
Macro F1:        0.8541
```

Experimental calibration evaluation:

```text
ECE ≈ 0.0193
```

The dataset is strongly imbalanced toward the Minimal category. Therefore, accuracy alone should not be used to judge model quality.

The model should undergo further validation, calibration, subgroup evaluation, and clinical review before any clinical or high-stakes use.

---

# 31. Dataset

The model was trained using a psychological assessment dataset containing PHQ-9 assessment data.

The project uses the PHQ-9 CSV data for the current V1 model.

The original dataset contains:

```text
24,292 participants
20 columns
```

The PHQ-9 data contains:

```text
export_id
score
question1 ... question9
time1 ... time9
```

The current model uses:

```text
question1 ... question9
time1 ... time9
```

and derives additional timing features.

---

# 32. Future Expansion

The project structure can be extended to support additional mental-health assessment models.

Potential future components include:

```text
PHQ-9
GAD-7
PSS
ISI
Emotion analysis
Behavioral analysis
Face/emotion model
Clinical review
Assessment history
Model versioning
```

Future API versions could use endpoints such as:

```text
POST /api/v2/predict
POST /api/v2/assessment
GET  /api/v2/model-info
```

These are future examples only and are not currently implemented.

---

# 33. Recommended Frontend Integration Pattern

For a frontend application:

### Step 1

Display question 1.

### Step 2

Start a timer.

### Step 3

User selects one of:

```text
Not at all
Several days
More than half the days
Nearly every day
```

### Step 4

Save:

```text
question1
time1
```

### Step 5

Repeat for questions 2–9.

### Step 6

Create the final request object:

```javascript
{
  question1,
  question2,
  question3,
  question4,
  question5,
  question6,
  question7,
  question8,
  question9,
  time1,
  time2,
  time3,
  time4,
  time5,
  time6,
  time7,
  time8,
  time9
}
```

### Step 7

Send:

```http
POST https://mentalhealthaimodel.onrender.com/predict
```

### Step 8

Read:

```javascript
result.data.predicted_severity
result.data.confidence
result.data.probabilities
```

### Step 9

Display the result according to the product's approved UX and clinical/safety requirements.

---

# 34. Minimal Integration Example

Any developer can integrate the API using this basic pattern:

```javascript
const response = await fetch(
  "https://mentalhealthaimodel.onrender.com/predict",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question1: 1,
      question2: 1,
      question3: 1,
      question4: 0,
      question5: 1,
      question6: 0,
      question7: 1,
      question8: 0,
      question9: 0,

      time1: 8.5,
      time2: 10.2,
      time3: 7.8,
      time4: 6.4,
      time5: 9.1,
      time6: 5.8,
      time7: 8.2,
      time8: 6.7,
      time9: 7.5
    })
  }
);

const result = await response.json();

if (result.status === "success") {
  const severity = result.data.predicted_severity;
  const confidence = result.data.confidence;
  const probabilities = result.data.probabilities;

  console.log("Severity:", severity);
  console.log("Confidence:", confidence);
  console.log("Probabilities:", probabilities);
}
```

This is the core integration contract for the current API.

---

# 35. Important Integration Notes

1. Always send all 18 required fields.
2. `question1`–`question9` should use values `0`, `1`, `2`, or `3`.
3. `time1`–`time9` should correspond to the same question numbers.
4. Send the request as JSON.
5. Use `/predict` only when an assessment is ready to be evaluated.
6. Use `/` for health checks.
7. Do not call `/predict` as a keep-alive mechanism.
8. Handle HTTP `400` and `500` responses in the frontend.
9. Treat `confidence` as model probability output, not clinical certainty.
10. The current model is experimental and should not be presented as an autonomous diagnosis.

---

# 36. Current API Summary

| Item | Value |
|---|---|
| API | Mental Health AI Model API |
| Base URL | `https://mentalhealthaimodel.onrender.com` |
| Framework | Flask |
| Server | Gunicorn |
| ML Model | XGBoost |
| Model Version | v1 |
| Input | 9 PHQ-9 responses + 9 response times |
| Features | 36 |
| Output | Severity + confidence + probabilities |
| Health Endpoint | `GET /` |
| Test UI | `GET /test` |
| Prediction Endpoint | `POST /predict` |
| Deployment | Render |
| CORS | Enabled |
| Current model purpose | Experimental PHQ-9 severity classification |

---

# 37. Disclaimer

This project is intended for research, development, screening, and software integration purposes.

The model output is not a medical diagnosis, does not replace a qualified clinician, and should not be used by itself to make medical, emergency, treatment, or medication decisions.

In particular, responses to the ninth PHQ-9 question can indicate potential self-harm risk. A production system should implement an appropriate safety and clinical escalation workflow rather than relying solely on this API's classification output.

---

# 38. Maintainer / Project Information

**Project:** Mental Health AI Model API

**Backend:** Flask + Python

**ML:** XGBoost + scikit-learn

**Deployment:** Render

**API Base URL:**

```text
https://mentalhealthaimodel.onrender.com
```

For integration questions, first verify:

```text
GET /
```

Then test:

```text
POST /predict
```

using the request schema documented above.
