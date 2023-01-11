SELECT
    AVG(grades.grade) AS avg
FROM grades AS grades
    LEFT JOIN subjects AS subjects ON grades.subject_id = subjects.id

WHERE grades.student_id = :student_id
    AND subjects.teacher_id = :teacher_id
    