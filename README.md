# Voice Assistant Django Project
<p align="center">
    <img src="./logo.png" alt="voice assistant logo">
</p>

## Overview
This repository contains a voice assistant application built with Django. The application features pitch shift, voice denoise, and hot word detection capabilities in both online and offline modes.

## Features
- **Pitch Shift**: Adjusts the pitch of the voice input.
- **Voice Denoise**: Reduces background noise from the voice input.
- **Hot Word Detection**: Detects specific trigger words in the voice input. Works in both online and offline modes.

## Getting Started

### Prerequisites
- Docker
- Python 3.x
- Django

### Installation
1. Clone the repository:

   ```shell
   git clone https://github.com/hesamdavarpanah/voice-assistant.git
   ```

2. Navigate to the project directory
   ```shell
   cd voice-assistant
   ```

3. Run the Docker containers
   ```shell
   docker compose up -d
   ```


Now, you can access the application at `http://0.0.0.0:8000`.

## Usage
To use this application, you can send a voice file with the required fields to the voice gallery URL to perform CRUD operations on the voice gallery. You can also send the stored voice file to the offline hot word detection URL, pitch shift URL, or denoise URL to use the voice assistant abilities.
## License
This project is licensed under the [MIT License](./LICENSE).

## Contact
Hesam Davarpanah - hesamdavarpanah@gmail.com
