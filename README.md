python manage.py runserver (IP:port_address)<br />
    Stop the server!<br />
python manage.py migrate --run-syncdb<br />

Create Super User/Admin: python manage.py createsuperuser<br />

Run: python manage.py runserver (IP:port_address)<br />
Stop the server!<br />
python manage.py migrate --run-syncdb<br />
python manage.py runserver (IP:port_address)<br />

For hosting update the below statements in settings.py:
    ALLOWED_HOSTS = ['10.168.134.248']<br />
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')<br />

    Generate static files using the command below:
    python manage.py collectstatic
