from src import np, plt

class AcousticModelPlot:

    @staticmethod
    def plot(model: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax.imshow(model, cmap="jet", aspect="auto")
        ax.set_title("VP Model", fontsize=15)
        ax.set_xlabel("Distance [m]",fontsize=12)
        ax.set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, label='VP [m/s]')
        cax.set_ticks(np.linspace(model.min(), model.max(), num=5))

        ax.set_xticks(xloc)
        ax.set_xticklabels(xlab)

        ax.set_yticks(zloc)
        ax.set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()
        return fig

