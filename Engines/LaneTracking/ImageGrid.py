class ImageGrid:
    grid = None

    def __init__(self, image):
        if image.shape != (240, 320):
            raise Exception("Image dimensions not supported! Required: 240x320")

        ul_field = image[0:80, 0:106]  # upper left
        um_field = image[0:80, 106:213]  # upper middle
        ur_field = image[0:80, 213:320]  # upper right

        ml_field = image[80:160, 0:106]  # middle left
        mm_field = image[80:160, 106:213]  # middle middle
        mr_field = image[80:160, 213:320]  # middle right

        bl_field = image[160:240, 0:106]  # bottom left
        bm_field = image[160:240, 106:213]  # bottom middle
        br_field = image[160:240, 213:320]  # bottom right

        self.grid = [ul_field, um_field, ur_field, ml_field, mm_field, mr_field, bl_field, bm_field, br_field]

    def get_grid(self):
        return self.grid

    def get_field(self, grid_field):
        """
        TODO
        :param grid_field: Location of the field in the grid
        :return: Selected image segment
        """
        return self.grid[grid_field.value]
