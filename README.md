# 🌟 YouTube Video and Audio Downloader

Welcome to the **YouTube Video and Audio Downloader**! This Django-based project empowers you to download YouTube videos and audio in your preferred format and resolution. 🎥🎵

---

## ✨ Features

- 🎬 **Download YouTube Videos**: Choose your desired resolution and format.
- 🎧 **Download YouTube Audio**: Extract and save audio files with ease.
- 🔄 **Convert Formats**: Seamlessly convert audio files using `ffmpeg`.
- 🖥️ **User-Friendly Interface**: Enjoy a modern and intuitive web app.

---

## 📋 Prerequisites

Ensure you have the following installed:

- 🐍 **Python 3.8+**
- 📦 **pip**
- 🌐 **Django Framework**
- 🎚️ **ffmpeg** (for audio conversion)

---

## 🚀 Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Ensure `ffmpeg` Folder is Present**:
   Make sure the `ffmpeg` folder is in the downloader folder of this project.
   ![image](https://github.com/user-attachments/assets/47582c34-ee41-425d-bb75-aacbcee1d4c4)


5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the App**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---

## ⚙️ Setting Up `ffmpeg`

`ffmpeg` is essential for audio processing. Follow these steps to install and configure it:

### Windows

1. **Download `ffmpeg`**:
   - Visit [ffmpeg.org](https://ffmpeg.org/download.html) and download the Windows version.

2. **Extract the Archive**:
   - Unzip the downloaded file and copy the `ffmpeg` folder.

3. **Place in Project Directory**:
   - Paste the `ffmpeg` folder into the root directory of this project (same as `manage.py`).

4. **Add to System PATH**:
   - Go to **System Properties** → **Advanced** → **Environment Variables**.
   - Edit the `Path` variable under **System Variables**.
   - Add the path to the `bin` folder inside your `ffmpeg` directory (e.g., `C:\youtube-downloader\ffmpeg\bin`).

### Linux/MacOS

1. **Install `ffmpeg`**:
   - **Linux**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - **MacOS**:
     ```bash
     brew install ffmpeg
     ```

2. **Verify Installation**:
   ```bash
   ffmpeg -version
   ```

3. **Optional**: Copy the `ffmpeg` folder into the project directory for local use.

---

## 🎯 Usage

1. **Launch the App**:
   Open the application in your browser.

2. **Enter YouTube URL**:
   Paste the link to the YouTube video you wish to download.

3. **Choose Format and Resolution**:
   Select your preferred video or audio options.

4. **Download**:
   Click the **Download** button and enjoy your content offline! 🌟

---

## 🖼️ Screenshots

### Youtube Video Downloader Page
![Home Page](https://github.com/user-attachments/assets/ab4f96cd-0f27-4b4b-9b2a-0ae31165adf3)

### Download Page
![image](https://github.com/user-attachments/assets/5093fea2-1de5-43d1-8f1b-8a0a7e6a79c4)


---

## 🤝 Contributions

We welcome contributions! Feel free to open issues or submit pull requests to improve this project. 🌟

---

## 🙌 Acknowledgements

A big thanks to the developers of:

- `pytube`
- `yt-dlp`
- `ffmpeg`

for their incredible tools that make this project possible! 💡
