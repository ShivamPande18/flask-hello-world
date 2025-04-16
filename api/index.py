from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import google.generativeai as genai
from EvaTTS import EdgeTTSSpeaker
import fitz 
from io import BytesIO
import edge_tts


# from tika import parser
# import re
# import spacy
# nlp = spacy.load('en_core_web_sm')
# from spacy.matcher import Matcher

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api_key = ""
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])

speaker = EdgeTTSSpeaker()

# matcher = Matcher(nlp.vocab)

# def get_email_addresses(string):
#     r = re.compile(r'[\w\.-]+@[\w\.-]+')
#     return r.findall(string)


# def get_phone_numbers(string):
#     r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
#     phone_numbers = r.findall(string)
#     return [re.sub(r'\D', '', num) for num in phone_numbers]


# def extract_name(text):
#    nlp_text = nlp(text)
  
#    # First name and Last name are always Proper Nouns
#    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
  
#    matcher.add('NAME', [pattern], on_match = None)
  
#    matches = matcher(nlp_text)
  
#    for match_id, start, end in matches:
#        span = nlp_text[start:end]
#        return span.text






@app.route('/')
def hello_world():
    return 'Hello from Flask!'


# @app.route('/cvExtract', methods=['POST'])
# def cvExtract():
#     data = request.get_json()
#     if not data or 'cvData' not in data:
#         return jsonify({'error': 'Error parsing cv'}), 400

#     text = data['cvData']
#     parsed_content = {}
#     email = get_email_addresses(text)
#     parsed_content['E-mail'] = email
    
#     phone_number= get_phone_numbers(text)
#     if len(phone_number) <= 10:
#         print(phone_number)
#         parsed_content['Phone number'] = phone_number

#     name = extract_name(text)
#     parsed_content['Name'] =  name

#     Keywords = ["education",
#             "summary",
#             "accomplishments",
#             "executive profile",
#             "professional profile",
#             "personal profile",
#             "work background",
#             "academic profile",
#             "other activities",
#             "qualifications",
#             "experience",
#             "interests",
#             "skills",
#             "achievements",
#             "publications",
#             "publication",
#             "certifications",
#             "workshops",
#             "projects",
#             "internships",
#             "trainings",
#             "hobbies",
#             "overview",
#             "objective",
#             "position of responsibility",
#             "jobs",
#             "gpa"
#            ]

#     text = text.replace("\n"," ")
#     text = text.replace("[^a-zA-Z0-9]", " ");  
#     re.sub('\W+','', text)
#     text = text.lower()

#     content = {}
#     indices = []
#     keys = []
#     for key in Keywords:
#         try:
#             content[key] = text[text.index(key) + len(key):]
#             indices.append(text.index(key))
#             keys.append(key)
#         except:
#             pass

#     zipped_lists = zip(indices, keys)
#     sorted_pairs = sorted(zipped_lists)
#     sorted_pairs

#     tuples = zip(*sorted_pairs)
#     indices, keys = [ list(tuple) for tuple in  tuples]

#     content = []
#     for idx in range(len(indices)):
#         if idx != len(indices)-1:
#             content.append(text[indices[idx]: indices[idx+1]])
#         else:
#             content.append(text[indices[idx]: ])

#     for i in range(len(indices)):
#         parsed_content[keys[i]] = content[i]  


#     return jsonify({'result': parsed_content})



@app.route('/eva', methods=['POST'])
def eva():
    data = request.get_json()
    prompt = data.get('prompt')
    response = chat.send_message(prompt)
    speaker.tts(response.text)
    return send_file('test.mp3', 
                    mimetype='audio/mpeg',
                    as_attachment=True,
                    download_name='response.mp3')

@app.route('/convert', methods=['POST'])
async def convert_text_to_speech():
    print(request.json)
    text = request.json['text']
    output_file = "speech_output.mp3"
    communicate = edge_tts.Communicate(text, "en-GB-LibbyNeural", rate="+20%")
    await communicate.save(output_file)
    return send_file(output_file, mimetype="audio/mpeg")

@app.route('/extractor', methods=['POST'])
def pdfExtractor():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    pdf_file = request.files['file']
    
    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"name": "Shivam Pande", "about me": "Demo about me", "language": ["English","native"], "Education": ["Army Public School", "98%"], "Skills": ["next","react","python","mongo"], "WorkExperience":["Frantiger", "sep 2020 - oct 2024", "1) Resposibility 1\n2) resposibility 2"], "Project":["Proj Name", "2012", "Details", ["Skil1", "skill2", "skill3"]], "certification":["Deatil 1", "Detail 2"] })
    else:
        return jsonify({"error": "File must be a PDF"}), 400


@app.route('/scrapper', methods=['POST'])
def pdfEx():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    pdf_file = request.files['file']
    
    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
        try:
            # Use BytesIO to handle the file in memory
            pdf_bytes = BytesIO(pdf_file.read())
            
            # Open the PDF with PyMuPDF
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            # Extract text from all pages
            text = ""
            for page in doc:
                text += page.get_text()
            
            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File must be a PDF"}), 400

if __name__ == '__main__':
    port = int(5000)  
    app.run(host="0.0.0.0", port=port, debug=True)
