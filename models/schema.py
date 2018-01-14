
from utilities import interact_database

def user(regno, name, email, mobile):
    details = {
        "regno": regno,
        "name": name,
        "email": email,
        "mobile": mobile
    }
    return details


def create_time_table_schema(days):
    table = [{"day": day, "schedule": []} for day in days]
    interact_database.create_collection(table)
