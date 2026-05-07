-- Q01 Profesores que superan el promedio de su depto Y el promedio global
SELECT i.name,
       i.salary,
       i.dept_name,
       AVG(i2.salary)                       AS promedio_depto,
       (SELECT AVG(salary) FROM instructor) AS promedio_global
FROM instructor i
JOIN instructor i2 ON i2.dept_name = i.dept_name
GROUP BY i.ID, i.name, i.salary, i.dept_name
HAVING i.salary > AVG(i2.salary)
   AND i.salary > (SELECT AVG(salary) FROM instructor)
ORDER BY i.dept_name, i.salary DESC;


-- Q02 Presupuesto restante por departamento tras pagar salarios
SELECT d.dept_name,
       d.budget,
       SUM(i.salary)             AS total_salario,
       d.budget - SUM(i.salary)  AS presupuesto_restante,
       COUNT(i.ID)               AS num_profesores
FROM department d
JOIN instructor i ON d.dept_name = i.dept_name
GROUP BY d.dept_name, d.budget
ORDER BY presupuesto_restante ASC;


-- Q03 Profesores que impartieron secciones en Fall y Spring del mismo año
SELECT i.name AS profesor,
       t1.year AS año,
       COUNT(DISTINCT t1.course_id) AS cursos_fall,
       COUNT(DISTINCT t2.course_id) AS cursos_spring
FROM instructor i
JOIN teaches t1 ON i.ID = t1.ID AND t1.semester = 'Fall'
JOIN teaches t2 ON i.ID = t2.ID AND t2.semester = 'Spring'
                AND t1.year = t2.year
GROUP BY i.ID, i.name, t1.year
ORDER BY t1.year DESC, i.name;


-- Q04 Estudiantes que han tomado cursos de más de un departamento
SELECT s.name                       AS estudiante,
       s.dept_name                  AS depto_estudiante,
       COUNT(DISTINCT c.dept_name)  AS deptos_distintos,
       COUNT(DISTINCT t.course_id)  AS total_cursos
FROM student s
JOIN takes   t   ON s.ID          = t.ID
JOIN section sec ON t.course_id   = sec.course_id
                AND t.sec_id      = sec.sec_id
                AND t.semester    = sec.semester
                AND t.year        = sec.year
JOIN course  c   ON sec.course_id = c.course_id
GROUP BY s.ID, s.name, s.dept_name
HAVING COUNT(DISTINCT c.dept_name) > 1
ORDER BY deptos_distintos DESC, total_cursos DESC;


-- Q05 Departamentos sin profesores cuyo presupuesto supera el promedio
SELECT d.dept_name,
       d.budget,
       d.building,
       d.budget - (SELECT AVG(budget) FROM department) AS exceso_vs_promedio
FROM department d
LEFT JOIN instructor i ON d.dept_name = i.dept_name
WHERE i.ID IS NULL
  AND d.budget > (SELECT AVG(budget) FROM department)
ORDER BY d.budget DESC;


-- Q06 Estudiantes cuyo asesor pertenece a un departamento distinto al suyo
SELECT s.name      AS estudiante,
       s.dept_name AS depto_estudiante,
       s.tot_cred,
       i.name      AS asesor,
       i.dept_name AS depto_asesor,
       d.budget    AS presupuesto_depto_asesor
FROM advisor    a
JOIN student    s ON a.s_ID      = s.ID
JOIN instructor i ON a.i_ID      = i.ID
JOIN department d ON i.dept_name = d.dept_name
WHERE i.dept_name <> s.dept_name
ORDER BY s.dept_name, i.dept_name;


-- Q07 Lugares disponibles por sección (capacidad - inscritos)
SELECT c.title        AS curso,
       sec.sec_id,
       sec.semester,
       sec.year,
       cl.building,
       cl.room_number,
       cl.capacity,
       COUNT(t.ID)               AS inscritos,
       cl.capacity - COUNT(t.ID) AS lugares_disponibles
FROM section   sec
JOIN course    c  ON sec.course_id   = c.course_id
JOIN classroom cl ON sec.building    = cl.building
                 AND sec.room_number = cl.room_number
LEFT JOIN takes t ON sec.course_id = t.course_id
                 AND sec.sec_id    = t.sec_id
                 AND sec.semester  = t.semester
                 AND sec.year      = t.year
GROUP BY c.title, sec.sec_id, sec.semester, sec.year,
         cl.building, cl.room_number, cl.capacity
ORDER BY lugares_disponibles ASC;


-- Q08 Estudiantes que tomaron más cursos que el promedio de su departamento
SELECT s.name       AS estudiante,
       s.dept_name,
       COUNT(t.course_id) AS cursos_tomados,
       (SELECT AVG(sub.total)
        FROM (
            SELECT s2.ID, COUNT(t2.course_id) AS total
            FROM student s2
            JOIN takes t2 ON s2.ID = t2.ID
            WHERE s2.dept_name = s.dept_name
            GROUP BY s2.ID
        ) sub
       ) AS promedio_depto
FROM student s
JOIN takes t ON s.ID = t.ID
GROUP BY s.ID, s.name, s.dept_name
HAVING COUNT(t.course_id) > (
    SELECT AVG(sub.total)
    FROM (
        SELECT s2.ID, COUNT(t2.course_id) AS total
        FROM student s2
        JOIN takes t2 ON s2.ID = t2.ID
        WHERE s2.dept_name = s.dept_name
        GROUP BY s2.ID
    ) sub
)
ORDER BY s.dept_name, cursos_tomados DESC;


-- Q09 Pares de profesores con 2 o más estudiantes compartidos
SELECT i1.name  AS profesor_1,
       i2.name  AS profesor_2,
       COUNT(DISTINCT s.ID) AS estudiantes_compartidos
FROM teaches  t1
JOIN instructor i1  ON t1.ID         = i1.ID
JOIN takes      tk1 ON t1.course_id  = tk1.course_id
                   AND t1.sec_id     = tk1.sec_id
                   AND t1.semester   = tk1.semester
                   AND t1.year       = tk1.year
JOIN student    s   ON tk1.ID        = s.ID
JOIN takes      tk2 ON tk1.ID        = tk2.ID
JOIN teaches    t2  ON tk2.course_id = t2.course_id
                   AND tk2.sec_id    = t2.sec_id
                   AND tk2.semester  = t2.semester
                   AND tk2.year      = t2.year
JOIN instructor i2  ON t2.ID         = i2.ID
WHERE i1.ID < i2.ID
GROUP BY i1.ID, i1.name, i2.ID, i2.name
HAVING COUNT(DISTINCT s.ID) >= 2
ORDER BY estudiantes_compartidos DESC;


-- Q10 Estudiantes que reprobaron más cursos que el promedio
SELECT s.name       AS estudiante,
       s.dept_name,
       COUNT(t.course_id) AS cursos_reprobados,
       (SELECT AVG(conteo)
        FROM (
            SELECT COUNT(t2.course_id) AS conteo
            FROM takes t2
            WHERE t2.grade = 'F'
            GROUP BY t2.ID
        ) sub
       ) AS promedio_reprobados
FROM student s
JOIN takes t ON s.ID = t.ID
WHERE t.grade = 'F'
GROUP BY s.ID, s.name, s.dept_name
HAVING COUNT(t.course_id) > (
    SELECT AVG(conteo)
    FROM (
        SELECT COUNT(t2.course_id) AS conteo
        FROM takes t2
        WHERE t2.grade = 'F'
        GROUP BY t2.ID
    ) sub
)
ORDER BY cursos_reprobados DESC;