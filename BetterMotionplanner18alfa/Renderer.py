from pyglet.gl import *
import math as m

class Renderer():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.render_objects = {}
        self.circle_num_angles = 361

    """adds a new prmitive that is going to be rendered on screen id is name of the primitive. For example triangle1.
    Type is Point, Triangle, Quad or Circle
    vertices is a list of position for the vertices, where each point is a tuple. 
    If type is Circle then vertices only stores a list of the circle's center-point (tuple) and radius
    Vertices are given in counter-clockwise order"""
    def add_render_object(self, type, vertices, id, color):
        self.render_objects[id] = {}
        self.render_objects[id]["type"] = type
        if type == "Circle":
            # vertices always stores center-point as first element in list and radius as second element
            center = vertices[0]
            radius = vertices[1]
            #A circle has a center-point and radius
            self.render_objects[id]["vertices"] = [center]
            for i in range(self.circle_num_angles):
                self.render_objects[id]["vertices"].append((center[0]+m.cos(m.radians(i))*radius,
                                                            center[1]+m.sin(m.radians(i))*radius))
        elif type == "Quad":
            #A quad is rendered as two trangles where the diagonals are overlapping
            self.render_objects[id]["vertices"] = [vertices[0], vertices[1], vertices[2],
                                                   vertices[0], vertices[2], vertices[3]]
        else:
            self.render_objects[id]["vertices"] = vertices
        self.render_objects[id]["color"] = color

    def remove_render_object(self, id):
        if id in self.render_objects:
            del self.render_objects[id]
            return True
        else:
            return False

    def draw(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        for obj in self.render_objects.values():
            if obj["type"] == "Triangle" or obj["type"] == "Quad":
                glBegin(GL_TRIANGLES)
                for vertex in obj["vertices"]:
                    rgb = obj["color"]
                    glColor3f(rgb[0], rgb[1], rgb[2])
                    glVertex2f(vertex[0], vertex[1])
                glEnd()
            elif obj["type"] == "Circle":
                glBegin(GL_TRIANGLE_FAN)
                for vertex in obj["vertices"]:
                    rgb = obj["color"]
                    glColor3f(rgb[0], rgb[1], rgb[2])
                    glVertex2f(vertex[0], vertex[1])
                glEnd()
            elif obj["type"] == "Point":
                glPointSize(4)
                glBegin(GL_POINTS)
                for vertex in obj["vertices"]:
                    rgb = obj["color"]
                    glColor3f(rgb[0], rgb[1], rgb[2])
                    glVertex2f(vertex[0], vertex[1])
                glEnd()
            elif obj["type"] == "Line":
                glBegin(GL_LINES)
                for vertex in obj["vertices"]:
                    rgb = obj["color"]
                    glColor3f(rgb[0], rgb[1], rgb[2])
                    glVertex2f(vertex[0], vertex[1])
                glEnd()