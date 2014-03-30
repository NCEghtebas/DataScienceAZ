import sys
from database import connect
from sweep import sweep, sweep_range

def main():
    conn = connect(sys.argv[1])
    n = int(sys.argv[2])

    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS sir_runs (
            id SERIAL PRIMARY KEY,
            gamma REAL,
            beta REAL
        )''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS sir_results (
            id INTEGER REFERENCES sir_runs,
            s INTEGER,
            i INTEGER,
            r INTEGER,
            t SMALLINT
        );''')
    conn.commit()

    sr = sweep_range(0.99, 0.01, n)
    for g, b, sw in sweep(1000, 5, 0, sr, sr):
        print g, b, len(sw)
        cur.execute(
            '''INSERT INTO sir_runs
                (gamma, beta) VALUES (%s, %s)
                RETURNING id;''', (g, b))
        id, = cur.fetchone()
        for t in xrange(len(sw)):
            s, i, r = sw[t]
            cur.execute(
                'INSERT INTO sir_results VALUES (%s, %s, %s, %s, %s);',
                (id, s, i, r, t))
    conn.commit()


if __name__ == '__main__':
    main()
