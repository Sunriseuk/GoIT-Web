SELECT 
	students.firstname AS firstname,
	students.lastname AS lastname,
	AVG(grades.grade) AS avg
FROM
	students AS students
		INNER JOIN grades AS grades
		ON students.id = grades.student_id

GROUP BY
	students.firstname,
	students.lastname

ORDER BY
	avg DESC

LIMIT 5