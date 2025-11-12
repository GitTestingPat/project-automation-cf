# Informe Técnico: Pruebas E2E Inestables en CI/CD

## Resumen Ejecutivo

Las pruebas end-to-end (E2E) con Selenium presentan **fallas intermitentes en GitHub Actions** que no ocurren en ejecución local. Después de múltiples intentos de solución durante varias sesiones, el problema persiste de manera impredecible.

---

## Contexto del Problema

### Síntomas
- **Pruebas que pasan localmente fallan aleatoriamente en CI/CD**
- **Patrón intermitente**: Las mismas pruebas fallan en diferentes ejecuciones en distintos navegadores
- **Error principal**: `TimeoutException` al esperar elementos del DOM (botones de horario, películas, etc.)
- **Navegador más problemático**: Microsoft Edge, seguido de Chrome y Firefox

### Pruebas Más Afectadas
1. `test_attempt_change_movie_without_confirming_selection.py`
2. `test_attempt_enter_text_in_numeric_fields_during_checkout.py`
3. `test_attempt_purchase_whithout_seat_selection.py`
4. `test_attempt_purchase_with_empty_name_field.py`
5. `test_attempt_purchase_with_invalid_ticket_type.py`
6. `test_attempt_purchase_with_previously_used_email_adress.py`

---

## Causa Raíz Identificada

### Problema Principal: Aplicación React + Infraestructura Limitada

La aplicación Fake Cinema está construida con **React**, que renderiza contenido dinámicamente en el cliente. Esto combinado con las **máquinas virtuales compartidas de GitHub Actions** (recursos limitados) causa:

1. **Timing impredecible**: React tarda diferentes tiempos en renderizar elementos en cada ejecución
2. **Recursos insuficientes**: Las VMs de GitHub Actions gratuitas tienen CPU/memoria limitada
3. **Concurrencia**: Múltiples jobs compitiendo por recursos

### Problemas Específicos Detectados

#### 1. Película "Jurassic World" sin horarios en CI/CD
**Descubrimiento**: Todas las pruebas que usaban `JURASSIC_WORLD_DETAIL_BUTTON` fallaban consistentemente porque esta película **no tiene horarios disponibles** en el ambiente de CI/CD.

**Solución aplicada**: Cambiar a `FANTASTIC_FOUR_DETAIL_BUTTON` que sí tiene horarios.

**Resultado**: Redujo fallas de ~15 pruebas a ~3 pruebas.

#### 2. Selección manual de fechas antes del método resiliente
**Problema**: Varios tests llamaban a `select_first_available_date()` ANTES de `select_first_available_time_resilient()`, causando conflictos cuando el método resiliente intentaba cambiar de fecha.

**Solución aplicada**: Eliminamos todas las llamadas a `select_first_available_date()` en 20+ archivos de pruebas, dejando que el método resiliente maneje todo.

**Código removido**:
```python
# ANTES (causaba conflictos)
home_page.select_first_available_date()  # ❌ Pre-selecciona una fecha
home_page.select_first_available_time_resilient()  # Intenta cambiar de fecha si es necesario

# DESPUÉS (correcto)
home_page.select_first_available_time_resilient()  # ✅ Maneja fechas automáticamente
```

#### 3. Selección por posición en grilla vs. selectores específicos
**Problema**: El test `test_attempt_change_movie_without_confirming_selection.py` seleccionaba películas por posición CSS (`div:nth-of-type(4)`, `div:nth-of-type(5)`), lo cual es frágil porque:
- La grilla puede tardar en renderizarse
- Las posiciones pueden cambiar
- El DOM puede no estar estable

**Solución aplicada**: Cambiar a selectores específicos de películas (`FANTASTIC_FOUR_DETAIL_BUTTON`, `JURASSIC_WORLD_DETAIL_BUTTON`).

**Resultado**: No resolvió el problema completamente debido a la naturaleza intermitente.

---

## Soluciones Intentadas (Sin Éxito Completo)

### 1. Aumentar Timeouts
```python
# De 10 a 20, 30, incluso 60 segundos
WebDriverWait(driver, 60).until(...)
```
**Resultado**: ❌ Aumentó tiempo de ejecución de 23 min a 60+ min sin resolver intermitencia

### 2. Aumentar Número de Reintentos
```python
# De 3 a 5 intentos en el metodo resiliente
def select_first_available_time_resilient(self, max_attempts=5):
```
**Resultado**: ❌ Solo aumentó el tiempo de espera antes de fallar

### 3. Agregar Esperas Explícitas
```python
time.sleep(1)
time.sleep(2)
time.sleep(3)
```
**Resultado**: ❌ Empeoró los tiempos sin garantizar estabilidad

### 4. Esperar Estabilidad del DOM
```python
# Esperar que el DOM deje de cambiar
WebDriverWait(driver, 15).until(
    lambda d: (
        d.execute_script("return document.querySelectorAll('*').length;"),
        time.sleep(0.3),
        d.execute_script("return document.querySelectorAll('*').length;")
    )[-1] == d.execute_script("return document.querySelectorAll('*').length;")
)
```
**Resultado**: ❌ No funciona en ambiente CI/CD

### 5. Screenshots para Diagnóstico
**Resultado**: ❌ Mostró que los elementos simplemente no se renderizan a tiempo en CI/CD

---

## Método Resiliente Actual

El método `select_first_available_time_resilient()` implementa:

