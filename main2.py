from bs4 import BeautifulSoup
import os
import csv

# ====================================================================================
# ================ EDIT: USER CONFIG =================================================
# ====================================================================================
csv_input_filepath = "data/input.csv"       # Input csv filepath
csv_output_filepath = "data/output.csv"     # Desired output CSV filepath
output_dir = 'output_files'                 # Folder for generated HTML files
                          
# ====================================================================================
# ======= DO NOT EDIT UNDER THIS LINE ================================================
# ====================================================================================

def write_csv(csv_input_filepath, csv_output_filepath):
    data = []
    with open(csv_input_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url = row[0]
            filename = url.split('/')[-1]
            try:
                name_parts = filename.split('_')
                galleryname = name_parts[0]
                ordernum = int(name_parts[1])
            except (IndexError, ValueError):
                print(f"Skipping malformed filename: {filename}")
                continue
            data.append((galleryname, ordernum, filename, url))

    data.sort(key=lambda x: (x[0], x[1]))

    with open(csv_output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gallery Name', 'Order Number', 'File Name', 'Link'])
        writer.writerows(data)

    print("✅ CSV file created at:", csv_output_filepath)


def makehtml(csv_filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    html_template_start = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{gallery_name}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 1rem; }}
    .gallery-container {{ width: 100%; height: 75vh; overflow: hidden; display: flex; }}
    .gallery {{ display: flex; overflow-x: auto; overflow-y: hidden; height: 100%; scroll-snap-type: x mandatory; gap: 10px; padding-left: 10px; box-sizing: border-box; }}
    .gallery-item {{ flex-shrink: 0; scroll-snap-align: start; display: flex; flex-direction: column; height: 100%; max-width: 100%; }}
    .gallery-item video {{ height: 100%; width: auto; object-fit: cover; display: block; }}
    .gallery-item img {{ height: 100%; width: auto; object-fit: cover; display: block; }}
    .toggle-sound-btn {{ margin-top: 8px; width: 30px; height: 30px; cursor: pointer; background: transparent; border: 1px solid #ccc; border-radius: 4px; font-size: 0; }}
  </style>
</head>
<body>

<column-set gutter="1.3rem">
  <column-unit slot="0" span="4">
    <h1>{gallery_name}</h1>
    <br><br>
    WRITE A DESCRIPTION
  </column-unit>
  <column-unit slot="1" span="8">
    <div class="gallery-container">
      <div class="gallery">
"""

    html_template_end = """
      </div>
    </div>
  </column-unit>
</column-set>

<script>
  document.querySelectorAll('.gallery-item video').forEach(video => {
    video.muted = true;
    const btn = document.createElement('button');
    btn.className = 'toggle-sound-btn';
    video.parentNode.appendChild(btn);
    btn.addEventListener('click', () => {
      video.muted = !video.muted;
    });
  });
</script>

</body>
</html>"""

    image_template = """
        <div class="gallery-item">
          <img alt="{alt}" src="{src}">
        </div>
    """

    video_template = """
        <div class="gallery-item">
          <video autoplay controls loop muted width="300">
            <source src="{src}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
    """

    # Group CSV rows by gallery
    galleries = {}
    with open(csv_filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gallery = row['Gallery Name']
            order = int(row['Order Number'])
            filename = row['File Name']
            link = row['Link']
            ext = filename.lower().split('.')[-1]
            if gallery not in galleries:
                galleries[gallery] = []
            galleries[gallery].append({
                'order': order,
                'filename': filename,
                'link': link,
                'ext': ext
            })

    # Generate HTML per gallery
    for gallery_name, items in galleries.items():
        items.sort(key=lambda x: x['order'])
        html_content = html_template_start.format(gallery_name=gallery_name)

        for item in items:
            if item['ext'] in ['mp4', 'mov']:
                html_content += video_template.format(src=item['link'])
            else:
                html_content += image_template.format(alt=item['filename'], src=item['link'])

        html_content += html_template_end
        filename = f"{gallery_name.replace(' ', '_')}.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Generated: {filepath}")

# Run the full pipeline
write_csv(csv_input_filepath, csv_output_filepath)
makehtml(csv_output_filepath, output_dir)
