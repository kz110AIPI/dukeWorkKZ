import json

# Load the JSON file with ordered image paths
with open('cnv_image_paths.json', 'r') as json_file:
    data = json.load(json_file)

# Start HTML content with centered title and two images per line
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shared CNV Analysis KZ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        h1 {
            text-align: center;
            width: 100%;
            margin-bottom: 20px;
        }
        .gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 1700px; /* Set max-width for two images per line */
        }
        .image-container {
            margin: 10px;
            border: 1px solid #ddd;
            padding: 10px;
            width: calc(50% - 40px); /* Two images per line with margin */
            box-sizing: border-box;
        }
        .image-container img {
            max-width: 100%;
            height: auto;
            display: block;
        }
    </style>
</head>
<body>
    <h1>Invasive and Noninvasive Shared CNV Analysis</h1>
    <div class="gallery">
"""

# Loop through each image in the JSON and add it to the HTML
for index, image_path in enumerate(data["images"], start=1):
    html_content += f"""
    <div class="image-container">
        <img src="{image_path}" alt="Image {index}">
    </div>
    """

# End HTML content
html_content += """
</body>
</html>
"""

# Write the HTML content to a file
with open('invasive-noninvasive_cnv_comaprision.html', 'w') as file:
    file.write(html_content)

print("HTML file created successfully.")
