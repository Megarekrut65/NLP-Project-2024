import pandas as pd

def to_one_format(filename, header_count, selected_header=0):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    headers = [lines[i].strip().split("\t") for i in range(header_count)]
    data = lines[header_count:]

    df = pd.DataFrame(columns=headers[selected_header])
    required_count = len(headers[selected_header])

    for line in data:
        values = line.strip().split("\t")
        for i in range(required_count-len(values)):
            values.append("")

        df.loc[len(df)] = values

    return df
