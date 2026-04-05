# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini merupakan analisis data menggunakan **Bike Sharing Dataset** yang mencatat 
jumlah peminjaman sepeda dari sistem Capital Bikeshare di Washington D.C. selama 
tahun 2011–2012. Analisis menjawab dua pertanyaan bisnis utama:

1. **Bagaimana pengaruh musim (season) terhadap rata-rata jumlah peminjaman sepeda harian?**
2. **Bagaimana pola peminjaman sepeda per jam pada hari kerja dibandingkan hari libur/weekend?**

## Struktur Direktori

```
submission/
├─ dashboard/
│  ├─ main_data.csv       # Data bersih untuk dashboard
│  └─ dashboard.py        # Aplikasi Streamlit
├─ data/
│  ├─ day.csv             # Data harian (731 baris)
│  └─ hour.csv            # Data per jam (17.379 baris)
├─ notebook.ipynb         # Jupyter/Colab Notebook analisis lengkap
├─ README.md              # Dokumentasi ini
├─ requirements.txt       # Daftar library yang digunakan
└─ url.txt                # Link dashboard Streamlit Cloud
```

## Setup Environment

### Langkah Instalasi

1. **Clone atau ekstrak folder submission ini.**

2. **Buat virtual environment (opsional):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install semua dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pastikan dataset ada di folder `data/`:**
   - Download [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)
   - Letakkan `day.csv` dan `hour.csv` di dalam folder `data/`

## Menjalankan Notebook

Buka `notebook.ipynb` menggunakan Jupyter Notebook atau Google Colab:

```bash
jupyter notebook notebook.ipynb
```

Atau upload ke [Google Colab](https://colab.research.google.com) dan jalankan semua sel secara berurutan.

## Menjalankan Dashboard

Setelah `main_data.csv` tersedia di folder `dashboard/`, jalankan dashboard:

```bash
cd submission
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser: `http://localhost:8501`

### Fitur Dashboard

- **Filter interaktif:** Rentang tanggal, musim, dan kondisi cuaca
- **KPI Metrics:** Total peminjaman, rata-rata harian, puncak harian
- **Visualisasi Pertanyaan 1:** Bar chart & box plot pengaruh musim
- **Visualisasi Pertanyaan 2:** Line chart pola per jam & heatmap jam vs musim
- **Analisis tambahan:** Tren bulanan, pengaruh cuaca & suhu, clustering permintaan

## Hasil Analisis Utama

| Musim  | Rata-rata Peminjaman/Hari |
|--------|--------------------------|
| Fall   | ~5.644                   |
| Summer | ~4.992                   |
| Winter | ~4.728                   |
| Spring | ~2.604                   |

- Hari kerja: pola bimodal dengan puncak pukul **08:00** dan **17:00–18:00** (komuter)
- Hari libur: pola unimodal dengan puncak pukul **12:00–14:00** (rekreasi)

## Library yang Digunakan

- **pandas** — manipulasi dan analisis data
- **numpy** — komputasi numerik
- **matplotlib** — visualisasi dasar
- **seaborn** — visualisasi statistik
- **streamlit** — pembuatan dashboard interaktif

## Kontak

- **Nama:** Hasna Nur Saudah
- **Email:** cdcc180d6x1807@student.devacademy.id
- **ID Dicoding:** CDCC180D6X1807
