# Django Blog Project

Welcome to **Django Blog Project**, a simple yet powerful blog application built with Django. This project is designed to provide a robust platform for blogging, perfect for both learning Django and deploying a fully functional blog site.

## Features

- **Post Management**: Create, edit, and delete blog posts.
- **Comment System**: Users can comment on posts, enabling interaction and feedback.
- **Tagging System**: Categorize posts using tags for easy navigation.
- **Search Functionality**: Easily search for blog posts.

## Screenshots

![Home Page](screenshots/home.png)
![Post Detail](screenshots/post_detail.png)
![Create Post](screenshots/create_post.png)

## Technologies Used

- **Python 3.12**
- **Django 4.1.13**


## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.x installed on your machine.
- Virtualenv installed (`pip install virtualenv`).

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/keni2002/mysite.git
   cd mysite
   ```

2. **Create and activate a virtual environment**:
   ```sh
   virtualenv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```sh
   python manage.py runserver
   ```

7. **Visit the application**:
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

- **Homepage**: View recent blog posts.
- **Create Post**: Write and publish new posts.
- **Post Detail**: Read posts in detail and comment on them.
- **Admin Panel**: Manage posts, comments, and users.

## Contributing

Feel free to fork this repository and contribute by submitting a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- All the developers who have contributed to making Django and its ecosystem awesome!
