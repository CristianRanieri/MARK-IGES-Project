import pandas as pd


def count_libraries(file):
    dict = {}
    for index, row in file.iterrows():
        libraries = row['libraries']
        libraries = libraries.replace("{", "").replace("}", "").replace("'", "").replace(" ", "").split(",")
        for lib in libraries:
            if lib in dict:
                dict[lib] += 1
            else:
                dict[lib] = 1
    # save dict as csv
    df = pd.DataFrame(list(dict.items()), columns=['library', 'count'])
    return df

def main():
    file = pd.read_csv("consumer_libraries.csv")
    df = count_libraries(file)
    df.to_csv("consumer_libraries_count.csv", index=False)

if __name__ == "__main__":
    main()
