# Agent Development Guide

## 0. Verificación y Gestión Preventiva de Servidores MCP (Regla Crítica de Rendimiento)

Antes de iniciar cualquier tarea o responder al usuario en un proyecto:

1. **Adecuar los MCPs al tipo de proyecto:**
   - **Proyectos Android:** El MCP `android-studio-index` debe estar habilitado únicamente si **Android Studio está abierto** con el proyecto cargado y respondiendo en su puerto local (por defecto `29171`). Si Android Studio no está en ejecución, dicho MCP debe mantenerse deshabilitado (`"disabled": true`) para evitar congelamientos por timeout de red (etiqueta "Working...").
   - **Proyectos Unity:** Habilitar `unity-mcp` y verificar que el editor de Unity y su relay estén activos.
   - **Proyectos Generales / Backend / Web:** Deshabilitar los MCPs de IDEs específicos que no se estén utilizando.
2. **Verificación de Conexiones:**
   - Comprobar que los endpoints o comandos configurados en `mcp_config.json` sean accesibles y no generen errores de socket, WebSocket o reintentos en bucle.
3. **Bloqueo Preventivo ante Fallos:**
   - **Si una conexión MCP falla, no responde o está en un estado erróneo, la IA DEBE INFORMARLO DE INMEDIATO AL USUARIO** para corregirlo o deshabilitarlo antes de proceder con cualquier planificación o implementación en el código.

---

## 1. Contexto y objetivo del proyecto

Antes de comenzar cualquier tarea, debes familiarizarte con la estructura, objetivos, arquitectura y estado actual del proyecto.

La carpeta `_Project Guide` contiene la documentación de referencia del proyecto. Debes revisar su contenido antes de realizar cambios que puedan afectar la arquitectura, funcionalidades, flujo de trabajo o planificación.

### Regla principal

**No asumir el estado del proyecto. Verificarlo primero.**

Antes de implementar una funcionalidad:

1. Revisar `_Project Guide`.
2. Leer el `work_plan` y cualquier documentación relevante.
3. Revisar el código existente relacionado con la tarea.
4. Identificar qué partes ya están implementadas.
5. Determinar dependencias, riesgos y posibles efectos sobre otras funcionalidades.
6. Solo después comenzar la implementación.

La documentación del proyecto y el código existente deben utilizarse como contexto para mantener la coherencia de la solución.

---

# 2. Desarrollo sistemático

El proyecto debe desarrollarse de manera **estructurada y sistemática**, siguiendo un proceso organizado por fases, funcionalidades y módulos.

Evita implementar funcionalidades de manera aislada si forman parte de un sistema mayor.

Cada tarea debe seguir, cuando sea aplicable, este flujo:

**Analizar → Planificar → Implementar → Verificar → Documentar → Actualizar el plan**

El objetivo no es únicamente conseguir que una funcionalidad "funcione", sino integrarla correctamente con la arquitectura existente y mantener el proyecto en un estado coherente y mantenible.

---

# 3. Revisión y Organización de `_Project Guide`

La carpeta `_Project Guide` es la fuente principal de contexto documental del proyecto.

### Organización y Archivado Preventivo (Evitar Latencia y Saturación)

Para evitar que la acumulación de decenas de archivos markdown sature el escaneo de contexto y ralentice las respuestas de la IA:

1. **Carpeta de Archivo (`_Project Guide/archive/`):** Todos los `implementation_plan_*.md` y `walkthrough_*.md` de fases ya terminadas y validadas deben organizarse dentro de `_Project Guide/archive/`.
2. **Raíz Limpia:** La raíz de `_Project Guide` debe contener únicamente los archivos activos:
   - `work_plan.md` (estado activo y tareas inmediatas).
   - `work_plan_history.md` (registro histórico de fases pasadas).
   - Documentos de arquitectura vigentes y el Implementation Plan / Walkthrough de la fase en curso.

---

# 4. Estructura, Generación y Mantenimiento del Work Plan

Al iniciar cualquier proyecto nuevo, la IA debe leer primero `agent.md` y posteriormente **generar el `work_plan.md` inicial** dentro de `_Project Guide/`.

## 4.1. Estructura Estándar del `work_plan.md`

