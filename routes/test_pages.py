from flask import render_template


def test_page():
    return render_template("test1.html", id=12345)


def another_page():
    return render_template("test1.html", id=321)
