from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red

def draw_polygon(output_name="polygon.pdf", coords = [], fill_color=red):
    """Creates a PDF file with a red polygon drawn on it."""

    c = canvas.Canvas(output_name, pagesize=letter)

    # Set the fill color to fill_color
    c.setFillColor(fill_color)

    # Draw the polygon
    path = c.beginPath()
    path.moveTo(coords[0][0], coords[0][1])
    for x, y in coords[1:]:
        path.lineTo(x, y)
    path.lineTo(coords[0][0], coords[0][1])

    c.drawPath(path, fill=1)  # fill=1 means fill the path

    # Save the PDF file
    c.save()
    print(f"PDF file '{output_name}' created successfully with a polygon.")

if __name__ == "__main__":
    # Define the vertices of the polygon
    width, height = letter
    points = [
        (10, 10),
        (10, height - 50),
        (width - 50, height - 10),
        (width - 100, 50),
    ]

    draw_polygon(output_name = "output.pdf", coords = points, fill_color=red)
