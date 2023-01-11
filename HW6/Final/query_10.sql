SELECT DISTINCT subjects.name AS subject
FROM grades AS grades
    LEFT JOIN subjects AS subjects ON grades.subject_id = subjects.id
WHERE grades.student_id = 4
    AND subjects.teacher_id = 5
ORDER BY subjects.name
