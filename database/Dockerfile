# Python 3.9 imajını kullan
FROM python:3.9

# Çalışma dizinini belirle
WORKDIR /app

# Gereksinim dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Flask uygulamanızı kopyalayın
COPY . .

# Uygulamayı başlat
CMD ["python", "db_0.py"]
