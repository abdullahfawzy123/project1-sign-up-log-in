import requests.

def main():
    res = request.get("https://www.goodreads.com/book/review_counts.json ", params={"key": "rYlZz0UYSciZ9yOEPJpbA", "isbns": "0380795272"})
    if res.status_code != 200:
        raise Exception("ERROR")
    data = res.json()
    print(data)


if __name__ =="__main__":
    main()
