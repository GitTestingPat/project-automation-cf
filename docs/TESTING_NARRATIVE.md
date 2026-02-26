# Las Tres Historias Entrelazadas: ShopHub, Fake-Cinema y API-Airports

> **Documento de análisis de testing**
> 
> PROBAR es contar tres historias entrelazadas: una sobre el estado del producto, una sobre cómo se probó, y una sobre qué tan buenas fueron las pruebas.

---

## Prólogo: El Contexto de la Investigación

Estos tres proyectos representan meses de trabajo sistemático: no simplemente "encontrar bugs" sino generar información relevante sobre el comportamiento de los sistemas bajo prueba. La narrativa que sigue está estructurada como tres historias entrelazadas —como una trenza— porque eso es precisamente lo que fue el trabajo: un proceso iterativo donde descubrir algo sobre el producto llevaba a ajustar cómo probabas, lo cual revelaba las limitaciones de las pruebas mismas.

---

## Historia 1: El Estado del Producto

*...sobre qué hace, cómo falló, y cómo podría fallar de maneras que importan a los clientes...*

### ShopHub — El Comercio Electrónico con Secretos Oscuros

ShopHub es una aplicación de e-commerce construida sobre React/Next.js. En la superficie, ofrece las funcionalidades esperadas: navegación por categorías, carrito de compras, autenticación de usuarios.

#### Lo que descubrí sobre cómo falla

**Autenticación sin validación real (BUG-002 - Crítico)**

El módulo de autenticación no valida credenciales. Cualquier combinación de email y contraseña resulta en un login "exitoso". El sistema muestra "Welcome back, usuario_invalido@example.com" incluso con credenciales completamente inventadas. 

Las pruebas automatizadas capturaron screenshots que documentan este comportamiento. El flujo completo revela: el usuario llega a `/login/success`, ve el mensaje "Logged In", pero el header nunca actualiza su estado —el botón "Login" permanece visible como si nada hubiera pasado.

**Estado del carrito inconsistente**

El carrito de compras presenta una inconsistencia arquitectónica: el contador del header incrementa correctamente cuando agregas un producto (0 → 1), pero al navegar a la página del carrito, este aparece vacío. El estado no persiste entre componentes, lo que sugiere un problema en cómo React maneja el estado global o cómo se sincronizan los stores.

#### Por qué importa a los clientes

Un sistema de autenticación que acepta cualquier credencial es una vulnerabilidad de seguridad crítica. Para los usuarios finales, significa que sus cuentas podrían ser accedidas por cualquiera. Para el negocio, significa que no hay manera confiable de identificar quién está haciendo qué en la plataforma.

---

### Fake-Cinema — La Taquilla que Acepta Todo

Fake-Cinema es una aplicación de reserva de boletos para cine. Visualmente atractiva, con un flujo aparentemente completo desde selección de película hasta pago.

#### Lo que descubrí sobre cómo falla

**Validación de datos de pago inexistente (Crítico - Seguridad)**

El sistema acepta:

| Campo | Valor Aceptado | Debería Aceptar |
|-------|----------------|-----------------|
| Número de tarjeta | `"abcd1234efgh5678"` (texto) | Solo dígitos, 13-19 caracteres |
| CVV | `"ABC"` | Solo 3-4 dígitos |
| Email | `"admin@demo"` (sin TLD) | Formato RFC 5322 válido |

Esto no es un "bug menor" —es una ausencia total de validación client-side en campos críticos de seguridad financiera. El flujo permite completar la compra y llegar a `/confirmation` sin que ningún dato sea verificado.

**Estado de sesión no persistente**

Al recargar la página durante el checkout, el carrito se pierde y el usuario es redirigido a `/cart` vacío. No hay uso de localStorage ni sessionStorage. Toda la información vive únicamente en memoria (React state), lo que hace imposible cualquier flujo que involucre navegación o refresh.

**Botones sin funcionalidad**

| Elemento | Comportamiento Esperado | Comportamiento Real |
|----------|------------------------|---------------------|
| "Elige tu cine" | Filtrar películas por ubicación | No dispara ninguna acción |
| Agregar comida | Actualizar carrito | Sin efecto visible |
| Botón accesibilidad | Feedback visual de activación | Sin feedback |

#### Por qué importa

Para un sistema de pagos, la ausencia de validación significa que la base de datos recibe datos corruptos, el procesamiento de pagos real fallaría, y los usuarios podrían completar flujos que en producción serían rechazados. La falta de persistencia de estado hace que cualquier interrupción (conexión inestable, navegación accidental) destruya todo el progreso del usuario.

---

### API-Airports — La Infraestructura Inestable

La API de aerolíneas es un backend RESTful que maneja autenticación, gestión de usuarios, aeropuertos, vuelos, reservas y pagos.

