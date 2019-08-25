# Post It

This website is for practice purposes.

---
## Live Version
http://post-itapp.herokuapp.com/

---
## About

* A simple Django App that allows registered users to post articles/posts to their profiles, with the option to update/delete their posts.
* The app has a following/followers system where the user can choose whose posts should appear on their homepage.
* Comments system on users' posts, with the option to update/delete their comments.
* Like/Unlike system on users's posts.
* For a better User Experience; Creating, Updating and Deleting posts/comments are done using AJAX requests to eliminate the page refreshes and to live-update the number of comments at the moment of a comment is created or deleted.
* Post liking uses an AJAX request to update the number of likes on a post, with each user like.
* Following/Unfollowing profiles also uses AJAX requests.
* Following suggested profiles from the hompage uses an AJAX request, then reloads the page with the posts of the newly followed profile.
* Notifications for user's new comments, likes and following.

---

## Prerequisites

1. Front End:
    * HTML (Jinja2)
    * CSS
    * Javascript (JQuery)
    * Bootstrap
2. Back End (Python3.6.x):
    * Django 2.2.4.
    * django-Crispy-forms
    * Django-Countries
    * Django-Notifications

---

## Configuration and Installation

1. Set Environment Variables in the ~/.bashrc file:

    ```
    export EMAIL_HOST_USER='<Your Email>'
    export EMAIL_HOST_PASSWORD='<Your Email Password>'
    export SECRET_KEY='<Your App Secret Key>'
    export DEBUG_VALUE='True'
    ```

2. `git clone https://github.com/MShbana/post_it.git` to clone the app from GitHub.com.
3. `python3 -m venv post_it_venv` to create a new virtual environment.
4. `source post_it_venv/bin/activate` to activate the virtual environment.

5. `pip install -r requirements.txt` to install the required software.

6. `python manage.py makemigrations` to set the database migrations.

7. `python manage.py migrate` to run the database migrations.

8. `python manage.py runserver` to run the server on the default port.

The app will run on http://127.0.0.1:8000 (http://localhost:8000) by default.

---

## Apps and Models

1. **Accounts App:**
    * **User Registeration:** Extended Django's [UserCreationForm][link_UserCreationForm] to add extra fields such as *First Name*, *Last Name*, *Email*, and made those extra fields required, using a mixin.
    * **Email Verification:** Used Django [EmailMessage][link_EmailMessage] class and stored the registered user as inactive until they verify their account via the received email.
    * **Password Reset:** Used Django's [Authentication Views][link_authentication_views] (*PasswordResetView*, *PasswordResetDoneView*, *PasswordResetCofirmView*, *PasswordResetCompleteView*) with my own templates to handle the password reset process.
    * **User Information Update:** Extended Django's [ModelForm][link_ModelForm] to add the extra User's required Fields and Profile Fields, and made sure that the user can update the field with their own email, without considering it as duplicat email.
    * **Password Change:** Used Django's [PasswordChangeForm][link_PasswordChangeForm] with my own template.
    * **User Authentication:** Used Django's [User Model][link_user_model].
    * **Profile Model:**
        1. **Relationship:** A One To One relationship with Django's User Model. It gets creaetd when a user is created.
        2. **Symmetry:** This relationship is asymmetrical relationship, as one user following a user.. doesn't mean they are followed back.
        3. **Slug Field:** A unique slug that gets created/derived from the registered user's username, and by which the user's account URI will be dynamically created.
        4. **Following:**
            * A Many To Many relationship with itself (User's Profile to one or more Users' Profiles).
            * Used to create a following and followers list for each User Profile, where each user can follow/unfollow and be followed/unfollowed by any number of other Users'Profiles.
            * Only the User's Profiles that they follow will appear on their homepage; that and their own posts of course.
2. **Posts App:**
    * **Post Model:**
        * **Slug Field:** A unique slug that gets created from according to the title of the post.
        * **likes Field:** A field that has a Many To Many relationship with User and Post models.
    * **Comment Model:** Has a Many To One relationship with both the User and Post models.
3. **CRUD Operations:**
    * Used Ajax requests for the create/update/delete views.
4. **Notifications App:**
    * Used [Django-notification][link_django_notifications] to implement the notifications for user's comments, likes and following

---

[//]:  # (Links and images relative paths)

[link_UserCreationForm]: https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.UserCreationForm>
[link_EmailMessage]: <https://docs.djangoproject.com/en/2.2/topics/email/>
[link_authentication_views]: <https://docs.djangoproject.com/en/2.2/topics/auth/default/>
[link_ModelForm]: <https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/>
[link_PasswordChangeForm]: <https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.PasswordChangeForm>
[link_user_model]: <https://docs.djangoproject.com/en/2.2/ref/contrib/auth/>
[link_django_notifications]: <https://github.com/django-notifications/django-notifications/>