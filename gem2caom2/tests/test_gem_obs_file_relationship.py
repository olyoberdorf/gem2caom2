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

from datetime import datetime

from gem2caom2 import GemObsFileRelationship
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
        'GN-CAL20170616-11-022,2017-06-19T03:21:29.345417'), \
        'wrong content'
    assert len(list(temp)) == 500, 'wrong count'
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
        'GN-2018B-FT-113-24-015,2018-12-17T18:08:29.362826+00'), \
        'wrong content'
    assert len(list(temp)) == 98, 'wrong count'

    temp = gofr.subset(start=start, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GN-2018B-FT-113-24-015,2018-12-17T18:08:29.362826+00'), \
        'wrong content'
    assert len(list(temp)) == 3, 'wrong maxrec count'


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_subset_only_end():
    end = datetime.strptime('2018-12-16T18:12:26.16614', ISO_DATE)
    gofr = GemObsFileRelationship(TEST_FILE)
    temp = gofr.subset(end=end)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GN-CAL20170616-11-022,2017-06-19T03:21:29.345417+00'), \
        'wrong content'
    assert len(list(temp)) == 402, 'wrong count'

    temp = gofr.subset(end=end, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GN-CAL20170616-11-022,2017-06-19T03:21:29.345417+00'), \
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
        'GN-CAL20150925-2-007,2017-06-20T14:50:59.795755+00:00'), \
        'wrong content'
    assert len(list(temp)) == 306, 'wrong count'

    temp = test_subject.subset(start=start, end=end, maxrec=3)
    assert temp is not None, 'should have content'
    assert temp[0].startswith(
        'GN-CAL20150925-2-007,2017-06-20T14:50:59.795755+00:00'), \
        'wrong content'
    assert len(list(temp)) == 3, 'wrong maxrec count'


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_is_processed():
    tests = {
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
                'repair failed for {} got {} instead of {}'.format(
                    ii, test_result, test_main_app.LOOKUP[ii][0])
        else:
            assert test_result == test_main_app.LOOKUP[ii][0], \
                'repair failed for {} got {} instead of {}'.format(
                    ii, test_result, test_main_app.LOOKUP[ii][0])


test_subjects = [
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,1]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,1]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,1]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,1]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,1]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,2]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,2]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,2]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,2]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,2]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,3]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,3]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,3]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,3]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,3]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,4]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,4]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,4]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,4]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,4]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,5]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,5]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,5]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,5]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,5]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,6]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,6]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,6]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,6]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,6]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,7]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,7]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,7]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,7]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,7]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,8]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,8]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,8]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,8]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,8]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,9]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,9]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,9]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,9]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,9]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,10]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,10]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,10]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,10]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,10]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,11]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,11]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,11]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,11]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,11]'],
    ['S20141226S0203', 'GS-CAL20141226-7-026',
     'tmpfile22889S20141226S0203.fits[SCI,12]'],
    ['S20141226S0204', 'GS-CAL20141226-7-027',
     'tmpfile22889S20141226S0204.fits[SCI,12]'],
    ['S20141226S0205', 'GS-CAL20141226-7-028',
     'tmpfile22889S20141226S0205.fits[SCI,12]'],
    ['S20141226S0206', 'GS-CAL20141226-7-029',
     'tmpfile22889S20141226S0206.fits[SCI,12]'],
    ['S20141226S0207', 'GS-CAL20141226-7-030',
     'tmpfile22889S20141226S0207.fits[SCI,12]'],
    ['N20070819S0339', 'GN-2007B-Q-107-150-004',
     'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'GN-2007B-Q-107-150-005',
     'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'GN-2007B-Q-107-150-006',
     'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'GN-2007B-Q-107-150-007',
     'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'GN-2007B-Q-107-150-008',
     'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'GN-2007B-Q-107-150-009',
     'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'GN-2007B-Q-107-150-010',
     'N20070819S0345.fits[SCI,1]'],
    ['N20070819S0339', 'GN-2007B-Q-107-150-004',
     'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'GN-2007B-Q-107-150-005',
     'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'GN-2007B-Q-107-150-006',
     'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'GN-2007B-Q-107-150-007',
     'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'GN-2007B-Q-107-150-008',
     'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'GN-2007B-Q-107-150-009',
     'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'GN-2007B-Q-107-150-010',
     'N20070819S0345.fits[SCI,1]'],
    ['N20070819S0339', 'GN-2007B-Q-107-150-004',
     'N20070819S0339.fits[SCI,1]'],
    ['N20070819S0340', 'GN-2007B-Q-107-150-005',
     'N20070819S0340.fits[SCI,1]'],
    ['N20070819S0341', 'GN-2007B-Q-107-150-006',
     'N20070819S0341.fits[SCI,1]'],
    ['N20070819S0342', 'GN-2007B-Q-107-150-007',
     'N20070819S0342.fits[SCI,1]'],
    ['N20070819S0343', 'GN-2007B-Q-107-150-008',
     'N20070819S0343.fits[SCI,1]'],
    ['N20070819S0344', 'GN-2007B-Q-107-150-009',
     'N20070819S0344.fits[SCI,1]'],
    ['N20070819S0345', 'GN-2007B-Q-107-150-010',
     'N20070819S0345.fits[SCI,1]'],
    ['N20130404S0512', 'GN-2013A-Q-63-54-051',
     'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'GN-2013A-Q-63-54-052',
     'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'GN-2013A-Q-63-54-053',
     'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'GN-2013A-Q-63-54-054',
     'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'GN-2013A-Q-63-54-055',
     'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'GN-2013A-Q-63-54-056',
     'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'GN-2013A-Q-63-54-057',
     'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'GN-2013A-Q-63-54-058',
     'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'GN-2013A-Q-63-54-059',
     'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'GN-2013A-Q-63-54-060',
     'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20130404S0512', 'GN-2013A-Q-63-54-051',
     'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'GN-2013A-Q-63-54-052',
     'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'GN-2013A-Q-63-54-053',
     'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'GN-2013A-Q-63-54-054',
     'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'GN-2013A-Q-63-54-055',
     'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'GN-2013A-Q-63-54-056',
     'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'GN-2013A-Q-63-54-057',
     'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'GN-2013A-Q-63-54-058',
     'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'GN-2013A-Q-63-54-059',
     'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'GN-2013A-Q-63-54-060',
     'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20130404S0512', 'GN-2013A-Q-63-54-051',
     'tmp29851gemcombineN20130404S0512.fits[SCI,1]'],
    ['N20130404S0513', 'GN-2013A-Q-63-54-052',
     'tmp29851gemcombineN20130404S0513.fits[SCI,1]'],
    ['N20130404S0514', 'GN-2013A-Q-63-54-053',
     'tmp29851gemcombineN20130404S0514.fits[SCI,1]'],
    ['N20130404S0515', 'GN-2013A-Q-63-54-054',
     'tmp29851gemcombineN20130404S0515.fits[SCI,1]'],
    ['N20130404S0516', 'GN-2013A-Q-63-54-055',
     'tmp29851gemcombineN20130404S0516.fits[SCI,1]'],
    ['N20130404S0517', 'GN-2013A-Q-63-54-056',
     'tmp29851gemcombineN20130404S0517.fits[SCI,1]'],
    ['N20130404S0518', 'GN-2013A-Q-63-54-057',
     'tmp29851gemcombineN20130404S0518.fits[SCI,1]'],
    ['N20130404S0519', 'GN-2013A-Q-63-54-058',
     'tmp29851gemcombineN20130404S0519.fits[SCI,1]'],
    ['N20130404S0520', 'GN-2013A-Q-63-54-059',
     'tmp29851gemcombineN20130404S0520.fits[SCI,1]'],
    ['N20130404S0521', 'GN-2013A-Q-63-54-060',
     'tmp29851gemcombineN20130404S0521.fits[SCI,1]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,1]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,1]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,1]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,1]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,1]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,1]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,1]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,1]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,1]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,1]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,1]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,1]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,1]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,1]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,1]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,1]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,1]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,1]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,1]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,1]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,2]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,2]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,2]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,2]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,2]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,2]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,2]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,2]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,2]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,2]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,2]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,2]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,2]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,2]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,2]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,2]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,2]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,2]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,2]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,2]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,3]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,3]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,3]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,3]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,3]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,3]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,3]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,3]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,3]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,3]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,3]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,3]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,3]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,3]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,3]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,3]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,3]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,3]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,3]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,3]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,4]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,4]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,4]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,4]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,4]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,4]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,4]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,4]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,4]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,4]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,4]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,4]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,4]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,4]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,4]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,4]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,4]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,4]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,4]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,4]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,5]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,5]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,5]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,5]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,5]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,5]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,5]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,5]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,5]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,5]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,5]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,5]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,5]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,5]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,5]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,5]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,5]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,5]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,5]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,5]'],
    ['N20141109S0266', 'GN-CAL20141109-2-001',
     'tmpfile16849_1610gN20141109S0266.fits[SCI,6]'],
    ['N20141109S0267', 'GN-CAL20141109-2-002',
     'tmpfile16849_1610gN20141109S0267.fits[SCI,6]'],
    ['N20141109S0269', 'GN-CAL20141109-2-004',
     'tmpfile16849_1610gN20141109S0269.fits[SCI,6]'],
    ['N20141109S0268', 'GN-CAL20141109-2-003',
     'tmpfile16849_1610gN20141109S0268.fits[SCI,6]'],
    ['N20141109S0270', 'GN-CAL20141109-2-005',
     'tmpfile16849_1610gN20141109S0270.fits[SCI,6]'],
    ['N20141112S0002', 'GN-CAL20141111-1-002',
     'tmpfile16849_1610gN20141112S0002.fits[SCI,6]'],
    ['N20141112S0005', 'GN-CAL20141111-1-005',
     'tmpfile16849_1610gN20141112S0005.fits[SCI,6]'],
    ['N20141112S0001', 'GN-CAL20141111-1-001',
     'tmpfile16849_1610gN20141112S0001.fits[SCI,6]'],
    ['N20141112S0003', 'GN-CAL20141111-1-003',
     'tmpfile16849_1610gN20141112S0003.fits[SCI,6]'],
    ['N20141112S0004', 'GN-CAL20141111-1-004',
     'tmpfile16849_1610gN20141112S0004.fits[SCI,6]'],
    ['N20141112S0093', 'GN-CAL20141112-1-003',
     'tmpfile16849_1610gN20141112S0093.fits[SCI,6]'],
    ['N20141112S0091', 'GN-CAL20141112-1-001',
     'tmpfile16849_1610gN20141112S0091.fits[SCI,6]'],
    ['N20141112S0095', 'GN-CAL20141112-1-005',
     'tmpfile16849_1610gN20141112S0095.fits[SCI,6]'],
    ['N20141112S0092', 'GN-CAL20141112-1-002',
     'tmpfile16849_1610gN20141112S0092.fits[SCI,6]'],
    ['N20141112S0094', 'GN-CAL20141112-1-004',
     'tmpfile16849_1610gN20141112S0094.fits[SCI,6]'],
    ['N20141113S0115', 'GN-CAL20141113-5-001',
     'tmpfile16849_1610gN20141113S0115.fits[SCI,6]'],
    ['N20141113S0116', 'GN-CAL20141113-5-002',
     'tmpfile16849_1610gN20141113S0116.fits[SCI,6]'],
    ['N20141113S0118', 'GN-CAL20141113-5-004',
     'tmpfile16849_1610gN20141113S0118.fits[SCI,6]'],
    ['N20141113S0117', 'GN-CAL20141113-5-003',
     'tmpfile16849_1610gN20141113S0117.fits[SCI,6]'],
    ['N20141113S0119', 'GN-CAL20141113-5-005',
     'tmpfile16849_1610gN20141113S0119.fits[SCI,6]'],
    ['N20150804S0348', 'GN-2015B-Q-53-138-061',
     'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'GN-2015B-Q-53-138-062',
     'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'GN-2015B-Q-53-138-063',
     'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'GN-2015B-Q-53-138-064',
     'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'GN-2015B-Q-53-138-065',
     'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'GN-2015B-Q-53-138-066',
     'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'GN-2015B-Q-53-138-067',
     'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'GN-2015B-Q-53-138-068',
     'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'GN-2015B-Q-53-138-069',
     'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'GN-2015B-Q-53-138-070',
     'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20150804S0348', 'GN-2015B-Q-53-138-061',
     'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'GN-2015B-Q-53-138-062',
     'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'GN-2015B-Q-53-138-063',
     'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'GN-2015B-Q-53-138-064',
     'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'GN-2015B-Q-53-138-065',
     'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'GN-2015B-Q-53-138-066',
     'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'GN-2015B-Q-53-138-067',
     'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'GN-2015B-Q-53-138-068',
     'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'GN-2015B-Q-53-138-069',
     'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'GN-2015B-Q-53-138-070',
     'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20150804S0348', 'GN-2015B-Q-53-138-061',
     'tmp62119gemcombineN20150804S0348.fits[SCI,1]'],
    ['N20150804S0349', 'GN-2015B-Q-53-138-062',
     'tmp62119gemcombineN20150804S0349.fits[SCI,1]'],
    ['N20150804S0350', 'GN-2015B-Q-53-138-063',
     'tmp62119gemcombineN20150804S0350.fits[SCI,1]'],
    ['N20150804S0351', 'GN-2015B-Q-53-138-064',
     'tmp62119gemcombineN20150804S0351.fits[SCI,1]'],
    ['N20150804S0352', 'GN-2015B-Q-53-138-065',
     'tmp62119gemcombineN20150804S0352.fits[SCI,1]'],
    ['N20150804S0353', 'GN-2015B-Q-53-138-066',
     'tmp62119gemcombineN20150804S0353.fits[SCI,1]'],
    ['N20150804S0354', 'GN-2015B-Q-53-138-067',
     'tmp62119gemcombineN20150804S0354.fits[SCI,1]'],
    ['N20150804S0355', 'GN-2015B-Q-53-138-068',
     'tmp62119gemcombineN20150804S0355.fits[SCI,1]'],
    ['N20150804S0356', 'GN-2015B-Q-53-138-069',
     'tmp62119gemcombineN20150804S0356.fits[SCI,1]'],
    ['N20150804S0357', 'GN-2015B-Q-53-138-070',
     'tmp62119gemcombineN20150804S0357.fits[SCI,1]'],
    ['N20160403S0236', 'GN-CAL20160403-7-027',
     'rgN20160403S0236.fits[SCI,2]'],
    ['N20160403S0237', 'GN-CAL20160403-7-028',
     'rgN20160403S0237.fits[SCI,2]'],
    ['N20160403S0238', 'GN-CAL20160403-7-029',
     'rgN20160403S0238.fits[SCI,2]'],
    ['N20160403S0235', 'GN-CAL20160403-7-026',
     'rgN20160403S0235.fits[SCI,2]'],
    ['N20160403S0240', 'GN-CAL20160403-7-031',
     'rgN20160403S0240.fits[SCI,2]'],
    ['N20160403S0239', 'GN-CAL20160403-7-030',
     'rgN20160403S0239.fits[SCI,2]'],
    ['N20160403S0234', 'GN-CAL20160403-7-025',
     'rgN20160403S0234.fits[SCI,2]'],
    ['N20160403S0241', 'GN-CAL20160403-7-032',
     'rgN20160403S0241.fits[SCI,2]'],
    ['N20160403S0229', 'GN-CAL20160403-7-020',
     'rgN20160403S0229.fits[SCI,2]'],
    ['N20160403S0228', 'GN-CAL20160403-7-019',
     'rgN20160403S0228.fits[SCI,2]'],
    ['N20160403S0230', 'GN-CAL20160403-7-021',
     'rgN20160403S0230.fits[SCI,2]'],
    ['N20160403S0231', 'GN-CAL20160403-7-022',
     'rgN20160403S0231.fits[SCI,2]'],
    ['N20160403S0233', 'GN-CAL20160403-7-024',
     'rgN20160403S0233.fits[SCI,2]'],
    ['N20160403S0232', 'GN-CAL20160403-7-023',
     'rgN20160403S0232.fits[SCI,2]'],
    ['N20160404S0141', 'GN-CAL20160404-7-023',
     'rgN20160404S0141.fits[SCI,2]'],
    ['N20160404S0140', 'GN-CAL20160404-7-022',
     'rgN20160404S0140.fits[SCI,2]'],
    ['N20160404S0139', 'GN-CAL20160404-7-021',
     'rgN20160404S0139.fits[SCI,2]'],
    ['N20160404S0142', 'GN-CAL20160404-7-024',
     'rgN20160404S0142.fits[SCI,2]'],
    ['N20160404S0143', 'GN-CAL20160404-7-025',
     'rgN20160404S0143.fits[SCI,2]'],
    ['N20160404S0145', 'GN-CAL20160404-7-027',
     'rgN20160404S0145.fits[SCI,2]'],
    ['N20160404S0144', 'GN-CAL20160404-7-026',
     'rgN20160404S0144.fits[SCI,2]'],
    ['N20160404S0138', 'GN-CAL20160404-7-020',
     'rgN20160404S0138.fits[SCI,2]'],
    ['N20160404S0137', 'GN-CAL20160404-7-019',
     'rgN20160404S0137.fits[SCI,2]'],
    ['N20160404S0136', 'GN-CAL20160404-7-018',
     'rgN20160404S0136.fits[SCI,2]'],
    ['N20160404S0135', 'GN-CAL20160404-7-017',
     'rgN20160404S0135.fits[SCI,2]'],
    ['S20131007S0067', 'GS-2013B-Q-69-59-004',
     'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'GS-2013B-Q-69-59-005',
     'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'GS-2013B-Q-69-59-006',
     'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20131007S0067', 'GS-2013B-Q-69-59-004',
     'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'GS-2013B-Q-69-59-005',
     'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'GS-2013B-Q-69-59-006',
     'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20131007S0067', 'GS-2013B-Q-69-59-004',
     'tmp71808gemcombineS20131007S0067.fits[SCI,1]'],
    ['S20131007S0068', 'GS-2013B-Q-69-59-005',
     'tmp71808gemcombineS20131007S0068.fits[SCI,1]'],
    ['S20131007S0069', 'GS-2013B-Q-69-59-006',
     'tmp71808gemcombineS20131007S0069.fits[SCI,1]'],
    ['S20140124S0039', 'GS-2013B-Q-16-277-019',
     'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'GS-2013B-Q-16-277-020',
     'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'GS-2013B-Q-16-277-021',
     'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'GS-2013B-Q-16-277-022',
     'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'GS-2013B-Q-16-277-023',
     'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'GS-2013B-Q-16-277-024',
     'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20140124S0039', 'GS-2013B-Q-16-277-019',
     'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'GS-2013B-Q-16-277-020',
     'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'GS-2013B-Q-16-277-021',
     'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'GS-2013B-Q-16-277-022',
     'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'GS-2013B-Q-16-277-023',
     'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'GS-2013B-Q-16-277-024',
     'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20140124S0039', 'GS-2013B-Q-16-277-019',
     'tmp67553gemcombineS20140124S0039.fits[SCI,1]'],
    ['S20140124S0040', 'GS-2013B-Q-16-277-020',
     'tmp67553gemcombineS20140124S0040.fits[SCI,1]'],
    ['S20140124S0041', 'GS-2013B-Q-16-277-021',
     'tmp67553gemcombineS20140124S0041.fits[SCI,1]'],
    ['S20140124S0042', 'GS-2013B-Q-16-277-022',
     'tmp67553gemcombineS20140124S0042.fits[SCI,1]'],
    ['S20140124S0043', 'GS-2013B-Q-16-277-023',
     'tmp67553gemcombineS20140124S0043.fits[SCI,1]'],
    ['S20140124S0044', 'GS-2013B-Q-16-277-024',
     'tmp67553gemcombineS20140124S0044.fits[SCI,1]'],
    ['S20141129S0331', 'GS-CAL20141129-1-001',
     'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'GS-CAL20141129-1-002',
     'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'GS-CAL20141129-1-003',
     'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'GS-CAL20141129-1-004',
     'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'GS-CAL20141129-1-005',
     'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'GS-CAL20141129-1-006',
     'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'GS-CAL20141129-1-007',
     'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20141129S0331', 'GS-CAL20141129-1-001',
     'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'GS-CAL20141129-1-002',
     'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'GS-CAL20141129-1-003',
     'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'GS-CAL20141129-1-004',
     'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'GS-CAL20141129-1-005',
     'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'GS-CAL20141129-1-006',
     'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'GS-CAL20141129-1-007',
     'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20141129S0331', 'GS-CAL20141129-1-001',
     'tmp5862gemcombineS20141129S0331.fits[SCI,1]'],
    ['S20141129S0332', 'GS-CAL20141129-1-002',
     'tmp5862gemcombineS20141129S0332.fits[SCI,1]'],
    ['S20141129S0333', 'GS-CAL20141129-1-003',
     'tmp5862gemcombineS20141129S0333.fits[SCI,1]'],
    ['S20141129S0334', 'GS-CAL20141129-1-004',
     'tmp5862gemcombineS20141129S0334.fits[SCI,1]'],
    ['S20141129S0335', 'GS-CAL20141129-1-005',
     'tmp5862gemcombineS20141129S0335.fits[SCI,1]'],
    ['S20141129S0336', 'GS-CAL20141129-1-006',
     'tmp5862gemcombineS20141129S0336.fits[SCI,1]'],
    ['S20141129S0337', 'GS-CAL20141129-1-007',
     'tmp5862gemcombineS20141129S0337.fits[SCI,1]'],
    ['S20181219S0216', '', 'rgS20181219S0216[SCI,1]'],
    ['S20190301S0556', '',
     'tmpfile31966S20190301S0556.fits[SCI,1]'],
    ['S20041117S0073', 'GS-2004B-Q-42-1-001',
     'mfrgS20041117S0073_trn'],
    ['S20041117S0074', 'GS-2004B-Q-42-1-002',
     'mfrgS20041117S0074_trn'],
    ['S20160310S0154', 'GS-2016A-Q-7-175-001',
     'mfrgS20160310S0154_trn'],
    ['S20160310S0155', 'GS-2016A-Q-7-175-002',
     'mfrgS20160310S0155_trn'],
    ['S20160310S0156', 'GS-2016A-Q-7-175-003',
     'mfrgS20160310S0156_trn'],
    ['S20160310S0157', 'GS-2016A-Q-7-175-004',
     'mfrgS20160310S0157_trn'],
    ['S20160310S0158', 'GS-2016A-Q-7-175-005',
     'mfrgS20160310S0158_trn'],
    ['S20160310S0160', 'GS-2016A-Q-7-175-007',
     'mfrgS20160310S0160_trn'],
    ['N20160311S0691', 'GN-2016A-Q-68-46-001',
     'mrgN20160311S0691_trn'],
    ['N20160311S0692', 'GN-2016A-Q-68-46-002',
     'mrgN20160311S0692_trn'],
    ['N20160311S0693', 'GN-2016A-Q-68-46-003',
     'mrgN20160311S0693_trn'],
    ['N20160311S0694', 'GN-2016A-Q-68-46-004',
     'mrgN20160311S0694_trn'],
    ['S20160901S0122', 'GS-2016B-Q-72-23-001',
     'mrgS20160901S0122_trn'],
    ['S20160901S0123', 'GS-2016B-Q-72-23-002',
     'mrgS20160901S0123_trn'],
    ['S20160901S0124', 'GS-2016B-Q-72-23-003',
     'mrgS20160901S0124_trn'],
    ['S20160901S0125', 'GS-2016B-Q-72-23-004',
     'mrgS20160901S0125_trn']
]


@pytest.mark.skipif(single_test, reason='Single test mode')
def test_repair_provenance():
    if em.gofr is None:
        em.gofr = GemObsFileRelationship(TEST_FILE)
    for ii in test_subjects:
        test_result = _repair_provenance_value(ii[2], 'test obs')
        if ii[0] in ['S20181219S0216', 'S20190301S0556']:
            assert test_result is None
        else:
            assert test_result is not None, 'failed lookup {}'.format(ii)
            assert test_result[0] == ii[1], 'error {}'.format(ii[2])