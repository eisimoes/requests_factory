# Projeto: requests_factory

Método Factory para geração de sessão do módulo Requests

## Instalação

O módulo pode ser instalado a partir do repositório Github. Para instalar, use o comando:

```pip install git+https://github.com/eisimoes/requests_factory```

Para instalar uma versão específica:

```pip install git+https://github.com/eisimoes/requests_factory@1.0.0```

## Parâmetros de configuração

A função de configuração de sesssão ***configure_session()*** aceita os seguintes parâmetros:

- **auth (AuthBase):** Objeto do tipo AuthBase.
- **headers (dict):** Dicionário de headers para a sessão.
- **cookies (CookieJar):** Objeto do tipo CookieJar.
- **proxies (dict):** Dicionário de proxies para a sessão.

## Exemplo de uso

```
from requests_factory import configure_session, get_session

configure_session(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
    },
    proxies={
        http="10.0.0.X:3128",
        https="10.0.0.X:3128"
    }
)

with get_session() as session:
    response = session.get("https://www.google.com")

with get_session() as session:
    response = session.get("https://www.duckduckgo.com")
```

Para projetos grandes, basta acionar a função ***configure_session()*** na incialização do projeto. Após a configuração inicial, as sessões obtidas à partir da invocação da função ***get_session()*** usarão os parâmetros de configuração inicialmente informados.