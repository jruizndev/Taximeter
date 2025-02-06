# Rangos horarios y sus tarifas
TIME_SLOTS = {
    'morning_rush': {
        'start': '07:00',
        'end': '09:00',
        'motion_rate': 0.06,
        'stopped_rate': 0.025,
        'description': 'Hora punta mañana'
    },
    'evening_rush': {
        'start': '17:00',
        'end': '19:00',
        'motion_rate': 0.06,
        'stopped_rate': 0.025,
        'description': 'Hora punta tarde'
    },
    'night_life': {
        'start': '00:00',
        'end': '07:00',
        'motion_rate': 0.07,
        'stopped_rate': 0.03,
        'description': 'Tarifa nocturna'
    },
    'low_demand': {
        'start': '10:00',
        'end': '16:00',
        'motion_rate': 0.035,
        'stopped_rate': 0.015,
        'description': 'Horas valle'
    },
    'normal': {
        'motion_rate': 0.04,
        'stopped_rate': 0.02,
        'description': 'Tarifa normal (resto de horas)'
    }
}

# Multiplicadores especiales
SPECIAL_CONDITIONS = {
    'rain': 1.2,    
    'events': 1.3,  
}