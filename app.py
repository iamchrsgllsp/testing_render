from flask import Flask, render_template, request, redirect
import os
import openai
import asyncio
from testsongs import songs

chatgpt = os.environ['CHATTOKEN']
app = Flask(__name__, static_folder="static")

openai.api_key = chatgpt


def resp(prompt):
  engine = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role": "user",
              "content": prompt,
          },
      ],
  )
  print(engine)
  return engine.choices[0].message.content


@app.route('/')
def home():
  return render_template("home.html", songs=songs)


@app.route('/getsongs', methods=["POST", "GET"])
def getsongs():
  if request.method == "POST":
    print(request.json)
    prompt = f"from this list of ranked songs, recommend 9 other songs and 1 opposing style song: {request.json}. also recommend 1 movie, 1 game and 1 book that would have similar vibe to the songs"
    data = resp(prompt)
    print(data)
    data = str(data)
    data = data.replace("\n", ", <br>").replace("\\", "")

    return {"data": data}  # You can return a string as an example response
  else:
    return redirect('/')


@app.route('/foundsongs')
def index():
  #data = resp()

  return render_template("songs.html", data=data)


app.run(host='0.0.0.0', port=80, debug=True)
