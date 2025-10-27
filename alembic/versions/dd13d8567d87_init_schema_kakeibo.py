from alembic import op

# revision identifiers, used by Alembic.
revision = "init_kakeibo"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    -- ユーザグループテーブル
    CREATE TABLE "ユーザグループテーブル" (
      "id" SERIAL PRIMARY KEY NOT NULL,
      "name" VARCHAR(256) NOT NULL,
      "created_at" TIMESTAMPTZ DEFAULT now(),
      "updated_at" TIMESTAMPTZ DEFAULT now(),
      "deleted_at" TIMESTAMPTZ
    );

    -- ユーザテーブル
    CREATE TABLE "ユーザテーブル" (
      "id" SERIAL PRIMARY KEY NOT NULL,
      "user_group_id" INTEGER,
      "line_user_id" VARCHAR(256),
      "email" VARCHAR(256),
      "password" VARCHAR(256),
      "display_name" VARCHAR(100) NOT NULL,
      "created_at" TIMESTAMPTZ DEFAULT now(),
      "updated_at" TIMESTAMPTZ DEFAULT now(),
      "deleted_at" TIMESTAMPTZ,
      FOREIGN KEY ("user_group_id") REFERENCES "ユーザグループテーブル" ("id") ON DELETE CASCADE
    );

    -- カテゴリーテーブル（月予算額あり）
    CREATE TABLE "カテゴリーテーブル" (
      "id" SERIAL PRIMARY KEY,
      "user_group_id" INTEGER,
      "category_name" VARCHAR(100) NOT NULL DEFAULT 'カテゴリ',
      "balance_kind" SMALLINT NOT NULL DEFAULT 0,
      "month_amount" INTEGER NOT NULL DEFAULT 0,
      "created_at" TIMESTAMPTZ DEFAULT now(),
      "updated_at" TIMESTAMPTZ DEFAULT now(),
      "deleted_at" TIMESTAMPTZ,
      FOREIGN KEY ("user_group_id") REFERENCES "ユーザグループテーブル" ("id") ON DELETE CASCADE
    );

    -- 家計簿テーブル
    CREATE TABLE "家計簿テーブル" (
      "id" SERIAL PRIMARY KEY,
      "user_group_id" INTEGER,
      "category_id" INTEGER,
      "balance_kind" SMALLINT NOT NULL DEFAULT 0,
      "balance_name" VARCHAR(20),
      "amount" INTEGER NOT NULL DEFAULT 0,
      "memo" VARCHAR(256),
      "occur_date" DATE NOT NULL DEFAULT CURRENT_DATE,
      "created_at" TIMESTAMPTZ DEFAULT now(),
      "updated_at" TIMESTAMPTZ DEFAULT now(),
      "deleted_at" TIMESTAMPTZ,
      FOREIGN KEY ("user_group_id") REFERENCES "ユーザグループテーブル" ("id") ON DELETE CASCADE,
      FOREIGN KEY ("category_id") REFERENCES "カテゴリーテーブル" ("id") ON DELETE SET NULL
    );

    -- 固定費テーブル
    CREATE TABLE "固定費テーブル" (
      "id" SERIAL PRIMARY KEY,
      "user_group_id" INTEGER,
      "category_id" INTEGER,
      "balance_kind" SMALLINT NOT NULL DEFAULT 0,
      "balance_name" VARCHAR(20),
      "billing_day" INTEGER NOT NULL DEFAULT 0,
      "amount" INTEGER DEFAULT 0,
      "created_at" TIMESTAMPTZ DEFAULT now(),
      "updated_at" TIMESTAMPTZ DEFAULT now(),
      "deleted_at" TIMESTAMPTZ,
      FOREIGN KEY ("user_group_id") REFERENCES "ユーザグループテーブル" ("id") ON DELETE CASCADE,
      FOREIGN KEY ("category_id") REFERENCES "カテゴリーテーブル" ("id") ON DELETE SET NULL
    );

    -- 推奨インデックス
    CREATE INDEX "idx_ユーザ_user_group_id"     ON "ユーザテーブル" ("user_group_id");
    CREATE INDEX "idx_カテゴリ_user_group_id"   ON "カテゴリーテーブル" ("user_group_id");
    CREATE INDEX "idx_家計簿_user_group_id"     ON "家計簿テーブル" ("user_group_id");
    CREATE INDEX "idx_家計簿_category_id"       ON "家計簿テーブル" ("category_id");
    CREATE INDEX "idx_家計簿_occur_date"        ON "家計簿テーブル" ("occur_date");
    CREATE INDEX "idx_固定費_user_group_id"     ON "固定費テーブル" ("user_group_id");
    CREATE INDEX "idx_固定費_category_id"       ON "固定費テーブル" ("category_id");
    """)

def downgrade():
    op.execute("""
    DROP TABLE IF EXISTS "固定費テーブル";
    DROP TABLE IF EXISTS "家計簿テーブル";
    DROP TABLE IF EXISTS "カテゴリーテーブル";
    DROP TABLE IF EXISTS "ユーザテーブル";
    DROP TABLE IF EXISTS "ユーザグループテーブル";
    """)
