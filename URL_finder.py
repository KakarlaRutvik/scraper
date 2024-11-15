import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# List of main URLs to scrape
import json

# List of main URLs to scrape (with college names)
urls = [
    ("Nagarjuna University", "https://www.nagarjunauniversity.ac.in/"),
    ("Angrau", "https://angrau.ac.in/"),
    ("AKNU", "https://aknu.edu.in/"),
    ("Akkiah University", "https://akuprakasam.ac.in/"),
    ("Andhra University", "https://www.andhrauniversity.edu.in/"),
    ("DSNLU", "https://dsnlu.ac.in/"),
    ("AHUUK", "https://ahuuk.ac.in/"),
    ("BRAOU", "https://www.braou.ac.in/"),
    ("Dr. NTR University of Health Sciences", "https://drntr.uhsap.in/index/index.html"),
    ("YSR Agricultural University", "https://www.ysrafu.ac.in/"),
    ("Dry SRHU", "https://drysrhu.ap.gov.in/"),
    ("Dravidian University", "https://www.dravidianuniversity.ac.in/"),
    ("JNTUA", "https://www.jntua.ac.in/"),
    ("JNTUK", "https://www.jntuk.edu.in/"),
    ("JNTUGV", "https://jntugv.edu.in/"),
    ("KR University", "https://kru.ac.in/"),
    ("RGUKT", "https://www.rgukt.in/"),
    ("Rayalaseema University", "https://www.rayalaseemauniversity.ac.in/"),
    ("SK University", "http://skuniversity.ac.in/"),
    ("SPMVV", "https://www.spmvv.ac.in/"),
    ("SVIMSTPT", "https://svimstpt.ap.nic.in/"),
    ("SV University", "https://svuniversity.edu.in/"),
    ("SV Vedic University", "https://www.svvedicuniversity.ac.in/"),
    ("SVVU", "https://www.svvu.edu.in/"),
    ("VSU", "https://vsu.ac.in/"),
    ("YVU", "https://yvu.edu.in/"),
    ("SRMAP", "https://srmap.edu.in/"),
    ("VITAP", "https://vitap.ac.in/"),
    ("CUTM", "https://cutm.ac.in/"),
    ("Best IU", "https://bestiu.edu.in/"),
    ("MBU", "https://www.mbu.asia/"),
    ("Amrita University", "https://www.amrita.edu/"),
    ("KL University", "https://www.kluniversity.in/"),
    ("SSSIHL", "https://www.sssihl.edu.in/"),
    ("Vignan University", "https://vignan.ac.in/newvignan/"),
    ("SAHE", "https://www.sahe.in/"),
    ("Aditya Tekkkali", "https://www.adityatekkali.edu.in/"),
    ("ANITS", "https://anits.edu.in/"),
    ("AITS Rajampet", "https://aitsrajampet.ac.in/"),
    ("AIET Guntur", "https://aietg.ac.in/"),
    ("BVCEC", "https://bvcec.edu.in/"),
    ("Chalapathi Engineering College", "https://chalapathiengg.ac.in/"),
    ("DIET", "https://diet.ac.in/"),
    ("MIC Tech", "https://www.mictech.edu.in/"),
    ("Gitam University", "https://www.gitam.edu/"),
    ("GVPEC", "https://www.gvpce.ac.in/"),
    ("GIET", "https://giet.ac.in/"),
    ("GPREC", "https://www.gprec.ac.in/"),
    ("GMRIT", "https://gmrit.edu.in/"),
    ("GEC Gudlavalleru", "https://www.gecgudlavalleru.ac.in/"),
    ("KRUCET", "https://krucet.ac.in/"),
    ("KSRMCE", "https://www.ksrmce.ac.in/"),
    ("LBRCE", "https://lbrce.ac.in/"),
    ("MITS", "https://mits.ac.in/"),
    ("MVGRCE", "https://mvgrce.com/"),
    ("NRTEC", "https://www.nrtec.in/"),
    ("NBKIST", "https://www.nbkrist.co.in/"),
    ("NRIIT", "https://nriit.edu.in/"),
    ("QIS", "https://qiscet.edu.in/qiscet/"),
    ("Raghu Engineering College", "https://www.raghuenggcollege.com/"),
    ("RGMCET", "https://www.rgmcet.edu.in/"),
    ("RVRJC", "https://rvrjcce.ac.in/"),
    ("SRKREC", "https://srkrec.edu.in/"),
    ("SVEC", "https://www.gecgudlavalleru.ac.in/"),
    ("Srisivani", "https://srisivani.com/"),
    ("SRivasavi Engineering College", "https://srivasaviengg.ac.in/"),
    ("SVPCET", "http://svpcet.org/"),
    ("SACET", "https://sacet.ac.in/"),
    ("SIETK", "https://www.sietk.org/"),
    ("VVIT", "https://vvitguntur.com/"),
    ("VRSiddhartha", "https://www.vrsiddhartha.ac.in/"),
    ("Vignan IIT", "https://vignaniit.edu.in/"),
    ("Vishnu University", "https://vishnu.edu.in/"),
    ("Quba College", "https://www.qubacollege.in/"),
    ("SVEC", "https://www.svec.education/"),
    ("Dr. BR Ambedkar College of Law", "https://www.drbrambedkarcollegeoflaw.com/"),
    ("SV College of Law", "http://www.svcollegeoflaw.com/"),
    ("Gitam School of Law", "https://www.gitam.edu/visakhapatnam/gitam-school-of-law"),
    ("KL University Law", "https://www.kluniversity.in/law/default.aspx"),
    ("NVPLaw College", "http://www.nvplawcollege.com/"),
    ("DSR Hindu College of Law", "https://dsrhinducollegeoflaw.com/"),
    ("SRKMLC", "https://www.srkmlcedu.in/"),
    ("ER Law College", "https://www.erlawcollege.com/"),
    ("IP College of Law", "http://www.ipcollegeoflaw.com/"),
    ("Anantha College of Law", "http://anantha.edu.in/trupathi/index.html"),
    ("SVDSiddhartha Law College", "https://www.svdsiddharthalawcollege.ac.in/"),
    ("Ambedkar Law College", "https://www.ambedkarlaw.edu.in/"),
    ("Vijayanagar Law College", "http://www.vijayanagarlaw.edu.in/"),
    ("VR Law College", "https://vrlaw.college/"),
    ("Guntur Medical College", "https://gunturmedicalcollege.edu.in/"),
    ("Kurnool Medical College", "https://www.kurnoolmedicalcollege.ac.in/"),
    ("Kadapa Medical College", "https://governmentmedicalcollegekadapa.edu.in/"),
    ("CUAP", "https://cuap.ac.in/"),
    ("CTUAP", "https://www.ctuap.ac.in/"),
    ("NSKTU", "https://nsktu.ac.in/"),
    ("AIIMS", "https://www.aiims.edu/index.php/en"),
    ("IIMA", "https://www.iima.ac.in/"),
    ("IITM", "https://www.iitm.ac.in/"),
    ("IIITDM", "https://www.iiitdm.ac.in/"),
    ("IIITS", "https://www.iiits.ac.in/"),
    ("IIPE", "https://iipe.ac.in/"),
    ("IISC", "https://iisc.ac.in/"),
    ("IMU Visakhapatnam", "https://www.imu.edu.in/imunew/visakhapatnam-campus"),
    ("NIT Andhra", "https://nitandhra.ac.in/main/"),
    ("NIO", "https://www.nio.res.in/"),
    ("SPAV", "https://www.spav.ac.in/"),
    ("NID", "https://www.nid.ac.in/"),
    ("ICIT", "https://www.icitirupati.in/"),
    ("IIFT", "https://www.iift.ac.in/iift/index.php"),
    ("IITTM", "https://www.iittm.ac.in/"),
    ("CTRI", "https://ctri.icar.gov.in/"),
    ("NACIN", "https://www.nacin.gov.in/"),
]

# Creating the dictionary to store the data
college_urls = {college_name: url for college_name, url in urls}

# Save the data to a JSON file
with open('university_colleges_urls.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(college_urls, jsonfile, ensure_ascii=False, indent=4)

print("The college URLs have been saved to 'university_colleges_urls.json'.")



# Open a CSV file to write the results
with open('university_page_urls.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["mainurl", "pageurls"])  # Header row

    # Loop through each main URL
    for main_url in urls:
        try:
            # Send a GET request to the main URL
            response = requests.get(main_url)
            response.raise_for_status()  # Check if the request was successful

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <a> tags with 'href' attribute
            links = []
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                # Create the full URL
                full_url = urljoin(main_url, link)
                links.append(full_url)

            # Write each link to the CSV file, associating it with the main URL
            for page_url in links:
                writer.writerow([main_url, page_url])

            print(f"Successfully processed {main_url}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to process {main_url}: {e}")

print("All URLs have been processed and saved to university_page_urls.csv.")
