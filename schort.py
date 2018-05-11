#!/usr/bin/env python3
import base64
import hashlib
import sqlite3
import time
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, abort, escape

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'HEAD'])
@app.route('/<short_link>', methods=['GET', 'POST'])
def short(short_link=""):
    if request.method == "GET" or request.method == 'HEAD':
        if short_link:
            no_auto = short_link[-1] == "+"
            if no_auto:
                short_link = short_link[:-1]
            conn = sqlite3.connect("data/links.sqlite")
            c = conn.cursor()
            result = c.execute('SELECT longLink FROM links WHERE shortLink=?', (short_link,)).fetchone()
            conn.close()
            if result:
                url = result[0]
                parsed_url = urlparse(url)
                if parsed_url.scheme == "":
                    url = "http://" + url

                if "resolve" in request.args:
                    return escape(url)
                else:
                    if no_auto:
                        url = str(escape(url))
                        html = "<a href=" + url + ">" + url + "</a>"
                        return html
                    else:
                        return redirect(url, code=301)  # Redirect to long URL saved in the database
            else:
                return render_template("index.html", name=short_link, message="Enter long URL for " + request.url_root + short_link + ":",
                                       message_type="info")  # Custom link page
        else:
            return render_template("index.html", name=short_link)  # Landing page
    elif request.method == "POST":  # Someone submitted a new link to short
        long_url = request.form["url"]  # required, accept the exception if the key does not exist
        wish_id = request.form.get("wishId")
        if len(long_url) <= 0:
            abort(400)
        database_id = insert_id_unique(long_url, id_to_check=wish_id)
        return request.url_root + database_id  # Short link in plain text


def insert_id_unique(origin_url, id_to_check=None):
    hash_url = hashlib.sha256(origin_url.encode()).digest()
    base64_url = base64.urlsafe_b64encode(hash_url).decode()
    if id_to_check is None or id_to_check == "":
        id_to_check = base64_url[:4]

    conn = sqlite3.connect("data/links.sqlite")
    c = conn.cursor()
    try:
        c.execute('INSERT INTO links VALUES (?, ?, ?, ?, ?)', (id_to_check, origin_url, int(time.time()), request.remote_addr, "default"))
        database_id = id_to_check
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        print("Hash already exists, does the long URL matches?")
        long_url_db = c.execute('SELECT * FROM links WHERE shortLink=?', (id_to_check,)).fetchone()
        if origin_url == long_url_db[1]:
            print(origin_url + " is already in database with id " + id_to_check + ". Serving old id…")
            database_id = id_to_check
        else:
            print("Found real hash collision for " + origin_url + " and " + long_url_db[1])
            conn.commit()
            conn.close()
            if len(base64_url) - 1 >= len(id_to_check) + 1:
                database_id = insert_id_unique(origin_url, id_to_check=base64_url[:len(id_to_check) + 1])
            else:
                print("Can't produce a long enough hash from the new link to be unique. This should never happen")
                print("Bailing out, you are on your own. Good luck.")
                print("=========================================================================================")
                abort(500)

    return database_id


def init_db():
    conn = sqlite3.connect("data/links.sqlite")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links (shortLink UNIQUE NOT NULL, longLink, timestamp, ip, redirectMethod);''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # If you call this file directly it will always run in debug mode. THIS IS VERY DANGEROUS!

# vim: noexpandtab:ts=2:sw=2:sts=2
