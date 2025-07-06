from bs4 import BeautifulSoup
import os
import csv

# ====================================================================================
# ================ EDIT: USER CONFIG =================================================
# ====================================================================================
html_file_name = "test_html"      # Name of source HTML file (without .html)
csv_file_name = "image_links_csv"    # Desired output CSV filename (without .csv)
output_dir = 'output_files' # Write name of folder you want HTML files to be generated in.
                          # Does not have to be an existing folder
                          
# ====================================================================================
# ======= DO NOT EDIT UNDER THIS LINE ================================================
# ====================================================================================

def write_csv(html_filename, csv_filename):
    # ======== HTML PARSER ===============
    html_filepath = "html_files/" + html_filename + ".html"

    with open(html_filepath, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # ============== CSV DATA EXTRACTION =============
    data = []
    for tag in soup.find_all('a', href=True):
        url = tag['href']
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
    csv_filepath = "data/" + csv_filename + ".csv"
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['galleryname', 'ordernum', 'filename', 'url'])  # Header
        writer.writerows(data)

    print("✅ CSV file created successfully at this location:")
    print("==================================")
    print(csv_filepath)
    print("==================================")
    return csv_filepath

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
        return filepath

csv_filepath = write_csv(html_file_name, csv_file_name)
makehtml(csv_filepath, output_dir)
