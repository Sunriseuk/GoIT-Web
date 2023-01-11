SELECT
	groups.groupname,
	AVG(grades.grade) as avg
FROM groups as groups
	INNER JOIN students as students ON groups.id = students.group_id
	INNER JOIN grades AS grades ON students.id = grades.student_id
WHERE grades.subject_id = 3

GROUP BY
	groups.groupname

ORDER BY
	avg DESC