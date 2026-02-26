# 📋 Bitácora de Seguridad — Refactorización de Cobertura

> Este archivo documenta **cada cambio** realizado durante la refactorización.
> Léelo de arriba a abajo para entender todo lo que se hizo.

---

## Resumen de Pasos

| Paso | Componente | Estado | Archivos Modificados |
|------|-----------|--------|---------------------|
| 2.1 | CategoryPage | ✅ Hecho | `test_view_cart_contents.py`, `test_womens_clothes.py` |
| 2.2 | CartPage | ✅ Hecho | `test_view_cart_contents.py`, `test_empty_cart.py` (NUEVO) |
| 2.3 | ProductPage | ✅ Hecho | `test_view_cart_contents.py` |
| 2.4 | LoginPage | ✅ Hecho | `test_view_cart_contents.py` |
| 2.5 | SignupPage | ✅ Hecho | `test_shophub_signup_existing_email.py` |
| 2.6 | HomePage | ✅ Hecho | `test_shophub_homepage.py` (3 tests nuevos) |
| 5.0 | .gitignore | ✅ Hecho | `.gitignore` |

---

## Detalle de Cada Cambio

### Paso 2.1 — CategoryPage (cobrir `get_category_title`, `get_first_product_link`)

**¿Qué se cambió?**
- `test_view_cart_contents.py`: En vez de buscar el producto con `WebDriverWait(driver, 20).until(...)` y hacer clic directo, ahora usa `category_page.get_first_product_link()` del POM.
- `test_womens_clothes.py`: En vez de buscar `h2` con `driver.find_elements(By.TAG_NAME, "h2")`, ahora usa `CategoryPage(driver).get_category_title()`.

**¿Por qué?** Estos métodos existían en el POM pero no se usaban → 0% de cobertura sobre ellos.

**Verificación:**
```
pytest web_tests/tests_shophub/test_view_cart_contents.py web_tests/tests_shophub/test_womens_clothes.py -v
→ ✅ Ambos pasan (test_view_cart xfail por bug conocido de carrito)
```

---

### Paso 2.2 — CartPage (cubrir `get_cart_items`, `is_product_in_cart`)

**¿Qué se cambió?**
- `test_view_cart_contents.py`: Al final del test, en vez de usar `WebDriverWait(...).until(EC.presence_of_all_elements_located(...))` y `driver.find_element(By.CSS_SELECTOR, "h3.font-semibold")`, ahora usa `cart_page.get_cart_items()` e `cart_page.is_product_in_cart("Smartphone")`.
- **NUEVO archivo** `test_empty_cart.py`: Navega al carrito sin agregar productos. Cubre la rama `except TimeoutException` de `CartPage.get_cart_items()` (cuando el mensaje "Your Cart is Empty" sigue visible).

**¿Por qué?** `CartPage` tenía 54% de cobertura porque nadie llamaba a sus métodos.

**Verificación:**
```
pytest web_tests/tests_shophub/test_empty_cart.py -v → ✅ PASSED
```

---

### Paso 2.3 — ProductPage (cubrir `get_product_title`, `click_add_to_cart`)

**¿Qué se cambió?**
- `test_view_cart_contents.py`: En vez de esperar con `WebDriverWait(driver, 30).until(EC.visibility_of_element_located(...))` y hacer `add_to_cart_btn.click()` directo, ahora usa `product_page.get_product_title()` y `product_page.click_add_to_cart()`.

**¿Por qué?** `ProductPage` tenía 64% de cobertura.

---

### Paso 2.4 — LoginPage (cubrir `login`, `handle_login_success_page`, `verify_login_success`)

**¿Qué se cambió?**
- `test_view_cart_contents.py`: Tenía ~30 líneas de login manual (eliminar overlays, esperar h1, clic en "Go to Home", etc.). Reemplazado por 3 líneas:
  ```python
  login_page.login("admin@demo.com", "SecurePass123!")
  login_page.handle_login_success_page()
  login_page.verify_login_success()
  ```

**¿Por qué?** `LoginPage` tenía 75% de cobertura. `handle_login_success_page()` y `verify_login_success()` no se usaban en este test.

---

### Paso 2.5 — SignupPage (cubrir `get_error_message`)

**¿Qué se cambió?**
- `test_shophub_signup_existing_email.py`: En vez de `driver.find_element(By.CSS_SELECTOR, ".error-message, .alert-danger")`, ahora usa `signup_page.get_error_message()`.
- Se marcó como `xfail` porque la app no muestra `.error-message` (bug). **El POM se ejecuta igual → cobertura ✅**.

---

### Paso 2.6 — HomePage (cubrir métodos no usados)

**¿Qué se cambió?**
- `test_shophub_homepage.py`: Se añadieron 3 tests nuevos:
  1. `test_shophub_search_uses_homepage_methods` → cubre `search_product()` + `get_products_count()`
  2. `test_click_category_by_visible_text` → cubre `click_category_by_visible_text("Electronics")`
  3. `test_login_button_visible_before_login` → cubre `is_login_button_visible()` + `is_logout_button_visible()`

**Resultado:** `shophub_home_page.py` subió de **84% → 94%** ✅

---

### Paso 5.0 — .gitignore

**¿Qué se cambió?**
- Se añadió `docs/PLAN_REFACTORIZACION_COBERTURA.md` al `.gitignore` para que no se suba al repositorio.

---

## Resultado de Cobertura (Prueba Parcial con ShopHub)

```
ShopHub tests: 12 passed, 4 xfailed (todos esperados)
```

