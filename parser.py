import requests
from bs4 import BeautifulSoup as bs

url = r"https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaMIBiAEBmAExuAEXyAEU2AEB6AEB-" \
          r"AECiAIBqAID&lang=en-us&sid=5d7b54b0d5bd32212aa9dc4e7a3e3de2&sb=1&src=searchresults&src_elem=sb&error_url=" \
          r"https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaMIBiAEBmAExuAEX" \
          r"yAEU2AEB6AEB-AECiAIBqAID%3Bsid%3D5d7b54b0d5bd32212aa9dc4e7a3e3de2%3Bac_click_type%3Db%3Bac_position%3D0%3B" \
          r"checkin_month%3D11%3Bcheckin_monthday%3D19%3Bcheckin_year%3D2018%3Bcheckout_month%3D11%3Bcheckout_monthday" \
          r"%3D21%3Bcheckout_year%3D2018%3Bclass_interval%3D1%3Bdest_id%3D-2980155%3Bdest_type%3Dcity%3Bfrom_sf%3D1%3B" \
          r"group_adults%3D2%3Bgroup_children%3D0%3Biata%3DPEE%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Braw" \
          r"_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_" \
          r"r_match%3D0%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bsrpvid%3De4987a346a3301eb%3Bss%3DPerm%252C%2520Perm%2520" \
          r"Krai%2520%252C%2520Russia%3Bss_raw%3D%25D0%259F%25D0%25B5%25D1%2580%25D0%25BC%3Bssb%3Dempty%26%3B&ss=Perm" \
          r"&is_ski_area=0&ssne=Perm&ssne_untouched=Perm&city=-2980155&checkin_month=11&checkin_monthday=28&checkin_" \
          r"year=2018&checkout_month=11&checkout_monthday=30&checkout_year=2018&group_adults=2&group_children=0&" \
          r"no_rooms=1&from_sf=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}
end = True
while end:

    r = requests.get(url, headers=headers)
    soup = bs(r.content, 'html.parser')

    cards = soup.find_all('div', class_='sr_item_content')
    i = 0
    for card in cards:
        i += 1
        name = card.find('span', class_='sr-hotel__name').get_text().strip()
        print(name)
        price = card.find('strong', class_='price')
        if price:
            print(price.get_text().strip())

    nextUrl = soup.find('a', class_='paging-next')
    if nextUrl:
        url = "https://www.booking.com" + nextUrl['href']
    else:
        end = False

