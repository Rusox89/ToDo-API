export PYTHONPATH=/app
python3 << EOF
from api.models import initialize_database
initialize_database(
	hostname='localhost',
	username='$POSTGRES_USER',
	password='$POSTGRES_PASSWORD',
	database='$POSTGRES_DB',
	protocol='postgres'
)
EOF
