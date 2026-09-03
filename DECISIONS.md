# DECISIONS

Registro de decisiones tecnicas del proyecto Inbox IA Business.

---

1. **Frontend:** React + TypeScript.
   Ecosistema maduro, tipado estatico, gran soporte de herramientas.

2. **Herramienta de desarrollo frontend:** Vite.
   Builds rapidos en desarrollo, configuracion minima, soporte nativo de React + TS.

3. **Backend:** Python + FastAPI.
   Alto rendimiento asincrono, validacion automatica con Pydantic, documentacion OpenAPI integrada.

4. **API inicial:** REST.
   Suficiente para el MVP; GraphQL o WebSockets se evaluaran si el producto lo requiere.

5. **Base de datos futura del MVP:** PostgreSQL.
   Relacional, robusto, amplio soporte en el ecosistema Python.

6. **Arquitectura multiempresa desde el modelo de datos.**
   El esquema de base de datos contemplara multitenancy desde el inicio para evitar migraciones costosas.

7. **Los recursos empresariales deberan estar asociados a `company_id`.**
   Toda entidad de negocio llevara referencia explicita a la empresa propietaria.

8. **La autorizacion multiempresa sera validada siempre en backend.**
   El frontend nunca tomara decisiones de acceso; solo el backend filtra por `company_id`.

9. **Las API keys y credenciales externas nunca estaran expuestas al frontend.**
   Toda comunicacion con servicios externos se proxia a traves del backend.

10. **La IA no enviara mensajes automaticamente durante el MVP.**
    La IA sugerira respuestas; un agente humano siempre aprobara y enviara.

11. **WhatsApp y otras redes sociales quedan fuera hasta completar las funciones correspondientes de Fase 1.**
    Se priorizara la logica de negocio central antes de integrar canales externos.

12. **Identificadores UUID para Company y User.**
    Se utiliza `uuid.uuid4()` para evitar identificadores predecibles e id conflictivos.

13. **User pertenece obligatoriamente a Company.**
    La relacion multiempresa queda forzada desde la tabla `users` mediante `company_id`.

14. **Email unico globalmente.**
    Para el MVP, un email solo puede pertenecer a un usuario/empresa, simplificando autenticacion inicial.

15. **CompanyStatus limitado a ACTIVE/SUSPENDED.**
    Restringe la maquina de estados de la empresa a lo esencial para el MVP.

16. **Alembic como mecanismo oficial para cambios de esquema.**
    No se usara `Base.metadata.create_all()` en la aplicacion, para garantizar la consistencia y el versionamiento del esquema mediante migraciones.

17. **Se priorizara simplicidad y cambios pequenos sobre arquitectura especulativa.**
    No se crearan carpetas, abstracciones ni dependencias que no sean necesarias en la version actual.

18. **Autenticación mediante sesiones opacas server-side.**
    Para el MVP, la autenticación web se realizará mediante sesiones almacenadas en PostgreSQL y expuestas mediante cookie HttpOnly, evitando JWT y localStorage. El identificador (`token_hash`) se persiste de forma segura (hasheado) sin guardar el token en texto claro, y la empresa se resuelve a través de la relación de `User` en lugar de duplicar `company_id` en la sesión.
