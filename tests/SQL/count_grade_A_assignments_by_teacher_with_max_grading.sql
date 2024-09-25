-- -- Write query to find the number of grade A's given by the teacher who has graded the most assignments

--  WITH TeacherAssignmentCounts AS (
--         SELECT 
--             teacher_id,
--             COUNT(*) AS total_assignments
--         FROM 
--             assignments
--         WHERE 
--             state = 'GRADED'
--         GROUP BY 
--             teacher_id
--     ),
--     TopTeacher AS (
--         SELECT 
--             teacher_id
--         FROM 
--             TeacherAssignmentCounts
--         ORDER BY 
--             total_assignments DESC
--         LIMIT 1
--     )
--     SELECT 
--         COUNT(*) AS grade_a_count
--     FROM 
--         assignments
--     WHERE 
--         grade = 'A' 
--         AND state = 'GRADED'
--         AND teacher_id = (SELECT teacher_id FROM TopTeacher);

-- Find the teacher who graded the most assignments and the count of grade A assignments
WITH teacher_max_grading AS (
    SELECT teacher_id, COUNT(*) AS total_grades
    FROM assignments
    GROUP BY teacher_id
    ORDER BY total_grades DESC
    LIMIT 1
)
SELECT COUNT(*)
FROM assignments
WHERE grade = 'A' 
AND teacher_id = (SELECT teacher_id FROM teacher_max_grading);
