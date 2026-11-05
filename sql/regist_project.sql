INSERT INTO projects (
    name,
    description,
    start_date,
    end_date,
    status,
    created_by
)
VALUES (
    %(name)s,
    %(description)s,
    %(start_date)s,
    %(end_date)s,
    %(status)s,
    %(created_by)s
)
RETURNING id;