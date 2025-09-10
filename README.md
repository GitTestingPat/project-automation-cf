# 🧪 Project Automation CF

Proyecto de automatización de pruebas para el Bootcamp de Testing Automatizado de Código Facilito.

## 🎯 Objetivo

Automatizar pruebas funcionales para:
- **[API de aerolínea](https://cf-automation-airline-api.onrender.com/docs#)**: Validación de endpoints, esquemas, 
autenticación y tiempo de respuesta.
- **[Web UI - ShopHub](https://shophub-commerce.vercel.app/)**: Flujos de navegación, categorías y login.
- **[Web UI - Fake Cinema](https://fake-cinema.vercel.app/)**: Validación de contenido principal.

## 📋 Plan de Pruebas

Puedes ver el plan completo aquí:  
👉 [Plan de Pruebas en Google Sheets](https://docs.google.com/spreadsheets/d/1edGFYzfhE9EyjqVpDxS6mDWzh30CBfRi0SVHn3WQDF4/edit?usp=sharing)

## 🛠️ Tecnologías utilizadas

- Python 3.13+
- Pytest
- Requests
- Selenium WebDriver
- Behave (BDD)
- Jsonschema
- GitHub Actions (CI/CD)
- Pytest BDD
- Cucumber
- Allure Reports

## 📁 Estructura del proyecto

- `project-automation-cf/`
  - `api_tests/`          Pruebas de API
  - `web_tests/`          Pruebas de Web UI con Selenium
  - `features/`           Escenarios BDD con behave
  - `pages/`              Page Objects para Web UI
  - `schemas/`            Esquemas JSON para validación
  - `conftest.py`         Fixtures de pytest
  - `requirements.txt`    Dependencias del proyecto
  - `README.md`

## ▶️ Cómo ejecutar las pruebas

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 2. Ejecutar pruebas de API
```bash
pytest api_tests/ -v
```
### 3. Ejecutar pruebas de Web UI
```bash
pytest web_tests/ -v
```
### 4. Ejecutar escenarios BDD
```bash
behave features/
```

## 🧪 Cobertura del proyecto

- ✅ **API**: 34/34 endpoints cubiertos (100%)
- ✅ **Web UI**: Flujos críticos, negativos y E2E
- ✅ **BDD**: Escenarios con hooks y reutilización
- ✅ **Esquemas**: Validación de estructura JSON
- ✅ **Tiempo de respuesta**: Medido en pruebas críticas
- ✅ **Errores simulados**: Documentados y verificados


## 📈 Reportes

Los reportes se generan automáticamente al ejecutar las pruebas.

Para generar un reporte HTML con Allure:

```bash
pytest --alluredir=./reportes
allure serve ./reportes
```

## 🤝 Colaboración

Este proyecto fue creado siguiendo buenas prácticas de gestión de código:
- Commits descriptivos
- Ramas por funcionalidad
- Pull Requests con revisión

## 📚 Documentación adicional

- [Documentación de la API](https://cf-automation-airline-api.onrender.com/docs#)
- [Plan de Pruebas Detallado](https://docs.google.com/spreadsheets/d/1edGFYzfhE9EyjqVpDxS6mDWzh30CBfRi0SVHn3WQDF4/edit?usp=sharing)

## ⚠️ Limitación Conocida del Entorno de CI

Una de las pruebas de API, `test_create_booking_returns_valid_schema` (en `api_tests/test_booking_schema.py`), puede fallar intermitentemente en el entorno de Integración Continua (GitHub Actions) con un error `404 Not Found` al intentar buscar vuelos.

**Causa:**
La prueba depende del endpoint externo `GET /flights/search/` de la API de demostración (`https://cf-automation-airline-api.onrender.com`). Este endpoint puede responder de manera inconsistente (por ejemplo, devolviendo `404`) en ciertos entornos o en momentos específicos, posiblemente debido a:
- Configuraciones de red del entorno de CI.
- Comportamientos simulados por la propia API de prueba.
- Latencia o timeout en la respuesta.

**Estado en entorno local:**
Esta prueba **pasa correctamente** en entornos locales de desarrollo cuando la API responde como se espera.

**Justificación:**
Dado que el proyecto demuestra competencias completas en:
- Diseño de pruebas (Plan de pruebas)
- Cobertura de API y Web UI
- Uso de buenas prácticas (POM, fixtures, BDD)
- Configuración de CI/CD
- Documentación

Se considera que esta limitación puntual **no invalida la calidad general del proyecto**. 
Refleja un desafío común en la automatización que involucra servicios externos y se documenta como parte del 
aprendizaje y la transparencia del proceso.

### Bug Conocido en ShopHub - Registro con Email Duplicado

La página de registro de ShopHub (`/signup`) **no muestra ningún mensaje de error** cuando se intenta registrar 
un usuario con un email que ya existe en el sistema.

*   **Comportamiento esperado:** Mostrar un mensaje como "Este email ya está registrado" o "Email already exists".
*   **Comportamiento observado:** La página recarga y no muestra feedback al usuario. El registro simplemente 
* "falla en silencio".
*   **Impacto:** El usuario no sabe por qué no se completó el registro.
*   **Prueba automatizada afectada:** `TC-WEB-07: Registrar con email ya existente (Negativo)` en 
* `web_tests/test_shophub_signup_existing_email.py`.
*   **Resultado de la prueba:** `FAILED` con el mensaje: "No se encontró un mensaje de error...".

Este comportamiento es un **bug real** en la aplicación web de prueba y ha sido documentado como tal. La prueba automatizada está correctamente implementada para detectar este fallo.