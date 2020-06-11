import requests

def main():
    res = request.get("https://www.goodreads.com/book/isbn/ISBN?format=FORMAT")
    if res.status_code != 200:
        raise Exception("ERROR")
    data = res.json()
    print(data)


if __name__ =="__main__":
    main()
