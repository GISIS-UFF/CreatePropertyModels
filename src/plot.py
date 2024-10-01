from src import np, plt

class Plot:
    @staticmethod
    def plot_acoustic(model: list, Nx: int, Nz: int):
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

    
    @staticmethod
    def plot_elastic(model_vp: list, model_vs: list, model_rho: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax[0].imshow(model_vp, cmap="jet", aspect="auto")
        ax[0].set_title("VP Model", fontsize=13)
        #ax[0].set_xlabel("Distance [m]",fontsize=12)
        ax[0].set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, ax=ax[0], label='VP [m/s]')
        cax.set_ticks(np.linspace(model_vp.min(), model_vp.max(), num=5))

        im2 = ax[1].imshow(model_vs, cmap="jet", aspect="auto")
        ax[1].set_title("VS Model", fontsize=13)
        #ax[1].set_xlabel("Distance [m]",fontsize=12)
        ax[1].set_ylabel("Depth [m]", fontsize=12)
        cax2 = fig.colorbar(im2, ax=ax[1], label='VS [m/s]')
        cax2.set_ticks(np.linspace(model_vs.min(), model_vs.max(), num=5))

        im3 = ax[2].imshow(model_rho, cmap="jet", aspect="auto")
        ax[2].set_title("Density Model", fontsize=13)
        ax[2].set_xlabel("Distance [m]",fontsize=12)
        ax[2].set_ylabel("Depth [m]", fontsize=12)
        cax3 = fig.colorbar(im3, ax=ax[2], label='Density [kg/m$^3$]')
        cax3.set_ticks(np.linspace(model_rho.min(), model_rho.max(), num=5))

        for i in range(len(ax)):
            ax[i].set_xticks(xloc)
            ax[i].set_xticklabels(xlab)

            ax[i].set_yticks(zloc)
            ax[i].set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()
        return fig


