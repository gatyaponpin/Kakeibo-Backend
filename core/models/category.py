from django.db import models

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_group = models.ForeignKey(
        "core.UserGroup",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="categories"
    )
    category_name = models.CharField(max_length=100, default="カテゴリ")
    month_budget = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "categories"
        indexes = [
            models.Index(fields=["user_group"], name="idx_category_user_group_id"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user_group", "category_name"],
                name="ux_categories_group_name"
            ),
        ]

    def __str__(self):
        return self.category_name
