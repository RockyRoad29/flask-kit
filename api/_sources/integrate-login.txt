Flask-Login Integration
=======================

Here we'll go through the `extension's official documentation <https://flask-login.readthedocs.org/en/latest/>`_
(as of version 0.2.11)
and correlate items with flask-kit code.

Not only it should help us to master the application architecture,
but it will also help us to add features add upgrade to future
versions of the extension.

Configuration
-------------

The heart to the extension::

   login_manager = LoginManager()

is instanciated in the :mod:`ext` module: :data:`ext.login_manager`

Then we should call::

   login_manager.init_app(app)

The `init_app()` method is called by the *private* method
:meth:`helpers.AppFactory._bind_extensions`
for all extensions registered
in :attr:`settings.BaseConfig.EXTENSIONS`.

How it Works
------------

**Providing a user_loader callback**::

   @login_manager.user_loader
   def load_user(userid):
       return User.get(userid)

This is done in the base blueprint `views` module: :func:`base.views.load_user` .


Once a user has authenticated, you log them in with the `login_user`
function. For example::

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # login and validate the user...
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        return render_template("login.html", form=form)

In *Flask-kit*, instead of decorated functions, we're using [*pluggable views*](http://flask.pocoo.org/docs/views/)
based on :class:`flask.views.MethodView`.

So the corresponding is in :class:`base.views.LoginView` in methods
:meth:`~base.views.LoginView.get` and :meth:`~base.views.LoginView.post` .


You can then access the logged-in user with the
`current_user` proxy.

This occurs in :file:`base/templates/blocks` templates
:file:`login_form.html` and :file:`auth_header.html`.

Views that require your users to be logged in can be
decorated with the `login_required` decorator::

    @app.route("/settings")
    @login_required
    def settings():
        pass

For example, :func:`base.views.logout` , which is following the
the given example::

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(somewhere)

They will be logged out, and any cookies for their session will be cleaned up.

Your User Class
---------------
    The class that you use to represent users needs to implement these methods:

    `is_authenticated()`
        Returns `True` if the user is authenticated, i.e. they have provided
        valid credentials. (Only authenticated users will fulfill the criteria
        of `login_required`.)

    `is_active()`
        Returns `True` if this is an active user - in addition to being
        authenticated, they also have activated their account, not been suspended,
        or any condition your application has for rejecting an account. Inactive
        accounts may not log in (without being forced of course).

    `is_anonymous()`
        Returns `True` if this is an anonymous user. (Actual users should return
        `False` instead.)

    `get_id()`
        Returns a `unicode` that uniquely identifies this user, and can be used
        to load the user from the `~LoginManager.user_loader` callback. Note
        that this **must** be a `unicode` - if the ID is natively an `int` or
        other type, you will need to convert it to `unicode`.

    To make implementing a user class easier, you can inherit from `UserMixin`,
    which provides default implementations for all of these methods. (It's not
    required, though.)

.. todo::
   In *Flask-kit*, the :class:`base.models.User` inherits from :class:`flask.ext.login.UserMixin`
   so the needed methods are not implemented properly.

   Write a few tests first and then implement as needed.

Customizing the Login Process
-----------------------------
This is done in our :mod:`base.views` module.

    By default, when a user attempts to access a `login_required` view without
    being logged in, Flask-Login will flash a message and redirect them to the
    log in view. (If the login view is not set, it will abort with a 401 error.)

    The name of the log in view can be set as `LoginManager.login_view`.
    For example::

        login_manager.login_view = "users.login"

    The default message flashed is ``Please log in to access this page.`` To
    customize the message, set `LoginManager.login_message`::

        login_manager.login_message = u"Bonvolu ensaluti por uzi tio paĝo."

    To customize the message category, set `LoginManager.login_message_category`::

        login_manager.login_message_category = "info"

    When the log in view is redirected to, it will have a ``next`` variable in the
    query string, which is the page that the user was trying to access.

    If you would like to customize the process further, decorate a function with
    `LoginManager.unauthorized_handler`::

        @login_manager.unauthorized_handler
        def unauthorized():
            # do stuff
            return a_response

Custom Login using Request Loader
---------------------------------
Not used in this version of *flask-kit*.

Anonymous Users
---------------
Not used in this version of *flask-kit*.

    By default, when a user is not actually logged in, `current_user` is set to
    an `AnonymousUserMixin` object. It has the following properties:

    - `is_active` and `is_authenticated` return `False`
    - `is_anonymous` returns `True`
    - `get_id` returns `None`

    If you have custom requirements for anonymous users (for example, they need
    to have a permissions field), you can provide a callable (either a class or
    factory function) that creates anonymous users to the `LoginManager` with::

        login_manager.anonymous_user = MyAnonymousUser


Remember Me
-----------
Not used in this version of *flask-kit*.

Session Protection
------------------
Not used in this version of *flask-kit*.

Localization
------------
Not used in this version of *flask-kit*.

    By default, the `LoginManager` uses ``flash`` to display messages when a user
    is required to log in. These messages are in English. If you require
    localization, set the `localize_callback` attribute of `LoginManager` to a
    function to be called with these messages before they're sent to ``flash``,
    e.g. ``gettext``. This function will be called with the message and its return
    value will be sent to ``flash`` instead.




:copyright: \(c) 2014 by Michelle Baert.
