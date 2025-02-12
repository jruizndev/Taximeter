# Taxímetro Digital 🚕

## Estado del Proyecto
🚧 Under Construction 🚧

## Tabla de Contenidos
- [Descripción](#descripción)
- [Estado Actual](#estado-actual)
- [Tecnologías](#tecnologías)
- [Estructura](#estructura)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [Documentación API](#documentación-api)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Descripción
Sistema de taxímetro digital desarrollado en Python que permite calcular tarifas de viajes en taxi según diferentes franjas horarias y condiciones especiales.

## Estado Actual
### Implementado ✅
- Sistema base de cálculo de tarifas
- Gestión de viajes y estados
- Sistema de logs
- Interfaz de línea de comandos
- Refactorización a POO

### En Desarrollo 🛠️
- Sistema de autenticación
- Base de datos MySQL
- Interfaz gráfica

## Tecnologías
- Python 3.12
- MySQL
- pytest para testing

### Dependencias
- mysql-connector-python: Conexión con base de datos MySQL
- python-dotenv: Gestión de variables de entorno
- pytest: Framework de testing

## Estructura
```
taximeter/
    ├── main.py           # Programa principal
    ├── config.py         # Configuración de tarifas
    ├── requirements.txt  # Dependencias
    ├── tests/           # Tests unitarios
    ├── logs/            # Registros del sistema
    ├── history/         # Historial de viajes
    ├── database/        # Configuración BD
    └── auth/            # Sistema autenticación
```

## Instalación
```bash
# Clonar repositorio
git clone https://github.com/jruizndev/Taximeter.git

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

## Uso
### Iniciar el programa
```bash
python main.py
```

### Funcionalidades principales
- Iniciar nuevo trayecto
- Ver tarifas actuales
- Gestionar condiciones especiales (lluvia, eventos)
- Consultar historial de viajes

### Tarifas
El sistema maneja diferentes tarifas según:
- Hora del día (valle, punta, noche)
- Estado del taxi (movimiento/parado)
- Condiciones especiales (lluvia, eventos)

## Tests
### Ejecutar tests
```bash
npm test
```

### Estructura de tests
- Tests unitarios para cálculo de tarifas
- Tests para cambios de estado
- Tests para condiciones especiales

## Documentación API
[Esta sección se completará cuando se implemente la API REST]

## Contribuir
### Cómo contribuir
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'feat: add nueva caracteristica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

### Convenciones
- Seguir estilo PEP 8
- Documentar funciones y clases
- Mantener tests actualizados
