"""
Обработчик векторов инициализации (IV)
"""


class ОбработчикIV:
    """Класс для работы с векторами инициализации"""
    
    @staticmethod
    def сгенерировать_iv() -> bytes:
        """
        Генерирует случайный вектор инициализации
        
        Returns:
            bytes: 16-байтовый IV
        """
        # Импортируем здесь, чтобы избежать циклических импортов
        from .csprng import generate_random_bytes
        return generate_random_bytes(16)
    
    @staticmethod
    def преобразовать_iv_в_hex(iv_bytes: bytes) -> str:
        """
        Преобразует IV из bytes в hex-строку
        
        Args:
            iv_bytes: IV в формате bytes
            
        Returns:
            str: hex-строка IV
        """
        return iv_bytes.hex()
    
    @staticmethod
    def преобразовать_hex_в_iv(iv_hex: str) -> bytes:
        """
        Преобразует IV из hex-строки в bytes
        
        Args:
            iv_hex: IV в hex-формате
            
        Returns:
            bytes: IV в формате bytes
        """
        return bytes.fromhex(iv_hex)
    
    @staticmethod
    def извлечь_iv_из_данных(данные: bytes):
        """
        Извлекает IV из начала данных
        
        Args:
            данные: Данные, содержащие IV в первых 16 байтах
            
        Returns:
            tuple: (iv_bytes, остальные_данные)
            
        Raises:
            ValueError: Если данных меньше 16 байт
        """
        if len(данные) < 16:
            raise ValueError(f"Недостаточно данных для извлечения IV. "
                           f"Требуется минимум 16 байт, получено {len(данные)}")
        
        iv = данные[:16]
        остальные_данные = данные[16:]
        
        return iv, остальные_данные
    
    @staticmethod
    def добавить_iv_к_данным(iv: bytes, данные: bytes) -> bytes:
        """
        Добавляет IV к началу данных
        
        Args:
            iv: Вектор инициализации (16 байт)
            данные: Исходные данные
            
        Returns:
            bytes: Данные с IV в начале
        """
        return iv + данные
