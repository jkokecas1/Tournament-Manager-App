# Football Tournament Manager

A complete Python/Flask application to manage football tournaments, including match scheduling, team management, standings, and image handling.

## Features

- **Tournament Management**: Create and configure tournaments (points for win/draw/loss).
- **Match Scheduling**: Automatic generation of matchdays (Jornadas).
- **Team Management**: Add teams, players, and manage team logos (with auto-resizing).
- **Standings**: Automatic calculation of points, goal difference, and form guide.
- **Match Events**: Record goals, cards, and generate minute-by-minute updates.
- **Image Export**: Export standings and schedule as images.
- **Team Withdrawal**: Handle team withdrawals with automatic 3-0 results.

## Prerequisites

- Python 3.8+
- pip

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd fut
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    - Windows: `venv\Scripts\activate`
    - macOS/Linux: `source venv/bin/activate`

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1.  **Initialize the database:**
    This will create the `fut.db` SQLite database and populate initial configuration.
    ```bash
    python init_db.py
    ```

## Running the Application

1.  **Start the server:**
    ```bash
    python run.py
    ```

2.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.

## Project Structure

- `app/`: Main application source code.
    - `blueprints/`: Route handlers organized by feature.
    - `models.py`: Database models.
    - `templates/`: HTML templates.
    - `static/`: CSS, JS, and image assets.
- `instance/`: Flask instance configuration.
- `tools/`: Utility scripts.
- `requirements.txt`: Python dependencies.
- `init_db.py`: Database initialization script.
- `run.py`: Entry point for the application.

## License

[MIT License](LICENSE)
