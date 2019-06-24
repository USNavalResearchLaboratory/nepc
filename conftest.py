def pytest_addoption(parser):
    parser.addoption("--local", action="store_true",
                     help="use local copy of NEPC database")
    parser.addoption("--dbug", action="store_true",
                     help="extra printing")


def pytest_generate_tests(metafunc):
    if 'local' in metafunc.fixturenames:
        if metafunc.config.getoption('local'):
            local = [True]
        else:
            local = [False]
        metafunc.parametrize("local", local)
    if 'dbug' in metafunc.fixturenames:
        if metafunc.config.getoption('dbug'):
            dbug = [True]
        else:
            dbug = [False]
        metafunc.parametrize("dbug", dbug)
