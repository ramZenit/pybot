from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
    


def test():
    test_write_file()
    ##
    #test_file_reading()
    ##
    #test_files_listing()
    ##
    

def test_write_file():
    print("##### write file lorem.txt:")
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    print()
    print("##### write file pkg/morelorem.txt:")
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    print()
    print("##### write file /tmp/temp.txt:")
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
    print()


def test_file_reading():
    print("##### test read file main.py:")
    result = get_file_content("calculator", "main.py")
    print(result)
    print()
    print("##### test read file pkg/calculator.py:")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    print()
    print("##### test read file /bin/cat:") # should error
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print()

def test_files_listing():
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
    print()


if __name__ == "__main__":
    test()