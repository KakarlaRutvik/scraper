import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# List of main URLs to scrape
urls = [
    "https://www.nagarjunauniversity.ac.in/",
    "https://angrau.ac.in/",
    "https://aknu.edu.in/",
    "https://akuprakasam.ac.in/",
    "https://www.andhrauniversity.edu.in/",
    "https://dsnlu.ac.in/",
    "https://ahuuk.ac.in/",
    "https://www.braou.ac.in/",
    "https://drntr.uhsap.in/index/index.html",
    "https://www.ysrafu.ac.in/",
    "https://drysrhu.ap.gov.in/",
    "https://www.dravidianuniversity.ac.in/",
    "https://www.jntua.ac.in/",
    "https://www.jntuk.edu.in/",
    "https://jntugv.edu.in/",
    "https://kru.ac.in/",
    "https://www.rgukt.in/",
    "https://www.rayalaseemauniversity.ac.in/",
    "http://skuniversity.ac.in/",
    "https://www.spmvv.ac.in/",
    "https://svimstpt.ap.nic.in/",
    "https://svuniversity.edu.in/",
    "https://www.svvedicuniversity.ac.in/",
    "https://www.svvu.edu.in/",
    "https://vsu.ac.in/",
    "https://yvu.edu.in/",
    "https://srmap.edu.in/",
    "https://vitap.ac.in/",
    "https://cutm.ac.in/",
    "https://bestiu.edu.in/",
    "https://www.mbu.asia/",
    "https://www.amrita.edu/",
    "https://www.kluniversity.in/",
    "https://www.sssihl.edu.in/",
    "https://vignan.ac.in/newvignan/",
    "https://www.sahe.in/",
    "https://www.adityatekkali.edu.in/",
    "https://anits.edu.in/",
    "https://aitsrajampet.ac.in/",
    "https://aietg.ac.in/",
    "https://bvcec.edu.in/",
    "https://chalapathiengg.ac.in/",
    "https://diet.ac.in/",
    "https://www.mictech.edu.in/",
    "https://www.gitam.edu/",
    "https://www.gvpce.ac.in/",
    "https://giet.ac.in/",
    "https://www.gprec.ac.in/",
    "https://gmrit.edu.in/",
    "https://www.gecgudlavalleru.ac.in/",
    "https://krucet.ac.in/",
    "https://www.ksrmce.ac.in/",
    "https://lbrce.ac.in/",
    "https://mits.ac.in/",
    "https://mvgrce.com/",
    "https://www.nrtec.in/",
    "https://www.nbkrist.co.in/",
    "https://nriit.edu.in/",
    "https://qiscet.edu.in/qiscet/",
    "https://www.raghuenggcollege.com/",
    "https://www.rgmcet.edu.in/",
    "https://rvrjcce.ac.in/",
    "https://srkrec.edu.in/",
    "https://www.gecgudlavalleru.ac.in/",
    "https://www.svec.education/",
    "https://srisivani.com/",
    "https://srivasaviengg.ac.in/",
    "http://svpcet.org/",
    "https://sacet.ac.in/",
    "https://www.sietk.org/",
    "https://vvitguntur.com/",
    "https://www.vrsiddhartha.ac.in/",
    "https://vignaniit.edu.in/",
    "https://vishnu.edu.in/",
    "https://www.qubacollege.in/",
    "https://www.svec.education/",
    "https://www.drbrambedkarcollegeoflaw.com/",
    "https://www.nagarjunauniversity.ac.in/",
    "https://dsnlu.ac.in/",
    "http://www.svcollegeoflaw.com/",
    "https://www.gitam.edu/visakhapatnam/gitam-school-of-law",
    "https://www.kluniversity.in/law/default.aspx",
    "http://www.nvplawcollege.com/",
    "https://dsrhinducollegeoflaw.com/",
    "https://www.srkmlcedu.in/",
    "https://www.erlawcollege.com/",
    "http://www.ipcollegeoflaw.com/",
    "http://anantha.edu.in/trupathi/index.html",
    "https://www.svdsiddharthalawcollege.ac.in/",
    "https://www.ambedkarlaw.edu.in/",
    "http://www.vijayanagarlaw.edu.in/",
    "https://vrlaw.college/",
    "https://gunturmedicalcollege.edu.in/",
    "https://www.kurnoolmedicalcollege.ac.in/",
    "https://governmentmedicalcollegekadapa.edu.in/",
    "https://cuap.ac.in/",
    "https://www.ctuap.ac.in/",
    "https://nsktu.ac.in/",
    "https://www.aiims.edu/index.php/en",
    "https://www.iima.ac.in/",
    "https://www.iitm.ac.in/",
    "https://www.iiitdm.ac.in/",
    "https://www.iiits.ac.in/",
    "https://iipe.ac.in/",
    "https://iisc.ac.in/",
    "https://www.imu.edu.in/imunew/visakhapatnam-campus",
    "https://nitandhra.ac.in/main/",
    "https://www.nio.res.in/",
    "https://www.spav.ac.in/",
    "https://www.nid.ac.in/",
    "https://www.icitirupati.in/",
    "https://www.iift.ac.in/iift/index.php",
    "https://www.iittm.ac.in/",
    "https://ctri.icar.gov.in/",
    "https://www.nacin.gov.in/"
]


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
