python manage.py runserver (IP:port_address)
    Stop the server!
python manage.py migrate --run-syncdb

Create Super User/Admin: python manage.py createsuperuser

Run: python manage.py runserver (IP:port_address)
Stop the server!
python manage.py migrate --run-syncdb
python manage.py runserver (IP:port_address)

For hosting update the below statements in settings.py:
    ALLOWED_HOSTS = ['10.168.134.248']
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    Generate static files using the command below:
    python manage.py collectstatic