Todo `work_plan.md` debe estructurarse con las siguientes secciones:

1. **Ficha Técnica & Metadatos del Proyecto:** Tabla con nombre de la app, estado actual, versión, package/bundle ID, SDKs/versiones de runtime, factor de forma y enlace al historial.
2. **Objetivo General & Arquitectura:** Resumen de alto nivel del sistema, arquitectura elegida (Clean Architecture, MVVM, etc.) y pila tecnológica.
3. **Resumen de Fases:** Lista de fases planificadas de alto nivel indicando su estado.
4. **Fase Activa & Tareas Pendientes:** Desglose detallado de la fase en desarrollo actual con casillas de verificación (`[ ] Pendiente`, `[x] Completado`).

## 4.2. Reglas de Mantenimiento y Actualización

Después de completar una tarea relevante:

- Marcarla como completada (`[x]`).
- Agregar nuevas subtareas descubiertas durante la implementación.
- Nunca marcar como completada una tarea que no haya sido realmente implementada y probada.

## 4.3. Regla de Archivado Histórico (Límite de Tamaño y Rendimiento)

Para mantener la máxima velocidad de respuesta y evitar el sobrecosto de tokens:

- El archivo `work_plan.md` activo debe mantenerse **ligero (menos de 5-10 KB)**.
- **Cuando se acumulen más de 3 a 5 fases completadas:**
  1. Mover el detalle minucioso de las fases finalizadas a `_Project Guide/work_plan_history.md`.
  2. Conservar en `_Project Guide/work_plan.md` únicamente un resumen en viñetas de las fases terminadas y el desglose completo de la **Fase Activa** y el **Roadmap Inmediato**.

---

# 5. Implementation Plans

Para tareas complejas, antes de modificar el código se debe preparar un **Implementation Plan**.

Un Implementation Plan es recomendable cuando la tarea:

- afecta múltiples archivos;
- requiere cambios de arquitectura;
- introduce un nuevo sistema o módulo;
- modifica estructuras de datos;
- afecta Firebase o servicios externos;
- requiere cambios importantes en UI y lógica;
- puede afectar funcionalidades existentes;
- contiene varias etapas de implementación.

El plan debe explicar, como mínimo:

1. Objetivo.
2. Estado actual relevante.
3. Problema que se pretende resolver.
4. Solución propuesta.
5. Archivos/componentes que serán modificados o creados.
6. Dependencias.
7. Flujo de implementación.
8. Consideraciones de seguridad.
9. Consideraciones de rendimiento, cuando sean relevantes.
10. Estrategia de pruebas y verificación.
11. Posibles riesgos o efectos secundarios.

## Aprobación

**No implementar cambios importantes basándose únicamente en un Implementation Plan que requiera aprobación hasta que haya sido aprobado.**

Una vez que el usuario apruebe un Implementation Plan:

1. conservar el plan aprobado;
2. crear una copia del plan;
3. guardarla dentro de `_Project Guide`;
4. utilizar esa copia como referencia durante la implementación;
5. mantenerla coherente con las decisiones tomadas durante el desarrollo.

Los Implementation Plans aprobados deben conservarse como documentación histórica y técnica del proyecto.

No sobrescribir un plan aprobado con cambios sustanciales sin dejar constancia de la modificación o crear una nueva versión cuando corresponda.

## Guardado de Walkthrough tras completar la implementación

Una vez que se hayan completado, verificado e implementado las tareas de un **Implementation Plan**:

1. redactar o actualizar el documento de **Walkthrough** (`walkthrough.md`) resumiendo los cambios implementados, las decisiones técnicas adoptadas, los archivos creados o modificados y los resultados de las pruebas;
2. **guardar obligatoriamente una copia del Walkthrough dentro de `_Project Guide`** utilizando una nomenclatura coherente y vinculada al plan (por ejemplo `_Project Guide/walkthrough_<nombre_del_plan>.md`);
3. asegurar que cada Implementation Plan completado cuente con su respectivo Walkthrough dentro de `_Project Guide` como evidencia técnica e histórica del trabajo terminado y validado.

---

# 6. Código y convenciones de nombres