```python
def select_first_available_time_resilient(self, max_attempts=5):
    """
    Método que maneja la selección de horarios cuando no hay disponibles.
    Si no encuentra horarios, intenta con otras fechas automáticamente.
    """
    timeout = 60 if os.getenv('CI') else 20  # Timeout extendido en CI
    
    for attempt in range(max_attempts):
        try:
            # 1. Esperar carga completa de la página
            # 2. Esperar estabilidad del DOM
            # 3. Hacer scroll
            # 4. Eliminar loaders
            # 5. Buscar botones de horario
            # 6. Si no hay horarios, intentar con otras fechas
            # 7. Seleccionar primer horario disponible
            
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(3)
                continue
            else:
                raise
```

**Limitaciones**:
- Aún falla intermitentemente en CI/CD
- No puede compensar por aplicación React lenta en VMs limitadas
- Timeout de 60 segundos × 5 intentos = hasta 5 minutos de espera antes de fallar

---

## Estado Actual del Pipeline

### Tiempos de Ejecución
- **Local**: 10-20 segundos por test
- **CI/CD**: 1-2 minutos por test
- **Pipeline completo**: 50-60 minutos (30 tests × 3 navegadores)

### Tasa de Fallas
- **Antes de optimizaciones**: ~8-15 tests fallaban por ejecución
- **Después de optimizaciones**: ~1-5 tests fallan intermitentemente
- **Intermitencia**: Las mismas pruebas pasan/fallan aleatoriamente entre ejecuciones

### Navegadores
- **Edge**: Más problemático (recursos limitados, driver menos estable)
- **Chrome**: Intermitente
- **Firefox**: Menos problemático pero no inmune

---

## Recomendaciones

### Soluciones Realistas

#### 1. Aceptar Intermitencia (Corto Plazo)
- **Re-ejecutar pipeline** cuando falle (1-2 veces)
- **Documentar pruebas conocidas como intermitentes**
- **No bloquear deploys** por estas fallas específicas

#### 2. Mejorar Infraestructura (Mediano Plazo)
```yaml
# Usar runners self-hosted con más recursos
runs-on: self-hosted  # En lugar de ubuntu-latest

# O usar runners pagos de GitHub
runs-on: ubuntu-latest-8-cores  # Más recursos
```

#### 3. Reducir Tests E2E (Largo Plazo)
- **Priorizar tests de API** (más rápidos, más estables)
- **Mantener solo tests E2E críticos** (happy paths principales)
- **Mover tests de validación a nivel unitario**

#### 4. Usar Herramientas Especializadas
- **BrowserStack**: VMs dedicadas para Selenium
- **Sauce Labs**: Infraestructura optimizada para E2E
- **Cypress/Playwright**: Alternativas más modernas y estables que Selenium

#### 5. Estrategia de Reintentos a Nivel Pipeline
```yaml
# En GitHub Actions
- name: Run tests
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 30
    max_attempts: 2
    command: pytest web_tests/
```

### Lo Que NO Funciona
❌ **Aumentar timeouts indefinidamente** → Solo aumenta tiempo de ejecución  
❌ **Agregar más `time.sleep()`** → Hace pipeline más lento sin garantías  
❌ **Esperar "estabilidad perfecta"** → Imposible con React + VMs compartidas  
❌ **Intentar "arreglar" cada falla individual** → El problema es sistémico  

---

## Conclusión

**Las fallas intermitentes en tests E2E con Selenium en GitHub Actions son un problema conocido de la industria**, especialmente con:
- Aplicaciones SPA (React/Vue/Angular)
- Runners gratuitos compartidos
- Múltiples navegadores

**No existe una solución mágica.** Las empresas reales:
1. Invierten en mejor infraestructura
2. Reducen dependencia de tests E2E
3. Aceptan cierto nivel de intermitencia
4. Usan herramientas de retry automático

**Para este proyecto de bootcamp**: La mejor estrategia es **aceptar 1-3 fallas intermitentes** y re-ejecutar el pipeline cuando sea necesario. El tiempo invertido en "arreglar perfectamente" estos tests **no justifica el beneficio** dado el contexto académico y los recursos limitados.

---

## Referencias Técnicas

### Archivos Modificados Durante Troubleshooting
- `pages/fake_cinema/cinema_home_page.py` (método `select_first_available_time_resilient`)
- 20+ archivos en `web_tests/tests_fake_cinema/` (eliminación de `select_first_available_date()`)
- Múltiples ajustes de timeouts en tests individuales

### Logs Típicos de Falla
```
WARNING ⚠️ No hay horarios para la fecha actual, probando otra fecha...
WARNING ⚠️ Intento 1 falló: TimeoutException
WARNING ⚠️ Intento 2 falló: TimeoutException
WARNING ⚠️ Intento 3 falló: TimeoutException
WARNING ⚠️ Intento 4 falló: TimeoutException
WARNING ⚠️ Intento 5 falló: TimeoutException
ERROR ❌ Todos los intentos fallaron
selenium.common.exceptions.TimeoutException: Message:
```

### Configuración CI/CD Actual
- **Runner**: `ubuntu-latest` (GitHub Actions gratuito)
- **Navegadores**: Chrome, Firefox, Edge (headless)
- **Python**: 3.13.9
- **Selenium**: 4.x
- **pytest**: 8.4.1

---

**Fecha del informe**: Noviembre 2025  
**Autor**: Patricio Andrade (QA Engineer - Bootcamp)  
**Estado**: PROBLEMA PERSISTENTE - Solución completa requiere cambios de infraestructura o arquitectura de testing