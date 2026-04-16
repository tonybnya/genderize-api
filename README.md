# Genderize.io API Integration & Data Processing

A Flask REST API that classifies names by gender using the [Genderize.io](https://genderize.io/) external API.
Returns structured responses with confidence scoring and performance metrics.

## Features

- **Single endpoint**: `GET /api/classify` - Classify names by gender
- **CORS enabled**: Accessible from any origin
- **Error handling**: 400, 422, 500, 502 error responses
- **Response**: Computes confidence scores and restructures data
- **Performance**: Flask processing under 500ms (excluding Genderize.io API latency)
- **Deployed on Vercel**: Serverless deployment with automatic scaling

## API Endpoint

```
GET /api/classify?name={name}
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "data": {
    "name": "tony",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 752575,
    "is_confident": true,
    "processed_at": "2026-04-10T12:30:45Z"
  }
}
```

**Error Response (400 BAD REQUEST):**

```json
{
  "status": "error",
  "message": "Missing 'name' query parameter"
}
```

## Data Processing Rules

1. **Field mapping**:
   - `gender` → preserved
   - `probability` → preserved
   - `count` → renamed to `sample_size`

2. **Confidence calculation**:
   - `is_confident: true` when `probability >= 0.7` AND `sample_size >= 100`
   - Both conditions must be met

3. **Timestamp**:
   - `processed_at` generated in UTC ISO 8601 format for every request

## Error Responses

| Status | Condition                    | Message                                                    |
| ------ | ---------------------------- | ---------------------------------------------------------- |
| 400    | Missing or empty name        | "Missing 'name' query parameter" or "Name cannot be empty" |
| 422    | Name is not a string         | "Name must be a string"                                    |
| 404    | Genderize returns null/empty | "No prediction available for the provided name"            |
| 502    | Upstream API timeout         | "Upstream API request timed out"                           |
| 502    | Upstream API failure         | "Upstream API error: {details}"                            |
| 500    | Server error                 | "Server error: {details}"                                  |

All errors follow this structure:

```json
{
  "status": "error",
  "message": "<error message>"
}
```

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js (optional, for Vercel CLI)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/tonybnya/genderize-api
cd genderize-api
```

2. Install dependencies:

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Start the Server (Local Development)

```bash
uv run python app.py
```

The server starts on `http://localhost:5000`

### Tests

#### Using curl (Local)

```bash
# Basic request
curl "http://localhost:5000/api/classify?name=yanis"

# With pretty output
curl "http://localhost:5000/api/classify?name=tony" | python -m json.tool
```

#### Using curl (Production)

```bash
# Basic request
curl "https://genderize-api-alpha.vercel.app/api/classify?name=yanis"

# With pretty output
curl "https://genderize-api-alpha.vercel.app/api/classify?name=tony" | python -m json.tool
```

#### Error Cases

```bash
# Missing parameter
curl "http://localhost:5000/api/classify"
# Returns: 400 BAD REQUEST

# Empty name
curl "http://localhost:5000/api/classify?name="
# Returns: 400 BAD REQUEST

# Edge case (unpredictable name)
curl "http://localhost:5000/api/classify?name=xyz123"
# Returns: 404 NOT FOUND (if Genderize API returns gender = null or count = 0)

# Edge case (unprocessable entity)
curl "http://localhost:5000/api/classify?name=123"
# Returns: 422 UNPROCESSABLE ENTITY
```

## Project Structure

```
genderize-api/
├── api/ # Vercel serverless entry point
│   ├── __init__.py
│   └── index.py # ASGI adapter for Vercel
├── app.py # Flask application with endpoints
├── utils.py # Helper functions
├── requirements.txt # Python dependencies
├── pyproject.toml # uv project configuration
├── uv.lock # uv lock file
├── vercel.json # Vercel deployment configuration
├── .vercelignore # Vercel ignore patterns
├── .env # Local environment variables
├── .env.example # Environment template
└── README.md
```

## Deployment

### Deploy on Vercel

This API is configured for serverless deployment on Vercel.

#### Prerequisites

- Vercel CLI: `npm i -g vercel`
- Vercel account (free tier available)

#### Deploy

```bash
# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

#### Environment Variables

Set environment variables in Vercel dashboard or CLI:

```bash
vercel env add DEBUG
vercel env add GENDERIZE_API_URL
```

### Deploy on Other Platforms

The project can be containerized for deployment on platforms like:

- Fly.io
- Railway
- Google Cloud Run
- AWS Lambda

Create a `Dockerfile` if needed for containerized deployment.

## License

Copyright © [2026] [@tonybnya]
