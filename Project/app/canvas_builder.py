class CanvasBuilder:
    def __init__(self, nid, height):
        self.__string = f'<canvas id="canvas{nid}" width="800" height="{height}" class="conc_tree"></canvas>\n'
        #self.__string += "<style>.conc_tree{width:600px;float:right;}</style>\n"
        self.__string += f"<script>var c = document.getElementById('canvas{nid}');var ctx = c.getContext('2d');\n"

    def append(self, row):
        self.__string += f"{row}\n"

        return self
    def close(self):
        self.__string += "</script>\n"

    def get(self):
        return self.__string
