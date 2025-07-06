import csv
import os

# =============================================================
# ================= USER CONFIG ===============================
# =============================================================
input_csv = 'data/sorted_mock.csv' # Name of CSV File
output_dir = 'html_files'


# =============================================================
# ======= DO NOT EDIT UNDER THIS LINE =========================
# =============================================================
os.makedirs(output_dir, exist_ok=True)

# Templates
html_start = """
<column-set gutter="1.3rem">
  <column-unit slot="0" span="4">
    <h1>{gallery_name}</h1>
    <br>
        <br>
    WRITE A DESCRIPTION
  </column-unit>

  <column-unit slot="1" span="8">
    <div class="gallery-container">
      <div class="gallery">
"""

html_end = """
      </div>
    </div>
  </column-unit>
</column-set>
"""

image_template = """
        <div class="gallery-item">
          <img alt="{alt}" src="{src}">
        </div>
"""

video_template = """
        <div class="gallery-item">
          <video autoplay="" controls="" loop="" muted="" width="300">
            <source src="{src}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
"""

# Step 1: Group data by gallery name
galleries = {}
with open(input_csv, newline='', encoding='utf-8') as f:
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

# Step 2: Generate HTML per gallery
for gallery_name, items in galleries.items():
    # Sort by order number
    items.sort(key=lambda x: x['order'])

    # Start HTML
    html_content = html_start.format(gallery_name=gallery_name)

    # Add each media item
    for item in items:
        if item['ext'] in ['mp4', 'mov']:
            html_content += video_template.format(src=item['link'])
        else:
            html_content += image_template.format(alt=item['filename'], src=item['link'])

    html_content += html_end

    # Write to file
    filename = f"{gallery_name.replace(' ', '_')}.html"
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Generated: {filename}")