Utilizar **inglés para todo el código fuente**.

Esto incluye:

- variables;
- constantes;
- clases;
- interfaces;
- métodos;
- propiedades;
- enums;
- eventos;
- archivos de código;
- namespaces;
- identificadores;
- nombres de componentes cuando formen parte del código.

Ejemplo:

```csharp
public class CustomerManager
{
    private string customerId;

    public void LoadCustomerProfile()
    {
        // ...
    }
}
```

Evitar:

```csharp
public class GestorCliente
{
    private string idCliente;

    public void CargarPerfilCliente()
    {
        // ...
    }
}
```

El idioma utilizado por la interfaz de usuario puede ser diferente. Los textos visibles para el usuario deben seguir las especificaciones del proyecto.

---

# 7. Calidad del código

Aplicar siempre buenas prácticas de programación y mantener como prioridad:

- claridad;
- mantenibilidad;
- modularidad;
- reutilización;
- separación de responsabilidades;
- bajo acoplamiento;
- alta cohesión;
- consistencia con la arquitectura existente;
- manejo adecuado de errores;
- seguridad;
- rendimiento;
- facilidad de pruebas.

Antes de crear una nueva clase, sistema o utilidad, comprobar si ya existe una implementación reutilizable.

**No duplicar lógica existente cuando pueda reutilizarse o refactorizarse correctamente.**

Evitar soluciones rápidas que introduzcan deuda técnica innecesaria.

No realizar refactorizaciones masivas no relacionadas con la tarea actual salvo que sean necesarias para completar correctamente la implementación.

---

# 8. Comprender antes de modificar

Antes de editar un archivo:

1. Leer el código relacionado.
2. Comprender su responsabilidad.
3. Identificar sus dependencias.
4. Revisar quién utiliza sus métodos, clases o eventos.
5. Evaluar posibles efectos secundarios.
6. Realizar el cambio más pequeño que resuelva correctamente el problema.

No modificar código basándose únicamente en el nombre de una clase, método o archivo.

---

# 9. Cambios incrementales

Preferir implementaciones pequeñas, verificables e incrementales.

Después de cada cambio significativo:

1. comprobar errores de compilación;
2. revisar referencias rotas;
3. comprobar la integración con los sistemas existentes;
4. ejecutar las pruebas disponibles;
5. verificar el comportamiento esperado;
6. corregir problemas antes de continuar.

No acumular grandes cantidades de cambios sin verificar el estado intermedio del proyecto.

---

# 10. Seguridad

La seguridad debe considerarse desde el diseño y no como una etapa exclusivamente posterior.

Cuando una funcionalidad involucre:

- autenticación;
- autorización;
- Firestore;
- Firebase Storage;
- datos personales;
- permisos;
- roles;
- operaciones sensibles;
- Cloud Functions;

se deben revisar las implicaciones de seguridad antes de considerar la funcionalidad terminada.

Nunca confiar exclusivamente en validaciones realizadas en el cliente cuando una operación requiera protección real en backend.

---

# 11. Firebase

Cuando se trabaje con Firebase, mantener coherencia entre:

- Authentication;
- Firestore;
- Storage;
- Cloud Functions;
- reglas de seguridad;
- modelos de datos;
- código cliente.

Cualquier modificación de la estructura de datos debe evaluarse respecto a las funcionalidades que ya dependen de ella.

Cuando se creen o modifiquen colecciones, documentos o campos, actualizar la documentación correspondiente si el cambio forma parte de la arquitectura del proyecto.

---

# 12. Unity

Para proyectos Unity:

**Utilizar el MCP de Unity siempre que esté disponible y sea aplicable a la tarea.**

El MCP de Unity debe utilizarse preferentemente para tareas que requieran interacción, inspección o modificación del proyecto Unity cuando dicha capacidad esté disponible.

Si la tarea requiere utilizar el MCP de Unity y este:

- no está activado;
- no está disponible;
- presenta errores;
- o no puede realizar la operación necesaria;

**informar claramente al usuario antes de continuar con una alternativa**, especialmente cuando el MCP sea necesario para garantizar una implementación o verificación correcta.

No afirmar que una operación fue realizada mediante Unity MCP si realmente no fue ejecutada mediante esa herramienta.

