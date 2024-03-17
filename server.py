from openai import OpenAI
import anthropic

from dotenv import load_dotenv
load_dotenv()

import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import signal
import pdfkit

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)


def exit_function(signum,frame):
    exit(0)

signal.signal(signal.SIGTERM,exit_function)
signal.signal(signal.SIGINT,exit_function)

path = os.path.join(os.path.dirname(__file__))

websockets = {}

#Claude
agentBehaviorClaude = '''
Eres un proveedor de material educativo de japonés para alumnos que intentan alcanzar la certificación N5 del examen JLPT
Quiero que generes material de estudio de japonés, lo harás con código HTML y CSS. Me lo darás en este formato JSON: {"content":"...","styles":"..."}
sin saltos de linea, aquí dejo un ejemplo del formato admitido:{
	"content": "<div class=\"container\"><header><h1>Bienvenido al Servicio de PDF</h1></header><p>Este es un ejemplo de HTML con estilos que puedes utilizar para poner a prueba tu servicio de generación de PDF. Puedes personalizar y agregar más contenido según tus necesidades.</p><p>Recuerda que los estilos CSS se mantendrán en el PDF generado, por lo que puedes crear documentos visualmente atractivos.</p><footer><p>Generado por tu servicio de PDF</p></footer></div>",
	"styles": "body { font-family: 'Arial', sans-serif; background-color: #f7f7f7; color: #333; margin: 50px; } header { text-align: center; margin-bottom: 20px; } h1 { color: #0066cc; } p { line-height: 1.6; } .container { max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); } footer { margin-top: 20px; text-align: center; color: #666; }"
}
'''
clientClaude = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

def get_claude_answer(messages,type):
    completion = clientClaude.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        system=agentBehavior,
        messages=messages
    )
    print(completion.content[0].text)
    if type==1:
        return completion.content[0].text
    else:
        #create_pdf(completion.content[0].text)
        return completion.content[0].text

#ChatGPT
agentBehavior = '''
¡Hola! Soy Katalina, una gata instructora de Japonés de entry level. Estoy aquí para ayudarte a conseguir tu certificación N5.
Mis respuestas serán cortas, no más de 3 oraciones. ¡Recuerda, después de cada respuesta, haz "ña" como un gato en japonés!
'''

def get_gpt_answer(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages = messages
    )
    return completion.choices[0].message.content

def process_message(data,websocket):
    print(data)
    if data["action"] == "registerID":
        websockets[data["id"]] = {"ws" : websocket, "chat_history":[{"role": "system", "content": agentBehavior}],"chat_history_claude":[]}
    elif data["action"] == "answerChat":
        websockets[data["id"]]["chat_history_claude"].append({"role":"user","content":data["message"]})
        response = get_claude_answer(websockets[data["id"]]["chat_history_claude"],1)
        websockets[data["id"]]["chat_history_claude"].append({"role":"assistant","content":response})
        websocket.send_data({"action":"gpt_answer","message":response})
    elif data["action"] == "answerPDF":
        websockets[data["id"]]["chat_history_claude"].append({"role":"user","content":data["message"]})
        response = get_claude_answer(websockets[data["id"]]["chat_history_claude"],2)
        websockets[data["id"]]["chat_history_claude"].append({"role":"assistant","content":response})
        websocket.send_data({"action":"answerPDF","message":response})
    else:
        print("no action")
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Websocket abierto")
    
    def on_close(self):
        print("Websocket cerrado")

    def send_data(self,data):
        self.write_message(json.dumps(data))

    def on_message(self,message):
        try:
            data = json.loads(message)
            process_message(data,self)
        except TypeError:
            print("error al processar mensaje")

class StaticHandler(tornado.web.StaticFileHandler):
    def get_content_type(self):
        _, extension = tornado.web.os.path.splitext(self.absolute_path)
        
        mime_types = {
            ".js": "application/javascript",
            ".css": "text/css",
            ".html": "text/html",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml"
        }
        
        return mime_types.get(extension, "text/plain")

TornadoSettings = static_handler_args={'debug':False}
application = tornado.web.Application([
    (r'/command', WebSocketHandler),
    (r'/(.*)',StaticHandler,{"path":os.path.join(path,"public\\"),"default_filename":"index.html"})
],**TornadoSettings)


def create_pdf(data2):
    # JSON con el HTML y CSS
    data = {
        "html": "<div class=\"container\">\n  <h1>Los números en japonés</h1>\n  \n  <table>\n    <tr>\n      <th>Número</th>\n      <th>Kanji</th>\n      <th>Hiragana</th>\n      <th>Romaji</th>\n    </tr>\n    <tr>\n      <td>0</td>\n      <td>零</td>\n      <td>れい</td>\n      <td>rei</td>\n    </tr>\n    <tr>\n      <td>1</td>\n      <td>一</td>\n      <td>いち</td>\n      <td>ichi</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>二</td>\n      <td>に</td>\n      <td>ni</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>三</td>\n      <td>さん</td>\n      <td>san</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>四</td>\n      <td>よん</td>\n      <td>yon</td>\n    </tr>\n    <tr>\n      <td>5</td>\n      <td>五</td>\n      <td>ご</td>\n      <td>go</td>\n    </tr>\n    <tr>\n      <td>6</td>\n      <td>六</td>\n      <td>ろく</td>\n      <td>roku</td>\n    </tr>\n    <tr>\n      <td>7</td>\n      <td>七</td>\n      <td>なな</td>\n      <td>nana</td>\n    </tr>\n    <tr>\n      <td>8</td>\n      <td>八</td>\n      <td>はち</td>\n      <td>hachi</td>\n    </tr>\n    <tr>\n      <td>9</td>\n      <td>九</td>\n      <td>きゅう</td>\n      <td>kyuu</td>\n    </tr>\n    <tr>\n      <td>10</td>\n      <td> 十</td>\n      <td>じゅう</td>\n      <td>juu</td>\n    </tr>\n  </table>\n</div>",
        "css": ".container {\n  max-width: 600px;\n  margin: 0 auto;\n  padding: 20px;\n  font-family: Arial, sans-serif;\n}\n\nh1 {\n  text-align: center;\n  color: #333;\n}\n\ntable {\n  width: 100%;\n  border-collapse: collapse;\n  margin-top: 20px;\n}\n\nth, td {\n  padding: 10px;\n  text-align: center;\n  border-bottom: 1px solid #ccc;\n}\n\nth {\n  background-color: #f0f0f0;\n  font-weight: bold;\n}\n\ntr:hover {\n  background-color: #f9f9f9;\n}\n\ntd:first-child {\n  font-weight: bold;\n  color: #333;\n}\n\ntd:nth-child(2) {\n  font-size: 24px;\n}\n\ntd:nth-child(3), td:nth-child(4) {\n  font-style: italic;\n  color: #666;\n}"
    }

    # Escribir el HTML en un archivo temporal
    with open("temp.html", "w", encoding="utf-8") as file:
        file.write(data["html"])

    # Convertir el HTML en PDF
    pdfkit.from_file("temp.html", "output.pdf", css="temp.css")

    # Eliminar el archivo temporal HTML
    os.remove("temp.html")

if __name__ == '__main__':
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()