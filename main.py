from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any

app = FastAPI(
    title="BSS Tender Intelligence API",
    description="API demo untuk BSS Tender Intelligence (dummy tender Indonesia yang realistis).",
    version="1.0.0",
)

# =====================================================
# CORS (supaya bisa diakses dari Gemini / HTML Dashboard)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Nanti bisa dibatasi ke domain BSS saja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DATA DUMMY REALISTIS
# =====================================================
TENDERS: List[Dict[str, Any]] = [
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
        "tahun": 2025,
        "tanggal_update": "2025-01-15",
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
        "tahun": 2025,
        "tanggal_update": "2025-01-10",
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
        "tahun": 2025,
        "tanggal_update": "2025-01-05",
    },
]

# =====================================================
# HELPER: FILTER & SORT
# =====================================================
def filter_tenders(
    q: Optional[str] = None,
    instansi: Optional[str] = None,
    lokasi: Optional[str] = None,
    status: Optional[str] = None,
    sumber: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = TENDERS

    if q:
        q_lower = q.lower()
        results = [
            t for t in results
            if q_lower in t["nama_paket"].lower()
            or q_lower in t["kode"].lower()
            or q_lower in t["instansi"].lower()
            or q_lower in t["lokasi"].lower()
        ]

    if instansi:
        results = [t for t in results if t["instansi"] == instansi]

    if lokasi:
        results = [t for t in results if t["lokasi"] == lokasi]

    if status:
        results = [t for t in results if t["status"] == status]

    if sumber:
        results = [t for t in results if t["sumber"] == sumber]

    return results


def sort_tenders(
    tenders: List[Dict[str, Any]],
    sort_by: Optional[str],
    sort_dir: Literal["asc", "desc"],
) -> List[Dict[str, Any]]:
    if not sort_by:
        return tenders

    if sort_by not in {"nilai_pagu", "nama_paket", "instansi", "lokasi", "status"}:
        return tenders

    reverse = sort_dir == "desc"
    return sorted(
        tenders,
        key=lambda t: t.get(sort_by) or 0,
        reverse=reverse,
    )


# =====================================================
# ROOT (INFO) – https://bss-tender-api.vercel.app/
# =====================================================
@app.get("/")
async def root_info():
    return {
        "service": "BSS Tender Intelligence API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "docs": {
            "openapi": "/openapi.json",
            "swagger_ui": "/docs",
            "redoc": "/redoc",
        },
        "endpoints": {
            "list_tenders": "/api/tenders",
            "detail_tender": "/api/tenders/{kode}",
            "search": "/api/search",
            "stats": "/api/stats",
            "instansi": "/api/instansi",
            "lokasi": "/api/lokasi",
            "status": "/api/status",
        },
    }


# =====================================================
# 1. LIST TENDER – /api/tenders
# =====================================================
@app.get("/api/tenders")
async def get_tenders(
    q: Optional[str] = Query(None, description="Search nama/kode/instansi/lokasi"),
    instansi: Optional[str] = Query(None),
    lokasi: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    sumber: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field: nilai_pagu | nama_paket | instansi | lokasi | status",
    ),
    sort_dir: Literal["asc", "desc"] = Query("desc"),
):
    filtered = filter_tenders(q, instansi, lokasi, status, sumber)
    sorted_data = sort_tenders(filtered, sort_by, sort_dir)

    paged = sorted_data[offset: offset + limit]

    return {
        "meta": {
            "total": len(filtered),
            "count": len(paged),
            "limit": limit,
            "offset": offset,
        },
        "data": paged,
    }


# =====================================================
# 2. DETAIL TENDER – /api/tenders/{kode}
# =====================================================
@app.get("/api/tenders/{kode}")
async def get_tender_by_kode(kode: str):
    for t in TENDERS:
        if t["kode"] == kode:
            return t
    raise HTTPException(status_code=404, detail="Tender tidak ditemukan")


# =====================================================
# 3. SEARCH – /api/search?q=...
# (shortcut dari /api/tenders dengan hanya parameter q)
# =====================================================
@app.get("/api/search")
async def search_tenders(
    q: str = Query(..., description="Kata kunci nama/kode/instansi/lokasi"),
    limit: int = Query(50, ge=1, le=200),
):
    filtered = filter_tenders(q=q)
    return {
        "meta": {
            "query": q,
            "total": len(filtered),
            "limit": limit,
        },
        "data": filtered[:limit],
    }


# =====================================================
# 4. STATS – /api/stats
# =====================================================
@app.get("/api/stats")
async def get_stats():
    total = len(TENDERS)
    total_pagu = sum(t["nilai_pagu"] for t in TENDERS)
    instansi_set = {t["instansi"] for t in TENDERS}
    lokasi_set = {t["lokasi"] for t in TENDERS}

    by_status: Dict[str, Dict[str, Any]] = {}
    for t in TENDERS:
        key = t["status"]
        if key not in by_status:
            by_status[key] = {"status": key, "jumlah": 0, "total_pagu": 0}
        by_status[key]["jumlah"] += 1
        by_status[key]["total_pagu"] += t["nilai_pagu"]

    return {
        "total_tender": total,
        "total_nilai_pagu": total_pagu,
        "jumlah_instansi": len(instansi_set),
        "jumlah_lokasi": len(lokasi_set),
        "by_status": list(by_status.values()),
    }


# =====================================================
# 5. INSTANSI – /api/instansi
# =====================================================
@app.get("/api/instansi")
async def get_instansi_stats():
    result: Dict[str, Dict[str, Any]] = {}

    for t in TENDERS:
        key = t["instansi"]
        if key not in result:
            result[key] = {
                "instansi": key,
                "jumlah_tender": 0,
                "total_nilai_pagu": 0,
            }
        result[key]["jumlah_tender"] += 1
        result[key]["total_nilai_pagu"] += t["nilai_pagu"]

    return {
        "total_instansi": len(result),
        "data": list(result.values()),
    }


# =====================================================
# 6. LOKASI – /api/lokasi
# =====================================================
@app.get("/api/lokasi")
async def get_lokasi_stats():
    result: Dict[str, Dict[str, Any]] = {}

    for t in TENDERS:
        key = t["lokasi"]
        if key not in result:
            result[key] = {
                "lokasi": key,
                "jumlah_tender": 0,
                "total_nilai_pagu": 0,
            }
        result[key]["jumlah_tender"] += 1
        result[key]["total_nilai_pagu"] += t["nilai_pagu"]

    return {
        "total_lokasi": len(result),
        "data": list(result.values()),
    }


# =====================================================
# 7. STATUS – /api/status
# =====================================================
@app.get("/api/status")
async def get_status_distribution():
    result: Dict[str, int] = {}

    for t in TENDERS:
        key = t["status"]
        result[key] = result.get(key, 0) + 1

    return {
        "total_tender": len(TENDERS),
        "data": [{"status": k, "jumlah": v} for k, v in result.items()],
    }
