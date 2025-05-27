import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MobiusStrip:
    def __init__(self, R=1.0, w=0.2, n=200):
        self.R = R      # Radius from the center to the strip
        self.w = w      # Width of the strip
        self.n = n      # Resolution
        self.u, self.v = np.meshgrid(
            np.linspace(0, 2 * np.pi, n),
            np.linspace(-w / 2, w / 2, n)
        )
        self.x, self.y, self.z = self._compute_coordinates()

    def _compute_coordinates(self):
        u = self.u
        v = self.v
        R = self.R
        x = (R + v * np.cos(u / 2)) * np.cos(u)
        y = (R + v * np.cos(u / 2)) * np.sin(u)
        z = v * np.sin(u / 2)
        return x, y, z

    def surface_area(self): # Approximate the surface area using the cross product of partial derivatives
        du = 2 * np.pi / (self.n - 1) 
        dv = self.w / (self.n - 1)

        xu, xv = np.gradient(self.x, du, dv, edge_order=2)
        yu, yv = np.gradient(self.y, du, dv, edge_order=2)
        zu, zv = np.gradient(self.z, du, dv, edge_order=2)

        # Cross product of tangent vectors
        cross = np.sqrt(         
            (yu * zv - zu * yv)**2 +
            (zu * xv - xu * zv)**2 +
            (xu * yv - yu * xv)**2
        )

        # Surface area ≈ sum of local parallelogram areas
        area = np.sum(cross) * du * dv
        return area

    def edge_length(self):
        # Get the edge coordinates (v = ±w/2)
        edge1 = self._get_curve(self.v[:, 0])  # v = -w/2
        edge2 = self._get_curve(self.v[:, -1]) # v = +w/2

        def curve_length(curve):
            dx = np.diff(curve[0])
            dy = np.diff(curve[1])
            dz = np.diff(curve[2])
            return np.sum(np.sqrt(dx**2 + dy**2 + dz**2))

        return curve_length(edge1) + curve_length(edge2)

    def _get_curve(self, v_vals):
        u_vals = np.linspace(0, 2 * np.pi, self.n)
        x = (self.R + v_vals * np.cos(u_vals / 2)) * np.cos(u_vals)
        y = (self.R + v_vals * np.cos(u_vals / 2)) * np.sin(u_vals)
        z = v_vals * np.sin(u_vals / 2)
        return x, y, z

    def plot(self):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.x, self.y, self.z, rstride=1, cstride=1, color='skyblue', edgecolor='k', alpha=0.8)
        ax.set_title("Möbius Strip")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(elev=30, azim=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    mobius = MobiusStrip(R=1.0, w=0.4, n=300)
    print(f"Surface Area ≈ {mobius.surface_area():.4f}")
    print(f"Edge Length ≈ {mobius.edge_length():.4f}")
    mobius.plot()
