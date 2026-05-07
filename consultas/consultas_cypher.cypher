// Q01 Profesores que superan el promedio de su depto Y el promedio global
MATCH (todos:Instructor)
WITH avg(toFloat(todos.salary)) AS promedio_global
MATCH (i:Instructor)-[:PERTENECE_A]->(d:Department)
WITH i, d, promedio_global
MATCH (peer:Instructor)-[:PERTENECE_A]->(d)
WITH i, d, promedio_global, avg(toFloat(peer.salary)) AS promedio_depto
WHERE toFloat(i.salary) > promedio_depto
  AND toFloat(i.salary) > promedio_global
RETURN i.name,
       i.salary,
       d.dept_name,
       promedio_depto,
       promedio_global
ORDER BY d.dept_name, i.salary DESC;


// Q02 Presupuesto restante por departamento tras pagar salarios
MATCH (i:Instructor)-[:PERTENECE_A]->(d:Department)
WITH d,
     count(i)               AS num_profesores,
     sum(toFloat(i.salary)) AS masa_salarial
RETURN d.dept_name,
       d.budget,
       num_profesores,
       masa_salarial,
       toFloat(d.budget) - masa_salarial AS presupuesto_restante
ORDER BY presupuesto_restante ASC;


// Q03 Profesores que impartieron secciones en Fall y Spring del mismo año
MATCH (i:Instructor)-[:TEACHES]->(sf:Section {semester: 'Fall'})
MATCH (i)-[:TEACHES]->(sp:Section {semester: 'Spring'})
WHERE sf.year = sp.year
WITH i, sf.year AS año,
     count(DISTINCT sf.course_id) AS cursos_fall,
     count(DISTINCT sp.course_id) AS cursos_spring
RETURN i.name AS profesor, año, cursos_fall, cursos_spring
ORDER BY año DESC, profesor;


// Q04 Estudiantes que han tomado cursos de más de un departamento
MATCH (s:Student)-[:TAKES]->(sec:Section)-[:ES_DE]->(c:Course)-[:PERTENECE_A]->(d:Department)
WITH s, count(DISTINCT d) AS deptos_distintos,
        count(DISTINCT c) AS total_cursos
WHERE deptos_distintos > 1
RETURN s.name      AS estudiante,
       s.dept_name AS depto_estudiante,
       deptos_distintos,
       total_cursos
ORDER BY deptos_distintos DESC, total_cursos DESC;


// Q05 Departamentos sin profesores cuyo presupuesto supera el promedio
MATCH (todos:Department)
WITH avg(toFloat(todos.budget)) AS promedio_presupuesto
MATCH (d:Department)
WHERE NOT (:Instructor)-[:PERTENECE_A]->(d)
  AND toFloat(d.budget) > promedio_presupuesto
RETURN d.dept_name,
       d.budget,
       d.building,
       toFloat(d.budget) - promedio_presupuesto AS exceso_vs_promedio
ORDER BY d.budget DESC;


// Q06 Estudiantes cuyo asesor pertenece a un departamento distinto al suyo
MATCH (i:Instructor)-[:ADVISES]->(s:Student),
      (i)-[:PERTENECE_A]->(d:Department)
WHERE i.dept_name <> s.dept_name
RETURN s.name      AS estudiante,
       s.dept_name AS depto_estudiante,
       s.tot_cred,
       i.name      AS asesor,
       i.dept_name AS depto_asesor,
       d.budget    AS presupuesto_depto_asesor
ORDER BY s.dept_name, i.dept_name;


// Q07 Lugares disponibles por sección (capacidad - inscritos)
MATCH (sec:Section)-[:ES_DE]->(c:Course),
      (sec)-[:SE_IMPARTE_EN]->(cl:Classroom)
OPTIONAL MATCH (s:Student)-[:TAKES]->(sec)
WITH c, sec, cl, count(s) AS inscritos
RETURN c.title     AS curso,
       sec.sec_id,
       sec.semester,
       sec.year,
       cl.building,
       cl.room_number,
       cl.capacity,
       inscritos,
       toInteger(cl.capacity) - inscritos AS lugares_disponibles
ORDER BY lugares_disponibles ASC;


// Q08 Estudiantes que tomaron más cursos que el promedio de su departamento
MATCH (s:Student)-[:TAKES]->(:Section)
WITH s, count(*) AS cursos_tomados
MATCH (peer:Student)-[:TAKES]->(:Section)
WHERE peer.dept_name = s.dept_name
WITH s, cursos_tomados, peer, count(*) AS c_peer
WITH s, cursos_tomados, avg(toFloat(c_peer)) AS promedio_depto
WHERE cursos_tomados > promedio_depto
RETURN s.name      AS estudiante,
       s.dept_name AS depto_estudiante,
       cursos_tomados,
       promedio_depto
ORDER BY depto_estudiante, cursos_tomados DESC;


// Q09 Pares de profesores con 2 o más estudiantes compartidos
MATCH (i1:Instructor)-[:TEACHES]->(sec1:Section)<-[:TAKES]-(s:Student)
      -[:TAKES]->(sec2:Section)<-[:TEACHES]-(i2:Instructor)
WHERE i1.ID < i2.ID
WITH i1, i2, count(DISTINCT s) AS estudiantes_compartidos
WHERE estudiantes_compartidos >= 2
RETURN i1.name AS profesor_1,
       i2.name AS profesor_2,
       estudiantes_compartidos
ORDER BY estudiantes_compartidos DESC;


// Q10 Estudiantes que reprobaron más cursos que el promedio
MATCH (s2:Student)-[t2:TAKES]->(:Section)
WHERE t2.grade = 'F'
WITH s2, count(t2) AS conteo
WITH avg(toFloat(conteo)) AS promedio_reprobados
MATCH (s:Student)-[t:TAKES]->(:Section)
WHERE t.grade = 'F'
WITH s, count(t) AS cursos_reprobados, promedio_reprobados
WHERE cursos_reprobados > promedio_reprobados
RETURN s.name      AS estudiante,
       s.dept_name,
       cursos_reprobados,
       promedio_reprobados
ORDER BY cursos_reprobados DESC;
