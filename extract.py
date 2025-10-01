def extract_newdocs(cursor):
  query = """ 
    -- Documentos cargados por coordinación
    SELECT DISTINCT d.docalumno_id AS id_doc, d.docalumno_alumno AS alumno_id, 
      CONCAT(p.alumno_apellido, ", ", p.alumno_nombre) AS alumno,
        o.os_nombre,
        d.docalumnotipo_nombre AS nombre_doc,
        DATE_FORMAT(d.docalumno_fec_carga, '%d-%m-%Y') AS fec_carga,
      d.docalumnoseccion_nombre, d.docalumno_anio AS anio, u_doc.user_name AS usuario, r_doc.`role` AS rol, 
        'DOC' AS tipo
    FROM v_docs_alumno d
    LEFT JOIN v_prestaciones p
      ON d.docalumno_alumno = p.prestacion_alumno
    LEFT JOIN v_os o
      ON p.prestacion_os = o.os_id
    LEFT JOIN v_users u_doc
        ON d.usuario_carga = u_doc.user_name
    LEFT JOIN v_users_roles r_doc
        ON u_doc.user_id = r_doc.user_id
    WHERE 
      p.prestacion_estado = 1
        AND p.prestipo_nombre_corto != "TERAPIAS"
        AND d.docalumnoseccion_nombre IN ('GENERAL', 'SAIE')
        AND d.docalumno_anio IN ('GENERAL', '2025')
        AND r_doc.`role` IN ("COORDI", "COORDINACION_GENERAL", "RESP_INCLUSION")
        AND d.docalumno_fec_carga >= CURDATE() - INTERVAL 7 DAY

    UNION ALL

    -- Informes cargados por coordinación
    SELECT DISTINCT i.alumnoinforme_id AS id_doc, i.alumno_id AS alumno_id, 
      CONCAT(p.alumno_apellido, ", ", p.alumno_nombre) AS alumno, 
        o.os_nombre,
        i.informecat_nombre AS nombre_doc,
        DATE_FORMAT(i.fec_carga, '%d-%m-%Y') as fec_carga,
      "INFORMES" AS docalumnoseccion_nombre, i.alumnoinforme_anio AS anio, u_inf.user_name AS usuario, 
        r_inf.`role` AS rol, 'INF' AS tipo
    FROM v_informes i
    LEFT JOIN v_prestaciones p
      ON i.alumno_id = p.prestacion_alumno
    LEFT JOIN v_os o
      ON p.prestacion_os = o.os_id
    LEFT JOIN v_users u_inf
        ON i.usuario = u_inf.user_name
    LEFT JOIN v_users_roles r_inf
        ON u_inf.user_id = r_inf.user_id
    WHERE 
      p.prestacion_estado = 1
        AND p.prestipo_nombre_corto != "TERAPIAS"
        AND r_inf.`role` IN ("COORDI", "COORDINACION_GENERAL", "RESP_INCLUSION")
        AND i.fec_carga >= CURDATE() - INTERVAL 7 DAY
      ORDER BY alumno;
 """
  cursor.execute(query)
  return cursor.fetchall()