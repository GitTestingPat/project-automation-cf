"""
data.py - Datos de prueba centralizados para el proyecto de automatización

Este archivo contiene todos los datos de entrada utilizados en los tests,
incluyendo credenciales de usuarios, datos de productos, URLs, y otros
valores de configuración.
"""


# ==================== CONFIGURACIÓN DE LA APLICACIÓN ====================
class AppConfig:
    """Configuración general de la aplicación bajo prueba"""
    BASE_URL = "https://shophub-commerce.vercel.app"
    TIMEOUT_DEFAULT = 10  # Segundos
    TIMEOUT_OVERLAY = 10  # Segundos para esperar overlays
    WAIT_AFTER_LOGIN = 5  # Segundos después de login success
    WAIT_AFTER_ADD_TO_CART = 3  # Segundos después de agregar al carrito


# ==================== CREDENCIALES DE USUARIOS ====================
class Users:
    """Credenciales de usuarios de prueba"""

    class Admin:
        """Usuario administrador"""
        EMAIL = "admin@demo.com"
        PASSWORD = "SecurePass123!"
        FIRST_NAME = "Admin"
        LAST_NAME = "User"

    class RegularUser:
        """Usuario regular para pruebas"""
        EMAIL = "user@test.com"
        PASSWORD = "TestPass123!"
        FIRST_NAME = "Test"
        LAST_NAME = "User"

    class InvalidUser:
        """Credenciales inválidas para pruebas negativas"""
        EMAIL = "invalid@test.com"
        PASSWORD = "WrongPassword123!"


# ==================== DATOS DE PRODUCTOS ====================
class Products:
    """Información de productos disponibles en el catálogo"""

    class MensClothes:
        """Productos en categoría Men's Clothes"""
        COTTON_T_SHIRT = "Cotton T-Shirt"
        DENIM_JEANS = "Denim Jeans"
        LEATHER_JACKET = "Leather Jacket"
        CATEGORY_NAME = "Men's Clothes"

    class WomensClothes:
        """Productos en categoría Women's Clothes"""
        SUMMER_DRESS = "Summer Dress"
        SILK_BLOUSE = "Silk Blouse"
        CATEGORY_NAME = "Women's Clothes"

    class Electronics:
        """Productos en categoría Electronics"""
        SMARTPHONE = "Smartphone"
        LAPTOP = "Laptop"
        HEADPHONES = "Headphones"
        CATEGORY_NAME = "Electronics"


# ==================== DATOS DE NAVEGACIÓN ====================
class Categories:
    """Nombres de categorías en el sitio"""
    MENS_CLOTHES = "Men's Clothes"
    WOMENS_CLOTHES = "Women's Clothes"
    ELECTRONICS = "Electronics"


# ==================== MENSAJES ESPERADOS ====================
class Messages:
    """Mensajes esperados en la aplicación"""

    class Cart:
        """Mensajes relacionados con el carrito"""
        EMPTY_CART = "Your Cart is Empty"
        EMPTY_CART_MESSAGE = "Looks like you haven't added any items to your cart yet."

    class Login:
        """Mensajes relacionados con login"""
        SUCCESS = "Logged In"
        WELCOME_BACK = "Welcome back"
        INVALID_CREDENTIALS = "Invalid credentials"

    class Product:
        """Mensajes relacionados con productos"""
        OUT_OF_STOCK = "Out of Stock"
        ADDED_TO_CART = "Added to cart"


# ==================== DATOS PARA CASOS DE PRUEBA ESPECÍFICOS ====================
class TestData:
    """Datos específicos para casos de prueba"""

    class TC_WEB_08:
        """TC-WEB-08: Agregar producto al carrito data.py(logueado)"""
        USER_EMAIL = Users.Admin.EMAIL
        USER_PASSWORD = Users.Admin.PASSWORD
        PRODUCT_NAME = Products.MensClothes.DENIM_JEANS
        CATEGORY = Categories.MENS_CLOTHES
        EXPECTED_CART_INCREMENT = 1

    class TC_WEB_LOGIN:
        """Casos de prueba de login"""
        VALID_EMAIL = Users.Admin.EMAIL
        VALID_PASSWORD = Users.Admin.PASSWORD
        INVALID_EMAIL = Users.InvalidUser.EMAIL
        INVALID_PASSWORD = Users.InvalidUser.PASSWORD

    class TC_WEB_SEARCH:
        """Casos de prueba de búsqueda"""
        SEARCH_TERM_VALID = "shirt"
        SEARCH_TERM_NO_RESULTS = "xyzabc123"
        SEARCH_TERM_ELECTRONICS = "laptop"


# ==================== CONFIGURACIÓN DE ESPERAS ====================
class Waits:
    """Tiempos de espera para diferentes acciones"""
    SHORT = 1  # Para pequeñas pausas
    MEDIUM = 3  # Para esperas normales
    LONG = 5  # Para procesos largos
    VERY_LONG = 10  # Para procesos muy largos


# ==================== DATOS DE PAGO (si aplica) ====================
class PaymentData:
    """Datos de pago para pruebas (si la aplicación lo requiere)"""

    class TestCard:
        """Tarjeta de prueba"""
        NUMBER = "4111111111111111"
        CVV = "123"
        EXPIRY_MONTH = "12"
        EXPIRY_YEAR = "2025"
        CARDHOLDER_NAME = "Test User"


# ==================== HELPER FUNCTIONS ====================
def get_test_data(test_case_id: str) -> dict:
    """
    Obtiene los datos de prueba para un caso de prueba específico.

    Args:
        test_case_id: ID del caso de prueba (ej: "TC_WEB_08")

    Returns:
        dict: Diccionario con los datos del caso de prueba

    Example:
        >>> data = get_test_data("TC_WEB_08")
        >>> print(data['USER_EMAIL'])
        'admin@demo.com'
    """
    test_data_map = {
        "TC_WEB_08": {
            "USER_EMAIL": TestData.TC_WEB_08.USER_EMAIL,
            "USER_PASSWORD": TestData.TC_WEB_08.USER_PASSWORD,
            "PRODUCT_NAME": TestData.TC_WEB_08.PRODUCT_NAME,
            "CATEGORY": TestData.TC_WEB_08.CATEGORY,
        },
        "TC_WEB_LOGIN": {
            "VALID_EMAIL": TestData.TC_WEB_LOGIN.VALID_EMAIL,
            "VALID_PASSWORD": TestData.TC_WEB_LOGIN.VALID_PASSWORD,
            "INVALID_EMAIL": TestData.TC_WEB_LOGIN.INVALID_EMAIL,
            "INVALID_PASSWORD": TestData.TC_WEB_LOGIN.INVALID_PASSWORD,
        },
    }

    return test_data_map.get(test_case_id, {})


def get_product_by_category(category: str, product_name: str = None) -> str:
    """
    Obtiene el nombre de un producto de una categoría específica.

    Args:
        category: Nombre de la categoría
        product_name: Nombre específico del producto (opcional)

    Returns:
        str: Nombre del producto
    """
    category_products = {
        Categories.MENS_CLOTHES: Products.MensClothes,
        Categories.WOMENS_CLOTHES: Products.WomensClothes,
        Categories.ELECTRONICS: Products.Electronics,
    }

    if category in category_products:
        if product_name:
            return product_name
        # Retorna el primer producto de la categoría por defecto
        return list(vars(category_products[category]).values())[0]

    raise ValueError(f"Categoría '{category}' no encontrada")