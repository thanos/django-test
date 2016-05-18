# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# $Id$
#
#
# Developer: Thanos Vassilakis
# (c) RBCCM 2015
#

from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms import ValidationError
from django.test import TestCase
from pyquery import PyQuery as pq




class FormTests(TestCase):
    def test_edit_source(self, route_label, model_class, pk, **changed_fields):
        obj = model_class.objects.get(pk=pk)
        response = self.client.get(reverse( route_label, kwargs={'pk': pk}))
        doc = pq(response.content)
        field_settings = dict([(pq(p).attr('name'), pq(p).val()) for p in doc("[name]")])
        field_settings.update(dict([(pq(p).attr('name'), pq(p).find("option:selected").val()) for p in doc("select")]))
        field_settings.update(changed_fields)
        response = self.client.post(reverse(route_label, kwargs={'pk': pk}), field_settings)
        self.assertRedirects(response, reverse(route_label))
        obj = Source.objects.get(pk=pk)
        for field in changed_fields:
            self.assertEqual(getattr(field, obj), changed_fields)