---

# 13. Android

Para proyectos Android:

**Cuando sea aplicable, utilizar preferentemente las herramientas MCP de `android-studio-index` para navegación, inspección y refactorización del código.**

Esto es especialmente recomendable para:

- navegación entre símbolos;
- búsqueda de referencias;
- inspección de clases;
- refactorizaciones;
- cambios que involucren múltiples referencias;
- comprensión de dependencias dentro del proyecto Android.

Si la herramienta no está disponible, informar de la limitación cuando esta afecte la seguridad o confiabilidad de la operación.

## Despliegue y Ejecución Automática en Dispositivo Móvil (Pruebas en Vivo)

En cada iteración donde se realicen modificaciones de código, UI o comportamiento funcional en la aplicación Android:

1. **Verificar compilación y pruebas:** Ejecutar siempre `.\gradlew.bat testDebugUnitTest` o `.\gradlew.bat compileDebugKotlin` para garantizar que no existan errores de sintaxis ni regresiones.
2. **Compilar e instalar en el dispositivo conectado:** Cuando haya un dispositivo físico o emulador conectado vía ADB (`adb devices`), ejecutar `.\gradlew.bat installDebug` para transferir e instalar el APK de depuración automáticamente vía USB/red.
3. **Iniciar la aplicación en pantalla:** Ejecutar inmediatamente `adb shell am start -n com.gamypixel.premiapass/.MainActivity` tras la instalación. Esto abre la aplicación en primer plano en el teléfono sin que el usuario tenga que interactuar con la interfaz gráfica de Android Studio, dejándola lista para probar el resultado en tiempo real. Si no hay dispositivos conectados, compilar con `.\gradlew.bat assembleDebug` e indicar que el APK quedó listo para cuando se conecte el dispositivo.

---

# 14. Dependencias y herramientas

Antes de implementar una solución utilizando una librería, SDK, plugin, MCP o herramienta específica:

1. comprobar si ya existe en el proyecto;
2. comprobar cómo se utiliza actualmente;
3. evitar introducir dependencias duplicadas;
4. mantener compatibilidad con las versiones existentes;
5. evaluar el impacto de agregar una nueva dependencia.

No introducir una nueva tecnología simplemente porque ofrece una solución rápida si el proyecto ya dispone de mecanismos adecuados para resolver el problema.

---

# 15. UI y UX

Cuando se modifique la interfaz:

- respetar el sistema visual existente;
- reutilizar componentes compartidos;
- mantener consistencia entre pantallas;
- respetar los temas existentes;
- evitar duplicar estilos;
- mantener una jerarquía visual coherente;
- considerar diferentes tamaños y relaciones de aspecto;
- verificar interacción y navegación.

Si existe un componente reutilizable, utilizarlo en lugar de crear uno nuevo.

Los cambios visuales importantes deben evaluarse tanto funcionalmente como visualmente.

---

# 16. Rendimiento

El rendimiento debe considerarse durante la implementación, especialmente en dispositivos móviles.

Prestar atención a:

- consultas innecesarias a Firebase;
- descargas repetidas;
- operaciones costosas en cada frame;
- creación y destrucción excesiva de objetos;
- memoria;
- imágenes y texturas;
- listas grandes;
- operaciones asíncronas;
- latencia de red;
- actualizaciones innecesarias de UI.

No optimizar prematuramente sin necesidad, pero tampoco introducir patrones evidentemente costosos cuando existe una alternativa sencilla y correcta.

---

# 17. Manejo de errores

Las operaciones que dependan de red, Firebase, autenticación, almacenamiento o recursos externos deben contemplar errores y estados intermedios.

Considerar, cuando corresponda:

- loading;
- éxito;
- error;
- timeout;
- ausencia de datos;
- datos inválidos;
- pérdida de conexión;
- permisos insuficientes;
- operaciones canceladas.

Los errores deben comunicarse de forma consistente con el sistema de UI existente.

---

# 18. No inventar funcionalidades

No agregar funcionalidades, comportamientos o requisitos que no estén respaldados por:

