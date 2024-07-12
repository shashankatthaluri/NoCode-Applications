# Flappy Bird Game

This is a simple implementation of the classic Flappy Bird game using Python and Pygame. With the help of [getlazy](https://www.getlazy.ai/) ai tool and chat gpt I could build this using only 5 minutes. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Instructions](#game-instructions)
- [Code Overview](#code-overview)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/flappy-bird.git
    cd flappy-bird
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the game using the following command:
```bash
python app.py
```
## Game Instructions

- Click or press the spacebar to make the bird jump.
- Avoid the cylinders and keep the bird from falling out of the screen.
- Press 'P' to pause and resume the game.

## Code Overview

- `app.py`: The main game logic, including the game loop and event handling.
- `settings.py`: Initializes the game screen and defines game constants.
- `requirements.txt`: Lists the dependencies required to run the game.

### Game States

The game has the following states:
- **START**: Initial state, waiting for the player to start the game.
- **COUNTDOWN**: Countdown before the game starts.
- **PLAYING**: The main game state where the bird is flying and avoiding cylinders.
- **PAUSED**: The game is paused.
- **GAME_OVER**: The game has ended, and the player can restart.

### Classes

- `Bird`: Represents the player's bird, handles jumping and updating position.
- `Cylinder`: Represents the obstacles, handles movement and drawing.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
