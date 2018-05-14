#!/usr/bin/env python3
from urllib.parse import urlparse

from flask import render_template, request, redirect, abort, escape, jsonify

from app import app
from app.basic_resp import BasicResp
from app.dbutils import get_long_link, insert_id_unique
from app.logger import get_logger

logger = get_logger(__file__)


@app.route('/', methods=['GET', 'POST', 'HEAD'])
@app.route('/<short_link>', methods=['GET', 'POST'])
def short(short_link=""):
    if request.method == "GET" or request.method == 'HEAD':
        if short_link:
            no_auto = short_link[-1] == "+"
            if no_auto:
                short_link = short_link[:-1]
            result = get_long_link(short_link)
            logger.info("get long link {}".format(result))
            if result != "":
                url = result
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
        custom_id = request.form.get("customId")  # 自定义短域名
        if len(long_url) <= 0:
            abort(400)
        if custom_id is not None and len(custom_id) > 0:
            origin_url = get_long_link(custom_id)
            if long_url != origin_url and origin_url != '':
                resp = BasicResp(-1, 'error, customId exist', origin_url)
                return jsonify(resp.__dict__)
        database_id = insert_id_unique(long_url, custom_id, request.remote_addr)
        resp = BasicResp('success', request.url_root + database_id)
        return jsonify(resp.__dict__)  # Short link in plain text


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=4000)  # If you call this file directly it will always run in debug mode. THIS IS VERY DANGEROUS!
