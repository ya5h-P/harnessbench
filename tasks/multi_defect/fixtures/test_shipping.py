from shipping import quote

def run():
    # weak shown test: only simple light/short cases (no surcharge, no express, above minimum)
    assert quote(10, 100) == 20.0, quote(10, 100)
    assert quote(4, 50) == 12.0, quote(4, 50)
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run()
