# To-Do List Django WebApp

A full-featured To-Do List web application built with Python and the Django web framework. This app provides users with the ability to register, log in, and manage their own personalized to-do lists and tasks in a secure environment.

---

## Features

- **User Authentication**
  - Register new account
  - Log in and log out securely
  - Each user has isolated lists and tasks

- **Dashboard**
  - View all your created to-do lists
  - Easily navigate between lists in a sidebar
  - See task counts for each list

- **List Management**
  - Create new to-do lists
  - Delete existing lists
  - Select a list to view its items

- **Task Management**
  - Add new tasks to any list
  - Delete tasks
  - Toggle task completion status (mark as completed/incomplete)

- **Responsive UI**
  - Modern design using Tailwind CSS
  - Sidebar navigation and main content area for focused task management

- **Security**
  - CSRF protection on all forms
  - Access to dashboard and list management restricted to logged-in users

---

## Data Model

- **ToDoList**: Represents a user-created list. Linked to the Django `User` model.
- **ListItem**: Represents a task within a list. Contains text and completion status.

Models are defined in [`models.py`](todo_list_project/todo_list_app/models.py):

```python
class ToDoList(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ListItem(models.Model):
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    isCompleted = models.BooleanField(default=False)
```

---

## How it Works

- After registration/login, users access the dashboard to create and manage their lists.
- Selecting a list displays its tasks; users can add, delete, and toggle tasks.
- Lists and tasks are only accessible by their creator.
- All operations are performed via secure Django forms.

---

## Testing

Robust test coverage is provided in [`tests.py`](todo_list_project/todo_list_app/tests.py), including:

- **Model Tests**
  - ToDoList and ListItem creation and behavior

- **View Tests**
  - Dashboard view: access, permissions, and core logic
  - Registration and login views

- **User Journey Tests**
  - End-to-end journey through account creation, login, list and task management (using Django’s LiveServerTestCase and Selenium for UI automation)

- **Security Tests**
  - Ensures user isolation and CSRF protection

Sample test structure:

```python
class TestToDoList(TestCase):
    # Tests for list creation and user linkage

class TestDashboardView(TestCase):
    # Tests for correct filtering and display of user's lists

class UserJourneyText(LiveServerTestCase):
    # Selenium-based end-to-end UI tests
```

---

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MadsGit-98/todo-list-django-webapp.git
   cd todo-list-django-webapp/todo_list_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the app:**
   Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## Running Tests

Unit, integration, and end-to-end tests are included. To run all tests:

```bash
python manage.py test
```

For UI tests (Selenium), ensure you have the required WebDriver installed.

---

## License

This project is licensed under the MIT License.

---

## Author

Created by [MadsGit-98](https://github.com/MadsGit-98)