#### Lo que descubrí sobre cómo falla

**Errores 500 intermitentes (BUG-003)**

La API presenta errores 500 intermitentes, particularmente notables durante los cold starts de Render. Esto afecta especialmente a los fixtures de prueba que necesitan crear recursos (usuarios, aeropuertos) antes de ejecutar los tests principales.

La validación de esquemas JSON funcionó consistentemente —cuando la API respondía. El problema no está en la lógica de negocio sino en la estabilidad del hosting.

#### Por qué importa

Para una API que sirve como backend de reservas de vuelos, la inestabilidad significa que los clientes experimentarán errores intermitentes sin patrón predecible. Los sistemas que consumen esta API necesitarán implementar reintentos robustos, lo que complica la integración.

---

## Historia 2: Cómo Probé

*...cómo operé y observé el producto, cómo reconocí los problemas y su importancia, qué he probado hasta ahora y qué no...*

### Arquitectura de las Pruebas

Desde el inicio, el trabajo siguió el **Page Object Model (POM)** de manera estricta. Cada aplicación tiene sus propios Page Objects que encapsulan selectores y métodos de interacción:

```
pages/
├── shophub_home_page.py
├── shophub_login_page.py
├── shophub_category_page.py
├── fake_cinema/
│   └── cinema_home_page.py
```

Los tests nunca interactúan directamente con selectores CSS o XPath. Toda interacción pasa por métodos del Page Object, lo que permite cambiar la implementación sin modificar los tests.

### Observación Sistemática

**Para ShopHub**, implementé validaciones en capas:

- Estado inicial del DOM antes de cualquier acción
- Presencia/ausencia de elementos específicos (botón Logout vs Login)
- URLs después de acciones críticas
- Contenido de mensajes de confirmación/error
- Screenshots automáticos en cada punto de fallo

**Para Fake-Cinema**, el desafío principal fue el timing. Las aplicaciones React renderizan de forma asíncrona, y lo que funciona en una máquina local con recursos dedicados puede fallar en un entorno CI/CD con recursos compartidos. Desarrollé métodos "resilientes" con reintentos:

```python
def select_first_available_time_resilient(self, max_attempts=3):
    """
    Versión con retry para tests con timing issues en CI/CD.
    """
    import os
    timeout = 30 if os.getenv('CI') else 20
    
    for attempt in range(max_attempts):
        # Esperar que el documento esté completamente cargado
        # Scroll para forzar renderizado de elementos lazy
        # Esperar que desaparezcan loaders
        # Entonces intentar la acción
```

**Para la API**, cada test incluye manejo explícito de errores 500:

```python
if response.status_code == 500:
    pytest.fail(
        f"La API devolvió un error 500. "
        f"Esto indica un fallo interno del servidor. "
        f"Cuerpo: {response.text}"
    )
```

### Reconocimiento de Problemas y su Importancia

La documentación de bugs sigue un formato estructurado:

| ID | Descripción | Severidad | Estado |
|----|-------------|-----------|--------|
| BUG-001 | Header no actualiza estado después de login exitoso | Media | Documentado |
| BUG-002 | Login acepta credenciales inválidas | Crítica (Seguridad) | Documentado |
| BUG-003 | Errores 500 intermitentes en API | Media | Intermitente |

Cada bug documentado incluye pasos para reproducir, resultado esperado vs actual, evidencia (screenshots, logs), y workarounds implementados en los tests.

### Cobertura de Pruebas

#### Lo que probé

| Área | Cobertura |
|------|-----------|
| ShopHub - Autenticación | Login válido, login inválido, signup |
| ShopHub - Carrito | Agregar producto (logueado y guest) |
| Fake-Cinema - Flujo de compra | Selección de película, horario, asiento, pago |
| Fake-Cinema - Validaciones negativas | Campos vacíos, datos inválidos, estados no persistentes |
| API - Módulo Auth | Signup, login válido/inválido |
| API - Módulo Users | CRUD completo, perfiles |
| API - Módulo Airports | Listar, crear, obtener, actualizar, eliminar |
| API - Módulo Flights | Búsqueda, CRUD completo |
| API - Módulo Bookings | Crear, obtener, cancelar |
| API - Módulo Payments | Crear, obtener |

#### Lo que no probé (y por qué)

| Área | Razón |
|------|-------|
| Performance bajo carga | JMeter está en el roadmap, no implementado aún |
| Seguridad profunda | Solo validación superficial de inputs, no pentesting |
| Accesibilidad completa | Solo verificación básica de contraste y navegación por teclado |
| Internacionalización | Las apps están solo en inglés |

---

## Historia 3: Qué Tan Buenas Fueron las Pruebas

*...los riesgos y costos de probar o no probar, qué tan probable es que el producto haya sido probado, qué hizo las pruebas más difíciles...*

