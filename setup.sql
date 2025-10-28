CREATE TABLE "user_groups" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "name" VARCHAR(256) NOT NULL,
  "created_at" TIMESTAMPTZ DEFAULT now(),
  "updated_at" TIMESTAMPTZ DEFAULT now(),
  "deleted_at" TIMESTAMPTZ
);

CREATE TABLE "users" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "user_group_id" INTEGER,
  "line_user_id" VARCHAR(256),
  "email" VARCHAR(256),
  "password" VARCHAR(256),
  "display_name" VARCHAR(100) NOT NULL,
  "created_at" TIMESTAMPTZ DEFAULT now(),
  "updated_at" TIMESTAMPTZ DEFAULT now(),
  "deleted_at" TIMESTAMPTZ,
  FOREIGN KEY ("user_group_id") REFERENCES "user_groups" ("id") ON DELETE CASCADE
);

CREATE TABLE "categories" (
  "id" SERIAL PRIMARY KEY,
  "user_group_id" INTEGER,
  "category_name" VARCHAR(100) NOT NULL DEFAULT 'カテゴリ',
  "month_budget" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMPTZ DEFAULT now(),
  "updated_at" TIMESTAMPTZ DEFAULT now(),
  "deleted_at" TIMESTAMPTZ,
  FOREIGN KEY ("user_group_id") REFERENCES "user_groups" ("id") ON DELETE CASCADE
);

CREATE TABLE "expenses" (
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
  FOREIGN KEY ("user_group_id") REFERENCES "user_groups" ("id") ON DELETE CASCADE,
  FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE SET NULL
);

CREATE TABLE "subscriptions" (
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
  FOREIGN KEY ("user_group_id") REFERENCES "user_groups" ("id") ON DELETE CASCADE,
  FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE SET NULL
);

-- インデックス作成
-- ユーザ
CREATE INDEX "idx_user_group_id" ON "users" ("user_group_id");

-- カテゴリ
CREATE INDEX "idx_category_user_group_id" ON "categories" ("user_group_id");

-- 家計簿
CREATE INDEX "idx_expense_user_group_id" ON "expenses" ("user_group_id");
CREATE INDEX "idx_expense_category_id"   ON "expenses" ("category_id");
CREATE INDEX "idx_expense_occur_date"    ON "expenses" ("occur_date");

-- 固定費
CREATE INDEX "idx_subscription_user_group_id" ON "subscriptions" ("user_group_id");
CREATE INDEX "idx_subscription_category_id"   ON "subscriptions" ("category_id");

-- 同じグループ内でカテゴリ名は一意にしたい場合
ALTER TABLE "categories"
ADD CONSTRAINT "ux_categories_group_name"
UNIQUE ("user_group_id", "category_name");

-- ユーザのemailを一意にしたい場合（全体でユニーク）
ALTER TABLE "users"
ADD CONSTRAINT "ux_user_email" UNIQUE ("email");