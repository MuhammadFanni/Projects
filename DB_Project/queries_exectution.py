from queries_db_script import execute_query, query_1, query_2, query_3, query_4, query_5

DOUBLE_BAR = "============================================================"
# Example Keywords for testing
KEYWORD_1 = "Star"  # For Title search
KEYWORD_2 = "Hanks"  # For Staff search


def exe_query_1(keyword):
    print(DOUBLE_BAR)
    print("Executing Query 1 (Full Text Search - Title):")
    print(query_1.__doc__)
    print(f"Results for keyword '{keyword}':")
    query = query_1(keyword)
    execute_query(query, True)
    print()


def exe_query_2(keyword):
    print(DOUBLE_BAR)
    print("Executing Query 2 (Full Text Search - Staff):")
    print(query_2.__doc__)
    print(f"Results for keyword '{keyword}':")
    query = query_2(keyword)
    execute_query(query, True)
    print()


def exe_query_3():
    print(DOUBLE_BAR)
    print("Executing Query 3 (Revenue by Year):")
    print(query_3.__doc__)
    query = query_3()
    execute_query(query, True)
    print()


def exe_query_4():
    print(DOUBLE_BAR)
    print("Executing Query 4 (Top Rated Actors):")
    print(query_4.__doc__)
    query = query_4()
    execute_query(query, True)
    print()


def exe_query_5():
    print(DOUBLE_BAR)
    print("Executing Query 5 (High Budget & Languages):")
    print(query_5.__doc__)
    query = query_5()
    execute_query(query, True)
    print()


if __name__ == '__main__':
    exe_query_1(KEYWORD_1)
    exe_query_2(KEYWORD_2)
    exe_query_3()
    exe_query_4()
    exe_query_5()
