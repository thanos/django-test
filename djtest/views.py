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
    def test_edit_form(self, edit_route, success_route, model_class, pk, **changed_fields):
        obj = model_class.objects.get(pk=pk)
        response = self.client.get(reverse( edit_route, kwargs={'pk': pk}))
        doc = pq(response.content)
        field_settings = dict([(pq(p).attr('name'), pq(p).val()) for p in doc("[name]")])
        field_settings.update(dict([(pq(p).attr('name'), pq(p).find("option:selected").val()) for p in doc("select")]))
        field_settings.update(changed_fields)
        response = self.client.post(reverse(edit_route, kwargs={'pk': pk}), field_settings)
        self.assertRedirects(response, reverse(success_route))
        obj = model_class.objects.get(pk=pk)
        for field in changed_fields:
            self.assertEqual(getattr(obj, field), changed_fields[field])
