from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.core.db import get_conn
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

TABLE = 'カテゴリーテーブル'  # quoted in SQL

def row_to_category(row) -> Category:
    # 順序は SELECT に合わせる
    return Category(
        id=row[0],
        user_group_id=row[1],
        category_name=row[2],
        balance_kind=row[3],
        month_budget=row[4],
        created_at=row[5],
        updated_at=row[6],
        deleted_at=row[7],
    )

@router.get("", response_model=List[Category])
def list_categories(
    user_group_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    sql = f'''
        SELECT
          "id","user_group_id","category_name","balance_kind","月予算額",
          "created_at","updated_at","deleted_at"
        FROM "{TABLE}"
    '''
    params = []
    if user_group_id is not None:
        sql += ' WHERE "user_group_id" = %s'
        params.append(user_group_id)
    sql += ' ORDER BY "id" DESC LIMIT %s OFFSET %s'
    params.extend([limit, offset])

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [row_to_category(r) for r in rows]

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'''
            SELECT "id","user_group_id","category_name","balance_kind","月予算額",
                   "created_at","updated_at","deleted_at"
            FROM "{TABLE}" WHERE "id" = %s
        ''', (category_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "category not found")
    return row_to_category(row)

@router.post("", response_model=Category, status_code=201)
def create_category(payload: CategoryCreate):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO "{TABLE}"
                ("user_group_id","category_name","balance_kind","月予算額")
            VALUES (%s,%s,%s,%s)
            RETURNING "id","user_group_id","category_name","balance_kind","月予算額",
                      "created_at","updated_at","deleted_at"
        ''', (
            payload.user_group_id,
            payload.category_name,
            payload.balance_kind,
            payload.month_budget,
        ))
        row = cur.fetchone()
        conn.commit()
    return row_to_category(row)

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, payload: CategoryUpdate):
    # 動的UPDATE（与えられた項目のみ）
    sets = []
    params = []
    mapping = {
        "user_group_id": '"user_group_id"',
        "category_name": '"category_name"',
        "balance_kind": '"balance_kind"',
        "month_budget": '"月予算額"',
    }
    for field, col in mapping.items():
        val = getattr(payload, field)
        if val is not None:
            sets.append(f"{col} = %s")
            params.append(val)
    if not sets:
        # 何も更新がなければ現在の値を返す
        return get_category(category_id)

    sql = f'UPDATE "{TABLE}" SET ' + ", ".join(sets) + ', "updated_at" = now() WHERE "id" = %s RETURNING ' \
          + '"id","user_group_id","category_name","balance_kind","月予算額","created_at","updated_at","deleted_at"'
    params.append(category_id)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, "category not found")
        conn.commit()
    return row_to_category(row)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(f'DELETE FROM "{TABLE}" WHERE "id" = %s', (category_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "category not found")
        conn.commit()
    return