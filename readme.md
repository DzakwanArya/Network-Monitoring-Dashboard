# Network Monitoring Dashboard (Python)

## Deskripsi
Network Monitoring Dashboard adalah aplikasi berbasis Python yang digunakan
untuk memantau kondisi jaringan komputer secara otomatis dan terpusat.
Aplikasi ini mampu mendeteksi IP address dan subnet secara otomatis,
melakukan network discovery, serta menampilkan status perangkat jaringan
melalui dashboard.

## Tujuan Proyek
- Mendeteksi IP dan subnet jaringan secara otomatis
- Menemukan perangkat aktif dalam jaringan (auto discovery)
- Memantau status perangkat (UP/DOWN)
- Menyimpan data monitoring ke database
- Menyajikan informasi jaringan dalam dashboard sederhana

## Ruang Lingkup (MVP)
- Auto detect network interface (IP & subnet)
- Generate IP range berdasarkan subnet
- Scan jaringan menggunakan ping
- Simpan hasil scan ke database
- Tampilkan hasil monitoring di dashboard

## Teknologi yang Digunakan
- Python 3.10+
- psutil
- pythonping
- SQLAlchemy
- Streamlit
- MySQL (Laragon) / SQLite
- APScheduler

## Penggunaan (Run)
- Jalankan seluruh API + scheduler (direkomendasikan):

```powershell
python main.py
```

- Atau jalankan API saja (untuk pengembangan API):

```powershell
python -m api.app
```

- Jalankan UI (dashboard) di port 5000:

```powershell
python -m ui.app
```

Catatan: Pastikan dependency terinstal (`pip install -r requirements.txt`) dan database telah dikonfigurasi sebelum menjalankan aplikasi.

## Struktur Folder
network-monitor/
│
├── core/
│   ├── interface_detector.py
│   ├── subnet_generator.py
│   └── scanner.py
│
├── database/
│   ├── models.py
│   └── db.py
│
├── scheduler/
│   └── jobs.py
│
├── dashboard/
│   └── app.py
│
└── main.py
