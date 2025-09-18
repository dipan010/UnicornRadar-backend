# UnicornRadar Backend

A FastAPI-based backend service for tracking and analyzing potential unicorn companies. This service provides APIs for managing company data, founder information, and deal notes with AI-powered insights.

## 🚀 Features

- **Company Management**: Track company information including sector, stage, funding, and key metrics
- **Founder Profiles**: Manage founder data with roles, backgrounds, and social links
- **Deal Notes**: AI-generated insights and scoring for investment opportunities
- **Document Processing**: Upload and extract data from company documents
- **Database Migrations**: Alembic-based schema management
- **Docker Support**: Containerized deployment with Docker and docker-compose

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel
- **Migrations**: Alembic
- **Document Processing**: Custom extractor utilities
- **Containerization**: Docker & Docker Compose
- **Python**: 3.11+

## 📁 Project Structure

```
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLModel database models
│   ├── schemas.py           # Pydantic schemas for API
│   ├── db.py               # Database configuration
│   ├── crud.py             # Database operations
│   ├── routes/             # API route handlers
│   │   ├── companies.py    # Company endpoints
│   │   ├── deal_notes.py   # Deal notes endpoints
│   │   └── documents.py    # Document upload endpoints
│   └── utils/
│       └── extractor.py    # Document processing utilities
├── alembic/                # Database migrations
├── seed/                   # Database seeding scripts
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Multi-service setup
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dipan010/UnicornRadar-backend.git
   cd UnicornRadar-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Update `alembic.ini` with your PostgreSQL connection string
   - Run migrations:
   ```bash
   alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Using Docker

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📊 Database Schema

### Core Models

- **Company**: Core company information (name, sector, stage, etc.)
- **Founder**: Founder profiles linked to companies
- **DealNote**: AI-generated insights and scoring

### Migration Management

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current
```

## 🔧 API Endpoints

### Companies
- `GET /companies/` - List all companies
- `POST /companies/` - Create new company
- `GET /companies/{id}` - Get company details
- `PUT /companies/{id}` - Update company
- `DELETE /companies/{id}` - Delete company

### Deal Notes
- `GET /deal-notes/` - List deal notes
- `POST /deal-notes/` - Create deal note
- `GET /deal-notes/{id}` - Get deal note details

### Documents
- `POST /documents/upload` - Upload company documents
- `GET /documents/` - List uploaded documents

## 🧪 Development

### Running Tests
```bash
# Run tests (when implemented)
pytest
```

### Code Formatting
```bash
# Format code (when configured)
black app/
isort app/
```

### Database Seeding
```bash
python seed/seed.py
```

## 🐳 Docker Configuration

The project includes Docker support for easy deployment:

- **Dockerfile**: Single-service container setup
- **docker-compose.yml**: Multi-service orchestration
- **Environment variables**: Configurable via `.env` file

## 📝 Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/unicornradar
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Deployment

### Production Deployment

1. **Set up production database**
2. **Configure environment variables**
3. **Run migrations**: `alembic upgrade head`
4. **Deploy with Docker** or your preferred method

### Health Checks

- Health endpoint: `GET /health`
- Database connectivity: `GET /health/db`

## 📞 Support

For support and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ for tracking the next unicorns**