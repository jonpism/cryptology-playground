FROM python:3.10-slim

# Install system dependencies for PyQt6 and building Python extensions
RUN apt-get update && apt-get install -y \
    libegl1 \
    libgl1 \
    libxcb-render-util0 \
    libxcb1 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon0 \
    libxcb-cursor0 \
    libxrender1 \
    libsm6 \
    libxext6 \
    libx11-xcb1 \
    libpipewire-0.3-0 \
    gcc \
    g++ \
    make \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libxrandr2 \
    libxss1 \
    libdbus-1-3 \
    libpulse0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your app files and requirements
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for PyQt
ENV QT_QPA_PLATFORM=xcb

# Run the app
CMD ["python", "mainwindow.py"]
