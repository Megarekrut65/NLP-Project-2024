import os
import webbrowser

import pandas as pd

from app.drawing import Drawing
from app.utility import to_one_format

def format_frames(morf, markup):
    frame = to_one_format(morf, 2, 1)
    frame.to_csv(morf+".csv", index=False)

    frame = to_one_format(markup, 2, 1)
    frame.to_csv(markup+".csv", index=False)

    return morf+".csv", markup+".csv"

def main():
    types_file = "System/syntaxtypes.csv"
    vid_file = "System/sintaxvind.csv"

    morf_file = input("Enter file with morf data: ")
    markup_file = input("Enter file with markup data: ")
    text_fk = int(input("Enter text fk: "))
    sent_num = int(input("Enter sentence number: "))

    if not os.path.exists(morf_file+".csv") or not os.path.exists(markup_file+".csv"):
        morf_file, markup_file = format_frames(morf_file, markup_file)
    else:
        morf_file, markup_file = morf_file+".csv", markup_file+".csv"

    morf = pd.read_csv(morf_file)
    markup = pd.read_csv(markup_file)
    types = pd.read_csv(types_file)
    vid = pd.read_csv(vid_file)

    drawing = Drawing(morf, markup, types, vid)
    canvas = drawing.make_canvas(text_fk, sent_num)

    html = f"<html><body>{canvas}</body></html>"
    res_file = "Output/result.html"
    file = open(res_file, "w")
    file.write(html)
    file.close()

    webbrowser.open("file://" + os.path.realpath(res_file))

if __name__ == "__main__":
    main()