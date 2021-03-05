# ============================================================================ #
# Abgabe Projektarbeit Einführung ins Programmieren mit Python
# Name
#     Boughalem Mohammed, Mat.Nr. 2066343

# Please read the Jupyter Notebook version for more clarity
# ============================================================================ #
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve2d
import uuid

class GIFGenerator:

    def let_there_be_life(self, prob_life, size=(40, 40)):
        """ Implementing the Game of Life """
        board = self.create_board(size)
        stat = self.status(size, prob_life)

        fig, ax = plt.subplots(figsize=(16, 16))
        scatter = ax.scatter(*board, animated=True, s=100,
                             edgecolor=None, c='#ddc3a5')
        ax.set_facecolor('#ffcce7')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        def update(frame):
            nonlocal stat
            stat, alive_neigbors = self.life_rules(stat)
            colors = self.get_colors(stat, alive_neigbors)
            scatter.set_facecolor(colors)
            return scatter

        return FuncAnimation(fig, update, frames=200)


    def create_board(self, size):
        """ Takes a tuple size (n,m) to create a board (n x m) """
        x = np.arange(0, size[0])
        y = np.arange(0, size[1])
        board = np.meshgrid(x, y)
        return board


    def status(self, size, prob_life):
        stat = (np.random.uniform(0, 1, size=size) >= prob_life)
        return stat


    def life_rules(self, status):
        """
        Applies Conway's Game of Life rules given the current status of the game and returns a tuple of two arrays:
        a the new status of each cell and a representation of the number of its neighbors
        """
        alive_neighbors = self.count_alive_neighbors(status)

        # Under-population :
        survive_up = (alive_neighbors >= 2)
        # Over-population :
        survive_op = (alive_neighbors <= 3)
        # Survivors :
        survive = status * survive_up * survive_op
        # Reproduction :
        new_status = np.where(alive_neighbors == 3, True, survive)

        new_neighbors = self.count_alive_neighbors(new_status)
        return new_status, new_neighbors


    def count_alive_neighbors(self, status):
        """ Counts the number of neighboring alive cells """
        kernel = np.array(
            [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]])

        count = convolve2d(status, kernel, mode='same', boundary="wrap")
        return count


    def get_colors(self, status, count):
        cmap = mpl.cm.plasma
        rescale = count / 8
        colors = [cmap(neighbors) for neighbors in rescale.flatten()]
        cell_alive = status.flatten()
        colors = [(r, g, b, 0.9) if cell else (r, g, b, 0)
                  for cell, (r, g, b, a) in zip(cell_alive, colors)]
        return colors
    
    def generateGIF(self, prob_life=0.5, size=(80,80)):
        filename = str(uuid.uuid1())
        anim = self.let_there_be_life(prob_life=0.5, size=(80, 80))
        anim.save(f'temp/{filename}.gif', writer='pillow')
        return filename



if __name__ == "__main__":
    g = GIFGenerator()
    anim = g.let_there_be_life(prob_life=0.5, size=(80, 80))
    # anim.save('The game of life.gif', writer=animation.FFMpegFileWriter())
    anim.save('The game of life.gif', writer='pillow')