- la documentación del proyecto;
- el `work_plan`;
- el Implementation Plan aprobado;
- instrucciones explícitas del usuario;
- decisiones tomadas durante la conversación.

Si existe una ambigüedad importante, plantearla antes de tomar una decisión que pueda afectar la arquitectura o el comportamiento del producto.

Se pueden proponer mejoras, pero deben diferenciarse claramente de los requisitos existentes.

---

# 19. Verificación antes de finalizar una tarea

Una tarea no debe considerarse terminada simplemente porque el código fue escrito.

Antes de marcarla como completada:

- verificar compilación;
- comprobar referencias;
- comprobar errores;
- revisar integración;
- probar el flujo afectado cuando sea posible;
- verificar que no se hayan roto funcionalidades existentes;
- revisar seguridad cuando corresponda;
- compilar, instalar e iniciar la app en el dispositivo conectado (`.\gradlew.bat installDebug` y `adb shell am start -n com.gamypixel.premiapass/.MainActivity`) para permitir la validación directa en el móvil;
- guardar una copia del Walkthrough en `_Project Guide` tras completar un Implementation Plan;
- actualizar el `work_plan`;
- actualizar la documentación relevante.

Si algo no pudo verificarse, indicarlo explícitamente.

**Nunca afirmar que algo fue probado si no fue realmente probado.**

---

# 20. Documentación

La documentación debe mantenerse sincronizada con el estado real del proyecto.

Actualizar documentación cuando se produzcan cambios significativos en:

- arquitectura;
- estructura de datos;
- funcionalidades;
- flujos;
- integraciones;
- dependencias;
- configuración;
- seguridad;
- decisiones técnicas.

La documentación debe ser útil para que otro desarrollador pueda comprender el proyecto sin depender de información exclusivamente presente en la conversación.

---

# 21. Principio de mínima modificación

Cuando sea posible:

> **Modificar lo necesario, no todo lo posible.**

Evitar:

- reescribir archivos completos sin necesidad;
- cambiar APIs existentes sin justificación;
- eliminar código funcional sin motivo;
- realizar refactorizaciones no relacionadas;
- cambiar estilos globales para resolver un problema local;
- introducir complejidad innecesaria.

Los cambios deben ser precisos, controlados y coherentes con la arquitectura existente.

---

# 22. Comunicación del trabajo

Al finalizar una tarea, informar de forma breve:

### Implementado

Qué se modificó o creó.

### Verificado

Qué se comprobó y cómo.

### Documentación

Qué archivos de `_Project Guide` o `work_plan` fueron actualizados.

### Pendiente

Cualquier trabajo que aún sea necesario.

### Limitaciones

Herramientas, MCP, pruebas o verificaciones que no hayan podido ejecutarse.

La comunicación debe distinguir claramente entre:

- **implementado**;
- **verificado**;
- **pendiente**;
- **propuesto**.

---

# 23. Regla general de trabajo

Ante cualquier tarea, seguir este principio:

> **Primero comprender el proyecto, después planificar, luego implementar, verificar el resultado y finalmente actualizar la documentación y el estado del proyecto.**

El objetivo es mantener un desarrollo **sistemático, incremental, documentado, seguro y mantenible**, evitando soluciones improvisadas y preservando la coherencia de todo el proyecto a medida que crece.

---

# 24. Herramientas de Desarrollo, CLIs y Servidores MCP (IA Tooling)

A continuación se detallan los entornos de línea de comandos (CLIs) y servidores de protocolo de contexto de modelo (**MCP**) configurados y disponibles para la asistencia interactiva de la IA en el proyecto:

## 24.1 CLIs Instalados y Disponibles

