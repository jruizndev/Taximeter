# 🚕 Taxímetro Digital

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql)
![Status](https://img.shields.io/badge/Status-Open%20to%20Improvements-brightgreen?style=for-the-badge)

Sistema digital avanzado para el cálculo y gestión de tarifas de taxi, diseñado para ofrecer una solución completa tanto para conductores como para la gestión administrativa. El sistema cuenta con dos interfaces: una versión de terminal (CLI) para uso rápido y eficiente, y una interfaz gráfica (GUI) más intuitiva y visual.

Este taxímetro digital no solo calcula tarifas base, sino que también incorpora un sistema dinámico que tiene en cuenta diferentes franjas horarias y condiciones especiales como lluvia o eventos. Además, incluye un sistema de autenticación de usuarios y almacenamiento persistente de datos en MySQL.

</div>

## ✨ Características

<table>
  <tr>
    <td>🕒 Cálculo de Tarifas</td>
    <td>👥 Sistema de Usuarios</td>
    <td>📊 Registro de Viajes</td>
  </tr>
  <tr>
    <td>🌧️ Condiciones Especiales</td>
    <td>💾 Base de Datos MySQL</td>
    <td>📝 Sistema de Logs</td>
  </tr>
  <tr>
    <td>🖥️ Interfaz Gráfica</td>
    <td>⌨️ Interfaz CLI</td>
    <td>🔐 Autenticación</td>
  </tr>
</table>

## 🚀 Iniciar Aplicación

El sistema ofrece dos modos de uso diferentes para adaptarse a las necesidades del usuario:

### CLI (Terminal)

La interfaz de línea de comandos proporciona un acceso rápido y eficiente a todas las funcionalidades del sistema. Ideal para usuarios experimentados que prefieren un control directo.

```bash
python3 main.py
```

### GUI (Interfaz Gráfica)

La interfaz gráfica ofrece una experiencia más visual e intuitiva, con un diseño moderno y fácil de usar. Perfecta para nuevos usuarios o para quienes prefieren una interacción más visual.

```bash
python3 -m gui.gui_main
```

Ambas interfaces comparten la misma base de datos y funcionalidades, permitiendo una transición fluida entre ellas según las necesidades del momento.

## 💰 Sistema de Tarifas

El sistema implementa un modelo de tarifas dinámico y flexible que se adapta a diferentes situaciones y horarios. Las tarifas se han diseñado considerando los patrones de demanda típicos del servicio de taxi y las necesidades tanto de conductores como de pasajeros.

### Franjas Horarias

| Horario | Tipo              | En Movimiento | Parado   |
| ------- | ----------------- | ------------- | -------- |
| 07-09   | Hora Punta Mañana | 0.06€/s       | 0.025€/s |
| 17-19   | Hora Punta Tarde  | 0.06€/s       | 0.025€/s |
| 00-03   | Nocturna          | 0.07€/s       | 0.03€/s  |
| 10-16   | Valle             | 0.035€/s      | 0.015€/s |
| Resto   | Normal            | 0.04€/s       | 0.02€/s  |

### Multiplicadores Especiales

El sistema incorpora multiplicadores para situaciones especiales que afectan al servicio:

-   🌧️ **Lluvia**: x1.2 - Se aplica durante condiciones climatológicas adversas que aumentan la demanda y dificultan el servicio
-   🎪 **Eventos**: x1.3 - Para situaciones de alta demanda durante eventos especiales como conciertos, eventos deportivos o festivales

Estos multiplicadores se pueden activar y desactivar fácilmente desde ambas interfaces, y se aplican automáticamente a la tarifa base correspondiente.

## 📥 Instalación

### 1. Preparar Entorno

```bash
# Clonar repositorio
git clone https://github.com/jruizndev/Taximeter.git
cd Taximeter

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Base de Datos

```sql
CREATE DATABASE taximeter;
USE taximeter;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

CREATE INDEX idx_username ON users(username);
```

### 3. Variables de Entorno

```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=taximeter
```

## 📁 Estructura del Proyecto

```
taximeter/
   ├── auth/
   │   └── auth.py              # Sistema de autenticación
   ├── config/
   │   └── config.py            # Configuración de tarifas
   ├── core/
   │   ├── calculator.py        # Cálculo de tarifas
   │   ├── taximeter.py         # Clase principal del taxímetro
   │   ├── trip.py              # Gestión de viajes
   │   └── ui.py                # Interfaz de línea de comandos
   ├── database/
   │   ├── connection.py        # Conexión a la base de datos
   │   └── schema.sql           # Esquema de la base de datos
   ├── gui/
   │   └── frames/
   │       ├── auth_frame.py    # Interfaz de login
   │       └── meter_display.py # Display del taxímetro
   ├── history/
   │   └── trips.txt            # Historial de viajes realizados
   ├── logs/
   │   └── taximeter.log        # Registros del sistema
   ├── tests/
   │   └── test_taxi.py         # Tests unitarios
   ├── .env.example             # Configuración de entorno
   ├── main.py                  # Punto de entrada CLI
   ├── README.md                # Documentación
   └── requirements.txt         # Dependencias
```

## 👨‍💻 Buenas Prácticas Aplicadas

- **Programación Orientada a Objetos**: División del proyecto en clases (Taximeter, Trip, RateCalculator) para gestionar diferentes aspectos del sistema

- **Modularidad y Organización**: Código distribuido en módulos independientes (auth, core, gui, database) permitiendo mantener una estructura clara y escalable

- **Trabajo con Ramas**: Desarrollo en ramas específicas para cada funcionalidad, permitiendo un desarrollo paralelo y organizado

- **Control de Versiones**: Commits descriptivos siguiendo convenciones y documentación actualizada

- **Testing**: Implementación de tests unitarios para validar la funcionalidad del cálculo de tarifas

- **Interfaces Duales**: CLI mejorada visualmente con emojis y GUI desarrollada con Tkinter, ofreciendo dos opciones de uso

- **Gestión de Configuración**: Uso de variables de entorno (.env) y sistema de logs para seguimiento

## 🧪 Tests

```bash
# Ejecutar tests
python3 -m pytest -v

# Tests específicos
python3 -m pytest tests/test_taxi.py -v
```

## 🚀 Próximas Mejoras

-   [ ] Integrar base de datos para histórico de trayectos
-   [ ] Dockerizar la aplicación
-   [ ] Desarrollar versión web
-   [ ] Implementar sistema de geolocalización GPS
-   [ ] Añadir sistema de cobro y pagos

Estas mejoras se implementarán de forma gradual, priorizando según las necesidades del proyecto.

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama

```bash
git checkout -b feature/NuevaMejora
```

3. Commit y push

```bash
git commit -m "feat: add nueva mejora"
git push origin feature/NuevaMejora
```

## 📝 Convenciones

-   Seguir PEP 8
-   Tests para nuevas funcionalidades
-   Mantener tests actualizados
