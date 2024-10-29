"""
Módulo para configuração e geração de sessão do módulo Requests.

A sessão é criada com os parâmetros auth, headers, cookies e proxies definidos anteriormente.
"""

from contextlib import contextmanager
from http.cookiejar import CookieJar
from typing import Callable, Dict, Type, TypeVar

from requests import Session
from requests.auth import AuthBase


T = TypeVar('T')


def singleton(cls: Type[T]) -> Callable[[], T]:
    """
    Decorator para tornar uma classe um singleton.

    Args:
        cls (Type[T]): A classe a ser tornada um singleton.

    Returns:
        Callable[[], T]: Uma função que retorna a instância singleton da classe.
    """
    instances: Dict[Type[T], T] = {}

    def instance() -> T:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return instance


@singleton
class RequestsSessionFactory:
    """
    Classe Factory responsável por configurar e criar sessão do módulo Requests.

    Atributos:
        _auth (AuthBase): Objeto AuthBase do módulo Requests.
        _headers (dict): Dicionário de headers para a sessão.
        _cookies (dict): Dicionário de cookies para a sessão.
        _proxies (dict): Dicionário de proxies para a sessão.
    """

    def __init__(self) -> None:
        """
        Inicializa a instância da classe.
        """
        self._auth: AuthBase | None = None
        self._headers: Dict | None = None
        self._cookies: Dict | None = None
        self._proxies: Dict | None = None

    def set_auth(self, auth: AuthBase | None) -> None:
        """
        Define a autenticação para a sessão.

        Args:
            auth (AuthBase): Objeto do tipo AuthBase.
        """
        if isinstance(auth, AuthBase) or auth is None:
            self._auth = auth
        else:
            raise TypeError("O parâmetro `auth` deve ser um do tipo AuthBase ou None")

    def set_headers(self, headers: Dict | None) -> None:
        """
        Define os headers para a sessão.

        Args:
            headers (dict): Dicionário de headers para a sessão.
        """
        if isinstance(headers, dict) or headers is None:
            self._headers = headers
        else:
            raise TypeError("O parâmetro `headers` deve ser um dicionário ou None")

    def set_cookies(self, cookies: CookieJar) -> None:
        """
        Define os cookies para a sessão.

        Args:
            cookies (CookieJar): Objeto do tipo CookieJar.
        """
        if isinstance(cookies, CookieJar) or cookies is None:
            self._cookies = cookies
        else:
            raise TypeError("O parâmetro `cookies` deve ser um do tipo CookieJar ou None")

    def set_proxies(self, proxies: Dict) -> None:
        """
        Define os proxies para a sessão.

        Args:
            proxies (dict): Dicionário de proxies para a sessão.
        """
        if isinstance(proxies, dict) or proxies is None:
            self._proxies = proxies
        else:
            raise TypeError("O parâmetro `proxies` deve ser um dicionário ou None")

    def get_session(self) -> Session:
        """
        Cria e retorna uma sessão do módulo Requests.

        A sessão é criada com os headers, cookies e proxies definidos anteriormente.

        Returns:
            Session: Objeto Session do módulo Requests.
        """
        try:
            session = Session()

            if self._auth:
                session.auth = self._auth

            if self._headers:
                session.headers.update(self._headers)

            if self._cookies:
                session.cookies.update(self._cookies)

            if self._proxies:
                session.proxies.update(self._proxies)

            return session

        except Exception as e:
            raise e


def configure_session(
    auth: AuthBase = None, headers: Dict = None, cookies: CookieJar = None, proxies: Dict = None
) -> None:
    """
    Configura autenticação, headers, cookies e proxies para a sessão.

    Args:
        auth (AuthBase): Objeto do tipo AuthBase.
        headers (dict): Dicionário de headers para a sessão.
        cookies (CookieJar): Objeto do tipo CookieJar.
        proxies (dict): Dicionário de proxies para a sessão.
    """
    requests_session_factory = RequestsSessionFactory()

    requests_session_factory.set_auth(auth)
    requests_session_factory.set_headers(headers)
    requests_session_factory.set_cookies(cookies)
    requests_session_factory.set_proxies(proxies)


@contextmanager
def get_session() -> Session:
    """
    Gerenciador de contexto que cria e gerencia uma sessão do módulo Requests.
    """

    try:
        requests_session_factory = RequestsSessionFactory()
        session = requests_session_factory.get_session()
        yield session

    except Exception as e:
        raise Exception(f"Failed to create Session: {e}") from e

    finally:
        session.close()
