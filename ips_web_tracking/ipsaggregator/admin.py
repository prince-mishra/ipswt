from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf.urls import include, url
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

# Register your models here.
from models import Shipment, ShipmentEvent

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'processed', 'created', 'modified', 'last_shipment_event', 'last_shipment_event_time', 'last_shipment_event_status')

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
                    Shipment.objects.create(identifier = i.strip())
          # for line in .split('\n'):
          #   print line#Foo.objects.create(myfield=line)
            return HttpResponseRedirect(reverse('admin:ipsaggregator_shipment_changelist'))
        return TemplateResponse(request, "admin/ipsaggregator/shipment/bulkupload.html", context)

    last_shipment_event.allow_tags = True


admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentEvent)