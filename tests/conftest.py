import pytest


def pytest_addoption(parser):
    parser.addoption("--host", default="192.168.0.104")
    parser.addoption("--port", default=15000)


@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="session")
def port(request):
    return request.config.getoption("--port")
