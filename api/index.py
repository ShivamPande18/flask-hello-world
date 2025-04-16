from flask import Flask, request, send_file
from flask_cors import CORS
from api.EvaTTS import EdgeTTSSpeaker
import edge_tts



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



speaker = EdgeTTSSpeaker()


@app.route('/')
def hello_world():
    return 'Hello from Shivam pande!'


@app.route('/convert', methods=['POST'])
async def convert_text_to_speech():
    print(request.json)
    text = request.json['text']
    output_file = "speech_output.mp3"
    communicate = edge_tts.Communicate(text, "en-GB-LibbyNeural", rate="+20%")
    await communicate.save(output_file)
    return send_file(output_file, mimetype="audio/mpeg")


if __name__ == '__main__':
    port = int(5000)
    app.run(host="0.0.0.0", port=port, debug=True)