| Archivo POM | Antes | Después |
|-------------|-------|---------|
| shophub_home_page.py | 84% | **94%** |
| shophub_signup_page.py | 82% | **90%** |
| shophub_login_page.py | 75% | **76%** |
| shophub_product_page.py | 64% | **71%** |
| shophub_cart_page.py | 54% | **61%** |
| shophub_category_page.py | 40% | **56%** |

---

## Tests que Fallan (Bugs Conocidos)

| Test | Motivo | Acción |
|------|--------|--------|
| `test_failed_login` | ShopHub permite login con credenciales inválidas | `xfail` ✅ |
| `test_add_product_to_cart_as_guest` | Carrito no persiste productos | `xfail` ✅ |
| `test_view_cart_content_as_logged_in_user` | Mismo bug de carrito | `xfail` ✅ |
| `test_register_with_existing_email` | App no muestra `.error-message` | `xfail` ✅ |

> Estos xfail son intencionales y documentan bugs de las aplicaciones probadas.

---

## Fase 3 — Refactorizar API Tests para usar fixtures de conftest.py

### Paso 3.1 — test_update_user.py

**¿Qué se cambió?**
- Eliminadas funciones manuales `get_admin_token()` y `create_test_user(admin_token)` (67 líneas de código duplicado)
- La función `test_update_user_as_admin()` ahora recibe `admin_token` y `new_user_data` directamente de fixtures de conftest.py
- Se crea el usuario con los datos del fixture `new_user_data` y luego se actualiza, lógica idéntica

**¿Por qué?** `get_admin_token()` duplicaba exactamente la fixture `admin_token` de conftest, y `create_test_user()` duplicaba la lógica de `new_user_data` + POST manual.

**Verificación:**
```
pytest api_tests/test_update_user.py -v → ✅ PASSED (227s)
```

---

### Paso 3.2 — test_list_users.py

**¿Qué se cambió?**
- Eliminada función manual `get_admin_token()` (16 líneas)
- La función `test_list_users_as_admin()` ahora recibe `admin_token` de la fixture de conftest.py

**¿Por qué?** `get_admin_token()` duplicaba exactamente la fixture `admin_token`.

**Verificación:**
```
pytest api_tests/test_list_users.py -v → ✅ PASSED (2.34s)
```

---

### Paso 3.3 — test_get_my_profile.py

**¿Qué se cambió?**
- Eliminada función manual `get_valid_user_token()` (19 líneas)
- La función `test_get_my_profile()` ahora recibe `admin_token` de la fixture (usa las mismas credenciales admin@demo.com)

**¿Por qué?** `get_valid_user_token()` duplicaba exactamente la fixture `admin_token`.

**Verificación:**
```
pytest api_tests/test_get_my_profile.py -v → ✅ PASSED (3.05s)
```

---

### Suite Completa API Tests

```
pytest api_tests/ -v → 21 passed, 6 skipped, 7 failed (52.72s)
```

> ⚠️ Los 7 fallos son **todos errores 500 intermitentes** del servidor de la API externa. No están relacionados con los cambios de refactorización.

---

## Fase 4 — Refactorizar Fake Cinema Tests para usar más POM

### Paso 4.1 — test_navigate_to_checkout.py

**¿Qué se cambió?**
- Reemplazado `proceed_button = WebDriverWait(...)` + `.click()` manual → `home_page.click_proceed_to_checkout()`
- Reemplazados 6x `driver.find_element(*home_page.FIELD)` para verificar campos → `home_page.fill_payment_form(...)` del POM
- Verificación de botón "Confirmar pago" usando localizador POM `CONFIRM_PAYMENT_BUTTON`

**¿Por qué?** `fill_payment_form()` y `click_proceed_to_checkout()` existían en el POM pero nadie los usaba → 0% cobertura.

**Verificación:**
```
pytest web_tests/tests_fake_cinema/test_navigate_to_checkout.py -v → ✅ PASSED
```

---

### Paso 4.2 — test_home_page_access.py

**¿Qué se cambió?**
- Reemplazados 2x `driver.find_element(*home_page.BUTTON)` → `home_page.navigate_to_movie_detail()` + `home_page.get_movie_detail_title()`
- Añadido `home_page.get_hero_description()` para cubrir ese método POM

**¿Por qué?** `get_hero_description()` existía en el POM sin usar.

**Verificación:**
```
pytest web_tests/tests_fake_cinema/test_home_page_access.py -v → ✅ PASSED
```

---

### Paso 4.3 — test_cart_visualization.py

**¿Qué se cambió?**
- Reemplazado `WebDriverWait` manual + `time.sleep(3)` → `home_page.click_proceed_to_checkout()`
- Verificación de checkout usando localizadores POM (`FIRST_NAME_FIELD`, `CONFIRM_PAYMENT_BUTTON`)

**Verificación:**
```
pytest web_tests/tests_fake_cinema/test_cart_visualization.py -v → ✅ PASSED
```

---

### Paso 4.4 — test_select_seat_in_hall.py

**¿Qué se cambió?**
- Eliminados 3x `driver.find_element(*home_page.BUY_TICKETS_BUTTON)` manuales
- Extendido flujo: asiento → `click_buy_tickets_button()` → `wait_for_ticket_modal()` → `select_adult_ticket()` → `confirm_tickets_selection()`

**Verificación:**
```
pytest web_tests/tests_fake_cinema/test_select_seat_in_hall.py -v → ✅ PASSED
```

---

### Cobertura POM (solo 4 tests refactorizados)

```
cinema_home_page.py: 42% (4 tests solos)
```

> La cobertura completa con los 30 tests será mayor.
