# 🧪 Project Automation CF

[![Dependabot enabled](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://dependabot.com/)

[![Tests Status](https://img.shields.io/badge/Tests-Running-blue?logo=githubactions)](https://github.com/GitTestingPat/project-automation-cf/actions/)
[![Allure Report](https://img.shields.io/badge/Allure-Report-brightgreen)](https://gittestingpat.github.io/project-automation-cf/)

Proyecto de Automatización de Pruebas para el Bootcamp de Testing Automatizado de Código Facilito.

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

## 🔧 Solución de Problemas

¿Tienes errores al ejecutar los tests? Consulta nuestra guía completa:

👉 **[Guía de Troubleshooting](docs/TROUBLESHOOTING.md)**

Incluye soluciones para:
- Problemas de instalación
- Errores de tests API y UI
- Problemas con el pipeline CI/CD
- Configuración de navegadores
- Timeouts y errores de red
- Y mucho más...

## 📊 Reportes y Resultados

### Reportes Automáticos en CI/CD

Cada ejecución del pipeline genera reportes HTML que se guardan como **artefactos** en GitHub Actions:

#### 🔗 Cómo acceder a los reportes:

1. Ve a la pestaña **[Actions](../../actions)** del repositorio
2. Selecciona el workflow ejecutado (API Tests, Web Tests o BDD Tests)
3. Baja hasta la sección **"Artifacts"**
4. Descarga el reporte que necesites:
   - `api-test-report` - Resultados de tests de API
   - `web-test-report-chrome` - Tests UI en Chrome
   - `web-test-report-firefox` - Tests UI en Firefox
   - `web-test-report-edge` - Tests UI en Edge
   - `web-test-screenshots-*` - Screenshots de fallos
   - `bdd-test-report` - Tests BDD

#### ⏱️ Retención de reportes:
Los artefactos se conservan por **30 días** desde su generación.

#### 🌐 Matriz de navegadores:
Los tests UI se ejecutan simultáneamente en:
- ✅ Chrome (headless)
- ✅ Firefox (headless)
- ✅ Edge (headless)

Cada navegador genera su propio reporte independiente.

### Reportes Locales

#### Generar reporte HTML:
```bash
# API Tests
pytest api_tests/ --html=report.html --self-contained-html

# Web Tests
pytest web_tests/ --html=report.html --self-contained-html

# Con navegador específico
BROWSER=firefox pytest web_tests/ --html=report.html --self-contained-html
```

#### Generar reporte Allure:
```bash
# Ejecutar tests y generar datos
pytest api_tests/ --alluredir=allure-results

# Visualizar reporte
allure serve allure-results
```

### Screenshots automáticos
Los tests UI toman screenshots automáticamente cuando fallan. Se guardan en:
- **Local:** `screenshots/` en la raíz del proyecto
- **CI/CD:** Como artefacto `web-test-screenshots-{browser}`

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
### 4. Ejecutar escenarios BDD con behave
```bash
./run_behave.sh
```
### 5. Ejecutar escenarios BDD con pytest BDD
```bash
pytest pytest_bdd_tests/ -v
```

## 🧪 Cobertura del proyecto

- ✅ **API**: 34/34 endpoints cubiertos (100%)
- ✅ **Web UI**: Flujos críticos, negativos y E2E
- ✅ **BDD**: Escenarios con hooks y reutilización
- ✅ **Esquemas**: Validación de estructura JSON
- ✅ **Tiempo de respuesta**: Medido en pruebas críticas
- ✅ **Errores simulados**: Documentados y verificados


## 📈 Reportes

Para generar reportes con Allure:

1. Generación de reportes dentro del proyecto:
```bash
pytest --alluredir=./reportes
```
2. Generación de reportes web
```bash
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
- 📄 **[Análisis de Testing](docs/TESTING_NARRATIVE.md)** - Las tres historias: producto, proceso 
y calidad de las pruebas

## ⚠️ Limitación Conocida del Entorno de CI

Una de las pruebas de API, `test_create_booking_returns_valid_schema` (en `api_tests/test_booking_schema.py`), puede 
fallar intermitentemente en el entorno de Integración Continua (GitHub Actions) con un error `404 Not Found` al 
intentar buscar vuelos.

**Causa:**
La prueba depende del endpoint externo `GET /flights/search/` de la API de demostración 
(`https://cf-automation-airline-api.onrender.com`). Este endpoint puede responder de manera inconsistente 
(por ejemplo, devolviendo `404`) en ciertos entornos o en momentos específicos, posiblemente debido a:
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

Este comportamiento es un **bug real** en la aplicación web de prueba y ha sido documentado como tal. 
La prueba automatizada está correctamente implementada para detectar este fallo.

**INFORME DE FALLO: PRUEBAS DE CARRITO EN SHOPHUB**

---

**Fecha:** 13 de Septiembre de 2025
**Pruebas Afectadas:**
*   `test_add_product_to_cart_as_guest` (TC-WEB-09)
*   `test_view_cart_contents` (TC-WEB-10)

---

### **1. Resumen del Problema**

Las pruebas automatizadas diseñadas para verificar la funcionalidad del carrito de compras en ShopHub están fallando. 
Aunque el botón "Add to Cart" funciona correctamente (el producto se agrega al carrito), **la página `/cart` 
no refleja este cambio durante la ejecución de las pruebas**. La página del carrito se comporta como 
si estuviera vacía, lo que hace que las aserciones fallen.

---

### **2. Análisis Detallado**

#### **2.1. Comportamiento Esperado vs. Real**

*   **Esperado:**
    1.  El usuario hace clic en "Add to Cart" (ID `add-to-cart-21`).
    2.  El sistema registra el producto en el carrito del usuario.
    3.  Al navegar a `https://shophub-commerce.vercel.app/cart`, la página debe mostrar una lista de productos 
    agregados (al menos uno).
    4.  El método `cart_page.get_cart_items()` debe devolver una lista con al menos un elemento.

*   **Real (Durante la Prueba):**
    1.  El clic en "Add to Cart" se realiza con éxito (no hay excepción).
    2.  El sistema *parece* registrar el producto (el botón del carrito en la barra de navegación muestra un 
    badge con "1").
    3.  Al navegar a `/cart`, la página **NO muestra ningún producto**.
    4.  El método `cart_page.get_cart_items()` devuelve una **lista vacía (`[]`)**.
    5.  La aserción `assert len(cart_items) > 0` falla con el mensaje: `"La página del carrito está vacía. 
    No se encontraron productos."`

#### **2.2. Causa Raíz**

La causa raíz es una **inconsistencia en el estado de la aplicación entre la interfaz de usuario (UI) 
y la lógica de negocio**.

*   **UI (Interfaz de Usuario):** La aplicación actualiza correctamente la UI. El badge del carrito en la barra 
de navegación cambia a "1", lo que indica visualmente al usuario que el producto se ha agregado.
*   **Lógica de Negocio / Estado del Carrito:** La página `/cart`, que es la fuente de verdad para verificar 
el contenido del carrito, **no recibe ni muestra los datos del producto agregado durante la sesión 
de la prueba automatizada**.

Esto sugiere que el estado del carrito (la lista de productos) **no se está persistiendo o comunicando correctamente** 
entre la acción de "agregar" y la vista "carrito" en el contexto de una sesión controlada por Selenium. 
Es posible que la aplicación dependa de un estado de sesión, cookies, o almacenamiento 
local (`localStorage`/`sessionStorage`) que no se está manejando o sincronizando correctamente en el entorno de prueba.

---

### **3. Evidencia**

*   **Resultado de la Prueba:**
    ```
    E       AssertionError: La página del carrito está vacía. No se encontraron productos.
    E       assert 0 > 0
    E        +  where 0 = len([])
    ```
    Este error confirma que `get_cart_items()` devolvió una lista vacía.

*   **HTML de la Página `/cart` (Proporcionado):**
    El HTML estático proporcionado para `https://shophub-commerce.vercel.app/cart` muestra únicamente el estado 
"Your Cart is Empty". Esto indica que, desde la perspectiva del servidor o del estado inicial de la página, 
no hay productos en el carrito, a pesar de la acción previa de agregar uno.

*   **Comportamiento Manual:**
    Se ha confirmado que al interactuar manualmente con la aplicación, el flujo funciona: el producto se agrega 
y se puede ver en la página del carrito. Esto descarta un bug general en la funcionalidad y apunta a un problema 
específico con el entorno de prueba o la sincronización de estado.

---

### **4. Conclusión**

Las pruebas fallan no porque la funcionalidad de "agregar al carrito" esté rota, sino porque **existe una asincronía 
o un problema de persistencia de estado entre la acción de agregar un producto y la renderización de la página del 
carrito en el contexto de la prueba automatizada**.

La aplicación muestra un feedback visual correcto (badge del carrito), pero no logra transferir ese estado 
a la página `/cart` cuando es accedida por el script de prueba. Esto es un **fallo de integración** 
en el entorno de prueba, no necesariamente un bug en la lógica de negocio de la aplicación.

---

### **5. Recomendaciones para el README**

Agregue la siguiente sección al archivo `README.md` del proyecto, bajo un encabezado como **"Estado Actual 
de las Pruebas Automatizadas"** o **"Problemas Conocidos"**:

---

#### **Problemas Conocidos con Pruebas de Carrito**

Las pruebas automatizadas `TC-WEB-09` (Agregar producto al carrito) y `TC-WEB-10` (Ver contenido del carrito) 
están fallando actualmente.

*   **Síntoma:** La prueba puede hacer clic con éxito en el botón "Add to Cart", pero falla al intentar verificar 
el producto en la página `/cart`, la cual aparece vacía.
*   **Causa:** Se ha identificado una inconsistencia en la aplicación donde el estado del carrito 
(la lista de productos) no se persiste o comunica correctamente a la página `/cart` durante la ejecución 
de las pruebas automatizadas con Selenium. El feedback visual (badge del carrito) funciona, pero la página 
de destino no refleja el cambio.
*   **Impacto:** Estas pruebas no pueden pasar en su estado actual, a pesar de que la funcionalidad parece 
funcionar correctamente en pruebas manuales.
*   **Solución Propuesta:** Se requiere una investigación más profunda para determinar cómo la aplicación 
gestiona el estado del carrito (por ejemplo, mediante `localStorage`, `sessionStorage`, cookies o estado 
de sesión del servidor) y modificar las pruebas o la configuración del driver de Selenium para que puedan 
acceder y sincronizar correctamente con ese estado.
*   **Estado:** **En Investigación**. Las pruebas deben ser marcadas como `@pytest.mark.xfail` o movidas 
a una suite de pruebas pendientes hasta que se resuelva esta inconsistencia.

## Licencia

MIT License
---