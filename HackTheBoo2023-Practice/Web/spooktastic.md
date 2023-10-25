---
description: >-
  Chall do HackTheBoo (evento de Halloween do HackTheBox). Desafio resolvido em
  23/10.
---

# SpookTastic

Comecei a _challenge_ analisando o código da aplicação e logo de início, notei que a aplicação se comportava de forma semelhante ao desafio [_PumpkinSpice_](pumpkinspice.md). Havia um _array_ que era incrementado com base no nosso input e, em seguida, o valor era renderizado por um _bot_ por meio de uma página HTML em outra rota.

```jsx
registered_emails, socket_clients = [], {}

generate = lambda x: "".join([random.choice(string.hexdigits) for _ in range(x)])
BOT_TOKEN = generate(16)

def blacklist_pass(email):
    email = email.lower()

    if "script" in email:
        return False

    return True

def send_flag(user_ip):
    for id, ip in socket_clients.items():
        if ip == user_ip:
            socketio.emit("flag", {"flag": open("flag.txt").read()}, room=id)

def start_bot(user_ip):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    host, port = "localhost", 1337
    HOST = f"http://{host}:{port}"

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--safebrowsing-disable-auto-update")
    options.add_argument("--media-cache-size=1")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--user-agent=HTB/1.0")

    service = Service(executable_path="/usr/bin/chromedriver")
    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(f"{HOST}/bot?token={BOT_TOKEN}")

        WebDriverWait(browser, 3).until(EC.alert_is_present())

        alert = browser.switch_to.alert
        alert.accept()
        send_flag(user_ip)
    except Exception as e:
        pass
    finally:
        registered_emails.clear()
        browser.quit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/register", methods=["POST"])
def register():
    if not request.is_json or not request.json["email"]:
        return abort(400)
    
    if not blacklist_pass(request.json["email"]):
        return abort(401)

    registered_emails.append(request.json["email"])
    Thread(target=start_bot, args=(request.remote_addr,)).start()
    return {"success":True}

@app.route("/bot")
def bot():
    if request.args.get("token", "") != BOT_TOKEN:
        return abort(404)
    return render_template("bot.html", emails=registered_emails)
```

Depois de ter uma ideia do que precisava ser feito, fui verificar como era a parte visual da aplicação.

<figure><img src=".gitbook/assets/Untitled (2).png" alt=""><figcaption><p>Página principal</p></figcaption></figure>

A única diferença entre esse desafio e o _PumpkinSpice_ está na maneira de conseguir a flag. Na função _**`start_bot()`**_, é especificado que precisamos _triggar_ um _`alert()`_ para que a função _**`send_flag()`**_ seja chamada. Nessa função, a _flag_ é enviada por meio de um _websocket_.

{% code title="payload utilizado" %}
```jsx
<img src=x onerror=alert('hello') />vsmpython@gmail.com
```
{% endcode %}

Depois de entender o que precisava ser feito e como fazê-lo, só precisei criar uma _payload_ sem a _tag `<script>`_, pois havia um filtro. Ao enviar a _payload_, a flag era exibida na tela.

<figure><img src=".gitbook/assets/Untitled 1 (2).png" alt=""><figcaption><p>Payload sendo <em>triggado</em></p></figcaption></figure>
