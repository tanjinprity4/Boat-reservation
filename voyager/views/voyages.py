from collections import namedtuple

from flask import render_template
from flask import request

from voyager.db import get_db, execute

def voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def add_a_voyage(conn, sid, bid, date_of_voyage):
    execute(conn, "INSERT INTO Voyages(sid, bid, date_of_voyage) VALUES (:sid,:bid,:date_of_voyage) ", {'sid': sid, 'bid': bid, 'date_of_voyage': date_of_voyage } )

def views(bp):
    @bp.route("/voyages")
    def _voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)
    
    @bp.route("/voyages/add")
    def add_voyage_page():
        return render_template("form_voyage.html")

    @bp.route("/voyages/add/submit", methods = ['POST'])
    def _add_a_voyage():
        with get_db() as conn:
            sid = request.form['sid']
            bid = request.form['bid']
            date_of_voyage = request.form['date_of_voyage']
            add_a_voyage(conn, sid, bid, date_of_voyage)
            rows = voyages(conn)
        return render_template("table.html", name="Voyage Added", rows=rows)