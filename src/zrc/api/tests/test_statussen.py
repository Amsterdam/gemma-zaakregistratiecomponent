from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from zrc.datamodel.tests.factories import StatusFactory

from .utils import reverse


class StatusTests(APITestCase):
    @override_settings(
        LINK_FETCHER='zds_schema.mocks.link_fetcher_200',
        ZDS_CLIENT_CLASS='zds_schema.mocks.MockClient'
    )
    def test_filter_statussen_op_zaak(self):
        status1, status2 = StatusFactory.create_batch(2)
        assert status1.zaak != status2.zaak
        status1_url = reverse('status-detail', kwargs={'uuid': status1.uuid})
        status2_url = reverse('status-detail', kwargs={'uuid': status2.uuid})

        list_url = reverse('status-list')

        response = self.client.get(list_url, {
            'zaak': reverse('zaak-detail', kwargs={'uuid': status1.zaak.uuid})
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['url'],
            status1_url
        )
        self.assertNotEqual(
            response.data[0]['url'],
            status2_url
        )
