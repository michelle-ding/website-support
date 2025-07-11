from bs4 import BeautifulSoup
import os
import csv

# ====================================================================================
# ================ EDIT: USER CONFIG =================================================
# ====================================================================================
csv_input_filepath = "data/input.csv" # Input csv filepath
csv_output_filepath = "data/output.csv"    # Desired output CSV filepath (without .csv)
output_dir = 'output_files' # Write name of folder you want HTML files to be generated in.
                          # Does not have to be an existing folder
                          
# ====================================================================================
# ======= DO NOT EDIT UNDER THIS LINE ================================================
# ====================================================================================

def write_csv(csv_input_filepath, csv_output_filepath):
    # ============== CSV DATA EXTRACTION =============
    data = []
    with open(csv_input_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url=row[0]
            filename = url.split('/')[-1]
            try:
                # Expect filename format: GALLERY_ORDNUM_NAME.ext
                name_parts = filename.split('_')
                galleryname = name_parts[0]
                ordernum = int(name_parts[1])
            except (IndexError, ValueError):
                # If format is unexpected, skip or default
                print(f"Skipping malformed filename: {filename}")
                continue
            data.append((galleryname, ordernum, filename, url))

    # ============== SORT =============
    data.sort(key=lambda x: (x[0], x[1]))  # Sort by galleryname then ordernum

    # ============== CSV WRITER =============
    with open(csv_output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gallery Name', 'Order Number', 'File Name', 'Link'])  # Header
        writer.writerows(data)

    print("✅ CSV file created successfully at this location:")
    print("==================================")
    print(csv_output_filepath)
    print("==================================")

def makehtml(csv_filepath, output_dir):
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
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Generated: {filename}")
        print("==================================")
        print(filepath)
        print("==================================")

write_csv(csv_input_filepath, csv_output_filepath)
makehtml(csv_output_filepath, output_dir)
