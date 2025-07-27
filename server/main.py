from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.exception_handlers import catch_exceptions_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(title="MedMind API", description="API for MedMind application", version="1.0.0")

# CORS setup
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=["*"],
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"]   # Allow all headers
    )

# Middleware exception handlers
app.middleware("http")(catch_exceptions_middleware)

# routers

# 1. Upload PDFs
app.include_router(upload_router)
# 2. Ask questions
app.include_router(ask_router)