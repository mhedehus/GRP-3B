import tempfile
import pandas as pd
from pydicom.data import get_testdata_files
import pydicom

from MR_classifier import classify_MR


def test_classify_on_a_sample_MR():
    dcm = pydicom.read_file(get_testdata_files()[0])
    dcm.SeriesDescription = 'T2W_FLAIR'
    with tempfile.TemporaryFile(suffix='.dcm') as fp:
        dcm.save_as(fp)
        dcm_metadata = {
            'modality': 'MR',
            'info': {'header': {'dicom':  {
                        "header": {
                            "dicom": {
                                "SeriesDescription": "T2W_FLAIR",
                                "Modality": "MR"
                            }
                        }
                    }
            }}}
        ipp = [[0, 0, a] for a in range(100)]
        iop = [[0, 0, 0] for a in range(100)]
        df = pd.DataFrame({'ImagePositionPatient': ipp, 'ImageOrientationPatient': iop})
        res = classify_MR(df, dcm, dcm_metadata)
        assert res['classification']['Intent'] == ['Structural']
        assert res['classification']['Measurement'] == ['T2']