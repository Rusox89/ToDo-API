from unittest import TextTestRunner, TestSuite
from test_auth import suite as auth_suite
from test_entries import suite as entry_suite

if __name__ == "__main__":
    test_suites = [
        auth_suite,
        entry_suite
    ]
    main_suite = TestSuite()
    for suite in test_suites:
        main_suite.addTests(suite())
    ttr = TextTestRunner()
    ttr.run(main_suite)
