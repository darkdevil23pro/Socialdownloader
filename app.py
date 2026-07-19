from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# সাময়িকভাবে ফাইল রাখার ফোল্ডার
DOWNLOAD_DIR = '/sdcard/Download/temp_downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'format': 'best',
        'restrictfilenames': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # ফাইলটি সরাসরি ইউজারের নিজের ফোনের ক্রোম ব্রাউজারে ট্রান্সফার করা
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    if not os.path.exists('/sdcard/Download'):
        os.system('termux-setup-storage')
    app.run(host='0.0.0.0', port=5000)
