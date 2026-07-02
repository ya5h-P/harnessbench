from duration import parse_duration, format_duration
def run():
    assert parse_duration("45m") == 2700, parse_duration("45m")
    assert format_duration(2700) == "45m", format_duration(2700)
    print("ALL TESTS PASSED")
if __name__ == "__main__":
    run()
