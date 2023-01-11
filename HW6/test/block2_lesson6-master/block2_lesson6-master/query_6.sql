SELECT
    students.firstname AS firstname,
    students.lastname AS lastname

FROM 
    students AS students

WHERE students.group_id = :group_id