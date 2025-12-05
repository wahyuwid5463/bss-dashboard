from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="BSS Tender Intelligence API",
    description="API demo untuk BSS Tender Intelligence (dummy tender Indonesia yang realistis).",
    version="1.0.0",
)

# Izinkan diakses dari mana saja (supaya dashboard Gemini / HTML bisa fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# DATA DUMMY REALISTIS
# ======================

TENDERS = [
    {
        "kode": "PU-001/2025",
        "nama_paket": "Pembangunan Rumah Sakit Tk. IV Asmir Kodam IV Diponegoro",
        "instansi": "Kementerian PUPR",
        "lokasi": "Semarang, Jawa Tengah",
        "nilai_pagu": 95000000000,
        "status": "Pengumuman",
        "sumber": "LPSE",
        "isNew": True,
        "link": "https://lpse.example.go.id/tender/pu-001-2025",
    },
    {
        "kode": "KES-002/2025",
        "nama_paket": "Pengadaan Sistem Server Rumah Sakit Nasional",
        "instansi": "Kementerian Kesehatan",
        "lokasi": "Jakarta",
        "nilai_pagu": 5200000000,
        "status": "Evaluasi",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/kes-002-2025",
    },
    {
        "kode": "PU-003/2025",
        "nama_paket": "Peningkatan Jalan Nasional Ruas Bandung – Tasikmalaya",
        "instansi": "Kementerian PUPR",
        "lokasi": "Bandung, Jawa Barat",
        "nilai_pagu": 120000000000,
        "status": "Selesai",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/pu-003-2025",
    },
    {
        "kode": "HUB-004/2025",
        "nama_paket": "Pembangunan Terminal Tipe A dan Area Parkir Terpadu",
        "instansi": "Kementerian Perhubungan",
        "lokasi": "Surabaya, Jawa Timur",
        "nilai_pagu": 43000000000,
        "status": "Pengumuman",
        "sumber": "LPSE",
        "isNew": True,
        "link": "https://lpse.example.go.id/tender/hub-004-2025",
    },
    {
        "kode": "HUB-005/2025",
        "nama_paket": "Pengadaan Sistem ITS (Intelligent Transport System) Jalan Tol",
        "instansi": "Kementerian Perhubungan",
        "lokasi": "Jabodetabek",
        "nilai_pagu": 27500000000,
        "status": "Evaluasi",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/hub-005-2025",
    },
    {
        "kode": "PLN-006/2025",
        "nama_paket": "EPC Pembangunan Gardu Induk 150 kV dan Jaringan Transmisi",
        "instansi": "PT PLN (Persero)",
        "lokasi": "Makassar, Sulawesi Selatan",
        "nilai_pagu": 68000000000,
        "status": "Pengumuman",
        "sumber": "BUMN",
        "isNew": True,
        "link": "https://eproc.pln.example.id/tender/pln-006-2025",
    },
    {
        "kode": "PLN-007/2025",
        "nama_paket": "Pengadaan Pembangkit Listrik Tenaga Surya Atap (PLTS Rooftop)",
        "instansi": "PT PLN (Persero)",
        "lokasi": "Bali",
        "nilai_pagu": 15500000000,
        "status": "Evaluasi",
        "sumber": "BUMN",
        "isNew": False,
        "link": "https://eproc.pln.example.id/tender/pln-007-2025",
    },
    {
        "kode": "PERT-008/2025",
        "nama_paket": "Jasa Kontraktor EPC Pembangunan Tangki BBM Terintegrasi",
        "instansi": "PT Pertamina (Persero)",
        "lokasi": "Balikpapan, Kalimantan Timur",
        "nilai_pagu": 210000000000,
        "status": "Pengumuman",
        "sumber": "BUMN",
        "isNew": True,
        "link": "https://eproc.pertamina.example.id/tender/pert-008-2025",
    },
    {
        "kode": "PERT-009/2025",
        "nama_paket": "Rehabilitasi Jaringan Pipa Bahan Bakar Utama",
        "instansi": "PT Pertamina (Persero)",
        "lokasi": "Jawa Barat",
        "nilai_pagu": 87000000000,
        "status": "Evaluasi",
        "sumber": "BUMN",
        "isNew": False,
        "link": "https://eproc.pertamina.example.id/tender/pert-009-2025",
    },
    {
        "kode": "JSM-010/2025",
        "nama_paket": "Pembangunan Jalan Tol Lingkar Luar Kota Tahap II",
        "instansi": "PT Jasa Marga (Persero) Tbk",
        "lokasi": "Jakarta",
        "nilai_pagu": 350000000000,
        "status": "Pengumuman",
        "sumber": "BUMN",
        "isNew": True,
        "link": "https://eproc.jasamarga.example.id/tender/jsm-010-2025",
    },
    {
        "kode": "JSM-011/2025",
        "nama_paket": "Pemeliharaan Berkala Jalan Tol dan Rest Area",
        "instansi": "PT Jasa Marga (Persero) Tbk",
        "lokasi": "Jawa Tengah & Jawa Timur",
        "nilai_pagu": 42000000000,
        "status": "Selesai",
        "sumber": "BUMN",
        "isNew": False,
        "link": "https://eproc.jasamarga.example.id/tender/jsm-011-2025",
    },
    {
        "kode": "PEL-012/2025",
        "nama_paket": "Pengembangan Terminal Peti Kemas dan Dermaga Multipurpose",
        "instansi": "PT Pelabuhan Indonesia (Persero)",
        "lokasi": "Medan, Sumatera Utara",
        "nilai_pagu": 138000000000,
        "status": "Pengumuman",
        "sumber": "BUMN",
        "isNew": True,
        "link": "https://eproc.pelindo.example.id/tender/pel-012-2025",
    },
    {
        "kode": "ASDP-013/2025",
        "nama_paket": "Pengadaan Kapal Ro-Ro Penyeberangan Antar Pulau",
        "instansi": "PT ASDP Indonesia Ferry (Persero)",
        "lokasi": "Nusa Tenggara Timur",
        "nilai_pagu": 96000000000,
        "status": "Evaluasi",
        "sumber": "BUMN",
        "isNew": False,
        "link": "https://eproc.asdp.example.id/tender/asdp-013-2025",
    },
    {
        "kode": "PAR-014/2025",
        "nama_paket": "Pengembangan Kawasan Pariwisata Strategis Nasional",
        "instansi": "Kementerian Pariwisata dan Ekonomi Kreatif",
        "lokasi": "Labuan Bajo, Nusa Tenggara Timur",
        "nilai_pagu": 54000000000,
        "status": "Pengumuman",
        "sumber": "LPSE",
        "isNew": True,
        "link": "https://lpse.example.go.id/tender/par-014-2025",
    },
    {
        "kode": "KOM-015/2025",
        "nama_paket": "Pengadaan Infrastruktur Jaringan Serat Optik Nasional Tahap III",
        "instansi": "Kementerian Komunikasi dan Informatika",
        "lokasi": "Sulawesi & Maluku",
        "nilai_pagu": 165000000000,
        "status": "Evaluasi",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/kom-015-2025",
    },
]


# ======================
# ROUTES
# ======================

@app.get("/")
def root():
    """Healthcheck sederhana untuk ngecek API hidup."""
    return {
        "status": "ok",
        "message": "BSS Tender Intelligence API berjalan",
        "time": datetime.utcnow().isoformat() + "Z",
        "count": len(TENDERS),
    }


@app.get("/api/tenders")
def get_tenders():
    """Endpoint utama yang dipakai Dashboard BSS."""
    return TENDERS

