from flask import render_template, flash, redirect, request
from app import app
from app.forms import CppForm
import subprocess
import json
from threading import Timer

kill = lambda process: process.kill()

@app.route("/", methods=["GET", "POST"])
def home():
    form = CppForm()
    if request.method == "POST":
        f = open("compiled/tempCode.cpp", "w+")
        f.write(form.code.data)
        f.close()
        f = open("compiled/tempInput", "w+")
        f.write(form.inputText.data)
        f.close()
        error = ""
        output = ""
        try:
            error = str(
                subprocess.check_output(
                    "g++ compiled/tempCode.cpp -o compiled/tempCode; exit 0",
                    stderr=subprocess.STDOUT,
                    shell=True,
                ),
                "utf-8",
            ).split("\n")

            if error == [""]:
                error = ""

            subprocess.call(
                    ["./compiled/tempCode <compiled/tempInput >compiled/tempOutput"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    timeout=1
            )

            f = open("compiled/tempOutput", "r")
            output = f.readlines()
            f.close()
        except subprocess.TimeoutExpired:
            error = "Time Limit Exceeded"
        except Exception as e:
            error = str(e)

        return json.dumps({"error": error, "output": output})
    return render_template("home.html", title="Compiler", form=form)

