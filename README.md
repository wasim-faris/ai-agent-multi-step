# AI Product Finder

A small beginner-friendly full-stack demo. Describe a laptop or mobile you want, and the AI uses a backend search function to find matching sample products.

## Technologies

- React and Vite
- Python, Django, and Django REST Framework
- OpenRouter chat completions with function calling

The product catalog is a Python list in the backend. The project does not use a database for products or an external product API.

## Project Structure

```text
Multi-step/
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── products/
│   │   ├── catalog.py       # Sample products and search_products()
│   │   ├── services.py      # OpenRouter tool workflow
│   │   ├── views.py         # POST API endpoint
│   │   ├── urls.py
│   │   └── tests.py
│   ├── requirements.txt
│   └── .env                 # Local OpenRouter key; do not commit
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    └── package.json
```

## Configure OpenRouter

Create an OpenRouter API key at [openrouter.ai](https://openrouter.ai/). From a terminal at the repository root:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set `OPENROUTER_API_KEY` to your key. The default model is `openai/gpt-4o-mini`; change `OPENROUTER_MODEL` there to another OpenRouter model that supports function calling. Django reads the key from its environment. React never receives it.

## Install and Run the Backend

```bash
cd backend
python3 -m venv ../venv
source ../venv/bin/activate       # Windows: ..\venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000`. Product search does not require migrations.

## Install and Run the Frontend

Open a second terminal from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## How the Workflow Works

```text
User
 ↓
React
 ↓
Django REST API
 ↓
OpenRouter AI
 ↓
search_products()
 ↓
Product Data
 ↓
Results
 ↓
OpenRouter AI
 ↓
Final Response
 ↓
React
```

The AI understands the user's product requirements and requests the `search_products()` tool. Django executes the tool and searches the product data. The matching products are returned to the AI, which generates the final response for the user.

The model receives a tool schema for `category`, `brand`, `max_price`, `min_price`, `ram`, `storage`, and `color`. Django executes the function call itself; the model cannot access the catalog directly. Django then sends only matching products back to OpenRouter for a short answer.

## Try It

Enter a question such as:

```text
Show me laptops under 60000 with 16GB RAM
```

Other examples include `I need a mobile under 20000`, `Show me black laptops under 70000`, and `Find me a mobile under 25000 with 256GB storage`.

The endpoint is `POST http://127.0.0.1:8000/api/products/search/` and accepts:

```json
{ "message": "Show me laptops under 50000" }
```

It returns an AI-generated `message` and a `products` list. An empty result includes a helpful no-match response in the React page. OpenRouter and network errors are reported without exposing the API key.

## Test

From the repository root, with the backend virtual environment active:

```bash
python backend/manage.py test products
```

## Reviewer Summary

This demo separates interpreting a request from executing a search. OpenRouter extracts search filters by requesting a function call, Django runs the ordinary Python `search_products()` function against sample data, and then the AI turns those matching results into a short answer for React to display.
# ai-agent-multi-step
