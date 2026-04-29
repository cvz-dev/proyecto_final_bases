-- Q01 Profesores cuyo salario supera el promedio de su propio departamento
SELECT i.name, i.salary, i.dept_name,
       ROUND(AVG(i2.salary), 2) AS promedio_depto
FROM instructor i
JOIN department d  ON i.dept_name  = d.dept_name
JOIN instructor i2 ON i2.dept_name = i.dept_name
GROUP BY i.ID, i.name, i.salary, i.dept_name
HAVING i.salary > AVG(i2.salary)
ORDER BY i.dept_name, i.salary DESC;

-- ─────────────────────────────────────────────────────────────

-- Q02 Departamentos con número de profesores, promedio de salario
SELECT d.dept_name, d.budget,
       COUNT(i.ID)               AS num_profesores,
       ROUND(AVG(i.salary), 2)   AS avg_salary,
       ROUND(d.budget / COUNT(i.ID), 2) AS budget_por_profesor
FROM department d
JOIN instructor i ON d.dept_name = i.dept_name
GROUP BY d.dept_name, d.budget
ORDER BY budget_por_profesor DESC;

-- ─────────────────────────────────────────────────────────────

-- Q03 Profesores que impartieron más de una sección en el mismo semestre
SELECT i.name, t.semester, t.year,
       COUNT(*) AS secciones_en_semestre
FROM teaches t
JOIN instructor i ON t.ID = i.ID
GROUP BY i.ID, i.name, t.semester, t.year
HAVING COUNT(*) > 1
ORDER BY t.year DESC, secciones_en_semestre DESC;

-- ─────────────────────────────────────────────────────────────

-- Q04 Cursos con prerrequisitos
SELECT c.course_id AS curso_id,
       c.title AS curso,
       p.course_id AS prereq_id,
       p.title AS prereq_titulo,
       p.credits AS prereq_creditos
FROM course c
JOIN prereq pr ON c.course_id = pr.course_id
JOIN course p ON pr.prereq_id = p.course_id
ORDER BY c.course_id;

-- ─────────────────────────────────────────────────────────────

-- Q05 Departamentos sin profesores con presupuesto mayor a 50,000
SELECT d.dept_name, d.budget, d.building
FROM department d
LEFT JOIN instructor i ON d.dept_name = i.dept_name
WHERE i.ID IS NULL
  AND d.budget > 50000
ORDER BY d.budget DESC;

-- ─────────────────────────────────────────────────────────────

-- Q06 Estudiantes con su asesor y el departamento del asesor
SELECT s.name    AS estudiante,
       s.tot_cred,
       i.name    AS asesor,
       i.salary  AS salario_asesor,
       d.dept_name
FROM advisor    a
JOIN student    s ON a.s_ID      = s.ID
JOIN instructor i ON a.i_ID      = i.ID
JOIN department d ON i.dept_name = d.dept_name
ORDER BY d.dept_name, i.name;

-- ─────────────────────────────────────────────────────────────

-- Q07 Secciones del año 2009 con nombre del curso y capacidad del aula
SELECT sec.sec_id, sec.semester, sec.year,
       c.title   AS curso,
       c.credits,
       cl.building,
       cl.room_number,
       cl.capacity
FROM section   sec
JOIN course    c  ON sec.course_id   = c.course_id
JOIN classroom cl ON sec.building    = cl.building
                 AND sec.room_number = cl.room_number
WHERE sec.year = 2009
ORDER BY c.title, sec.semester;

-- ─────────────────────────────────────────────────────────────

-- Q08 Cursos aprobados por estudiante
SELECT s.name AS estudiante,
       c.title AS curso,
       c.credits,
       t.semester,
       t.year,
       t.grade
FROM takes t
JOIN student s ON t.ID = s.ID
JOIN section sec ON t.course_id = sec.course_id
                AND t.sec_id = sec.sec_id
                AND t.semester = sec.semester
                AND t.year = sec.year
JOIN course c ON sec.course_id = c.course_id
WHERE t.grade IS NOT NULL
  AND t.grade <> 'F'
ORDER BY s.name, t.year;

-- ─────────────────────────────────────────────────────────────

-- Q09 Profesores que comparten estudiantes
SELECT i.name AS profesor,
       s.name AS estudiante
FROM instructor i
JOIN teaches t ON i.ID = t.ID
JOIN takes tk ON t.course_id = tk.course_id
             AND t.sec_id = tk.sec_id
             AND t.semester = tk.semester
             AND t.year = tk.year
JOIN student s ON tk.ID = s.ID
ORDER BY i.name, s.name;

-- ─────────────────────────────────────────────────────────────

-- Q10 Cursos que nunca ha tomado nadie
SELECT c.course_id, c.title
FROM course c
LEFT JOIN section sec ON c.course_id  = sec.course_id
LEFT JOIN takes   t   ON sec.course_id = t.course_id
                     AND sec.sec_id    = t.sec_id
                     AND sec.semester  = t.semester
                     AND sec.year      = t.year
WHERE t.ID IS NULL
ORDER BY c.course_id;
