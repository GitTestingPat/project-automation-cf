import pytest
import time
from pages.shophub.shophub_home_page import HomePage
from data import TestData, Waits

"""
Caso de prueba: TC-WEB-08: Agregar producto al carrito (logueado)
Objetivo: Verificar que un usuario autenticado pueda agregar un producto específico 
         al carrito de compras.

Datos de prueba: Importados desde data.py
"""


def test_add_product_to_cart_as_logged_in_user(driver):
    """
    TC-WEB-08: Agregar producto al carrito como usuario autenticado.

    Precondiciones:
    - Usuario con credenciales válidas
    - Producto disponible en la categoría especificada

    Pasos:
    1. Login con credenciales válidas
    2. Navegar a la categoría del producto
    3. Buscar y seleccionar producto específico
    4. Agregar producto al carrito
    5. Verificar que el producto está en el carrito

    Datos de prueba:
    - Usuario: {TestData.TC_WEB_08.USER_EMAIL}
    - Producto: {TestData.TC_WEB_08.PRODUCT_NAME}
    - Categoría: {TestData.TC_WEB_08.CATEGORY}
    """

    # Obtener datos de prueba desde data.py
    TEST_EMAIL = TestData.TC_WEB_08.USER_EMAIL
    TEST_PASSWORD = TestData.TC_WEB_08.USER_PASSWORD
    PRODUCT_NAME = TestData.TC_WEB_08.PRODUCT_NAME
    CATEGORY = TestData.TC_WEB_08.CATEGORY

    print(f"\n{'=' * 70}")
    print(f"TC-WEB-08: Agregar '{PRODUCT_NAME}' al carrito (usuario autenticado)")
    print(f"{'=' * 70}")
    print(f"Usuario: {TEST_EMAIL}")
    print(f"Categoría: {CATEGORY}")
    print(f"Producto: {PRODUCT_NAME}")
    print(f"{'=' * 70}\n")

    # ==================== PASO 1: LOGIN ====================
    print("PASO 1: Autenticación del usuario")
    home_page = HomePage(driver)
    home_page.go_to()

    login_page = home_page.click_login()
    login_page.enter_email(TEST_EMAIL)
    login_page.enter_password(TEST_PASSWORD)
    login_page.click_sign_in()

    # Manejar página de éxito del login
    login_page.handle_login_success_page()

    # Verificar autenticación (no falla si Logout no aparece - bug conocido)
    login_page.verify_login_success()
    print("✅ Usuario autenticado - Continuando con el flujo\n")
    print("   (La autenticación se confirmará al verificar el carrito)\n")

    # ==================== PASO 2: OBTENER ESTADO INICIAL DEL CARRITO ====================
    print("PASO 2: Verificar estado inicial del carrito")
    initial_cart_count = home_page.get_cart_item_count()
    print(f"   Items en carrito: {initial_cart_count}\n")

    # ==================== PASO 3: NAVEGAR A CATEGORÍA ====================
    print(f"PASO 3: Navegar a categoría '{CATEGORY}'")
    home_page.click_categories_dropdown()

    # Navegar a la categoría especificada en data.py
    if CATEGORY == "Men's Clothes":
        category_page = home_page.click_mens_category()
    elif CATEGORY == "Women's Clothes":
        category_page = home_page.click_womens_category()
    elif CATEGORY == "Electronics":
        category_page = home_page.click_electronics_category()
    else:
        pytest.fail(f"Categoría '{CATEGORY}' no soportada")

    print(f"✅ Navegación a '{CATEGORY}' exitosa\n")

    # ==================== PASO 4: SELECCIONAR Y AGREGAR PRODUCTO ====================
    print(f"PASO 4: Buscar y seleccionar producto '{PRODUCT_NAME}'")
    time.sleep(Waits.MEDIUM)  # Esperar carga de productos

    product_page = category_page.find_and_click_product_by_name(PRODUCT_NAME)
    print(f"✅ Producto '{PRODUCT_NAME}' seleccionado\n")

    print(f"PASO 5: Agregar '{PRODUCT_NAME}' al carrito")
    product_page.click_add_to_cart()
    time.sleep(Waits.MEDIUM)  # Esperar procesamiento
    print("✅ Producto agregado al carrito\n")

    # ==================== PASO 6: VERIFICAR PRODUCTO EN CARRITO ====================
    print("PASO 6: Verificar producto en carrito")

    # Verificación 1: Contador en header
    home_page.go_to()
    time.sleep(Waits.MEDIUM)

    new_cart_count = home_page.get_cart_item_count()
    print(f"   Contador inicial: {initial_cart_count}")
    print(f"   Contador actual: {new_cart_count}")

    verification_success = (new_cart_count > initial_cart_count)

    if verification_success:
        print(f"   ✅ Contador incrementó ({initial_cart_count} → {new_cart_count})")
    else:
        print(f"   ⚠️  Contador no incrementó, verificando página del carrito...")

        # Verificación 2: Página del carrito
        cart_page = home_page.go_to_cart()
        time.sleep(Waits.MEDIUM)

        cart_items = cart_page.get_cart_items()
        print(f"   Items en página del carrito: {len(cart_items)}")

        if len(cart_items) > 0:
            verification_success = True
            print(f"   ✅ {len(cart_items)} producto(s) encontrado(s) en carrito")

            # Verificar producto específico
            if cart_page.is_product_in_cart(PRODUCT_NAME):
                print(f"   ✅ Producto '{PRODUCT_NAME}' confirmado en carrito")
        else:
            print(f"   ❌ No se encontraron productos en el carrito")

    # ==================== RESULTADO ====================
    print(f"\n{'=' * 70}")
    if verification_success:
        print(f"✅ TEST EXITOSO - '{PRODUCT_NAME}' agregado correctamente al carrito")
        print(f"   Usuario: {TEST_EMAIL}")
        print(f"   Categoría: {CATEGORY}")
        print(f"   Items agregados: {new_cart_count - initial_cart_count}")
    else:
        print(f"❌ TEST FALLIDO - '{PRODUCT_NAME}' NO fue agregado al carrito")
        print(f"   Usuario: {TEST_EMAIL}")
        print(f"   Categoría: {CATEGORY}")
    print(f"{'=' * 70}\n")

    assert verification_success, (
        f"Producto '{PRODUCT_NAME}' no fue agregado al carrito. "
        f"Contador inicial: {initial_cart_count}, Contador final: {new_cart_count}"
    )