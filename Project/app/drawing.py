import math

from app.canvas_builder import CanvasBuilder

class Drawing:
    def __init__(self, morf_frame, markup_frame, types_frame, vid_frame):
        self.morf_frame = morf_frame
        self.markup_frame = markup_frame
        self.types_frame = types_frame
        self.vid_frame = vid_frame


    def get_color(self, ct):
        items = self.types_frame[self.types_frame["ct"]==ct]
        if len(items) > 0:
            return "#"+items["color"].values[0]
        
        return "black"

    def synttolk(self, ct):
        items = self.types_frame[self.types_frame["ct"] == ct]
        if len(items) > 0:
            return f"{ct}: {items["ctname"].values[0]}"
        return ct

    def syntvidntolk(self, vid):
        if vid is None or math.isnan(vid):
            return ""
        vid = int(vid)

        items = self.vid_frame[self.vid_frame["vid"] == vid]
        if len(items) > 0:
            return f"{items["vname"].values[0]}"
        return vid
    
    def make_canvas(self, text_fk, sent_num, vstep=30):
        filtered_markup = (self.markup_frame[
            (self.markup_frame["text_fk"] == text_fk) & (self.markup_frame["sentence_number"] == sent_num)]
                           .reset_index(drop=True))

        filtered_morf = (self.morf_frame[
            (self.morf_frame["TextFK"] == text_fk) & (self.morf_frame["sentence_number"] == sent_num)].copy()
                         .reset_index(drop=True))

        filtered_morf["pos"] = 0
        height = len(filtered_markup) * vstep
        builder = CanvasBuilder(1, height)
        builder.append("ctx.font = '14px Arial';")

        deep = 0
        was_change = True
        max_ = 0

        while deep < 100 and was_change:
            deep += 1
            was_change = False
            for i in range(len(filtered_morf)):
                for k in range(len(filtered_morf)):
                    if (filtered_morf["w2"].values[i] == filtered_morf["w1"].values[k]
                            and filtered_morf["pos"].values[i] >= filtered_morf["pos"].values[k]):
                        filtered_morf.loc[k, "pos"] = filtered_morf.loc[i, "pos"] + 1
                        if filtered_morf["pos"].values[k] > max_:
                            max_ = filtered_morf["pos"].values[k]
                        was_change = True

        max_ += 2
        for i in range(len(filtered_morf)):
            pfrom = 0
            pto = 0

            for k in range(len(filtered_markup)):
                if filtered_morf["w1"].values[i] == filtered_markup["word_Id"].values[k]:
                    pfrom = k
                elif filtered_morf["w2"].values[i] == filtered_markup["word_Id"].values[k]:
                    pto = k
            
            
            pos = filtered_morf["pos"].values[i]
            builder.append("ctx.beginPath();")
            builder.append(f"ctx.strokeStyle='{self.get_color(filtered_morf["ct"].values[i][:2])}';")
            builder.append(f"ctx.moveTo({ pos * 20}, {pfrom * vstep + 7});")
            builder.append(f"ctx.lineTo({(pos + 1) * 20}, {pto * vstep + 7});")
            builder.append("ctx.stroke();")

            tga1 = math.atan(((pfrom - pto) * vstep) / 20.0)

            if pto < pfrom:
                builder.append("ctx.beginPath();")

                deltx = math.cos(tga1 - math.pi / 6) * 10
                delty = math.sin(tga1 - math.pi / 6) * 10
                builder.append(f"ctx.moveTo({(pos + 1) * 20 - int(deltx)}, {pto * vstep + 7 + int(delty)});")
                builder.append(f"ctx.lineTo({(pos + 1) * 20}, {pto * vstep + 7});")

                deltx = math.sin(math.pi / 2 - tga1 - math.pi / 6) * 10
                delty = math.cos(math.pi / 2 - tga1 - math.pi / 6) * 10
                builder.append(f"ctx.lineTo({(pos + 1) * 20 - int(deltx)}, {pto * vstep + 7 + int(delty)});")
                builder.append("ctx.stroke();")
            else:
                tga1 = math.atan(20.0 / ((pto - pfrom) * vstep))
                deltx = math.sin(tga1 - math.pi / 6) * 10
                delty = math.cos(tga1 - math.pi / 6) * 10
                builder.append(f"ctx.moveTo({(pos + 1)*20 - int(deltx)}, {pto * vstep + 7 - int(delty)});")
                builder.append(f"ctx.lineTo({(pos+1)*20}, {pto * vstep + 7});")

                deltx = math.cos(math.pi / 2 - tga1 - math.pi / 6) * 10
                delty = math.sin(math.pi / 2 - tga1 - math.pi / 6) * 10
                builder.append(f"ctx.lineTo({(pos+1)*20 - int(deltx)}, {pto * vstep + 7 - int(delty)});")
                builder.append("ctx.stroke();")

            builder.append("ctx.beginPath();")
            builder.append("ctx.strokeStyle='#ccc';")
            builder.append(f"ctx.moveTo({(pos+1)*20}, {pto * vstep + 7});")
            builder.append(f"ctx.lineTo({max_*20-5}, {pto * vstep + 7});")
            builder.append("ctx.stroke();")
            builder.append("ctx.fillStyle = '#000';")
            builder.append(f"ctx.fillText(\"{self.synttolk(filtered_morf["ct"].values[i])}\", {20 * max_ + 160}, {pto * vstep + 12});")
            builder.append("ctx.fillStyle = '#0b910b';")
            builder.append(f"ctx.fillText(\"{self.syntvidntolk(filtered_morf["vidn"].values[i])}\", {20 * max_ + 160}, {pto * vstep + 26});")

        builder.append("ctx.fillStyle = '#000';")
        for i in range(len(filtered_markup)):
            builder.append(f"ctx.fillText(\"{filtered_markup["word"].values[i].replace("\"", "'")}\", {20*max_}, {i * vstep + 12});")

        builder.close()

        return builder.get()


                