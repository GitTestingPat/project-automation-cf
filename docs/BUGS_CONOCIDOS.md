# 🐛 Bugs Conocidos en Aplicaciones de Prueba

Documentación de bugs detectados durante las pruebas automatizadas.

---

## ShopHub (https://shophub-commerce.vercel.app/)

### 🔴 BUG-001: Header no actualiza estado después de login exitoso

**Severidad:** Media  
**Estado:** Abierto  
**Detectado en:** test_shophub_login.py::test_successful_login

**Descripción:**
Después de un login exitoso, el botón "Login" en el header NO cambia a "Logout" ni desaparece. El usuario queda logueado (confirmado por página `/login/success` y mensaje "Logged In"), pero el header mantiene el estado de usuario no logueado.

**Pasos para reproducir:**
1. Ir a https://shophub-commerce.vercel.app/
2. Click en "Login"
3. Ingresar credenciales válidas: testuser@example.com / password123
4. Observar el header después del login

**Resultado esperado:**
- Botón "Login" debe cambiar a "Logout" O
- Debe aparecer nombre de usuario en el header O
- Botón "Login" debe desaparecer

**Resultado actual:**
- Botón "Login" permanece visible
- No hay indicación visual de usuario logueado en el header

**Evidencia:**
- Screenshot: `screenshots/test_successful_login_*.png`
- URL final: `https://shophub-commerce.vercel.app/login/success`

**Workaround en tests:**
Validar login exitoso mediante:
- Verificación de URL (`/login/success`)
- Presencia de texto "Logged In" en la página
- Cambio de título de la página

---

### 🔴 BUG-002: Login acepta credenciales inválidas (Crítico)

**Severidad:** Crítica (Seguridad)  
**Estado:** Abierto  
**Detectado en:** test_shophub_login.py::test_failed_login

**Descripción:**
La aplicación permite hacer login con credenciales completamente inválidas. Cualquier email (incluso inexistente) y cualquier contraseña resultan en un login "exitoso".

**Pasos para reproducir:**
1. Ir a https://shophub-commerce.vercel.app/
2. Click en "Login"
3. Ingresar credenciales INVÁLIDAS: usuario_invalido@example.com / contraseña_incorrecta
4. Click en "Sign In"

**Resultado esperado:**
- Error de autenticación
- Mensaje: "Credenciales inválidas" o similar
- Permanecer en página de login
- NO permitir acceso

**Resultado actual:**
- La app muestra "Logged In"
- Mensaje: "Welcome back, usuario_invalido@example.com"
- Permite acceso sin validar credenciales

**Impacto:**
- Vulnerabilidad de seguridad crítica
- Cualquier usuario puede acceder con cualquier credencial
- Bypasses de autenticación

**Evidencia:**
- Screenshot: `screenshots/test_failed_login_*.png`
- URL final: Varía (a veces `/login/success`, a veces home)

**Workaround en tests:**
Test marcado con `pytest.xfail()` debido a bug conocido.

---

## Airline API (https://cf-automation-airline-api.onrender.com)

### 🟡 BUG-003: Errores 500 intermitentes en fixtures

**Severidad:** Media  
**Estado:** Intermitente  
**Detectado en:** Múltiples tests de API

**Descripción:**
La API devuelve error 500 (Internal Server Error) intermitentemente al crear recursos en fixtures (usuarios, aviones, aeropuertos).

**Recursos afectados:**
- POST /aircrafts
- POST /airports  
- POST /auth/signup
- POST /users

**Comportamiento:**
- No es consistente
- Ocurre más frecuentemente en CI/CD
- Posible causa: Cold starts de Render
- Posible causa: Rate limiting

**Resultado esperado:**
201 Created con datos del recurso

**Resultado actual (intermitente):**
500 Internal Server Error

**Workaround en tests:**
- Tests usan `pytest.skip()` cuando detectan 500 en fixtures
- Mensaje descriptivo indica que es fallo de la API, no del test
- Tests pueden reejecutarse

**Código:**
```python
if response.status_code == 500:
    pytest.skip(
        f"La API devolvió un 500 al crear {recurso}. "
        f"Esto indica un posible fallo interno en el servidor de la API de prueba."
    )
```

---

### 🟡 BUG-004: API devuelve 200 en vez de 201 para creación

**Severidad:** Baja  
**Estado:** Abierto  
**Detectado en:** Múltiples endpoints de creación

**Descripción:**
Algunos endpoints devuelven código 200 OK en lugar del estándar 201 Created al crear recursos exitosamente.

**Endpoints afectados:**
- POST /flights (intermitente)

**Resultado esperado:**
201 Created (estándar HTTP para creación exitosa)

**Resultado actual:**
200 OK (indica éxito pero no es semánticamente correcto)

**Impacto:**
- Bajo (funcionalmente correcto)
- Viola convenciones HTTP/REST
- Puede confundir a consumidores de API

**Workaround en tests:**
```python
assert response.status_code in [200, 201], "Aceptar ambos códigos"
```

---

## 📋 Resumen de Bugs

| ID | Aplicación | Severidad | Estado | Tests Afectados |
|----|-----------|-----------|--------|-----------------|
| BUG-001 | ShopHub | Media | Abierto | test_shophub_login (success) |
| BUG-002 | ShopHub | **Crítica** | Abierto | test_shophub_login (failed) |
| BUG-003 | Airline API | Media | Intermitente | Múltiples fixtures |
| BUG-004 | Airline API | Baja | Abierto | test_create_flight |

---

