def pytest_addoption(parser):
    parser.addoption("--local", action="store_true",
                     help="use local copy of NEPC database")
    parser.addoption("--dbug", action="store_true",
                     help="extra printing")
    parser.addoption("--github", action="store_true", 
                     help="run tests on GitHub")


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
    if 'github' in metafunc.fixturenames:
        if metafunc.config.getoption('github'):
            github = [True]
        else:
            github = [False]
        metafunc.parametrize("github", github)
