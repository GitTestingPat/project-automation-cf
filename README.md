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