# Use an official, slim Python image
FROM python:3.11-slim

# 1. Install system-level build deps & libraries
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      pkg-config \
      libcairo2-dev \
      libpango1.0-dev \
      libglib2.0-dev \
      libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# 2. Set a working directory
WORKDIR /app

# 3. Copy only requirements first (caches pip install step)
COPY requirements.txt .

# 4. Install Python-level deps
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy (or mount) your application code into /app
#    You can overwrite this at runtime with a volume.
COPY . .

# 6. Make "python" the entrypoint so any args become script names
ENTRYPOINT ["python"]

# 7. Default to running "main.py" if no other arg is given
CMD ["main.py"]
