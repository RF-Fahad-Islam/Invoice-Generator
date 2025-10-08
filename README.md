# Invoice Generator

A full-stack web application for generating invoices, built with FastAPI.
<a href="https://ibb.co.com/D3Q765Z"><img src="https://i.ibb.co.com/ZyxhwW0/Opera-Snapshot-2025-10-08-161429-127-0-0-1.png" alt="Opera-Snapshot-2025-10-08-161429-127-0-0-1" border="0" width="100%" ></a>
## Tech Stack

- Backend: FastAPI
- Frontend: Vanilla JS

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/invoice-generator.git
cd invoice-generator
```

2. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Start the server
```bash
uvicorn app.main:app --reload
```

2. Access the application at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT
