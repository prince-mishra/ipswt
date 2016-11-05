import requests
from datetime import datetime
import traceback

from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from ipsaggregator.models import Shipment, ShipmentEvent

QUERY_URL = 'http://ipsweb.ptcmysore.gov.in/ipswebtracking/IPSWeb_item_events.asp?itemid=%s&Submit=Submit'

class Command(BaseCommand):
    help = 'For all open shipments, get current status'

    def handle(self, *args, **options):
        open_shipments = Shipment.objects.filter(processed = False)
        for s in open_shipments:
            identifier = s.identifier
            query_url = QUERY_URL % identifier
            r = requests.get(query_url, timeout=20)
            html_doc = r.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            tables = soup.find_all('table')
            try:
                events_table = tables[-1]
                rows = events_table.find_all('tr')[2:]

                for row in rows:
                    try:
                        cols = row.find_all('td')
                        event_time = datetime.strptime(cols[0].text.strip(), '%m/%d/%Y %I:%M:%S %p')
                        event_type = cols[3].text.strip()
                        row_obj = {
                            'shipment_id' : s.id,
                            'event_time' : event_time,
                            'country' : cols[1].text.strip(),
                            'location' : cols[2].text.strip(),
                            'event_type' : event_type,
                            'mail_category' : cols[4].text.strip(),
                            'next_office' : cols[5].text.strip(),
                            'extra_info_col1' : cols[6].text.strip(),
                            'extra_info_col2' : cols[7].text.strip(),
                        }
                        existing = ShipmentEvent.objects.filter(shipment_id = s.id, event_time = event_time)
                        if len(existing):
                            pass#self.stdout.write(self.style.ERROR(row_obj))
                        else:
                            ev = ShipmentEvent(**row_obj)
                            ev.save()
                            if 'Deliver item' in event_type:
                                s.processed = True
                                s.save()
                            #self.stdout.write(self.style.SUCCESS(row_obj))
                    except Exception, fault:
                        traceback.print_exc()
            except Exception, fault:
                print "Failed to sync shipment : %s" % s.identifier
                traceback.print_exc()



