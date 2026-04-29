// Q01 Profesores cuyo salario supera el promedio de su departamento
MATCH (i:Instructor)-[:PERTENECE_A]->(d:Department)
WITH d, avg(toFloat(i.salary)) AS promedio_depto
MATCH (i:Instructor)-[:PERTENECE_A]->(d)
WHERE toFloat(i.salary) > promedio_depto
RETURN i.name, i.salary, d.dept_name,
       round(promedio_depto, 2) AS promedio_depto
ORDER BY d.dept_name, i.salary DESC;

// ─────────────────────────────────────────────────────────────

// Q02 Departamentos con número de profesores, promedio de salario y presupuesto por profesor
MATCH (d:Department)<-[:PERTENECE_A]-(i:Instructor)
WITH d.dept_name AS depto, d.budget AS budget,
     count(i)               AS num_profesores,
     avg(toFloat(i.salary)) AS avg_salary
RETURN depto, budget, num_profesores,
       round(avg_salary, 2)                       AS avg_salary,
       round(toFloat(budget) / num_profesores, 2) AS budget_por_profesor
ORDER BY budget_por_profesor DESC;

// ─────────────────────────────────────────────────────────────

// Q03 Profesores que impartieron más de una sección en el mismo semestre
MATCH (i:Instructor)-[:TEACHES]->(sec:Section)
WITH i, sec.semester AS semester, sec.year AS year,
     count(sec) AS secciones_en_semestre
WHERE secciones_en_semestre > 1
RETURN i.name, semester, year, secciones_en_semestre
ORDER BY year DESC, secciones_en_semestre DESC;

// ─────────────────────────────────────────────────────────────

// Q04 Cursos con sus prerrequisitos
MATCH (c:Course)-[:REQUIERE]->(p:Course)
RETURN c.course_id AS curso_id,
       c.title     AS curso,
       p.course_id AS prereq_id,
       p.title     AS prereq_titulo,
       p.credits   AS prereq_creditos
ORDER BY curso_id;

// ─────────────────────────────────────────────────────────────

// Q05 Departamentos sin profesores con presupuesto mayor a 50,000
MATCH (d:Department)
WHERE NOT (:Instructor)-[:PERTENECE_A]->(d)
  AND toFloat(d.budget) > 50000
RETURN d.dept_name, d.budget, d.building
ORDER BY d.budget DESC;

// ─────────────────────────────────────────────────────────────

// Q06 Estudiantes con su asesor y el departamento del asesor
MATCH (i:Instructor)-[:ADVISES]->(s:Student),
      (i)-[:PERTENECE_A]->(d:Department)
RETURN s.name     AS estudiante,
       s.tot_cred,
       i.name     AS asesor,
       i.salary   AS salario_asesor,
       d.dept_name
ORDER BY d.dept_name, i.name;

// ─────────────────────────────────────────────────────────────

// Q07 Secciones del año 2009 con nombre del curso y capacidad del aula
MATCH (sec:Section)-[:ES_DE]->(c:Course),
      (sec)-[:SE_IMPARTE_EN]->(cl:Classroom)
WHERE sec.year = 2009
RETURN sec.sec_id, sec.semester, sec.year,
       c.title  AS curso,
       c.credits,
       cl.building,
       cl.room_number,
       cl.capacity
ORDER BY c.title, sec.semester;

// ─────────────────────────────────────────────────────────────

// Q08 Cursos aprobados por estudiante
MATCH (s:Student)-[t:TAKES]->(sec:Section)-[:ES_DE]->(c:Course)
WHERE t.grade IS NOT NULL
  AND t.grade <> 'F'
RETURN s.name      AS estudiante,
       c.title     AS curso,
       c.credits   AS creditos,
       sec.semester AS semestre,
       sec.year    AS anio,
       t.grade     AS calificacion
ORDER BY estudiante, anio;

// ─────────────────────────────────────────────────────────────

// Q09 Profesores y estudiantes que tuvieron en sus secciones
MATCH (i:Instructor)-[:TEACHES]->(sec:Section)<-[:TAKES]-(s:Student)
RETURN i.name AS profesor,
       s.name AS estudiante
ORDER BY profesor, estudiante;

// ─────────────────────────────────────────────────────────────

// Q10 Cursos que nunca ha tomado nadie
MATCH (c:Course)
WHERE NOT EXISTS {
    MATCH (c)<-[:ES_DE]-(sec:Section)<-[:TAKES]-(:Student)
}
RETURN c.course_id, c.title
ORDER BY c.course_id;
