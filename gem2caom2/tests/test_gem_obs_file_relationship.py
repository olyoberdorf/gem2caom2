# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2019.                            (c) 2019.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU Affero
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
# ***********************************************************************
#

import os
import pytest
import sys

from datetime import datetime

from gem2caom2 import GemObsFileRelationship, CommandLineBits
from gem2caom2.main_app import _repair_provenance_value
import gem2caom2.external_metadata as em

import test_main_app

ISO_DATE = '%Y-%m-%dT%H:%M:%S.%f'
PY_VERSION = '3.6'
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(THIS_DIR, 'data')
TEST_FILE = os.path.join(TEST_DATA_DIR, 'from_paul.txt')

single_test = False


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_subset_all():
    gofr = GemObsFileRelationship(TEST_FILE)
    temp = gofr.subset()
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-CAL20170616-11-022 2017-06-19T03:21:29.345'), \
        'wrong content'
    assert len(list(temp)) == 513, 'wrong count'
    result = gofr.get_file_names('GN-2015B-Q-1-12-1003')
    assert result == \
           ['N20150807G0044m.fits', 'N20150807G0044i.fits',
            'N20150807G0044.fits'], \
        'entry missing {}'.format(result)


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_subset_only_start():
    start = datetime.strptime('2018-12-16T03:47:03.939488', ISO_DATE)
    gofr = GemObsFileRelationship(TEST_FILE)
    temp = gofr.subset(start=start)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-2018B-FT-113-24-015 2018-12-17T18:08:29.362'), \
        'wrong content'
    assert len(list(temp)) == 97, 'wrong count'

    temp = gofr.subset(start=start, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-2018B-FT-113-24-015 2018-12-17T18:08:29.362'), \
        'wrong content'
    assert len(list(temp)) == 3, 'wrong maxrec count'


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_subset_only_end():
    end = datetime.strptime('2018-12-16T18:12:26.16614', ISO_DATE)
    gofr = GemObsFileRelationship(TEST_FILE)
    temp = gofr.subset(end=end)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-CAL20170616-11-022 2017-06-19T03:21:29.345'), \
        'wrong content'
    assert len(list(temp)) == 416, 'wrong count'

    temp = gofr.subset(end=end, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-CAL20170616-11-022 2017-06-19T03:21:29.345'), \
        'wrong content'
    assert len(list(temp)) == 3, 'wrong maxrec count'


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_subset_start_end():
    start = datetime.strptime('2017-06-20T12:36:35.681662', ISO_DATE)
    end = datetime.strptime('2017-12-17T20:13:56.572387', ISO_DATE)
    test_subject = GemObsFileRelationship(TEST_FILE)
    temp = test_subject.subset(start=start, end=end)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-CAL20150925-2-007 2017-06-20T14:50:59.795'), \
        'wrong content'
    assert len(list(temp)) == 314, 'wrong count'

    temp = test_subject.subset(start=start, end=end, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GEMINI GN-CAL20150925-2-007 2017-06-20T14:50:59.795'), \
        'wrong content'
    assert len(list(temp)) == 3, 'wrong maxrec count'


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_is_processed():
    tests = {
        'c2016may18_sci128': False,
        'abu01aug16_001': False,
        'ag2003feb19_6.0001': True,
        'TX06A_flt.2511': True,
        'GS20141226S0203_BIAS': True,
        'N20070819S0339_dark': True,
        'N20110927S0170_fringe': True,
        'N20120320S0328_stack_fringe': True,
        'N20130404S0512_flat': True,
        'N20140313S0072_flat': True,
        'N20141109S0266_bias': True,
        'N20150804S0348_dark': True,
        'N20160403S0236_flat_pasted': True,
        'S20120922S0406': False,
        'S20131007S0067_fringe': True,
        'S20140124S0039_dark': True,
        'S20141129S0331_dark': True,
        'S20161227S0051': False,
        'fmrgN20020413S0120_add': True,
        'gS20181219S0216_flat': True,
        'gS20190301S0556_bias': True,
        'mfrgS20041117S0073_add': True,
        'mfrgS20160310S0154_add': True,
        'mrgN20041016S0095': True,
        'mrgN20050831S0770_add': True,
        'mrgN20160311S0691_add': True,
        'mrgS20120922S0406': True,
        'mrgS20160901S0122_add': True,
        'mrgS20181016S0184_fringe': True,
        'rS20121030S0136': True,
        'rgS20100212S0301': True,
        'rgS20100316S0366': True,
        'rgS20130103S0098_FRINGE': True,
        'rgS20131109S0166_FRINGE': True,
        'rgS20161227S0051_fringe': True,
        'p2004may20_0048_FLAT': True,
        'p2004may19_0255_COMB': True,
        'P2003JAN14_0148_DARK': True,
        'P2002FEB03_0045_DARK10SEC': True,
        'P2002DEC02_0161_SUB': True,
        'P2002DEC02_0075_SUB.0001': True}
    for ii in tests:
        assert GemObsFileRelationship.is_processed(ii) == tests[ii], \
            'failed {}'.format(ii)


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_repair_data_label():
    if em.gofr is None:
        em.gofr = GemObsFileRelationship(TEST_FILE)
    for ii in test_main_app.LOOKUP:
        test_result = em.gofr.repair_data_label(ii)
        if ii == 'S20181230S0026':
            assert test_result == 'S20181230S0026', \
                'repair failed for {} actual {} expected {}'.format(
                    ii, test_result, test_main_app.LOOKUP[ii][0])
        else:
            assert test_result == test_main_app.LOOKUP[ii][0], \
                'repair failed for {} actual {} expected {}'.format(
                    ii, test_result, test_main_app.LOOKUP[ii][0])
    test_result = em.gofr.repair_data_label('N20181217S0266')
    assert test_result is not None, 'no result'
    assert test_result == 'GN-2018B-Q-133-20-001', 'wrong result'


test_subjects = [
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,1]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,1]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,1]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,1]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,1]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,2]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,2]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,2]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,2]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,2]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,3]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,3]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,3]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,3]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,3]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,4]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,4]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,4]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,4]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,4]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,5]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,5]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,5]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,5]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,5]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,6]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,6]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,6]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,6]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,6]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,7]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,7]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,7]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,7]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,7]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,8]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,8]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,8]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,8]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,8]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,9]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,9]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,9]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,9]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,9]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,10]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,10]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,10]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,10]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,10]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,11]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,11]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,11]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,11]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,11]'],
    ['S20141226S0203', 'tmpfile22889S20141226S0203.fits[SCI,12]'],
    ['S20141226S0204', 'tmpfile22889S20141226S0204.fits[SCI,12]'],
    ['S20141226S0205', 'tmpfile22889S20141226S0205.fits[SCI,12]'],
    ['S20141226S0206', 'tmpfile22889S20141226S0206.fits[SCI,12]'],
    ['S20141226S0207', 'tmpfile22889S20141226S0207.fits[SCI,12]'],
    ['N20070819S0339', 'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'N20070819S0345.fits[SCI,1]'],
    ['N20070819S0339', 'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'N20070819S0345.fits[SCI,1]'],
    ['N20070819S0339', 'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'N20070819S0345.fits[SCI,1]'],
    ['N20130404S0512', 'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20130404S0512', 'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20130404S0512', 'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,1]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,1]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,1]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,1]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,1]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,1]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,1]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,1]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,1]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,1]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,1]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,1]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,1]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,1]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,1]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,1]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,1]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,1]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,1]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,1]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,2]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,2]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,2]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,2]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,2]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,2]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,2]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,2]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,2]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,2]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,2]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,2]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,2]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,2]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,2]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,2]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,2]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,2]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,2]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,2]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,3]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,3]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,3]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,3]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,3]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,3]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,3]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,3]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,3]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,3]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,3]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,3]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,3]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,3]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,3]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,3]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,3]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,3]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,3]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,3]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,4]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,4]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,4]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,4]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,4]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,4]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,4]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,4]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,4]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,4]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,4]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,4]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,4]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,4]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,4]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,4]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,4]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,4]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,4]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,4]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,5]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,5]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,5]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,5]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,5]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,5]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,5]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,5]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,5]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,5]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,5]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,5]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,5]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,5]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,5]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,5]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,5]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,5]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,5]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,5]'],
    ['N20141109S0266', 'tmpfile16849_1610gN20141109S0266.fits[SCI,6]'],
    ['N20141109S0267', 'tmpfile16849_1610gN20141109S0267.fits[SCI,6]'],
    ['N20141109S0269', 'tmpfile16849_1610gN20141109S0269.fits[SCI,6]'],
    ['N20141109S0268', 'tmpfile16849_1610gN20141109S0268.fits[SCI,6]'],
    ['N20141109S0270', 'tmpfile16849_1610gN20141109S0270.fits[SCI,6]'],
    ['N20141112S0002', 'tmpfile16849_1610gN20141112S0002.fits[SCI,6]'],
    ['N20141112S0005', 'tmpfile16849_1610gN20141112S0005.fits[SCI,6]'],
    ['N20141112S0001', 'tmpfile16849_1610gN20141112S0001.fits[SCI,6]'],
    ['N20141112S0003', 'tmpfile16849_1610gN20141112S0003.fits[SCI,6]'],
    ['N20141112S0004', 'tmpfile16849_1610gN20141112S0004.fits[SCI,6]'],
    ['N20141112S0093', 'tmpfile16849_1610gN20141112S0093.fits[SCI,6]'],
    ['N20141112S0091', 'tmpfile16849_1610gN20141112S0091.fits[SCI,6]'],
    ['N20141112S0095', 'tmpfile16849_1610gN20141112S0095.fits[SCI,6]'],
    ['N20141112S0092', 'tmpfile16849_1610gN20141112S0092.fits[SCI,6]'],
    ['N20141112S0094', 'tmpfile16849_1610gN20141112S0094.fits[SCI,6]'],
    ['N20141113S0115', 'tmpfile16849_1610gN20141113S0115.fits[SCI,6]'],
    ['N20141113S0116', 'tmpfile16849_1610gN20141113S0116.fits[SCI,6]'],
    ['N20141113S0118', 'tmpfile16849_1610gN20141113S0118.fits[SCI,6]'],
    ['N20141113S0117', 'tmpfile16849_1610gN20141113S0117.fits[SCI,6]'],
    ['N20141113S0119', 'tmpfile16849_1610gN20141113S0119.fits[SCI,6]'],
    ['N20150804S0348', 'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20150804S0348', 'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20150804S0348', 'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20160403S0236', 'rgN20160403S0236.fits[SCI,2]'],
    ['N20160403S0237', 'rgN20160403S0237.fits[SCI,2]'],
    ['N20160403S0238', 'rgN20160403S0238.fits[SCI,2]'],
    ['N20160403S0235', 'rgN20160403S0235.fits[SCI,2]'],
    ['N20160403S0240', 'rgN20160403S0240.fits[SCI,2]'],
    ['N20160403S0239', 'rgN20160403S0239.fits[SCI,2]'],
    ['N20160403S0234', 'rgN20160403S0234.fits[SCI,2]'],
    ['N20160403S0241', 'rgN20160403S0241.fits[SCI,2]'],
    ['N20160403S0229', 'rgN20160403S0229.fits[SCI,2]'],
    ['N20160403S0228', 'rgN20160403S0228.fits[SCI,2]'],
    ['N20160403S0230', 'rgN20160403S0230.fits[SCI,2]'],
    ['N20160403S0231', 'rgN20160403S0231.fits[SCI,2]'],
    ['N20160403S0233', 'rgN20160403S0233.fits[SCI,2]'],
    ['N20160403S0232', 'rgN20160403S0232.fits[SCI,2]'],
    ['N20160404S0141', 'rgN20160404S0141.fits[SCI,2]'],
    ['N20160404S0140', 'rgN20160404S0140.fits[SCI,2]'],
    ['N20160404S0139', 'rgN20160404S0139.fits[SCI,2]'],
    ['N20160404S0142', 'rgN20160404S0142.fits[SCI,2]'],
    ['N20160404S0143', 'rgN20160404S0143.fits[SCI,2]'],
    ['N20160404S0145', 'rgN20160404S0145.fits[SCI,2]'],
    ['N20160404S0144', 'rgN20160404S0144.fits[SCI,2]'],
    ['N20160404S0138', 'rgN20160404S0138.fits[SCI,2]'],
    ['N20160404S0137', 'rgN20160404S0137.fits[SCI,2]'],
    ['N20160404S0136', 'rgN20160404S0136.fits[SCI,2]'],
    ['N20160404S0135', 'rgN20160404S0135.fits[SCI,2]'],
    ['S20131007S0067', 'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20131007S0067', 'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20131007S0067', 'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20140124S0039', 'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20140124S0039', 'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20140124S0039', 'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20141129S0331', 'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20141129S0331', 'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20141129S0331', 'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20181219S0216', 'rgS20181219S0216[SCI,1]'],
    ['S20190301S0556', 'tmpfile31966S20190301S0556.fits[SCI,1]'],
    ['S20041117S0073', 'mfrgS20041117S0073_trn'],
    ['S20041117S0074', 'mfrgS20041117S0074_trn'],
    ['S20160310S0154', 'mfrgS20160310S0154_trn'],
    ['S20160310S0155', 'mfrgS20160310S0155_trn'],
    ['S20160310S0156', 'mfrgS20160310S0156_trn'],
    ['S20160310S0157', 'mfrgS20160310S0157_trn'],
    ['S20160310S0158', 'mfrgS20160310S0158_trn'],
    ['S20160310S0160', 'mfrgS20160310S0160_trn'],
    ['N20160311S0691', 'mrgN20160311S0691_trn'],
    ['N20160311S0692', 'mrgN20160311S0692_trn'],
    ['N20160311S0693', 'mrgN20160311S0693_trn'],
    ['N20160311S0694', 'mrgN20160311S0694_trn'],
    ['S20160901S0122', 'mrgS20160901S0122_trn'],
    ['S20160901S0123', 'mrgS20160901S0123_trn'],
    ['S20160901S0124', 'mrgS20160901S0124_trn'],
    ['S20160901S0125', 'mrgS20160901S0125_trn']
]


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_repair_provenance():
    if em.gofr is None:
        em.gofr = GemObsFileRelationship(TEST_FILE)
    for ii in test_subjects:
        ignore, test_fid = _repair_provenance_value(ii[1], 'test obs')
        assert test_fid is not None, 'failed lookup {}'.format(ii)
        assert test_fid == ii[0], 'error {}'.format(ii[1])


y = 'https://archive.gemini.edu/fullheader/'
z = 'gemini:GEM/'
x = {
    'GS-2002B-Q-22-13-0161': [CommandLineBits(
        obs_id='GEMINI GS-2002B-Q-22-13-0161',
        urls='{}{} {}{} {}{}'.format(
            y, 'P2002DEC02_0161_SUB.0001.fits', y, 'P2002DEC02_0161_SUB.fits',
            y, '2002dec02_0161.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits {3}/{0}{3}.fits'.format(
            z, 'P2002DEC02_0161_SUB.0001', 'P2002DEC02_0161_SUB',
            '2002dec02_0161'))],
    'GN-2015B-Q-1-12-1003': [CommandLineBits(
        obs_id='GEMINI GN-2015B-Q-1-12-1003',
        urls='{0}{1} {0}{2} {0}{3}'.format(
            y, 'N20150807G0044m.fits', 'N20150807G0044i.fits',
            'N20150807G0044.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits {3}/{0}{3}.fits'.format(
            z, 'N20150807G0044m', 'N20150807G0044i', 'N20150807G0044'))],
    'GS-2010A-Q-36-5-246-RG': [CommandLineBits(
        obs_id='GEMINI GS-2010A-Q-36-5-246',
        urls='{}{}'.format(y, 'rgS20100212S0301.fits'),
        lineage='{0}/{1}{0}.fits'.format('rgS20100212S0301', z))],
    'GN-2002A-SV-78-7-003': [CommandLineBits(
        obs_id='GEMINI GN-2002A-SV-78-7-003-FMRG-ADD',
        urls='{}{}'.format(y, 'fmrgN20020413S0120_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'fmrgN20020413S0120_add'))],
    'GN-2004B-Q-30-1-001-MRG': [CommandLineBits(
        obs_id='GEMINI GN-2004B-Q-30-1-001',
        urls='{}{}'.format(y, 'mrgN20041016S0095.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mrgN20041016S0095'))],
    'GN-2005B-Q-28-32-001-MRG': [CommandLineBits(
        obs_id='GEMINI GN-2005B-Q-28-32-001-MRG-ADD',
        urls='{}{}'.format(y, 'mrgN20050831S0770_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mrgN20050831S0770_add'))],
    'GN-2007B-Q-107-150-004_DARK': [CommandLineBits(
        obs_id='GEMINI GN-2007B-Q-107-150-004-DARK',
        urls='{}{}'.format(y, 'N20070819S0339_dark.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20070819S0339_dark'))],
    'GN-2013A-Q-63-54-051_FLAT': [CommandLineBits(
        obs_id='GEMINI GN-2013A-Q-63-54-051-FLAT',
        urls='{}{}'.format(y, 'N20130404S0512_flat.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20130404S0512_flat'))],
    'GN-2013B-Q-75-163-011_STACK': [CommandLineBits(
        obs_id='GEMINI GN-2013B-Q-75-163-011-FLAT',
        urls='{}{}'.format(y, 'N20140313S0072_flat.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20140313S0072_flat'))],
    'GN-2015B-Q-53-138-061_STACK': [CommandLineBits(
        obs_id='GEMINI GN-2015B-Q-53-138-061-DARK',
        urls='{}{}'.format(y, 'N20150804S0348_dark.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20150804S0348_dark'))],
    'GN-2016A-Q-68-46-001-MRG-ADD': [CommandLineBits(
        obs_id='GEMINI GN-2016A-Q-68-46-001-MRG-ADD',
        urls='{}{}'.format(y, 'mrgN20160311S0691_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mrgN20160311S0691_add'))],
    'GN-CAL20110927-900-170': [CommandLineBits(
        obs_id='GEMINI GN-CAL20110927-900-170-FRINGE',
        urls='{}{}'.format(y, 'N20110927S0170_fringe.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20110927S0170_fringe'))],
    'GN-CAL20120320-900-328': [CommandLineBits(
        obs_id='GEMINI GN-CAL20120320-900-328-STACK-FRINGE',
        urls='{}{}'.format(y, 'N20120320S0328_stack_fringe.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'N20120320S0328_stack_fringe'))],
    'GN-CAL20141109-2-001-BIAS': [CommandLineBits(
        obs_id='GEMINI GN-CAL20141109-2-001-BIAS',
        urls='{0}{1} {0}{2}'.format(
            y, 'N20141109S0266_bias.fits', 'N20141109S0266_BIAS.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'N20141109S0266_bias', 'N20141109S0266_BIAS'))],
    'GN-CAL20160404-7-017-FLAT': [
        CommandLineBits(
            obs_id='GEMINI GN-CAL20160404-7-017-FLAT',
            urls='{0}{1}'.format(y, 'N20160403S0236_flat.fits'),
            lineage='{1}/{0}{1}.fits'.format(z, 'N20160403S0236_flat')),
        CommandLineBits(
            obs_id='GEMINI GN-CAL20160404-7-017-FLAT-PASTED',
            urls='{0}{1}'.format(y, 'N20160403S0236_flat_pasted.fits'),
            lineage='{1}/{0}{1}.fits'.format(z, 'N20160403S0236_flat_pasted'))
    ],
    'GS-2004A-Q-6-27-0255': [CommandLineBits(
        obs_id='GEMINI GS-2004A-Q-6-27-0255',
        urls='{}{}'.format(y, '2004may19_0255.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, '2004may19_0255'))],
    'GS-2004A-Q-6-27-0255-COMB-P': [CommandLineBits(
        obs_id='GEMINI GS-2004A-Q-6-27-0255-P-COMB',
        urls='{}{}'.format(y, 'p2004may19_0255_COMB.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'p2004may19_0255_COMB'))],
    'GS-2004B-Q-42-1-001': [CommandLineBits(
        obs_id='GEMINI GS-2004B-Q-42-1-001',
        urls='{0}{1} {0}{2}'.format(
            y, 'S20041117S0073.fits', 'rgS20041117S0073_FRINGE.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'S20041117S0073', 'rgS20041117S0073_FRINGE'))],
    'GS-2004B-Q-42-1-001-MFRG': [CommandLineBits(
        obs_id='GEMINI GS-2004B-Q-42-1-001-MFRG-ADD',
        urls='{}{}'.format(y, 'mfrgS20041117S0073_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mfrgS20041117S0073_add'))],
    'GS-2010A-Q-36-6-358-RG': [CommandLineBits(
        obs_id='GEMINI GS-2010A-Q-36-6-358',
        urls='{}{}'.format(y, 'rgS20100316S0366.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'rgS20100316S0366'))],
    'GS-2012B-Q-1-32-002-MRG': [CommandLineBits(
        obs_id='GEMINI GS-2012B-Q-1-32-002',
        urls='{0}{1} {0}{2}'.format(
            y, 'mrgS20120922S0406.fits', 'S20120922S0406.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'mrgS20120922S0406', 'S20120922S0406'))],
    'GS-2012B-Q-90-366-003-R': [CommandLineBits(
        obs_id='GEMINI GS-2012B-Q-90-366-003-R',
        urls='{}{}'.format(y, 'rS20121030S0136.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'rS20121030S0136'))],
    'GS-2013B-Q-16-277-019_STACK': [CommandLineBits(
        obs_id='GEMINI GS-2013B-Q-16-277-019-DARK',
        urls='{}{}'.format(y, 'S20140124S0039_dark.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'S20140124S0039_dark'))],
    'GS-2016A-Q-7-175-001-MFRG-ADD': [CommandLineBits(
        obs_id='GEMINI GS-2016A-Q-7-175-001-MFRG-ADD',
        urls='{}{}'.format(y, 'mfrgS20160310S0154_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mfrgS20160310S0154_add'))],
    'GS-2016B-Q-72-23-001-MRG-ADD': [CommandLineBits(
        obs_id='GEMINI GS-2016B-Q-72-23-001-MRG-ADD',
        urls='{}{}'.format(y, 'mrgS20160901S0122_add.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'mrgS20160901S0122_add'))],
    'GS-CAL20020203-4-0045': [CommandLineBits(
        obs_id='GEMINI GS-CAL20020203-4-0045',
        urls='{}{}'.format(y, 'P2002FEB03_0045_DARK10SEC.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'P2002FEB03_0045_DARK10SEC'))],
    'GS-CAL20021202-3-0075': [CommandLineBits(
        obs_id='GEMINI GS-CAL20021202-3-0075',
        urls='{0}{1} {0}{2}'.format(
            y, 'P2002DEC02_0075_SUB.0001.fits', '2002dec02_0075.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'P2002DEC02_0075_SUB.0001', '2002dec02_0075'))],
    'GS-CAL20030114-7-0148': [CommandLineBits(
        obs_id='GEMINI GS-CAL20030114-7-0148',
        urls='{}{}'.format(y, 'P2003JAN14_0148_DARK.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'P2003JAN14_0148_DARK'))],
    'GS-CAL20040520-7-0048-FLAT-P': [CommandLineBits(
        obs_id='GEMINI GS-CAL20040520-7-0048-P-FLAT',
        urls='{}{}'.format(y, 'p2004may20_0048_FLAT.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'p2004may20_0048_FLAT'))],
    'GS-CAL20130103-3-001': [CommandLineBits(
        obs_id='GEMINI GS-CAL20130103-3-001',
        urls='{0}{1} {0}{2}'.format(
            y, 'rgS20130103S0098_FRINGE.fits', 'S20130103S0098.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'rgS20130103S0098_FRINGE', 'S20130103S0098'))],
    'GS-CAL20131007-900-067': [CommandLineBits(
        obs_id='GEMINI GS-CAL20131007-900-067-FRINGE',
        urls='{}{}'.format(y, 'S20131007S0067_fringe.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'S20131007S0067_fringe'))],
    'GS-CAL20131109-17-001': [CommandLineBits(
        obs_id='GEMINI GS-CAL20131109-17-001',
        urls='{0}{1} {0}{2}'.format(
            y, 'rgS20131109S0166_FRINGE.fits', 'S20131109S0166.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'rgS20131109S0166_FRINGE', 'S20131109S0166'))],
    'GS-CAL20141129-1-001_DARK': [CommandLineBits(
        obs_id='GEMINI GS-CAL20141129-1-001-DARK',
        urls='{}{}'.format(y, 'S20141129S0331_dark.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'S20141129S0331_dark'))],
    'GS-CAL20141226-7-026-G-BIAS': [CommandLineBits(
        obs_id='GEMINI GS-CAL20141226-7-026-G-BIAS',
        urls='{}{}'.format(y, 'GS20141226S0203_BIAS.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'GS20141226S0203_BIAS'))],
    'GS-CAL20161227-5-001': [CommandLineBits(
        obs_id='GEMINI GS-CAL20161227-5-001',
        urls='{0}{1} {0}{2}'.format(
            y, 'S20161227S0051.fits', 'rgS20161227S0051_fringe.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'S20161227S0051', 'rgS20161227S0051_fringe'))],
    'GS-CAL20181016-5-001': [CommandLineBits(
        obs_id='GEMINI GS-CAL20181016-5-001',
        urls='{0}{1} {0}{2}'.format(
            y, 'mrgS20181016S0184_fringe.fits', 'S20181016S0184.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'mrgS20181016S0184_fringe', 'S20181016S0184'))],
    'GS-CAL20181219-4-021-G-FLAT': [CommandLineBits(
        obs_id='GEMINI GS-CAL20181219-4-021-G-FLAT',
        urls='{}{}'.format(y, 'gS20181219S0216_flat.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'gS20181219S0216_flat'))],
    'GS-CAL20190301-4-046-G-BIAS': [CommandLineBits(
        obs_id='GEMINI GS-CAL20190301-4-046-G-BIAS',
        urls='{}{}'.format(y, 'gS20190301S0556_bias.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'gS20190301S0556_bias'))],
    'TX20170321_flt.2505': [CommandLineBits(
        obs_id='GEMINI TX20170321_flt.2505',
        urls='{}{}'.format(y, 'TX20170321_flt.2505.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'TX20170321_flt.2505'))],
    'TX20170321_flt.2507': [CommandLineBits(
        obs_id='GEMINI TX20170321_flt.2507',
        urls='{}{}'.format(y, 'TX20170321_flt.2507.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'TX20170321_flt.2507'))],
    'TX20170321_raw.2505': [CommandLineBits(
        obs_id='GEMINI TX20170321.2505',
        urls='{0}{1} {0}{2} {0}{3}'.format(
            y, 'TX20170321_sum.2505.fits', 'TX20170321_raw.2505.fits',
            'TX20170321_red.2505.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits {3}/{0}{3}.fits'.format(
            z, 'TX20170321_sum.2505', 'TX20170321_raw.2505',
            'TX20170321_red.2505'))],
    'TX20170321_red.2507': [CommandLineBits(
        obs_id='GEMINI TX20170321.2507',
        urls='{0}{1} {0}{2}'.format(
            y, 'TX20170321_red.2507.fits', 'TX20170321_raw.2507.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'TX20170321_red.2507', 'TX20170321_raw.2507'))],
    'GS-2003A-Q-43-3-20001': [CommandLineBits(
        obs_id='GEMINI GS-2003A-Q-43-3-20001',
        urls='{0}{1} {0}{2}'.format(
            y, 'ag2003feb19_6.0001.fits', '2003feb19_6.0001.fits'),
        lineage='{1}/{0}{1}.fits {2}/{0}{2}.fits'.format(
            z, 'ag2003feb19_6.0001', '2003feb19_6.0001'))],
    'GS-CAL20150906-1-001-G-BIAS': [CommandLineBits(
        obs_id='GEMINI GS-CAL20150906-1-001-G-BIAS',
        urls='{0}{1}'.format(y, 'gS20150906S0222_bias.fits'),
        lineage='{1}/{0}{1}.fits'.format(z, 'gS20150906S0222_bias'))]
}


@pytest.mark.skipif(not sys.version.startswith(PY_VERSION),
                    reason='support 3.6 only')
def test_make_gem2caom2_args():
    gofr = GemObsFileRelationship('/app/data/from_paul.txt')

    for ii in x:
        test_result = gofr.get_args(ii)
        assert test_result is not None, 'no result'
        assert len(test_result) == len(x[ii]), \
            'wrong length for {}'.format(ii)
        for jj in test_result:
            found = False
            for kk in x[ii]:
                if jj.obs_id == kk.obs_id:
                    found = True
                    assert jj.lineage == kk.lineage, \
                        '{} lineage {} expected {}'.format(
                            jj.obs_id, jj.lineage, kk.lineage)
                    assert jj.urls == kk.urls, \
                        '{} urls {} expected {}'.format(jj.obs_id, jj.urls, kk.urls)
                    break
            assert found, 'new obs id {}'.format(jj.obs_id)


@pytest.mark.skipif(not sys.version.startswith(PY_VERSION),
                    reason='support 3.6 only')
def test_get_timestamp():
    gofr = GemObsFileRelationship('/app/data/from_paul.txt')
    test_result = gofr.get_timestamp('ag2003feb19_6.0001')
    assert test_result is not None, 'no result'
    assert test_result == 1498571069.924588, 'wrong result'
