"""
Video İndirici - Railway.app İçin (Node.js Runtime Fix)
YouTube JavaScript runtime sorunu çözüldü
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

# Konfigürasyon
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# HTML içeriği
HTML_CONTENT = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#6366f1">
    <title>Video & Ses İndirici</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            max-width: 600px;
            width: 100%;
        }
        .header {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
            border-radius: 24px 24px 0 0;
        }
        .header h1 { font-size: 32px; margin-bottom: 12px; }
        .header p { font-size: 15px; opacity: 0.95; }
        .content { padding: 30px; }
        .input-group { margin-bottom: 25px; }
        .input-group label {
            display: block;
            margin-bottom: 10px;
            color: #2d3436;
            font-weight: 600;
            font-size: 14px;
        }
        input[type="url"] {
            width: 100%;
            padding: 16px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 14px;
            font-size: 16px;
            background: #fafafa;
        }
        input[type="url"]:focus {
            outline: none;
            border-color: #6366f1;
            background: white;
        }
        .format-selector {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }
        .format-option input[type="radio"] { display: none; }
        .format-label {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 24px;
            border: 2px solid #e5e7eb;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s;
            background: #fafafa;
        }
        .format-label:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
        }
        .format-option input[type="radio"]:checked + .format-label {
            border-color: #6366f1;
            background: #eef2ff;
        }
        .format-label .icon { font-size: 40px; margin-bottom: 12px; }
        .format-label .title { font-weight: 700; color: #1f2937; }
        .format-label .desc { font-size: 13px; color: #6b7280; }
        .quality-selector { margin-bottom: 25px; }
        .quality-options {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .quality-option input[type="radio"] { display: none; }
        .quality-btn {
            width: 100%;
            padding: 14px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            background: #fafafa;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            color: #374151;
            transition: all 0.3s;
        }
        .quality-option input[type="radio"]:checked + .quality-btn {
            border-color: #6366f1;
            background: #eef2ff;
            color: #4f46e5;
        }
        .download-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: none;
            border-radius: 16px;
            color: white;
            font-size: 18px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s;
        }
        .download-btn:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.4);
        }
        .download-btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }
        .status-message {
            margin-top: 20px;
            padding: 16px 20px;
            border-radius: 12px;
            display: none;
            font-size: 14px;
        }
        .status-message.show { display: block; }
        .status-message.error {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }
        .status-message.success {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #6ee7b7;
        }
        .info-box {
            background: #f8fafc;
            border-left: 4px solid #6366f1;
            padding: 20px;
            margin-top: 30px;
            border-radius: 12px;
        }
        .info-box h3 {
            color: #6366f1;
            font-size: 17px;
            margin-bottom: 14px;
        }
        .info-box ul {
            list-style: none;
            color: #475569;
            font-size: 14px;
        }
        .info-box ul li {
            padding: 6px 0;
            padding-left: 28px;
            position: relative;
        }
        .info-box ul li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #10b981;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Video & Ses İndirici</h1>
            <p>YouTube, Instagram, TikTok ve 1000+ platform</p>
        </div>
        <div class="content">
            <div class="input-group">
                <label for="videoUrl">🔗 Video Linki</label>
                <input type="url" id="videoUrl" placeholder="https://www.youtube.com/watch?v=...">
            </div>

            <div class="input-group">
                <label>📁 Format</label>
                <div class="format-selector">
                    <div class="format-option">
                        <input type="radio" name="format" id="format-video" value="video" checked>
                        <label for="format-video" class="format-label">
                            <div class="icon">🎥</div>
                            <div class="title">Video</div>
                            <div class="desc">MP4 Format</div>
                        </label>
                    </div>
                    <div class="format-option">
                        <input type="radio" name="format" id="format-audio" value="audio">
                        <label for="format-audio" class="format-label">
                            <div class="icon">🎵</div>
                            <div class="title">Sadece Ses</div>
                            <div class="desc">MP3 320kbps</div>
                        </label>
                    </div>
                </div>
            </div>

            <div class="quality-selector" id="qualitySelector">
                <label>⚙️ Video Kalitesi</label>
                <div class="quality-options">
                    <div class="quality-option">
                        <input type="radio" name="quality" id="quality-best" value="best" checked>
                        <label for="quality-best" class="quality-btn">🌟 Ultra (1080p HD)</label>
                    </div>
                    <div class="quality-option">
                        <input type="radio" name="quality" id="quality-720" value="720p">
                        <label for="quality-720" class="quality-btn">⭐ Yüksek (720p)</label>
                    </div>
                    <div class="quality-option">
                        <input type="radio" name="quality" id="quality-480" value="480p">
                        <label for="quality-480" class="quality-btn">💫 Orta (480p)</label>
                    </div>
                    <div class="quality-option">
                        <input type="radio" name="quality" id="quality-360" value="360p">
                        <label for="quality-360" class="quality-btn">✨ Hızlı (360p)</label>
                    </div>
                </div>
            </div>

            <button class="download-btn" id="downloadBtn">⬇️ İNDİRMEYİ BAŞLAT</button>
            <div class="status-message" id="statusMessage"></div>

            <div class="info-box">
                <h3>💡 Kalite Seçenekleri</h3>
                <ul>
                    <li><strong>Ultra (1080p):</strong> En yüksek kalite - Büyük dosya</li>
                    <li><strong>Yüksek (720p):</strong> HD kalite - Dengeli</li>
                    <li><strong>Orta (480p):</strong> İyi kalite - Küçük dosya</li>
                    <li><strong>Hızlı (360p):</strong> Hızlı indirme</li>
                </ul>
            </div>
            
            <div class="info-box" style="margin-top: 15px;">
                <h3>🌐 Desteklenen Platformlar</h3>
                <ul>
                    <li>YouTube (videolar ve listeleri)</li>
                    <li>Instagram (reels, videolar, IGTV)</li>
                    <li>TikTok, Facebook, Twitter</li>
                    <li>Ve 1000+ platform daha!</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        const formatRadios = document.querySelectorAll('input[name="format"]');
        const qualitySelector = document.getElementById('qualitySelector');
        const downloadBtn = document.getElementById('downloadBtn');
        const urlInput = document.getElementById('videoUrl');
        const statusMessage = document.getElementById('statusMessage');

        formatRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                qualitySelector.style.display = e.target.value === 'video' ? 'block' : 'none';
            });
        });

        downloadBtn.addEventListener('click', async () => {
            const url = urlInput.value.trim();
            
            if (!url || !url.startsWith('http')) {
                showStatus('error', '⚠️ Geçerli bir URL girin!');
                return;
            }

            const format = document.querySelector('input[name="format"]:checked').value;
            const quality = format === 'video' ? 
                document.querySelector('input[name="quality"]:checked').value : 'best';

            downloadBtn.disabled = true;
            downloadBtn.textContent = '⏳ İndiriliyor...';
            
            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url, format, quality })
                });

                const data = await response.json();

                if (data.success) {
                    showStatus('success', `✅ Başarılı! ${data.filename}`);
                    if (data.download_url) {
                        window.location.href = data.download_url;
                    }
                } else {
                    showStatus('error', `❌ Hata: ${data.error}`);
                }
            } catch (error) {
                showStatus('error', `❌ Bağlantı hatası: ${error.message}`);
            } finally {
                downloadBtn.disabled = false;
                downloadBtn.textContent = '⬇️ İNDİRMEYİ BAŞLAT';
            }
        });

        function showStatus(type, message) {
            statusMessage.className = `status-message ${type} show`;
            statusMessage.textContent = message;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Ana sayfa"""
    return HTML_CONTENT

