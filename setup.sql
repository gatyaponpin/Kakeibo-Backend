CREATE TABLE "ユーザグループテーブル" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" VARCHAR(256) NOT NULL,
  "created_at" TIMESTAMPTZ DEFAULT now(),
  "updated_at" TIMESTAMPTZ DEFAULT now(),
  "deleted_at" TIMESTAMPTZ
);

CREATE TABLE "ユーザテーブル" (
  "id" SERIAL NOT NULL PRIMARY KEY,
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

CREATE TABLE "カテゴリーテーブル" (
  "id" SERIAL PRIMARY KEY,
  "user_group_id" INTEGER,
  "category_name" VARCHAR(100) NOT NULL DEFAULT 'カテゴリ',
  "month_budget" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMPTZ DEFAULT now(),
  "updated_at" TIMESTAMPTZ DEFAULT now(),
  "deleted_at" TIMESTAMPTZ,
  FOREIGN KEY ("user_group_id") REFERENCES "ユーザグループテーブル" ("id") ON DELETE CASCADE
);

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

-- インデックス作成
-- ユーザ
CREATE INDEX "idx_ユーザ_user_group_id" ON "ユーザテーブル" ("user_group_id");

-- カテゴリ
CREATE INDEX "idx_カテゴリ_user_group_id" ON "カテゴリーテーブル" ("user_group_id");

-- 家計簿
CREATE INDEX "idx_家計簿_user_group_id" ON "家計簿テーブル" ("user_group_id");
CREATE INDEX "idx_家計簿_category_id"   ON "家計簿テーブル" ("category_id");
CREATE INDEX "idx_家計簿_occur_date"    ON "家計簿テーブル" ("occur_date");

-- 予算
CREATE INDEX "idx_予算_user_group_id" ON "予算テーブル" ("user_group_id");
CREATE INDEX "idx_予算_category_id"   ON "予算テーブル" ("category_id");

-- 固定費
CREATE INDEX "idx_固定費_user_group_id" ON "固定費テーブル" ("user_group_id");
CREATE INDEX "idx_固定費_category_id"   ON "固定費テーブル" ("category_id");

-- 同じグループ内でカテゴリ名は一意にしたい場合
ALTER TABLE "カテゴリーテーブル"
ADD CONSTRAINT "ux_カテゴリ_group_name"
UNIQUE ("user_group_id", "category_name");

-- ユーザのemailを一意にしたい場合（全体でユニーク）
ALTER TABLE "ユーザテーブル"
ADD CONSTRAINT "ux_ユーザ_email" UNIQUE ("email");