| CLI / Herramienta | Versión / Ubicación | Estado / Propósito |
| **`adb`** (Android Debug Bridge) | **`1.0.41`** (`C:\Users\Josue\AppData\Local\Android\Sdk\platform-tools\adb.exe`) | **Configurado en PATH (Usuario).** Detección de emuladores/dispositivos físicos (`adb devices`), lectura de logs (`adb logcat`) e instalación directa de APKs (`adb install -r ...`). |
| **`firebase`** (Firebase Tools) | **`15.30.0`** (`C:\Users\Josue\AppData\Roaming\npm\firebase.cmd`) | Autenticado como `jrolando2012@gmail.com`. Gestión de proyectos, emuladores locales (`firebase emulators:start` con Firestore v1.22 y UI v1.15) y despliegue de reglas de seguridad (`firebase deploy --only firestore:rules`). |
| **`gcloud`** (Google Cloud CLI) | Configurado con ADC y Service Account | Autenticado con rol `roles/datastore.owner` en `premia-pass`. Inspección y consultas REST a Firestore y GCP APIs. |
| **`gradlew`** (Gradle Wrapper) | Wrapper del proyecto (JDK 17) | Compilación (`assembleDebug`), ejecución de tests unitarios, cobertura JaCoCo (`jacocoTestReport`) y análisis Sonar. |
| **`perfetto` / `trace_processor`** | Python SDK `perfetto-0.58.2` + `trace_processor_shell.exe` | **Auditoría de Rendimiento:** Procesamiento de trazas del sistema (`.trace`), consultas SQL sobre frames, detección de jank, binder blocks y cuellos de botella de GPU/CPU. |
| **`git`** | Repositorio local sincronizado | Control de versiones, ramas y diffs. |
| **`git-lfs`** | **`3.7.0`** (`C:\Program Files\Git LFS\git-lfs.exe`) | **Configurado en PATH y Git filters.** Gestión de assets binarios pesados (texturas, audio, 3D). |
| **`aapt2`** (Android Asset Packaging Tool) | **`2.20`** (`build-tools\36.0.0`) | **Configurado en PATH.** Inspección y volcado de recursos, layouts, drawables y configuraciones de APKs/AABs (`aapt2 dump ...`). |
| **`apkanalyzer`** (APK/AAB Inspector) | Android SDK (`cmdline-tools\latest`) | **Configurado en PATH.** Inspección CLI de tamaño de métodos Dex, descarga estimada, recursos y manifiesto de APKs sin abrir Android Studio. |
| **`profgen`** (Baseline Profile Generator) | Android SDK (`cmdline-tools\latest`) | **Configurado en PATH.** Generación y validación de perfiles de inicio rápido de Android (Baseline Profiles). |
| **`sdkmanager`** | **`12.0`** (`cmdline-tools\latest`) | **Configurado en PATH.** Instalación y actualización de paquetes del SDK de Android por CLI. |
| **`zipalign`** | Android SDK (`build-tools\36.0.0`) | **Configurado en PATH.** Alineación de archivos zip a límites de 4 bytes previa a la firma de APKs de release. |
| **`apksigner`** | **`0.9`** (`build-tools\36.0.0`) | **Configurado en PATH.** Firma y verificación criptográfica de APKs con esquemas v1, v2, v3 y v4 (`apksigner verify -v ...`). |
| **`keytool`** | JDK 21 (`C:\Program Files\Java\jdk-21.0.12\bin`) | **Configurado en PATH.** Generación y lectura de keystores (`.jks`), extracción de huellas SHA-1 / SHA-256 para Firebase Console (`keytool -list -v ...`). |
| **`unity`** (Unity CLI Wrapper) | Dinámico (`C:\Users\Josue\.local\bin\unity.cmd`) | **Configurado en PATH.** Ejecución de Unity en batchmode (`-batchmode -quit -executeMethod ...`). Detecta versión del proyecto en `ProjectVersion.txt` o fallback a Unity 6 (`6000.5.1f1`). |
| **`unity-yaml-merge`** | Dinámico (`C:\Users\Josue\.local\bin\unity-yaml-merge.cmd`) | **Configurado en PATH y como merge driver en Git.** Smart merge automático de escenas (`.unity`) y prefabs (`.prefab`). |
| **`rg`** (ripgrep) | **`15.1.0`** (`WinGet\Links\rg.exe`) | **Configurado en PATH.** Búsqueda de patrones y texto ultra-rápida en todo el repositorio para asistencia de la IA. |
| **`fd`** (find alternative) | **`10.5.0`** (`WinGet\Links\fd.exe`) | **Configurado en PATH.** Búsqueda rápida de archivos y rutas por nombre o extensión. |
| **`gh`** (GitHub CLI) | **`2.100.0`** (`C:\Program Files\GitHub CLI\gh.exe`) | **Configurado en PATH.** Gestión de PRs, issues, releases y verificación de workflows de CI en GitHub. |
| **`jq`** (JSON Processor) | **`1.8.2`** (`WinGet\Links\jq.exe`) | **Configurado en PATH.** Transformación, parseo y extracción de payloads JSON en CLI (FCM v1, Firestore REST, SonarQube). |
| **`ktlint`** (Kotlin Linter & Formatter) | **`1.8.0`** (`C:\Users\Josue\.local\bin\ktlint.cmd`) | **Configurado en PATH.** Análisis estático rápido y autoformateo de código Kotlin conforme a convenciones oficiales (`ktlint --format`). |
| **`sonar-scanner`** (SonarQube Standalone CLI) | **`5.0.0`** (`C:\Users\Josue\.local\bin\sonar-scanner.cmd`) | **Configurado en PATH.** Escaneo estático independiente contra servidor local SonarQube (`http://127.0.0.1:9000`) para proyectos fuera de Gradle (Unity, C#, scripts). |
| **`bundletool`** (Android App Bundle CLI) | **`1.18.3`** (`C:\Users\Josue\.local\bin\bundletool.cmd`) | **Configurado en PATH.** Manipulación e inspección de archivos `.aab`, extracción de APKs específicos por dispositivo e instalación con `adb`. |
| **`fcm-send`** (FCM HTTP v1 Tester) | Script CLI (`C:\Users\Josue\.local\bin\fcm-send.cmd`) | **Configurado en PATH.** Envío y validación (`-DryRun`) de notificaciones Push directas a dispositivos vía API v1 de FCM usando credenciales `gcloud`. |
| **`httptoolkit`** (HTTP/HTTPS Interceptor) | **`1.27.1`** (`C:\Users\Josue\.local\bin\httptoolkit.cmd`) | **Configurado en PATH.** Intercepción y diagnóstico de tráfico de red HTTPS en tiempo real entre la app Android y Firebase/servidores externos. |
| **`scrcpy`** (Screen Copy / Mirror) | **`4.1`** (`C:\Users\Josue\.local\bin\scrcpy.cmd`) | **Configurado en PATH.** Control, visualización y captura de pantalla/video en tiempo real de dispositivos Android físicos o emuladores (`scrcpy`). |
| **`uv`** (Python Package Manager) | **`0.11.24`** (`E:\Krita\ComfyUI\uv\uv.exe`) | **Configurado en PATH.** Gestor de paquetes y entornos virtuales de Python ultrarrápido escrito en Rust. |
| **`ruff`** (Python Linter & Formatter) | **`0.16.7`** (`C:\Users\Josue\.local\bin\ruff.exe`) | **Configurado en PATH.** Linter y formateador ultrarrápido en Rust para validación instantánea de código Python. |
| **`mypy`** (Static Type Checker) | **`2.3.1`** (`C:\Users\Josue\.local\bin\mypy.exe`) | **Configurado en PATH.** Chequeo estático de tipos para detectar bugs antes de la ejecución. |
| **`pytest`** (Testing Framework) | **`9.1.1`** + `pytest-cov 7.1.0` (`C:\Users\Josue\.local\bin\pytest.exe`) | **Configurado en PATH.** Ejecución de pruebas unitarias y cálculo de cobertura en scripts y utilidades Python. |
| **`pre-commit`** | **`4.6.2`** (`C:\Users\Josue\.local\bin\pre-commit.exe`) | **Configurado en PATH.** Gestión e invocación de hooks automáticos de Git previos a cada commit. |
| **`node` / `npm`** | Entorno global de Node.js | Ejecución de utilidades JavaScript y runtime para servidores MCP. |

## 24.2 Servidores MCP Configurados (Antigravity IDE)

| Servidor MCP | Tipo / Protocolo | Capacidad y Uso para la IA |
| :--- | :--- | :--- |
| **`android-studio-index`** | Streamable HTTP (`localhost:29171`) | **Navegación en Android Studio:** Búsqueda de definiciones, referencias, diagnósticos de compilación en tiempo real, jerarquías de llamadas y refactorización segura de símbolos Kotlin. |
| **`firebase-mcp-server`** | Stdio (`firebase.cmd mcp`) | **Gestión de Firebase:** Consulta de reglas de seguridad activas en vivo (`firebase_get_security_rules`), proyectos, huellas SHA-1/256 de Android y configuración de SDKs. |
| **`google-cloud-firestore`** | SSE (`https://firestore.googleapis.com/mcp`) | **Consultas a Base de Datos:** Listado de colecciones, inspección de documentos, agregaciones y gestión de índices en Firestore. |
| **`google-developer-knowledge`** | SSE (`https://developerknowledge.googleapis.com/mcp`) | **Documentación Oficial:** Consulta grounded de APIs de Google, Jetpack Compose, Material 3 y Firebase. |
| **`sonarqube`** | Stdio (`sonarqube-mcp-server.jar`) | **Auditoría de Calidad:** Verificación de Quality Gates, Security Hotspots, code smells y cobertura de tests en servidor SonarQube local. |
| **`unity-mcp`** | Stdio Relay (`relay_win.exe`) | **Ecosistema Multiplataforma:** Inspección y asistencia para la aplicación hermana *Premia Pass Business* (Unity). |

## 24.3 Estado de Herramientas de Entorno

- [x] **Android Debug Bridge (`adb`) agregado al PATH de usuario:** Configurado permanentemente en Windows (`C:\Users\Josue\AppData\Local\Android\Sdk\platform-tools`). Disponible para ejecución global de comandos de depuración e instalación.
- [x] **Android `cmdline-tools` (`apkanalyzer`, `profgen`, `sdkmanager`):** Descargadas e integradas en `C:\Users\Josue\AppData\Local\Android\Sdk\cmdline-tools\latest` con wrappers en PATH.
- [x] **Herramientas de Build y Firma de Android (`aapt2`, `zipalign`, `apksigner`, `keytool`):** Configuradas en PATH y con wrappers en `C:\Users\Josue\.local\bin\`. Variables `ANDROID_HOME` y `JAVA_HOME` registradas.
- [x] **Herramientas de Python (`uv`, `ruff`, `mypy`, `pytest`, `pre-commit`):** Entorno moderno en PATH gestionado por `uv tool` con linter, type-checker, test runner y hooks activos.
- [x] **Firebase Emulator Suite Preparado:** Binarios locales descargados para Firestore (v1.22.0) y Emulator UI (v1.15.0) para pruebas offline sin afectar producción.
- [x] **Gestión de Android App Bundles (`bundletool`):** Versión 1.18.3 configurada en PATH para inspección y despliegue de paquetes `.aab`.
- [x] **Pruebas de Notificaciones Push (`fcm-send`):** Helper CLI configurado en PATH para testing directo de la API FCM HTTP v1 sin necesidad de backend intermediario.
- [x] **Inspección de Tráfico de Red (`httptoolkit`):** Versión 1.27.1 instalada y accesible para auditoría de tráfico HTTPS en emuladores y dispositivos Android.
- [x] **Control y Mirroring de Dispositivos (`scrcpy`):** Actualizado a versión 4.1 y configurado en PATH para validación visual de UI en tiempo real.
- [x] **Herramientas Transversales (`rg`, `fd`, `gh`, `jq`):** Instaladas y configuradas en PATH para búsqueda y procesamiento CLI.
- [x] **Linters y Auditoría Standalone (`ktlint`, `sonar-scanner`):** `ktlint` 1.8.0 standalone en JDK 21 y `sonar-scanner` 5.0.0 configurados en PATH para validación de código Kotlin y proyectos multiplataforma.
- [x] **Unity CLI Wrapper (`unity`) agregado a PATH:** Configurado en `C:\Users\Josue\.local\bin\unity.cmd` con resolución dinámica según versión de proyecto.
- [x] **UnityYAMLMerge configurado en PATH y Git Driver:** Configurado en `C:\Users\Josue\.local\bin\unity-yaml-merge.cmd` y registrado como driver `merge.unityyamlmerge` global en `.gitconfig`.
- [x] **Git LFS verificado y activo:** Versión 3.7.0 en PATH y hooks configurados.

---
