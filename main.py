import psycopg2


def create_db(conn):
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS customer (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        last_name VARCHAR (60) NOT NULL,
        email VARCHAR(60),
        phones INTEGER
        );
        """)
    curs.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customer(id),
        phone VARCHAR(60)
        );
        """)
    conn.commit()
    curs.close()
    print('Database created')


def add_client(conn, first_name, last_name, email, phones=None):
    curs = conn.cursor()
    curs.execute("""
        INSERT INTO customer (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s);
        """, (first_name, last_name, email, phones))
    conn.commit()
    curs.close()
    print('Client added')


def add_phone(conn, client_id, phone):
    curs = conn.cursor()
    curs.execute("""
        INSERT INTO phonebook (customer_id, phone)
        VALUES (%s, %s);
        """, (client_id, phone))
    conn.commit()
    curs.close()
    print('Phone added')


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    curs = conn.cursor()
    curs.execute("""
        UPDATE customer
        SET first_name = %s, last_name = %s, email =%s, phones = %s
        WHERE id = %s;
        """, (first_name, last_name, email, phones, client_id))
    conn.commit()
    curs.close()
    print('Information updated')


def delete_phone(conn, client_id, phone):
    curs = conn.cursor()
    curs.execute("""
        DELETE FROM phonebook
        WHERE customer_id = %s and phone = %s';
        """, (client_id, phone))
    conn.commit()
    curs.close()
    print('Phone deleted')


def delete_client(conn, client_id):
    curs = conn.cursor()
    curs.execute("""
        DELETE FROM phonebook
        WHERE customer_id = %s;
        """, (client_id,))
    curs.execute("""
        DELETE FROM customer
        WHERE id = %s;
        """, (client_id,))
    conn.commit()
    curs.close()
    print('Client deleted')


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    curs = conn.cursor()
    if phone is not None:
        curs.execute("""
        SELECT * FROM customer c
        JOIN phonebook p ON c.id = p.customer_id
        WHERE phone = %s;
        """, (phone,))
    elif email is not None:
        curs.execute("""
        SELECT * FROM customer c
        JOIN phonebook p ON c.id = p.customer_id
        WHERE email = %s;
        """, (email,))
    elif last_name is not None:
        curs.execute("""
        SELECT * FROM customer c
        JOIN phonebook p ON c.id = p.customer_id
        WHERE last_name = %s;
        """, (last_name,))
    elif first_name is not None:
        curs.execute("""
        SELECT * FROM customer c
        JOIN phonebook p ON c.id = p.customer_id
        WHERE first_name = %s;
        """, (first_name,))
    print(curs.fetchall())
    conn.commit()
    curs.close()


def clean_db(conn):
    curs = conn.cursor()
    curs.execute("""
        DROP TABLE IF EXISTS phonebook CASCADE;
            """)
    curs.execute("""
        DROP TABLE IF EXISTS customer CASCADE;
            """)
    conn.commit()
    curs.close()
    print('Done')


with psycopg2.connect(database="customer", user="postgres", password="120290Vova") as conn:
    clean_db(conn)
    create_db(conn)
    add_client(conn, 'John', 'Doe', 'unknown@strange.com')
    add_client(conn, 'Mike', 'Myers', 'austin@spy.com')
    add_client(conn, 'Hell', 'Boy', 'inferno@dante.com')
    add_phone(conn, '1', '051-404')
    add_phone(conn, '3', '666-13-13')
    add_phone(conn, '2', '777-9-777')
    change_client(conn, '1', 'Italian', 'Stallion', 'rocky@porn.com')
    find_client(conn, 'Italian')
    find_client(conn, None, None, 'austin@spy.com')
    find_client(conn, None, None, None, '666-13-13')

conn.close()

# Сделать так, чтобы телефоны прибавлялись, отбавлялись, обновлялось кол-во