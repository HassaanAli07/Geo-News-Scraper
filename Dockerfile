FROM python:3.9-slim

WORKDIR /app

# 1. Install system dependencies first
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Python packages (including nltk)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Now download NLTK data
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/share/nltk_data')" && \
    python -c "import nltk; nltk.download('punkt_tab', download_dir='/usr/share/nltk_data')"
ENV NLTK_DATA=/usr/share/nltk_data

# 4. Copy app code
COPY . .

# 5. Add wait-for-it script
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /wait.sh && \
    chmod +x /wait.sh

CMD ["/bin/sh", "-c", "/wait.sh mongo:27017 -- python app.py"]