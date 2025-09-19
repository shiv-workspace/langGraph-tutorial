
FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for LangGraph server (default 8123/8000 depending on CLI)
EXPOSE 8123

# Default: run dev server (hot reload). For production you'd use langgraph build/up or a proper entry.
CMD ["langgraph", "dev", "--host", "0.0.0.0"]
