DELETE FROM projects
WHERE id = %(project_id)s
  AND created_by = %(user_id)s
RETURNING id;