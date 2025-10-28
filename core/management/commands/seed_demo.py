from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import UserGroup, User, Category, Expense, Subscription
from datetime import date

class Command(BaseCommand):
    help = "Demo data seeder"

    def handle(self, *args, **options):
        # 1) グループ
        group, _ = UserGroup.objects.get_or_create(name="Demo Group")

        # 2) ログインユーザー（emailでログイン）
        user, created = User.objects.get_or_create(
            email="demo@example.com",
            defaults=dict(display_name="Demo User", user_group=group, is_active=True),
        )
        if created:
            user.set_password("demo12345")  # ← 仮パスワード
            user.save()

        # 3) カテゴリ
        food, _ = Category.objects.get_or_create(user_group=group, category_name="食費", defaults={"month_budget": 30000})
        util, _ = Category.objects.get_or_create(user_group=group, category_name="光熱費", defaults={"month_budget": 10000})

        # 4) 定期支出（subscriptions）
        Subscription.objects.get_or_create(
            user_group=group, category=util, balance_kind=1, balance_name="電気",
            defaults=dict(billing_day=25, amount=6000)
        )
        Subscription.objects.get_or_create(
            user_group=group, category=util, balance_kind=1, balance_name="水道",
            defaults=dict(billing_day=20, amount=3000)
        )

        # 5) 家計簿明細（expenses）
        Expense.objects.get_or_create(
            user_group=group, category=food, balance_kind=0, balance_name="コンビニ",
            amount=850, occur_date=date.today()
        )
        Expense.objects.get_or_create(
            user_group=group, category=food, balance_kind=0, balance_name="スーパー",
            amount=1840, occur_date=date.today()
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
        self.stdout.write(self.style.WARNING("Login: demo@example.com / demo12345"))