# 📊 Guía de Reportes - Project Automation CF

## 🎯 Tipos de Reportes

Este proyecto genera múltiples tipos de reportes para diferentes necesidades:

### 1. Reportes HTML (pytest-html)
- **Formato:** HTML autónomo (self-contained)
- **Generación:** Automática en CI/CD
- **Ubicación:** Artefactos de GitHub Actions
- **Ventajas:** 
  - No requiere instalación adicional
  - Incluye logs detallados
  - Se puede abrir en cualquier navegador
  - Muestra duración de tests
  - Filtra por resultado (passed/failed/skipped)

### 2. Reportes Allure
- **Formato:** Dashboard interactivo
- **Generación:** Manual (local)
- **Ventajas:**
  - Gráficos y tendencias
  - Histórico de ejecuciones
  - Categorización de fallos
  - Timeline de ejecución

### 3. Screenshots de fallos
- **Formato:** PNG
- **Generación:** Automática al fallar test UI
- **Ubicación:** `screenshots/` (local) o artefactos (CI)

---

## 📥 Cómo Acceder a Reportes del Pipeline

### Paso 1: Ir a GitHub Actions
1. Abre el repositorio en GitHub
2. Click en la pestaña **"Actions"**
3. Verás el listado de ejecuciones

### Paso 2: Seleccionar ejecución
- Las ejecuciones exitosas tienen ✅ (check verde)
- Las fallidas tienen ❌ (cruz roja)
- Click en la ejecución que quieres revisar

### Paso 3: Descargar artefactos
1. Baja hasta el final de la página
2. Sección **"Artifacts"**
3. Click en el artefacto para descargarlo:

#### Artefactos disponibles:

| Artefacto | Contenido | Workflow |
|-----------|-----------|----------|
| `api-test-report` | Reporte HTML de tests API | API Tests |
| `web-test-report-chrome` | Reporte HTML UI (Chrome) | Web Tests |
| `web-test-report-firefox` | Reporte HTML UI (Firefox) | Web Tests |
| `web-test-report-edge` | Reporte HTML UI (Edge) | Web Tests |
| `web-test-screenshots-chrome` | Screenshots de fallos (Chrome) | Web Tests |
| `web-test-screenshots-firefox` | Screenshots de fallos (Firefox) | Web Tests |
| `web-test-screenshots-edge` | Screenshots de fallos (Edge) | Web Tests |
| `bdd-test-report` | Reporte HTML tests BDD | BDD Tests |

### Paso 4: Ver el reporte
1. Descomprime el archivo `.zip`
2. Abre el archivo `.html` en tu navegador
3. Navega por los resultados

---

## 🖥️ Generar Reportes Localmente

### Reporte HTML simple
```bash
# Tests de API
pytest api_tests/ -v --html=report-api.html --self-contained-html

# Tests de Web (navegador por defecto: Chrome)
pytest web_tests/ -v --html=report-web.html --self-contained-html

# Tests de Web con Firefox
BROWSER=firefox pytest web_tests/ -v --html=report-web-firefox.html --self-contained-html

# Tests BDD
pytest pytest_bdd_tests/ -v --html=report-bdd.html --self-contained-html
```

### Reporte Allure

#### 1. Instalar Allure (si no lo tienes)

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Windows:**
```bash
scoop install allure
```

#### 2. Generar y visualizar
```bash
# Ejecutar tests y generar datos Allure
pytest api_tests/ --alluredir=allure-results

# Visualizar reporte (abre navegador automáticamente)
allure serve allure-results

# O generar reporte estático
allure generate allure-results -o allure-report --clean
```

---

## 🔍 Interpretar Reportes HTML

### Secciones del reporte:

#### 1. Summary (Resumen)
- **Total de tests ejecutados**
- **Passed:** Tests exitosos ✅
- **Failed:** Tests fallidos ❌
- **Skipped:** Tests omitidos ⚠️
- **Duración total**

#### 2. Environment (Entorno)
- Python version
- Sistema operativo
- Plugins de pytest
- Variables de CI

#### 3. Results Table (Tabla de resultados)
Cada fila es un test con:
- **Result:** Estado del test
- **Test:** Nombre del test
- **Duration:** Tiempo de ejecución
- **Links:** Enlaces adicionales

#### 4. Detalles al expandir
Click en una fila para ver:
- **Logs completos** de la ejecución
- **Assertions** que fallaron
- **Stack trace** de errores
- **Screenshots** (tests UI)

### Filtros disponibles:
- Click en "Failed" para ver solo los fallidos
- Click en "Passed" para ver solo los exitosos
- "Show all details" / "Hide all details"

---

## 📸 Screenshots Automáticos

### ¿Cuándo se toman?
Los screenshots se toman **automáticamente** cuando un test UI falla.

### Ubicación:
- **Local:** `screenshots/` en la raíz del proyecto
- **CI/CD:** Artefacto `web-test-screenshots-{browser}`

### Naming:
```
{nombre_del_test}_{timestamp}.png
```

Ejemplo:
```
test_shophub_login_20251030_153045.png
```

### Ver screenshots en reportes HTML:
Los screenshots aparecen **incrustados** en el reporte HTML cuando expandes un test fallido.

---

## 🔄 Historial de Reportes

### En GitHub Actions:
- Los artefactos se conservan **30 días**
- Puedes ver ejecuciones históricas en Actions
- Cada commit/push genera nuevos reportes

### Local (Allure):
Allure puede mantener histórico si ejecutas:
```bash
# Primera ejecución
pytest --alluredir=allure-results

# Siguientes ejecuciones (acumula histórico)
pytest --alluredir=allure-results --clean-alluredir=False
```

---

## 🎨 Personalizar Reportes

### Agregar metadata a reportes HTML:

En `pytest.ini`:
```ini
[pytest]
addopts = 
    --html=report.html 
    --self-contained-html
    --metadata "Project" "Automation CF"
    --metadata "Tester" "Tu Nombre"
```

### Agregar descripción a tests:
```python
@pytest.mark.TC_API_01
def test_example():
    """
    TC-API-01: Descripción del test
    
    Este texto aparecerá en el reporte.
    """
    pass
```

---

## 🐛 Troubleshooting

### Problema: No se generan reportes
**Causa:** Falta librería pytest-html  
**Solución:**
```bash
pip install pytest-html
```

### Problema: Screenshots no aparecen
**Causa:** Carpeta `screenshots/` no existe  
**Solución:** Se crea automáticamente en conftest.py

### Problema: Artefactos no se suben en CI
**Causa:** Test terminó con error antes de `upload-artifact`  
**Solución:** Ya está configurado con `if: always()`

### Problema: Reporte muy pesado
**Causa:** Muchos screenshots o logs largos  
**Solución:** Usar `--tb=short` para logs más cortos

---

## 📋 Checklist de Reportes

Antes de entregar un reporte:

- [ ] Verificar que todos los tests críticos pasaron
- [ ] Revisar tests fallidos y sus logs
- [ ] Descargar screenshots de fallos
- [ ] Verificar duración de tests (timeout)
- [ ] Comparar con ejecución anterior
- [ ] Documentar bugs encontrados

---

## 🔗 Enlaces Útiles

- [Documentación pytest-html](https://pytest-html.readthedocs.io/)
- [Documentación Allure](https://docs.qameta.io/allure/)
- [GitHub Actions Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)