pip install sasl
pip install thrift
pip install thrift-sasl
pip install PyHive


from pyhive import hive
conn = hive.Connection(host="YOUR_HIVE_HOST", port=PORT, username="YOU")

cursor = conn.cursor()
cursor.execute("SELECT cool_stuff FROM hive_table")
for result in cursor.fetchall():
  use_result(result)

  import pandas as pd

  df = pd.read_sql("SELECT cool_stuff FROM hive_table", conn)