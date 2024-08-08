# Workout Logger MVP

## Description
The Workout Logger is a minimal viable product (MVP) designed to help users log their workouts and view exercise tutorials. This app provides a simple interface to log exercises, track the number of reps and sets, and view a history of logged workouts.

## Features
- **Exercise List**: View a list of exercises with video tutorials.
- **Log Workouts**: Log new workouts by entering the exercise name, number of reps, and sets.
- **Workout History**: View the history of all logged workouts in a tabular format.

## Setup
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/workout-logger.git
    cd workout-logger
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Run the Streamlit app**:
    ```sh
    streamlit run main.py
    ```

2. **Navigate the app**:
    - **Exercise List**: View exercises and their video tutorials.
    - **Log a New Workout**: Enter the exercise name, reps, and sets, then click "Log Exercise".
    - **Workout History**: View the history of your logged workouts.

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
