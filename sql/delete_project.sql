DELETE FROM projects
WHERE id = ANY(%(project_ids)s)
  AND created_by = %(user_id)s
RETURNING id;