### Riesgos y Costos

**El riesgo de no probar más profundo**

La validación de inputs en Fake-Cinema es un hallazgo crítico, pero solo descubrí la superficie. No investigué qué pasa server-side cuando esos datos inválidos llegan. ¿La base de datos los almacena? ¿Hay sanitización en el backend? Probar esto requeriría acceso al código del servidor o herramientas de análisis de tráfico más sofisticadas.

**El costo de probar en CI/CD**

Los tests que funcionan localmente pueden fallar en GitHub Actions por diferencias de timing. Invertí tiempo significativo desarrollando métodos resilientes con reintentos, timeouts extendidos, y esperas explícitas. Cada fallo intermitente en el pipeline requirió investigación: ¿es el test? ¿es la app? ¿es el ambiente?

La matriz de navegadores (Chrome, Firefox, Edge) multiplicó el tiempo de ejecución por tres, pero reveló comportamientos diferentes —Edge tenía timeouts más agresivos, Firefox renderizaba ciertos elementos más lento.

### Probabilidad de Cobertura Adecuada

| Nivel | Áreas |
|-------|-------|
| **Alta probabilidad** | Flujos principales (happy paths), validaciones de entrada para campos críticos, estados de autenticación |
| **Probabilidad media** | Casos edge (timeouts, conexiones perdidas), interacciones entre componentes, estados de error del servidor |
| **Baja probabilidad** | Condiciones de carrera (race conditions), ataques de seguridad reales, comportamiento bajo carga |

### Obstáculos Encontrados

1. **React y el DOM asíncrono**: Los elementos no están disponibles inmediatamente después de la navegación. Requirió implementar esperas explícitas y verificaciones de estado del DOM.

2. **Diferencias entre ambientes**: Local vs CI/CD presentan recursos diferentes. Un test que pasa en 2 segundos localmente puede necesitar 30 segundos en un runner de GitHub.

3. **Aplicaciones de práctica con bugs reales**: ShopHub y Fake-Cinema son apps de práctica, pero tienen bugs genuinos que a veces es difícil distinguir de problemas en los tests.

4. **Cold starts de la API**: Los tests de API fallan intermitentemente cuando el servidor de Render "despierta" después de inactividad.

### Recomendaciones para Mejora

**Implementar inmediatamente:**

- Agregar `pytest-rerunfailures` con `@pytest.mark.flaky(reruns=2)` para tests con timing sensible
- Separar tests estables de tests con dependencias externas
- Usar mocks para la API cuando se prueban flujos de UI

**Implementar a mediano plazo:**

- Paralelización de tests con `pytest-xdist`
- Contenedores Docker para ambiente consistente
- Tests de contrato para la API (Pact o similar)

**Lo que necesitaría para profundizar:**

- Acceso a logs del servidor de las aplicaciones
- Documentación de la arquitectura interna
- Criterios de aceptación claros del product owner

---

## Epílogo: La Trenza Completa

Estas tres historias no son independientes. Descubrir que ShopHub acepta cualquier credencial (producto) llevó a diseñar tests que verifican múltiples indicadores de estado de autenticación (proceso). Eso a su vez reveló que mis tests iniciales eran insuficientes porque solo verificaban un elemento (calidad del testing).

El método resiliente para Fake-Cinema nació de fallos en CI/CD (calidad del testing), lo que requirió entender cómo React renderiza (producto), y diseñar esperas inteligentes que no ralentizaran innecesariamente los tests (proceso).

Los errores 500 de la API (producto) forzaron decisiones sobre cómo manejar fallos externos en tests (proceso), y revelaron que los tests de API tienen dependencias de infraestructura que afectan su confiabilidad (calidad del testing).

Esta es la naturaleza del trabajo de testing: no es lineal, no es solo técnico, y definitivamente no es "encontrar bugs y reportarlos". Es generar información que permite tomar decisiones sobre el software, el proceso de desarrollo, y las pruebas mismas.

---

## Documentación Relacionada

| Documento | Descripción |
|-----------|-------------|
| [BUGS_CONOCIDOS.md](BUGS_CONOCIDOS.md) | Registro formal de bugs detectados |
| [test-cases/](../test-cases/) | Documentación de casos de prueba (IEEE 829) |
| [.github/workflows/](../.github/workflows/) | Pipelines de CI/CD |

### Trazabilidad

Cada test automatizado está vinculado a su caso de prueba mediante markers de pytest:

```python
@pytest.mark.TC_API_01
@pytest.mark.high
@pytest.mark.auth
@pytest.mark.positive
def test_signup_returns_valid_schema():
    ...
```

Ejecutar por caso específico:
```bash
pytest -m TC_API_01 -v
```

---

> *"El objetivo no es 'encontrar bugs' sino generar información relevante para decisiones."*
