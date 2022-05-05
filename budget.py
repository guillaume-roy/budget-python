from db_utils import select

def get_expense_for_month(year, month):
    return select("""
        select COALESCE(c2.label, c.label) as category_label, SUM(t.amount) as amount
        from transactions t
        LEFT OUTER JOIN category_patterns cp on t.category_pattern_id = cp.id
        LEFT OUTER JOIN categories c on cp.category_id = c.id
        LEFT OUTER JOIN categories c2 ON t.category_id = c2.id
        WHERE t.month = ? and t.year = ?
        GROUP BY COALESCE(c2.label, c.label)
        ORDER BY category_label
        """, (int(month), int(year),))

def get_budget_for_month(year, month):
    return select("""
        select COALESCE(c2.label, c.label) as category_label, SUM(t.amount) as amount
        from transactions t
        LEFT OUTER JOIN category_patterns cp on t.category_pattern_id = cp.id
        LEFT OUTER JOIN categories c on cp.category_id = c.id
        LEFT OUTER JOIN categories c2 ON t.category_id = c2.id
        WHERE t.month = ? and t.year = ?
        GROUP BY COALESCE(c2.label, c.label)
        ORDER BY category_label
        """, (int(month), int(year),))
