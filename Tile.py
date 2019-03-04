class Tile:
    def __init__(self,row,col,color,infected):
        self.__i_row = row
        self.__i_col = col
        self.__s_color = color
        self.__b_infected = infected

    def set_row(self,row):
        self.__i_row = row

    def get_row(self):
        return self.__i_row

    def set_col(self,col):
        self.__i_col = col

    def get_col(self):
        return self.__i_col

    def set_color(self,color):
        self.__s_color = color

    def get_color(self):
        return self.__s_color

    def set_infected(self,infected):
        self.__b_infected = infected

    def get_infected(self):
        return self.__b_infected
