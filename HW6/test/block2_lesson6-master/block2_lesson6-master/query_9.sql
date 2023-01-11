SELECT
    students.firstname AS firstname,
    students.lastname AS lastname,
    subjects.name AS subject

FROM students AS students
    INNER JOIN grades AS grades ON students.id = grades.student_id
    INNER JOIN subjects AS subjects ON grades.subject_id = subjects.id

ORDER BY students.lastname, students.firstname