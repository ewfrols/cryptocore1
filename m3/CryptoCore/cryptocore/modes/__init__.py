"""
Фабрика для создания режимов шифрования
"""
from .base_mode import БазовыйРежим
from .ecb import ECB
from .cbc import CBC
from .cfb import CFB
from .ofb import OFB
from .ctr import CTR


class ФабрикаРежимов:
    """Создает объекты режимов шифрования"""
    
    @staticmethod
    def создать_режим(имя_режима: str, ключ) -> БазовыйРежим:
        """
        Создает режим шифрования
        
        Args:
            имя_режима: Название режима (ecb, cbc, cfb, ofb, ctr)
            ключ: Ключ в формате bytes или hex-строка
        """
        print(f"\n[DEBUG Фабрика] Получен ключ типа: {type(ключ)}")
        
        # ОБРАБОТКА КЛЮЧА - безопасный вариант
        if isinstance(ключ, bytes):
            ключ_bytes = ключ
            print(f"[DEBUG Фабрика] Ключ уже bytes, длина: {len(ключ_bytes)}")
        elif isinstance(ключ, str):
            # Это hex-строка
            try:
                ключ_bytes = bytes.fromhex(ключ)
                print(f"[DEBUG Фабрика] Преобразовано из hex, длина: {len(ключ_bytes)}")
            except ValueError as e:
                raise ValueError(f"Неверный hex-формат ключа: {ключ[:20]}...") from e
        else:
            # Попробуем преобразовать в строку
            try:
                ключ_str = str(ключ)
                ключ_bytes = bytes.fromhex(ключ_str)
                print(f"[DEBUG Фабрика] Преобразовано через str(), длина: {len(ключ_bytes)}")
            except:
                raise ValueError(f"Неверный тип ключа: {type(ключ)}. Ожидается bytes или hex-строка")
        
        # Проверяем длину ключа
        if len(ключ_bytes) != 16:
            raise ValueError(f"Ключ должен быть 16 байт, получено {len(ключ_bytes)} байт")
        
        print(f"[DEBUG Фабрика] Ключ для режима {имя_режима}: {ключ_bytes.hex()[:16]}...")
        
        # Создаем нужный режим
        имя_режима = имя_режима.lower()
        
        try:
            if имя_режима == 'ecb':
                режим = ECB(ключ_bytes)
            elif имя_режима == 'cbc':
                режим = CBC(ключ_bytes)
            elif имя_режима == 'cfb':
                режим = CFB(ключ_bytes)
            elif имя_режима == 'ofb':
                режим = OFB(ключ_bytes)
            elif имя_режима == 'ctr':
                режим = CTR(ключ_bytes)
            else:
                raise ValueError(f"Неизвестный режим: {имя_режима}")
            
            print(f"[DEBUG Фабрика] Режим {имя_режима} успешно создан")
            return режим
            
        except Exception as e:
            print(f"[DEBUG Фабрика] Ошибка создания режима: {e}")
            raise