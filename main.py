from fastapi import FastAPI, HTTPException
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

# =====================================
# DATA DUMMY REALISTIS
# =====================================
TENDERS = [
    {
        "kode": "DUMMY-001/2025",
        "nama_paket": "Pembangunan Rumah Sakit Tk. IV Asmir Kodam IV Diponegoro",
        "instansi": "Kementerian PUPR",
        "lokasi": "Semarang, Jawa Tengah",
        "nilai_pagu": 95_000_000_000,
        "status": "Pengumuman",
        "sumber": "LPSE",
        "isNew": True,
        "link": "https://lpse.example.go.id/tender/1",
    },
    {
        "kode": "DUMMY-002/2025",
        "nama_paket": "Pengadaan Sistem Server Rumah Sakit",
        "instansi": "Kementerian Kesehatan",
        "lokasi": "Jakarta",
        "nilai_pagu": 5_200_000_000,
        "status": "Evaluasi",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/2",
    },
    {
        "kode": "DUMMY-003/2025",
        "nama_paket": "Tender Konstruksi Jalan Tol Jawa Barat",
        "instansi": "Kementerian PUPR",
        "lokasi": "Bandung, Jawa Barat",
        "nilai_pagu": 120_000_000_000,
        "status": "Selesai",
        "sumber": "LPSE",
        "isNew": False,
        "link": "https://lpse.example.go.id/tender/3",
    },
]

# =====================================
# UTIL & HEALTH CHECK
# =====================================

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "bss-tender-api",
        "time": datetime.utcnow().isoformat() + "Z",
    }


def _filter_tenders(
    q: str | None = None,
    instansi: str | None = None,
    status: str | None = None,
    min_pagu: int | None = None,
    max_pagu: int | None = None,
):
    """Filter list tender berdasarkan query."""
    results = TENDERS

    if q:
        q_low = q.lower()
        results = [
            t for t in results
            if q_low in t["nama_paket"].lower()
            or q_low in t["kode"].lower()
            or q_low in t["lokasi"].lower()
        ]

    if instansi:
        results = [t for t in results if t["instansi"] == instansi]

    if status:
        results = [t for t in results if t["status"] == status]

    if min_pagu is not None:
        results = [t for t in results if t["nilai_pagu"] >= min_pagu]

    if max_pagu is not None:
        results = [t for t in results if t["nilai_pagu"] <= max_pagu]

    return results


def _get_tender_by_kode(kode: str):
    for t in TENDERS:
        if t["kode"] == kode:
            return t
    return None


# =====================================
# ENDPOINT UTAMA
# =====================================

# 1) LIST + FILTER
@app.get("/api/tenders")
def get_tenders(
    q: str | None = None,
    instansi: str | None = None,
    status: str | None = None,
    min_pagu: int | None = None,
    max_pagu: int | None = None,
):
    """
    Contoh:
    - /api/tenders
    - /api/tenders?q=rumah
    - /api/tenders?instansi=Kementerian%20PUPR
    - /api/tenders?status=Pengumuman&min_pagu=1000000000
    """
    return _filter_tenders(q, instansi, status, min_pagu, max_pagu)


# 2) DETAIL BY PATH → /api/tenders/DUMMY-001/2025
@app.get("/api/tenders/{kode}")
def get_tender_detail_path(kode: str):
    tender = _get_tender_by_kode(kode)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender tidak ditemukan")
    return tender


# 3) DETAIL BY QUERY → /api/tender-detail?kode=DUMMY-001/2025
#    (biar cocok sama URL yang tadi bro pakai)
@app.get("/api/tender-detail")
def get_tender_detail_query(kode: str):
    tender = _get_tender_by_kode(kode)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender tidak ditemukan")
    return tender


# 4) SEARCH KHUSUS → /api/search?q=rumah
@app.get("/api/search")
def search_tenders(q: str):
    return _filter_tenders(q=q)


# 5) STATISTIK → /api/stats
@app.get("/api/stats")
def get_stats():
    total_tender = len(TENDERS)
    total_nilai_pagu = sum(t["nilai_pagu"] for t in TENDERS)
    instansi_set = {t["instansi"] for t in TENDERS}

    by_status: dict[str, int] = {}
    for t in TENDERS:
        s = t["status"]
        by_status[s] = by_status.get(s, 0) + 1

    by_instansi: dict[str, int] = {}
    for t in TENDERS:
        i = t["instansi"]
        by_instansi[i] = by_instansi.get(i, 0) + 1

    return {
        "total_tender": total_tender,
        "total_nilai_pagu": total_nilai_pagu,
        "jumlah_instansi": len(instansi_set),
        "by_status": by_status,
        "by_instansi": by_instansi,
        "last_update": datetime.utcnow().isoformat() + "Z",
    }

