# 🔧 Troubleshooting - Solución de Problemas

Guía completa para resolver problemas comunes en el proyecto de automatización.

---

## 📑 Índice

- [Problemas de Instalación](#-problemas-de-instalación)
- [Problemas con Tests de API](#-problemas-con-tests-de-api)
- [Problemas con Tests UI](#-problemas-con-tests-ui)
- [Problemas con el Pipeline CI/CD](#-problemas-con-el-pipeline-cicd)
- [Problemas con Reportes](#-problemas-con-reportes)
- [Problemas con Pytest](#-problemas-con-pytest)
- [Errores de Red y Timeouts](#-errores-de-red-y-timeouts)

---

## 🛠️ Problemas de Instalación

### Error: `ModuleNotFoundError: No module named 'X'`

**Causa:** Falta instalar dependencias.

**Solución:**
```bash
pip install -r requirements.txt
```

Si persiste:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### Error: `Python version mismatch`

**Causa:** Versión de Python incorrecta.

**Verificar versión:**
```bash
python --version
```

**Solución:**
```bash
# Instalar Python 3.13+
# macOS
brew install python@3.13

# Ubuntu
sudo apt-get update
sudo apt-get install python3.13
```

---

### Error: `ChromeDriver version mismatch`

**Causa:** Versión de Chrome no coincide con ChromeDriver.

**Solución:**
```bash
# Se instala automáticamente con webdriver-manager
pip install webdriver-manager --upgrade
```

O actualizar Chrome:
```bash
# macOS
brew upgrade --cask google-chrome

# Ubuntu
sudo apt-get update
sudo apt-get upgrade google-chrome-stable
```

---

## 🌐 Problemas con Tests de API

### Error: `ConnectionError: Failed to establish connection`

**Causa:** La API externa no está disponible.

**Verificar manualmente:**
```bash
curl https://cf-automation-airline-api.onrender.com/
```

**Soluciones:**
1. **Esperar:** La API en Render puede tener "cold starts" (demora inicial)
2. **Reintentar:** Ejecutar de nuevo después de 1-2 minutos
3. **Verificar estado:** Abrir la URL en el navegador

---

### Error: `500 Internal Server Error` en fixtures

**Causa:** La API de prueba tiene errores intermitentes.

**Comportamiento esperado:**
Los tests usan `pytest.skip()` o `pytest.fail()` para manejar estos errores.

**Verificar logs:**
```bash
pytest api_tests/test_nombre.py -v -s
```

**Si es persistente:**
- Revisar que los datos de prueba sean válidos
- Verificar que no haya conflictos de datos (emails duplicados)

---

### Error: `422 Unprocessable Entity`

**Causa:** Datos de entrada inválidos.

**Solución:**
Revisar el cuerpo de la petición en el test:
```python
# Ejemplo: email debe ser único
email = f"test_{int(time.time())}@example.com"
```

Verificar esquema esperado:
```bash
# Ver documentación de la API
open https://cf-automation-airline-api.onrender.com/docs
```

---

### Tests fallan con: `AssertionError: Expected 201, got 200`

**Causa:** La API a veces devuelve 200 en vez de 201.

**Solución (ya implementada):**
```python
# Aceptar ambos códigos
assert response.status_code in [200, 201]
```

---

## 🖥️ Problemas con Tests UI

### Error: `selenium.common.exceptions.WebDriverException`

**Causa:** Driver no encontrado o incompatible.

**Solución:**
```bash
# Reinstalar selenium
pip uninstall selenium
pip install selenium

# Limpiar cache
rm -rf ~/.wdm
```

---

### Error: `TimeoutException: Element not found`

**Causa:** Elemento no aparece a tiempo.

**Soluciones:**

1. **Aumentar tiempo de espera:**
```python
# En conftest.py
driver.implicitly_wait(20)  # De 10 a 20 segundos
```

2. **Usar espera explícita:**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.ID, "elemento")))
```

3. **Verificar selector:**
```python
# Imprimir HTML para debug
print(driver.page_source)
```

---

### Error: `StaleElementReferenceException`

**Causa:** Elemento cambió después de ser localizado.

**Solución:**
```python
# Re-localizar el elemento
elemento = driver.find_element(By.ID, "id")
# Si falla, buscar de nuevo
elemento = driver.find_element(By.ID, "id")
elemento.click()
```

---

### Tests UI pasan localmente pero fallan en CI

**Causa:** Diferencias de timing en entorno headless.

**Soluciones:**

1. **Agregar esperas:**
```python
import time
time.sleep(1)  # Espera corta después de clicks
```

2. **Verificar headless:**
```bash
# Ejecutar local en modo headless
pytest web_tests/ --headed=False
```

3. **Revisar screenshots:**
Los screenshots automáticos muestran el estado al fallar.

---

### Error: `ElementClickInterceptedException`

**Causa:** Otro elemento está encima (popup, modal).

**Solución:**
```python
# Esperar que elemento sea clickeable
from selenium.webdriver.support import expected_conditions as EC
wait.until(EC.element_to_be_clickable((By.ID, "boton"))).click()

# O cerrar popup primero
driver.find_element(By.CLASS_NAME, "close-modal").click()
```

---

## 🔄 Problemas con el Pipeline CI/CD

### Workflow no se ejecuta

**Causa:** Path filters o branch incorrectos.

**Verificar:**
```yaml
# En.github/workflows/api-tests.yml
on:
  push:
    branches: [ main, master ]  # Verificar nombre de tu branch
    paths:
      - 'api_tests/**'
```

**Solución:**
Hacer push a archivos dentro del path especificado.

---

### Error: `Action failed with "artifacts not found"`

**Causa:** Tests fallaron antes de `upload-artifact`.

**Verificar:**
Revisar logs del step "Run tests".

**Solución (ya implementada):**
```yaml
- name: Upload test report
  if: always()  # Ejecuta siempre, incluso si tests fallan
```

---

### Error: `Marker 'TC_API_XX' not found`

**Causa:** Falta definir marker en pytest.ini.

**Solución:**
Agregar en `pytest.ini`:
```ini
markers =
    TC_API_XX: Descripción del caso
```

---

### Tests pasan localmente pero fallan en GitHub Actions

**Causas comunes:**

1. **Variables de entorno faltantes:**
```yaml
env:
  BROWSER: chrome
```

2. **Diferencias de timezone:**
```python
# Ya configurado en conftest.py
options.add_argument("--timezone=UTC")
```

3. **Recursos limitados:**
CI tiene menos memoria/CPU. Agregar esperas.

---

## 📊 Problemas con Reportes

### No se genera reporte HTML

**Causa:** Falta pytest-html.

**Solución:**
```bash
pip install pytest-html
pytest api_tests/ --html=report.html --self-contained-html
```

---

### Reporte HTML vacío o corrupto

**Causa:** Pytest terminó abruptamente.

**Solución:**
Revisar logs:
```bash
pytest -v --tb=long
```

---

### Screenshots no aparecen en el reporte

**Causa:** Carpeta screenshots/ no existe o no tiene permisos.

**Verificar:**
```bash
ls -la screenshots/
```

**Solución:**
```bash
mkdir -p screenshots
chmod 755 screenshots
```

---

### Allure no muestra histórico

**Causa:** Flag `--clean-alluredir` borra resultados anteriores.

**Solución:**
```bash
# Mantener histórico
pytest --alluredir=allure-results --clean-alluredir=False
```

---

## 🧪 Problemas con Pytest

### Error: `fixture 'X' not found`

**Causa:** Fixture no está en conftest.py o no está importada.

**Solución:**
Verificar que esté definida en `conftest.py`:
```python
@pytest.fixture
def mi_fixture():
    return "valor"
```

---

### Tests no se ejecutan

**Causa:** Naming convention incorrecta.

**Verificar:**
- Archivos: `test_*.py` o `*_test.py`
- Funciones: `test_*`
- Clases: `Test*`

**Ejemplo correcto:**
```python
# test_ejemplo.py
def test_algo():
    assert True
```

---

### Error: `collected 0 items`

**Causa:** pytest no encuentra tests.

**Solución:**
```bash
# Ver qué encuentra pytest
pytest --collect-only

# Especificar directorio
pytest api_tests/ --collect-only
```

---

### Markers no funcionan

**Causa:** No están registrados en pytest.ini.

**Solución:**
Agregar en `pytest.ini`:
```ini
[pytest]
markers =
    slow: Tests lentos
    api: Tests de API
```

Ejecutar:
```bash
pytest -m api
```

---

## 🌐 Errores de Red y Timeouts

### Error: `ReadTimeout: Request took longer than X seconds`

**Causa:** API tarda en responder.

**Solución temporal:**
```python
# Aumentar timeout en requests
response = requests.get(url, timeout=30)
```

**Solución permanente:**
Verificar que la API no esté caída.

---

### Error: `ConnectionRefusedError`

**Causa:** Puerto bloqueado o servicio no corriendo.

**Solución:**
```bash
# Verificar puerto
lsof -i :8000

# Reiniciar servicio
# (si corres servidor local)
```

---

### Tests intermitentes (flaky)

**Causa:** Dependencia de timing o estado externo.

**Soluciones:**

1. **Agregar retries:**
```python
@pytest.mark.flaky(reruns=3)
def test_intermitente():
    pass
```

2. **Usar fixtures con estado limpio:**
```python
@pytest.fixture(autouse=True)
def limpiar_datos():
    # Limpiar antes de cada test
    pass
```

3. **Evitar dependencias entre tests:**
Cada test debe ser independiente.

---

## 🆘 Obtener Ayuda

Si el problema persiste:

### 1. Revisar logs completos
```bash
pytest -v -s --tb=long
```

### 2. Ejecutar test individual
```bash
pytest api_tests/test_ejemplo.py::test_function -v
```

### 3. Activar modo debug
```python
import pdb; pdb.set_trace()
```

### 4. Verificar versiones
```bash
pip list | grep -E 'pytest|selenium|requests'
```

### 5. Limpiar cache
```bash
pytest --cache-clear
rm -rf .pytest_cache __pycache__
```

---

## 📞 Recursos Adicionales

- [Documentación Pytest](https://docs.pytest.org/)
- [Documentación Selenium](https://www.selenium.dev/documentation/)
- [Documentación Requests](https://requests.readthedocs.io/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## 🐛 Reportar Bugs

Si encuentras un bug en el código del proyecto:

1. Verificar que no esté en esta guía
2. Reproducir localmente
3. Documentar pasos para reproducir
4. Crear issue en GitHub con:
   - Descripción del problema
   - Pasos para reproducir
   - Output de error completo
   - Versiones (Python, pytest, etc.)