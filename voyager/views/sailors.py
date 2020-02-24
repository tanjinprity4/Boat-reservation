from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def get_all_sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s ")

def get_all_sailors_name_from_boat(conn, b_name):
    return execute(conn, "SELECT DISTINCT s.sid, s.name, s.age, s.experience FROM ((Boats AS b INNER JOIN Voyages As v ON b.bid = v.bid) INNER JOIN Sailors AS s ON v.sid = s.sid) WHERE b.name = :b_name", {'b_name': b_name} )

def get_all_sailors_name_from_date(conn, date):
    return execute(conn, "SELECT DISTINCT s.sid, s.name, s.age, s.experience FROM (Voyages As v INNER JOIN Sailors AS s ON v.sid = s.sid) WHERE v.date_of_voyage = :date", {'date': date} )

def get_all_sailors_name_from_color(conn, color):
    return execute(conn, "SELECT DISTINCT s.sid, s.name, s.age, s.experience FROM ((Boats AS b INNER JOIN Voyages As v ON b.bid = v.bid) INNER JOIN Sailors AS s ON v.sid = s.sid) WHERE b.color = :color", {'color': color} )

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = get_all_sailors(conn)
        return render_template("table.html", name="Sailors", rows=rows)

    @bp.route("/sailors/who-sailed")
    def _get_all_sailors_name_from_boat():
        with get_db() as conn:
            boat_name = request.args.get('boat-name')
            rows = get_all_sailors_name_from_boat(conn, boat_name)
        return render_template("table.html", name="Sailors Who Sailed %s" %boat_name, rows=rows)
    
    @bp.route("/sailors/who-sailed-on-date")
    def _get_all_sailors_name_from_date():
        with get_db() as conn:
            date = request.args.get('date')
            rows = get_all_sailors_name_from_date(conn, date)
        return render_template("table.html", name="Sailors Who Sailed On %s" %date, rows=rows)

    @bp.route("/sailors/who-sailed-on-boat-of-color")
    def _get_all_sailors_name_from_color():
        with get_db() as conn:
            color = request.args.get('color')
            rows = get_all_sailors_name_from_color(conn, color)
        return render_template("table.html", name="Sailors who sailed on boat of %s color" %color, rows=rows)