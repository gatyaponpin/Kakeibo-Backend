from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from app.core.db import get_conn
from app.schemas.kakeibo import Kakeibo, KakeiboCreate, KakeiboUpdate

router = APIRouter(prefix="/kakeibo", tags=["kakeibo"])

TABLE = '家計簿テーブル'

def row_to_kakeibo(row) -> Kakeibo:
    return Kakeibo(
        id=row[0],
        user_group_id=row[1],
        category_id=row[2],
        balance_kind=row[3],
        balance_name=row[4],
        amount=row[5],
        memo=row[6],
        occur_date=row[7],
        created_at=row[8],
        updated_at=row[9],
        deleted_at=row[10],
    )

@router.get("", response_model=List[Kakeibo])
def list_kakeibo(
    user_group_id: Optional[int] = None,
    category_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    sql = f'''
        SELECT
          "id","user_group_id","category_id","balance_kind","balance_name",
          "amount","memo","occur_date","created_at","updated_at","deleted_at"
        FROM "{TABLE}"
    '''
    where = []
    params = []
    if user_group_id is not None:
        where.append('"user_group_id" = %s'); params.append(user_group_id)
    if category_id is not None:
        where.append('"category_id" = %s'); params.append(category_id)
    if date_from is not None:
        where.append('"occur_date" >= %s'); params.append(date_from)
    if date_to is not None:
        where.append('"occur_date" <= %s'); params.append(date_to)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += ' ORDER BY "occur_date" DESC, "id" DESC LIMIT %s OFFSET %s'
    params.extend([limit, offset])

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [row_to_kakeibo(r) for r in rows]

@router.get("/{entry_id}", response_model=Kakeibo)
def get_kakeibo(entry_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'''
            SELECT "id","user_group_id","category_id","balance_kind","balance_name",
                   "amount","memo","occur_date","created_at","updated_at","deleted_at"
            FROM "{TABLE}" WHERE "id" = %s
        ''', (entry_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "entry not found")
    return row_to_kakeibo(row)

@router.post("", response_model=Kakeibo, status_code=201)
def create_kakeibo(payload: KakeiboCreate):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO "{TABLE}"
                ("user_group_id","category_id","balance_kind","balance_name",
                 "amount","memo","occur_date")
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING "id","user_group_id","category_id","balance_kind","balance_name",
                      "amount","memo","occur_date","created_at","updated_at","deleted_at"
        ''', (
            payload.user_group_id,
            payload.category_id,
            payload.balance_kind,
            payload.balance_name,
            payload.amount,
            payload.memo,
            payload.occur_date,
        ))
        row = cur.fetchone()
        conn.commit()
    return row_to_kakeibo(row)

@router.put("/{entry_id}", response_model=Kakeibo)
def update_kakeibo(entry_id: int, payload: KakeiboUpdate):
    sets = []
    params = []
    mapping = {
        "user_group_id": '"user_group_id"',
        "category_id": '"category_id"',
        "balance_kind": '"balance_kind"',
        "balance_name": '"balance_name"',
        "amount": '"amount"',
        "memo": '"memo"',
        "occur_date": '"occur_date"',
    }
    for field, col in mapping.items():
        val = getattr(payload, field)
        if val is not None:
            sets.append(f"{col} = %s")
            params.append(val)

    if not sets:
        return get_kakeibo(entry_id)

    sql = f'UPDATE "{TABLE}" SET ' + ", ".join(sets) + ', "updated_at" = now() WHERE "id" = %s ' \
          + 'RETURNING "id","user_group_id","category_id","balance_kind","balance_name",' \
          + '"amount","memo","occur_date","created_at","updated_at","deleted_at"'
    params.append(entry_id)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, "entry not found")
        conn.commit()
    return row_to_kakeibo(row)

@router.delete("/{entry_id}", status_code=204)
def delete_kakeibo(entry_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'DELETE FROM "{TABLE}" WHERE "id" = %s', (entry_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "entry not found")
        conn.commit()
    return
