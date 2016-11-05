from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf.urls import include, url
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

# Register your models here.
from ipsaggregator.models import Shipment, ShipmentEvent


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'info', 'processed', 'last_shipment_event', 'last_shipment_event_time', 'last_shipment_event_status', 'all_events', 'external_link', 'created', 'modified')

    def last_shipment_event(self, obj):
        ret = ''
        last_shipment_event = ShipmentEvent.objects.filter(shipment_id = obj.id).order_by('-event_time')

        if last_shipment_event:
            idey = last_shipment_event[0].id
            ret = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % ('ipsaggregator', 'shipmentevent'), args = [idey]), idey
            )
        return ret

    def last_shipment_event_time(self, obj):
        ret = ''
        last_shipment_event = ShipmentEvent.objects.filter(shipment_id = obj.id).order_by('-event_time')
        if last_shipment_event:
            ret = last_shipment_event[0].event_time
        return ret

    def last_shipment_event_status(self, obj):
        ret = ''
        last_shipment_event = ShipmentEvent.objects.filter(shipment_id = obj.id).order_by('-event_time')
        if last_shipment_event:
            ret = last_shipment_event[0].event_type
        return ret

    def all_events(self, obj):
        event_count = ShipmentEvent.objects.filter(shipment_id = obj.id).count()

        return u'<a href="/admin/ipsaggregator/shipmentevent/?shipment__identifier=%s">%s</a>' % (obj.identifier, event_count)

    def external_link(self, obj):
        return u'<a href="http://ipsweb.ptcmysore.gov.in/ipswebtracking/IPSWeb_item_events.asp?itemid=%s&Submit=Submit" target="_blank">External</a>' % obj.identifier

    def get_urls(self):
        urls = super(ShipmentAdmin, self).get_urls()
        my_urls = [
            url(r'^bulkupload/$', self.admin_site.admin_view(self.bulk_upload))
        ]
        return my_urls + urls

    def bulk_upload(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
        )
        if request.method == 'POST':
            ids = request.POST['bulk-create-paste']
            for i in ids.split(','):
                cur = i.strip()
                if cur:
                    info = ''
                    splitted = cur.split('|')
                    identifier = splitted[0].strip()
                    if len(splitted) == 2:
                        info = splitted[1].strip()
                    Shipment.objects.create(identifier = identifier, info = info)
            return HttpResponseRedirect(reverse('admin:ipsaggregator_shipment_changelist'))
        return TemplateResponse(request, "admin/ipsaggregator/shipment/bulkupload.html", context)

    last_shipment_event.allow_tags = True
    all_events.allow_tags = True
    external_link.allow_tags = True

class ShipmentEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipment', 'event_time', 'country', 'location', 'event_type', 'mail_category', 'next_office', 'extra_info_col1', 'extra_info_col2', 'created', 'modified')
    list_filter = ('shipment__identifier',)
    ordering = ('event_time',)

admin.site.site_header = 'IPS Web Tracker'

admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentEvent, ShipmentEventAdmin)