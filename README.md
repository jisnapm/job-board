# Job Board API

A backend REST API built with Python, Django and Django REST Framework for managing job postings and job applications. Employers can post jobs, candidates can apply to them, and applications can be reviewed (shortlisted or rejected) with remarks. Incoming data is validated with DRF serializers and returned as structured JSON.

## Features

- Create, retrieve, update and delete job postings.
- Classify jobs by category and experience level, and mark them open or closed.
- Candidates can submit, view, update and withdraw applications to a job.
- Applications are checked against existing jobs: applying to a job that does not exist is rejected.
- Separate review endpoint to shortlist or reject an application with remarks.
- Candidates cannot change their own application status or remarks; only the review endpoint can.
- Validation errors return `400`, and requests for ids that do not exist return `404`.

## Tech Stack

- **Language:** Python
- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Database:** SQLite
- **API Testing:** HTTP request collection (`APIDOC.http`)

## Data Model

### Job

| Field | Type | Notes |
|---|---|---|
| `employer` | CharField (100) | Company posting the job |
| `title` | CharField (100) | Job title |
| `description` | TextField | Up to 1000 characters via the API |
| `category` | CharField, choices | See below. Default: `software` |
| `experience_level` | CharField, choices | `fresher`, `mid`, `senior`. Default: `fresher` |
| `location` | CharField (50) | City or region |
| `posted_date` | DateTimeField | Set automatically, read-only |
| `is_open` | BooleanField | Default: `true` |

**Category choices:** `software`, `data`, `design`, `marketing`, `sales`, `finance`, `hr`, `support`, `other`

### Application

| Field | Type | Notes |
|---|---|---|
| `job_id` | IntegerField | Id of the job applied to. Must match an existing job |
| `candidate_name` | CharField (50) | Applicant's name |
| `mobile_no` | CharField (15) | Stored as text so leading zeros and `+` are kept |
| `place` | CharField (50) | Applicant's location |
| `cover_letter` | TextField | Up to 1000 characters via the API |
| `status` | CharField, choices | `pending`, `shortlisted`, `rejected`. Default: `pending`. Read-only on the application endpoints |
| `remarks` | TextField, nullable | Reviewer's note. Read-only on the application endpoints |
| `applied_date` | DateTimeField | Set automatically, read-only |

Relationship: one job can have many applications (linked through `job_id`).

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jisnapm/job-board.git
   cd job-board
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

   macOS / Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install django djangorestframework
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

The API is then available at `http://127.0.0.1:8000/`.

## API Endpoints

### Jobs

| Method | Endpoint | Operation |
|---|---|---|
| GET | `/jobs/` | List all jobs |
| POST | `/jobs/` | Create a job |
| GET | `/jobs/<id>/` | Retrieve a job |
| PUT | `/jobs/<id>/` | Update a job |
| DELETE | `/jobs/<id>/` | Delete a job |

### Applications

| Method | Endpoint | Operation |
|---|---|---|
| GET | `/applications/` | List all applications |
| POST | `/applications/` | Submit an application |
| GET | `/applications/<id>/` | Retrieve an application |
| PUT | `/applications/<id>/` | Update an application |
| DELETE | `/applications/<id>/` | Delete an application |
| PUT | `/applications/<id>/review/` | Shortlist or reject an application, with remarks |

### Response codes

| Code | Meaning |
|---|---|
| `200` | Request succeeded |
| `400` | Validation failed. The response body lists the field errors |
| `404` | The job or application with that id does not exist |

## Example Requests

Create a job:

```http
POST http://127.0.0.1:8000/jobs/
Content-Type: application/json

{
    "employer": "Wipro",
    "title": "Backend Developer",
    "description": "Build and maintain REST APIs.",
    "category": "software",
    "experience_level": "fresher",
    "location": "Kochi",
    "is_open": true
}
```

Apply to a job:

```http
POST http://127.0.0.1:8000/applications/
Content-Type: application/json

{
    "job_id": 1,
    "candidate_name": "Jisna",
    "mobile_no": "9856487423",
    "place": "Kochi",
    "cover_letter": "I would like to apply for this role."
}
```

Review an application:

```http
PUT http://127.0.0.1:8000/applications/1/review/
Content-Type: application/json

{
    "status": "shortlisted",
    "remarks": "Good fit for the role."
}
```

Both `status` and `remarks` are required when reviewing. Example requests for every endpoint are in `APIDOC.http`, which can be run directly from VS Code (REST Client extension) or PyCharm.

## Project Structure

```
job_board/
├── job_board/        # Project settings and root URL configuration
├── jobs/             # App: models, serializers, views, migrations
│   ├── models.py
│   ├── serializer.py
│   ├── views.py
│   └── migrations/
├── APIDOC.http       # Sample API requests
└── manage.py
```

## Learning Objectives

This project practices Django REST Framework fundamentals: model design with choice fields, serializers with custom validation, class-based API views, CRUD operations, handling missing objects with `get_object_or_404`, and keeping a review workflow separate from the data a candidate can edit. It is a companion to [CodeWise](https://github.com/jisnapm/CodeWise), built with the same pattern in a different domain.

## Future Improvements

- Replace `job_id` with a real `ForeignKey` to the job, so applications are tied to jobs in the database (and removed with them).
- Reject applications to jobs that are closed (`is_open = false`).
- Prevent the same candidate (by mobile number) from applying to the same job twice.
- Return `201 Created` for successful creates.
- Add authentication, with employers managing their own jobs and reviewing applications, and candidates managing their own applications.
- Add pagination, filtering (category, location, experience level, status) and search.
- Add automated tests with `APITestCase`.
- Move `SECRET_KEY` and other settings into environment variables.
