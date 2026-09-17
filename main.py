from driver_setup import start_driver
from run_test import run_test
from driver_setup import Context

test_cases = ["test_case_4"]

for case in test_cases:
    ctx: Context = start_driver()
    run_test(ctx, case)

