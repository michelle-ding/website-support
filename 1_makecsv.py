from bs4 import BeautifulSoup
import os
import csv

# ====================================================================================
# ================ USER CONFIG =======================================================
# ====================================================================================
html_file_name = "test_html"      # Name of input HTML file (without .html)
csv_file_name = "image_links2"    # Desired output CSV filename (without .csv)



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
            # Expect filename format: GALLERY_ORD_NUM_NAME.ext
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

    print("✅ CSV file created successfully. Save this filepath:")
    print("==================================")
    print(csv_filepath)
    print("==================================")

write_csv(html_file_name, csv_file_name)
