
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def get_all_boats_from_sailor_name(conn, s_name):
    return execute(conn, "SELECT DISTINCT b.bid, b.name, b.color FROM ((Sailors AS s INNER JOIN Voyages As v ON s.sid = v.sid) INNER JOIN Boats AS b ON v.bid = b.bid) WHERE s.name = :s_name", {'s_name': s_name})

def get_all_boats_by_popularity(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color, count(v.bid) AS number_of_voyages FROM (Voyages As v INNER JOIN Boats AS b ON v.bid = b.bid) GROUP BY v.bid ORDER BY count(v.bid) desc")

def add_a_boat(conn, name, color):
    if name == None or color == None or name == "" or color == "":
        raise Exception
    return execute(conn, "INSERT INTO Boats(name,color) VALUES (:name,:color) ", {'name': name, 'color': color} )

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)

    @bp.route("/boats/sailed-by")
    def _get_all_boats_from_sailor_name():
        with get_db() as conn:
            sailors_name = request.args.get('sailor-name')
            rows = get_all_boats_from_sailor_name(conn, sailors_name)
        return render_template("table.html", name="Boats sailed by %s" %sailors_name, rows=rows)

    @bp.route("/boats/by-popularity")
    def _get_all_boats_by_popularity():
        with get_db() as conn:
            rows = get_all_boats_by_popularity(conn)
        return render_template("table.html", name="List of boats by order of popularity", rows=rows)

    @bp.route("/boats/add")
    def add_boat_page():
        return render_template("form_boat.html")

    @bp.route("/boats/add/submit", methods = ['POST'])
    def _add_a_boat():
        with get_db() as conn:
            name = request.form['name']
            color = request.form['color'].lower()
            try:
                add_a_boat(conn, name, color)
            except Exception:
                return render_template("form_error.html", errors = ["Your record was not added. Check your inputs."])
            rows = boats(conn)
        return render_template("table.html", name="%s Boat Added" %name, rows=rows)