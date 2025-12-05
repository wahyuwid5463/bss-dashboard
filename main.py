
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
from datetime import datetime

app = FastAPI(
    title="BSS Tender Intelligence API",
    description="API demo untuk BSS Tender Intelligence (dummy tender Indonesia yang realistis).",
    version="1.0.0",
)

# Izinkan diakses dari mana saja (supaya dashboard Gemeni / HTML bisa fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# DATA DUMMY REALISTIS
# =====================
TENDERS: List[Dict] = [
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

# =========
# ROOT
# =========
@app.get("/")
def root():
    return {
        "message": "BSS Tender Intelligence API",
        "docs": "/docs",
        "datetime": datetime.utcnow().isoformat() + "Z",
    }

# ==========================
# 1) LIST TENDER (utama)
# ==========================
@app.get("/api/tenders")
def list_tenders(
    q: Optional[str] = Query(default=None, description="Cari di nama paket / kode / lokasi"),
    instansi: Optional[str] = Query(default=None, description="Filter berdasarkan instansi"),
    status: Optional[str] = Query(default=None, description="Filter berdasarkan status"),
):
    """
    Endpoint utama yang dipakai dashboard.
    - /api/tenders                 -> semua tender
    - /api/tenders?q=rumah         -> cari kata 'rumah'
    - /api/tenders?status=Evaluasi -> filter status
    """
    q_lower = (q or "").lower()

    def match(t: Dict) -> bool:
        # Search text
        if q_lower:
            if not (
                q_lower in (t.get("nama_paket") or "").lower()
                or q_lower in (t.get("kode") or "").lower()
                or q_lower in (t.get("lokasi") or "").lower()
            ):
                return False

        # Filter instansi (exact match)
        if instansi and t.get("instansi") != instansi:
            return False

        # Filter status (exact match)
        if status and t.get("status") != status:
            return False

        return True

    filtered = [t for t in TENDERS if match(t)]
    return {
        "count": len(filtered),
        "items": filtered,
    }

# ============================================
# 2) DETAIL TENDER (pakai QUERY, bukan path)
# ============================================
@app.get("/api/tender-detail")
def tender_detail(
    kode: str = Query(..., description="Kode tender, contoh: DUMMY-001/2025"),
):
    """
    Karena kode mengandung '/', kita pakai query:
    /api/tender-detail?kode=DUMMY-001/2025
    """
    for t in TENDERS:
        if t.get("kode") == kode:
            return t
    raise HTTPException(status_code=404, detail="Tender tidak ditemukan")

# ==========================
# 3) SEARCH (shortcut)
# ==========================
@app.get("/api/search")
def search_tenders(
    q: str = Query(..., description="Kata kunci pencarian"),
):
    """
    Shortcut dari /api/tenders?q=
    /api/search?q=rumah
    """
    q_lower = q.lower()
    results = [
        t
        for t in TENDERS
        if q_lower in (t.get("nama_paket") or "").lower()
        or q_lower in (t.get("kode") or "").lower()
        or q_lower in (t.get("lokasi") or "").lower()
    ]
    return {
        "query": q,
        "count": len(results),
        "items": results,
    }

# ==========================
# 4) STATISTIK (untuk kartu)
# ==========================
@app.get("/api/stats")
def tender_stats():
    total_tender = len(TENDERS)
    total_pagu = sum(t.get("nilai_pagu", 0) for t in TENDERS)
    instansi_set = {t.get("instansi") for t in TENDERS if t.get("instansi")}
    status_count: Dict[str, int] = {}
    for t in TENDERS:
        s = t.get("status") or "Tidak Diketahui"
        status_count[s] = status_count.get(s, 0) + 1

    return {
        "total_tender": total_tender,
        "total_pagu": total_pagu,
        "jumlah_instansi": len(instansi_set),
        "by_status": status_count,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
