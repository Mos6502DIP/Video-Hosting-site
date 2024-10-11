# Video Hosting Project (WIP)

This project is a **work-in-progress** web-based video hosting platform. It allows users to upload videos, manage their accounts, and offers basic functionalities like user authentication, password recovery, and video conversion.

## Features

- **User Registration & Login**
  - Users can register, log in, and log out using session management.
  - Password hashing for security.
  
- **Email Verification**
  - Users must verify their email before account activation.

- **Password Recovery**
  - Users can request a password reset link via email.

- **Video Uploading**
  - Users can upload videos in multiple formats (e.g., MP4, MOV, MKV, WEBM).
  - Video thumbnails can also be uploaded.
  
- **Video Conversion**
  - The platform uses `ffmpeg` to convert uploaded videos to WebM format for better compatibility.

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite
- **File Storage**: Local directory for videos and thumbnails
- **Video Processing**: FFmpeg for conversion to WebM
- **Emailing**: Custom SMTP email integration for user verification and password recovery.

## Installation

Follow the steps below to set up the project locally.

### Prerequisites

- Python 3.x
- Flask
- FFmpeg (must be installed on your machine and added to your system's PATH)
  
### Clone the Repository

```bash
git clone https://github.com/yourusername/video-hosting-project.git
cd video-hosting-project
