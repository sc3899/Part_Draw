from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red, blue

class Part:
    def __init__(self, name):
        self.name = name
        self.anchor_points = {}
        self.points = []

    def add_anchor_point(self, name, offset):
        if name not in self.anchor_points:
            self.anchor_points[name] = {"offset_point":offset}
        else:
            print("Overwriting point {0}".format(name))
            self.anchor_points[name] = {"offset_point":offset}

    def add_shape(self, points):
        self.points = points

class draw_it:
    def __init__(self, output_name):
        self.output_name = output_name
        self.canvas = canvas.Canvas(output_name, pagesize = letter)
        pass

    def draw_shapes_at(self, start_x, start_y, anchor_point_name, obj):
        # Draw the polygon
        path = self.canvas.beginPath()
        self.canvas.setLineWidth(.5)
        self.canvas.setDash([.1, 0, .1])

        anchor_point = obj["connection"]

    def draw_shape_at(self, start_x, start_y, obj):
        # Draw the polygon
        path = self.canvas.beginPath()
        self.canvas.setLineWidth(.5)
        self.canvas.setDash([.1, 0, .1])
        
        next_x = start_x + obj["connection"][0]["offset_point"]["x"]
        next_y = start_y + obj["connection"][0]["offset_point"]["y"]

        for connection_point in obj["connection"]:
            if "absolute_point" in connection_point:
                print("Absolute point exists as {}:({},{})".format(
                    connection_point["name"],
                    connection_point["absolute_point"]
                ))
            abs_x = next_x - connection_point["offset_point"]["x"]
            abs_y = next_y - connection_point["offset_point"]["y"]
            connection_point["absolute_point"] = (abs_x, abs_y)
            self.canvas.circle(abs_x, abs_y, 5, fill = 0)
            print(abs_x, abs_y)
        
        path = self.canvas.beginPath()
        path.moveTo(next_x, next_y)

        for x, y in obj["points"][1:]:
            next_x = next_x + x
            next_y = next_y + y
            path.lineTo(next_x, next_y)
            #print("({0},{1})".format(next_x, next_y))

        next_x = start_x + obj["connection"][0]["offset_point"]["x"]
        next_y = start_y + obj["connection"][0]["offset_point"]["y"]

        path.lineTo(next_x, next_y)
        self.canvas.drawPath(path, fill=0)  # fill=1 means fill the path
 
    def draw_end(self):
        # Save the PDF file
        self.canvas.save()
        print(f"PDF file '{self.output_name}' created successfully.")



if __name__ == "__main__":
    # Define the vertices of the polygon
    width, height = letter

    obj_list = [{"connection":[
                    {"name":"A1", 
                        "offset_point" : {"x": -10, "y" : -50 }},
                    {"name":"B1", 
                        "offset_point" : {"x": -25, "y" : -190 }},    
                        ],
                "points":[(0, 0), (0, 200), (50, 0), (0, -100),]},

                {"connection":[{"name":"A1", 
                        "offset_point" : {"x": -10, "y" : -10 }
                        }],
                "points":[(0, 0), (100, 0), (0, 20), (-100, 0),]}
           ]

    
    d = draw_it("output.pdf")
    sx = 100
    sy = 200

    for obj in obj_list:
        d.draw_shape_at( sx, sy, obj)
        for conn in obj["connection"]:
            x, y = conn["absolute_point"]
            print("Absolute point exists as {}:({},{})".format(
                    conn["name"], x, y)
                )
            sx += 50
            sy += 50
    d.draw_end()
    