
# Task Manager

A simple and intuitive web-based task management application built with Flask and SQLAlchemy. This application allows users to create, edit, and manage tasks effectively.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication (sign up and login)
- Create, edit, and delete tasks
- Set due dates and priorities for tasks
- View previous tasks with status updates (Pending, Completed, Canceled)
- Responsive and user-friendly interface

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/TaskManagerApp.git
   cd TaskManagerApp
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

## Usage

1. Run the application:

   ```bash
   flask run
   ```

2. Open your browser and go to `http://10.0.0.72:5050/`.

3. Create a new account or log in with existing credentials.

4. Use the application to manage your tasks.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