@app.route('/api/download', methods=['POST'])
def download_video():
    """Video indirme - YouTube Shorts desteği ile"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('format', 'video')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'success': False, 'error': 'URL gerekli!'}), 400
        
        file_id = str(uuid.uuid4())[:8]
        output_template = f'{DOWNLOAD_FOLDER}/{file_id}_%(title)s.%(ext)s'
        
        # YouTube için Android client kullan
        base_cmd = ['yt-dlp']
        if 'youtube.com' in url or 'youtu.be' in url:
            base_cmd.extend(['--extractor-args', 'youtube:player_client=android'])
        
        if format_type == 'audio':
            cmd = base_cmd + [
                '-x',
                '--audio-format', 'mp3',
                '--audio-quality', '0',
                '-o', output_template,
                url
            ]
        else:
            # YouTube Shorts için özel format seçimi
            is_shorts = '/shorts/' in url
            
            if is_shorts:
                # Shorts için basit format - sorun çıkarmaz
                format_str = 'best[ext=mp4]/best'
            else:
                # Normal YouTube videoları için kaliteli format
                if quality == 'best':
                    format_str = (
                        'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/'
                        'bestvideo[height<=1080]+bestaudio/'
                        'best[height<=1080]/'
                        'best'
                    )
                elif quality == '720p':
                    format_str = (
                        'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/'
                        'best[height<=720]'
                    )
                elif quality == '480p':
                    format_str = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                else:
                    format_str = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
            
            cmd = base_cmd + [
                '-f', format_str,
                '--merge-output-format', 'mp4',
                '--no-check-formats',  # Format kontrolünü atla (Shorts için önemli)
                '-o', output_template,
                url
            ]
        
        print(f"🔧 URL: {url}")
        print(f"🔧 Shorts: {is_shorts if format_type == 'video' else 'N/A'}")
        print(f"🔧 Format: {format_str if format_type == 'video' else 'MP3'}")
        print(f"🔧 Komut: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        print(f"📊 Return code: {result.returncode}")
        if result.stdout:
            print(f"📤 STDOUT: {result.stdout[:300]}")
        if result.stderr:
            print(f"⚠️  STDERR: {result.stderr[:300]}")
        
        if result.returncode == 0:
            # Dosyayı bul
            files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith(file_id)]
            
            if files:
                filename = files[0]
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                file_size = os.path.getsize(file_path)
                
                print(f"✅ Dosya bulundu: {filename}")
                print(f"📊 Boyut: {file_size / (1024*1024):.2f} MB")
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'download_url': f'/api/file/{filename}',
                    'size_mb': round(file_size / (1024*1024), 2)
                })
            else:
                # Dosya bulunamadı - downloads klasörünü listele
                all_files = os.listdir(DOWNLOAD_FOLDER)
                print(f"❌ Dosya bulunamadı!")
                print(f"📂 Downloads klasörü: {all_files}")
                
                # Belki farklı ID ile oluştu - en son dosyayı dene
                if all_files:
                    latest_file = max(
                        [os.path.join(DOWNLOAD_FOLDER, f) for f in all_files],
                        key=os.path.getmtime
                    )
                    filename = os.path.basename(latest_file)
                    print(f"🔍 En son oluşan dosya: {filename}")
                    
                    return jsonify({
                        'success': True,
                        'filename': filename,
                        'download_url': f'/api/file/{filename}'
                    })
                
                return jsonify({
                    'success': False,
                    'error': 'Dosya oluşturulamadı! yt-dlp çıktısını kontrol edin.'
                }), 500
        else:
            error = result.stderr or result.stdout or 'Bilinmeyen hata'
            print(f"❌ yt-dlp hatası: {error[:500]}")
            return jsonify({
                'success': False,
                'error': f'İndirme hatası: {error[:200]}'
            }), 500
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout!")
        return jsonify({
            'success': False,
            'error': 'İndirme zaman aşımına uğradı (max 5 dakika)'
        }), 500
    except Exception as e:
        print(f"❌ Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Sunucu hatası: {str(e)}'
        }), 500

@app.route('/api/file/<filename>')
def download_file(filename):
    """Dosya indirme"""
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return jsonify({'success': False, 'error': 'Dosya bulunamadı'}), 404

@app.route('/api/health')
def health():
    """Sağlık kontrolü"""
    health_data = {'status': 'ok'}
    
    # yt-dlp kontrol
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            health_data['yt-dlp'] = result.stdout.decode().strip()
        else:
            health_data['yt-dlp'] = 'not working'
    except:
        health_data['yt-dlp'] = 'missing'
    
    # Node.js kontrol
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            health_data['nodejs'] = result.stdout.decode().strip()
        else:
            health_data['nodejs'] = 'not found'
    except:
        health_data['nodejs'] = 'not found'
    
    return jsonify(health_data)

if __name__ == '__main__':
    print("🚀 Video İndirici Başlatılıyor...")
    print(f"📂 Download klasörü: {os.path.abspath(DOWNLOAD_FOLDER)}")
    
    # Node.js kontrolü
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.decode().strip()}")
        else:
            print("⚠️  Node.js bulunamadı - YouTube indirme çalışmayabilir")
    except:
        print("⚠️  Node.js bulunamadı - nixpacks.toml ekleyin")
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
