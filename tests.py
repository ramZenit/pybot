from functions.get_files_info import get_files_info
    


def test():
    print("##### test in calculator dir:")
    result = get_files_info("calculator", ".")
    print(result)
    print()

    print("##### test in calculator/pkg dir")
    result = get_files_info("calculator", "pkg")
    print(result)
    print()

    print("##### test in calculator/bin dir")
    result = get_files_info("calculator", "/bin")
    print(result)
    print()

    print("##### test outside working dir")
    result = get_files_info("calculator", "../")
    print(result)


if __name__ == "__main__":
    test()