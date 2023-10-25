---
description: >-
  Chall do HackTheBoo (evento de Halloween do HackTheBox). Desafio resolvido em
  24/10.
---

# Spellbound Servants

Analisando o código, é possível perceber que a função **`isAuthenticated()`** está vulnerável a uma desserialização insegura. Ela é chamada na rota `/home` com o objetivo de verificar se o usuário está autenticado ou não.

```jsx
@web.route('/home', methods=['GET', 'POST'])
@isAuthenticated
def homeView(user):
    return render_template('index.html', user=user)

def isAuthenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('auth', False)

        if not token:
            return abort(401, 'Unauthorised access detected!')
        
        try:
            user = pickle.loads(base64.urlsafe_b64decode(token))
            kwargs['user'] = user
            return f(*args, **kwargs)
        except:
            return abort(401, 'Unauthorised access detected!')

    return decorator

@api.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return response('All fields are required!'), 401
    
    user = register_user_db(username, password)
    
    if user:
        return response('User registered! Please login'), 200
        
    return response('User already exists!'), 403
```

Depois de encontrar a vulnerabilidade no código, criei um usuário na aplicação atraves do endpoint `/register` e autentiquei.

<figure><img src=".gitbook/assets/Untitled (3).png" alt=""><figcaption><p>Dashboard da aplicação após autenticação</p></figcaption></figure>



Para criar minha _payload_, utilizei um repositório chamado [python-deserialization-attack-payload-generator](https://github.com/j0lt-github/python-deserialization-attack-payload-generator), que contém vários módulos para a desserialização insegura em Python. Sabendo que a flag estava em `/flag.txt`, solicitei que o arquivo fosse copiado para o _path_ `/application/static/js/flag.js`. Como eu não tinha certeza do caminho exato da aplicação, usei "`/proc/self/cwd`" para obter o _path_ de onde o processo estava sendo executado

{% code title="payload utilizado" lineNumbers="true" %}
```jsx
cp /flag.txt /proc/self/cwd/application/static/js/flag.js
```
{% endcode %}

Após criar a _payload_, só precisei enviá-la no valor do cookie e, em seguida, acessar o path da aplicação para validar se o _payload_ tinha sido _trigado_.

<figure><img src=".gitbook/assets/Untitled 1 (3).png" alt=""><figcaption><p>Enviando a <em>payload</em></p></figcaption></figure>

<figure><img src=".gitbook/assets/Untitled 2 (1).png" alt=""><figcaption><p>Acessando a flag</p></figcaption></figure>
