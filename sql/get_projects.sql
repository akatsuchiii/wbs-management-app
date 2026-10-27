SELECT *
FROM projects
WHERE deleted_at IS NULL
ORDER BY id;
