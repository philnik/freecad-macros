import FreeCAD as App
import FreeCADGui as Gui
import Part
import math

# Create a new document
doc = App.newDocument("Impeller")

# Parameters
hub_radius = 10           # Radius of the hub (center)
hub_height = 10           # Height of the hub
blade_height = 15         # Height of each blade
blade_thickness = 2       # Thickness of the blades
outer_radius = 30         # Outer radius of the impeller
num_blades = 6           # Number of blades
blade_twist = 20         # Degrees of twist for blades
blade_length = outer_radius - hub_radius  # Blade length

# Create the hub (central cylinder)
hub = Part.makeCylinder(hub_radius, hub_height)

# Create blades
blades = []
angle_step = 360 / num_blades  # Angle increment per blade

for i in range(num_blades):
    # Define blade
    blade = Part.makeBox(blade_thickness, blade_length, blade_height)

    # Move blade to start from hub edge
    blade.translate(App.Vector(-blade_thickness / 2, hub_radius, 0))

    # Rotate blade around Z-axis to its correct position
    blade = blade.copy()  # Ensure transformations work properly
    blade.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), i * angle_step)

    # Twist blade slightly (optional)
    try:
        if blade_twist != 0:
            rot_matrix = App.MatrixRotation(App.Vector(1, 0, 0), blade_twist)
            blade = blade.transformGeometry(rot_matrix)
    except:
        pass

    blades.append(blade)

# Fuse all blades with the hub
impeller = hub
for blade in blades:
    impeller = impeller.fuse(blade)

# Add an outer shroud (optional)
shroud = Part.makeCylinder(outer_radius, 2)  # Thin shroud
shroud.translate(App.Vector(0, 0, hub_height + blade_height))  # Move on top

# Combine impeller and shroud
impeller = impeller.fuse(shroud)

# Add final object to FreeCAD
Part.show(impeller)
doc.recompute()

# Adjust view
Gui.activeDocument().activeView().viewAxometric()
Gui.SendMsgToActiveView("ViewFit")
