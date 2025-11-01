import pytest
import time
from pages.shophub_home_page import HomePage

"""
Caso de prueba: TC-WEB-08: Agregar producto al carrito (logueado)
Objetivo: Verificar que un usuario autenticado pueda agregar un producto al carrito de compras.
Esta prueba requiere un usuario autenticado.
"""


def test_add_product_to_cart_as_logged_in_user(driver):
    """
    TC-WEB-08: Agregar producto al carrito (logueado).
    Este test usa métodos POM donde es posible.
    """
    # Credenciales del usuario de prueba
    test_email = "admin@demo.com"
    test_password = "SecurePass123!"

    # 1. Ir a la página principal
    home_page = HomePage(driver)
    home_page.go_to()

    # 2. Hacer login usando métodos POM
    login_page = home_page.click_login()
    login_page.enter_email(test_email)
    login_page.enter_password(test_password)
    login_page.click_sign_in()
    print("ℹ️  Login realizado.")

    # 3. Volver a la página principal
    home_page.go_to()

    # 4. Obtener contador inicial del carrito usando método POM
    initial_cart_count = home_page.get_cart_item_count()
    print(f"📊 Contador inicial del carrito: {initial_cart_count}")

    # 5. Abrir menú Categories usando método POM
    try:
        home_page.click_categories_dropdown()
        print("✅ Menú 'Categories' abierto.")
    except Exception as e:
        pytest.fail(f"No se pudo abrir el menú Categories. Error: {e}")

    # 6. Hacer clic en Men's Clothes usando método POM
    try:
        category_page = home_page.click_mens_category()
        print("✅ Categoría 'Men's Clothes' seleccionada.")
    except Exception as e:
        pytest.fail(f"No se pudo seleccionar Men's Clothes. Error: {e}")

    # 7. Seleccionar primer producto usando método POM de CategoryPage
    try:
        product_page = category_page.get_first_product_link()
        print("✅ Primer producto seleccionado.")
    except Exception as e:
        pytest.fail(f"No se pudo seleccionar el primer producto. Error: {e}")

    # 8. Agregar al carrito usando método POM de ProductPage
    try:
        product_page.click_add_to_cart()
        time.sleep(1)  # Esperar a que se actualice el carrito
        print("✅ Producto agregado al carrito.")
    except Exception as e:
        pytest.fail(f"No se pudo agregar al carrito. Error: {e}")

    # 9. Verificar - Estrategia 1: Contador del carrito
    verification_success = False

    try:
        time.sleep(1)
        new_cart_count = home_page.get_cart_item_count()
        print(f"📊 Contador después de agregar: {new_cart_count}")

        if new_cart_count > initial_cart_count:
            print(f"✅ Contador incrementó: {initial_cart_count} → {new_cart_count}")
            verification_success = True
        else:
            print("⚠️  Contador no incrementó. Intentando verificación alternativa...")
    except Exception as e:
        print(f"⚠️  Error al verificar contador: {e}. Intentando verificación alternativa...")

    # 10. Verificar - Estrategia 2: Navegar al carrito y verificar items
    if not verification_success:
        try:
            # Usar método POM para ir al carrito
            cart_page = home_page.go_to_cart_robust()
            print("✅ Navegando a la página del carrito...")
            time.sleep(2)

            # Verificar que hay items usando método POM
            cart_items = cart_page.get_cart_items()
            if len(cart_items) > 0:
                print("✅ Producto encontrado en el carrito.")
                verification_success = True
            else:
                pytest.fail("No se encontraron productos en el carrito.")

        except Exception as cart_error:
            pytest.fail(f"Error al verificar carrito: {cart_error}")

    # 11. Verificación final
    assert verification_success, "No se pudo verificar que el producto fue agregado al carrito"
    print("✅ TEST COMPLETADO EXITOSAMENTE")
