#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to add Spanish translations to the messages.po file
"""

# Translation dictionary - English to Spanish
translations = {
    # Admin Dashboard
    "👑 Admin Dashboard": "👑 Panel de Administración",
    "Tournaments": "Torneos",
    "Teams": "Equipos",
    "Matches": "Partidos",
    "Users": "Usuarios",
    "⚙️ Site Settings": "⚙️ Configuración del Sitio",
    "Company Name": "Nombre de la Empresa",
    "Company Logo": "Logo de la Empresa",
    "Social Media Links": "Enlaces de Redes Sociales",
    "Default Language": "Idioma Predeterminado",
    "Save Settings": "Guardar Configuración",
    "👤 User Management": "👤 Gestión de Usuarios",
    "Create User": "Crear Usuario",
    "Username": "Nombre de Usuario",
    "Password": "Contraseña",
    "Role:": "Rol:",
    "Assign Team (For Reps):": "Asignar Equipo (Para Representantes):",
    "Existing Users": "Usuarios Existentes",
    "🏆 Tournament Management": "🏆 Gestión de Torneos",
    "Direct Access to all Tournaments:": "Acceso Directo a todos los Torneos:",
    "No tournaments found.": "No se encontraron torneos.",
    "Create New Tournament": "Crear Nuevo Torneo",
    "Create": "Crear",
    
    # Base template
    "Home": "Inicio",
    "Dashboard": "Panel",
    "Standings": "Clasificación",
    "Admin": "Administración",
    "Logout": "Cerrar Sesión",
    "Login": "Iniciar Sesión",
    
    # Index
    "Category:": "Categoría:",
    "Manage": "Gestionar",
    "No tournaments found. Create one to get started!": "No se encontraron torneos. ¡Crea uno para comenzar!",
    
    # Login
    
    # Tournament Dashboard
    "Manage teams and players": "Gestionar equipos y jugadores",
    "Matches (Schedule)": "Partidos (Calendario)",
    "View fixtures and results": "Ver encuentros y resultados",
    "View table and stats": "Ver tabla y estadísticas",
    "Metrics": "Métricas",
    "Top scorers & records": "Máximos goleadores y récords",
    "Danger Zone": "Zona de Peligro",
    "Are you sure? This will replace existing matches.": "¿Estás seguro? Esto reemplazará los partidos existentes.",
    "Generate Round Robin Schedule": "Generar Calendario Round Robin",
    
    # Teams
    "Teams & Players": "Equipos y Jugadores",
    "Add Team": "Agregar Equipo",
    "Team Name": "Nombre del Equipo",
    "🔍 Search Team...": "🔍 Buscar Equipo...",
    "Players": "Jugadores",
    "Upload Logo": "Subir Logo",
    "Player Name": "Nombre del Jugador",
    "Pos": "Pos",
    "Add Player": "Agregar Jugador",
    
    # Schedule
    "Schedule": "Calendario",
    "Filter by Matchday:": "Filtrar por Jornada:",
    "All Matchdays": "Todas las Jornadas",
    "Matchday": "Jornada",
    "Filter by Team:": "Filtrar por Equipo:",
    "All Teams": "Todos los Equipos",
    "Filter": "Filtrar",
    "Clear": "Limpiar",
    "Match": "Partido",
    "Result": "Resultado",
    "Action": "Acción",
    "Edit": "Editar",
    "Update": "Actualizar",
    "No matches scheduled yet.": "Aún no hay partidos programados.",
    
    # Standings
    "Pos": "Pos",
    "Team": "Equipo",
    "P": "PJ",
    "W": "G",
    "D": "E",
    "L": "P",
    "GF": "GF",
    "GA": "GC",
    "GD": "DG",
    "Pts": "Pts",
    "Last 5": "Últimos 5",
    "Won": "Ganado",
    "Drawn": "Empatado",
    "Lost": "Perdido",
    
    # Match Detail
    "Match Details": "Detalles del Partido",
    "Referee:": "Árbitro:",
    "Not assigned": "No asignado",
    "Assign Referee:": "Asignar Árbitro:",
    "Save Ref": "Guardar Árbitro",
    "Update Score": "Actualizar Marcador",
    "📢 Match Events": "📢 Eventos del Partido",
    "Unknown Player": "Jugador Desconocido",
    "Goal": "Gol",
    "Yellow Card": "Tarjeta Amarilla",
    "Red Card": "Tarjeta Roja",
    "Home": "Inicio",
    "Away": "Visitante",
    "No events recorded.": "No se registraron eventos.",
    "Events": "Eventos",
    "Player:": "Jugador:",
    "Event:": "Evento:",
    "Minute:": "Minuto:",
    "Add Event": "Agregar Evento",
    "Back to Schedule": "Volver al Calendario",
    
    # Metrics
    "📊 Tournament Metrics": "📊 Métricas del Torneo",
    "⚽ Top Scorers": "⚽ Máximos Goleadores",
    "Player": "Jugador",
    "Goals": "Goles",
    "🔥 Most Goals in a Single Match": "🔥 Más Goles en un Solo Partido",
    "🏆 Most Wins": "🏆 Más Victorias",
    "🎯 Best Attack (Goals For)": "🎯 Mejor Ataque (Goles a Favor)",
    "🥅 Most Conceded (Goals Against)": "🥅 Más Goles Recibidos (Goles en Contra)",
    "😇 Fair Play (Fewest Cards)": "😇 Fair Play (Menos Tarjetas)",
    
    # Auth & Errors
    "Login Required": "Inicio de Sesión Requerido",
    "You need to be logged in to access this page.": "Necesitas iniciar sesión para acceder a esta página.",
    "Please log in with your credentials to continue.": "Por favor, inicia sesión con tus credenciales para continuar.",
    "Go to Home": "Ir al Inicio",
    "Access Denied": "Acceso Denegado",
    "You do not have permission to access this page.": "No tienes permiso para acceder a esta página.",
    "This page requires special permissions. Please contact an administrator if you believe you should have access.": "Esta página requiere permisos especiales. Por favor contacta a un administrador si crees que deberías tener acceso.",
    "Go Back": "Volver",
    
    # Index & Tournaments
    "Available Tournaments": "Torneos Disponibles",
    "Category": "Categoría",
    "Tournament Name": "Nombre del Torneo",
    "Category (e.g., U12)": "Categoría (ej. Sub-12)",
    "Points System": "Sistema de Puntos",
    "Win": "Victoria",
    "Draw": "Empate",
    "Loss": "Derrota",
    "Create Tournament": "Crear Torneo",
    
    # Withdrawal & Pending Goals
    "Withdrawn": "Retirado",
    "Pending Goals": "Goles Pendientes",
    "⚽ Pending Goal Assignments": "⚽ Asignación de Goles Pendientes",
    "You have no pending goals to assign. Great job!": "No tienes goles pendientes por asignar. ¡Buen trabajo!",
    "The following matches had an opponent withdraw. You must assign 3 goals per match to your players.": "Los siguientes partidos tuvieron un oponente retirado. Debes asignar 3 goles por partido a tus jugadores.",
    "Goals Pending": "Goles Pendientes",
    "Assign to Player": "Asignar a Jugador",
    "Select Player": "Seleccionar Jugador",
    "Assign Goal": "Asignar Gol",
    "Back to Home": "Volver al Inicio",
    "Are you sure you want to withdraw this team? This will set all matches to 3-0.": "¿Estás seguro de que quieres retirar este equipo? Esto establecerá todos los partidos a 3-0.",
    "Team Withdrawn": "Equipo Retirado",
    "Withdraw Team": "Retirar Equipo",
    
    # Images
    "Export as Image": "Exportar como Imagen",
    "Schedule Image": "Imagen del Calendario",
    "Standings Image": "Imagen de la Clasificación",
    "Copy to Clipboard": "Copiar al Portapapeles",
    "Download": "Descargar",
    "Image copied to clipboard!": "¡Imagen copiada al portapapeles!",
    "Error copying to clipboard. Please try downloading instead.": "Error al copiar al portapapeles. Por favor, intenta descargarla.",
    
    # Misc
    "Please log in to access this page.": "Por favor inicia sesión para acceder a esta página.",
    "Upload\n                Logo": "Subir Logo", # Handling the multiline split found in PO
}

def add_translations_to_po(po_file_path):
    """Add Spanish translations to the .po file"""
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        output_lines.append(line)
        
        # Check if this is a msgid line
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            # Extract the English text
            english_text = line[7:-2]  # Remove 'msgid "' and '"\n'
            
            # Check if next line is an empty msgstr
            if i + 1 < len(lines) and lines[i + 1].strip() == 'msgstr ""':
                # Look up translation
                if english_text in translations:
                    spanish_text = translations[english_text]
                    output_lines.append(f'msgstr "{spanish_text}"\n')
                    i += 2  # Skip the original msgstr line
                    continue
        
        i += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Added Spanish translations to {po_file_path}")

if __name__ == "__main__":
    po_file = "app/translations/es/LC_MESSAGES/messages.po"
    add_translations_to_po(po_file)
