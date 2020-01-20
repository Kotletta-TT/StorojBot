import psycopg2


dbname = 'storojdb'
dbuser = 'storoj'
conn = psycopg2.connect('dbname=' + dbname + ' user=' + dbuser)
cur = conn.cursor()
cur.execute("DROP TABLE ads;")
cur.execute("CREATE TABLE ads (id serial primary key, id_ads integer, adname text, price text, city text, url text, addate text);")

conn.commit()
conn.close()

