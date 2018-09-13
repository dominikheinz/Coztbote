class PixelRow():
    index = None

    left_edge_pos = 0
    right_edge_pos = 0

    edge_distance = None

    left_edge_offset = 0
    right_edge_offset = 0

    def __init__(self, raw_row, index):

        self.raw_row = raw_row
        self.index = index

        self.calculate_edges()
        self.calculate_offsets()

        self.wanted_offset = (self.right_edge_pos - self.left_edge_pos) / 2

    def calculate_edges(self):

        for i in range(self.raw_row.shape[0]):

            if self.raw_row[i] == 255:

                if self.left_edge_pos is None:
                    self.left_edge_pos = i

                else:
                    self.right_edge_pos = i
                    break

    def calculate_offsets(self):

        self.left_edge_offset = 160 - self.left_edge_pos
        self.right_edge_offset = self.right_edge_pos - 160

    @staticmethod
    def get_pixel_rows(img, number_of_rows=3, step=40):
        h, w = img.shape
        pixel_rows = []

        for i in range(number_of_rows):
            pixel_rows.append(PixelRow(img[h - (step + i * step)], i))

        return pixel_rows
