from src import np, plt

class Plot:
    def __init__(self, p, img):
        self.Nz, self.Nx = img.height, img.width
        self.model_vp = img.model
        self.model_vs = None
        self.model_rho = None

        if p.model_id == 1:
            self.plot_acoustic()
        elif p.model_id == 2:
            self.plot_elastic()

    def plot_acoustic(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, self.Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, self.Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax.imshow(self.model_vp, cmap="jet", aspect="auto")
        ax.set_title("VP Model", fontsize=15)
        ax.set_xlabel("Distance [m]", fontsize=12)
        ax.set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, label='VP [m/s]')
        cax.set_ticks(np.linspace(self.model_vp.min(), self.model_vp.max(), num=5))

        ax.set_xticks(xloc)
        ax.set_xticklabels(xlab)

        ax.set_yticks(zloc)
        ax.set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()

    def plot_elastic(self):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, self.Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, self.Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax[0].imshow(self.model_vp, cmap="jet", aspect="auto")
        ax[0].set_title("VP Model", fontsize=13)
        ax[0].set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, ax=ax[0], label='VP [m/s]')
        cax.set_ticks(np.linspace(self.model_vp.min(), self.model_vp.max(), num=5))

        im2 = ax[1].imshow(self.model_vs, cmap="jet", aspect="auto")
        ax[1].set_title("VS Model", fontsize=13)
        ax[1].set_ylabel("Depth [m]", fontsize=12)
        cax2 = fig.colorbar(im2, ax=ax[1], label='VS [m/s]')
        cax2.set_ticks(np.linspace(self.model_vs.min(), self.model_vs.max(), num=5))

        im3 = ax[2].imshow(self.model_rho, cmap="jet", aspect="auto")
        ax[2].set_title("Density Model", fontsize=13)
        ax[2].set_xlabel("Distance [m]", fontsize=12)
        ax[2].set_ylabel("Depth [m]", fontsize=12)
        cax3 = fig.colorbar(im3, ax=ax[2], label='Density [kg/m$^3$]')
        cax3.set_ticks(np.linspace(self.model_rho.min(), self.model_rho.max(), num=5))

        for i in range(len(ax)):
            ax[i].set_xticks(xloc)
            ax[i].set_xticklabels(xlab)

            ax[i].set_yticks(zloc)
            ax[i].set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()


