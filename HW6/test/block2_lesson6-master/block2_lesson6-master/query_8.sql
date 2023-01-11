SELECT
    teachers.firstname AS firstname,
    teachers.lastname AS lastname,
    AVG(grades.grade) AS avg

FROM teachers AS teachers
    LEFT JOIN subjects AS subjects ON teachers.id = subjects.teacher_id
        LEFT JOIN grades AS grades ON subjects.id = grades.subject_id

WHERE
    teachers.id = :teachers.id
GROUP BY
    teachers.firstname,
    teachers.lastname