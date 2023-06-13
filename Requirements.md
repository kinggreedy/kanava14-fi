# Main objectives

Create a simple blog with these features:
* Have a view to list blog posts:
  * Show title and creation time
  * Ordered post by creation time (latest first)
  * Pagination: show 5 posts per page by default, create a dropdown to allow user to change the number of posts per page with these options: 5, 10, 20
* Have a view to show single blog post:
  * All blog post’s details (title, body, author name, etc.)
  * Edit blog post user own
* Support multiple authors. Author can login using username and password, after that they can:
  * Write new blog post
  * Note: author can see blog posts from other authors, but can only edit own posts
* Anonymous user can’t see any blog post without signing in

# Bonus (optional)
Create a periodic task (using e.g: Celery, Huey, ApScheduler, etc) which runs every 10 minutes to scan the database and automatically detect the language of the blog post’s content and save that information to the database.
You can use the free API at: https://languagelayer.com/ or https://detectlanguage.com/ for this purpose.

# Requirements
* Python code should be covered by tests (using pytest), coverage should be at least 60%
* Python code should be PEP8 compliant (you can use flake8 to test)
* README should contain:
  * How to setup the app locally for development
  * How to start the periodic task for detecting language
* Must use:
  * Python 3.7+
  * Pyramid 1.10
  * PostgreSQL 11+
  * SQLAlchemy
  * pytest
* Apart from above list, you are free to choose any technology you like
