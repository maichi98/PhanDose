# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 19:25:15 2024
@author: Diallo
"""
#-----------------------------------------------------------------------------------------------------------------------------------------------------
import os
import pickle
import numpy as np
import pandas as pd
import copy
from shapely import geometry
from datetime import datetime
from statistics import mode
import warnings
warnings.filterwarnings("ignore")
start_time = datetime.now()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------
Projet = os.path.normpath('C:\DUYEN\TO_MOHAMED')
RDFolders = [x[0] for x in os.walk(Projet) if os.path.basename(os.path.normpath(x[0]))=='RTDOSE']
#-----------------------------------------------------------------------------------------------------------------------------------------------------
ROIVolumeConsistency_df = pd.DataFrame()
for RDFolder in RDFolders:
    NEWDOSIFOLDER = os.path.join(os.path.dirname(RDFolder), 'NEWDOSI')
    print(NEWDOSIFOLDER)
    if not os.path.exists(NEWDOSIFOLDER):
        os.makedirs(NEWDOSIFOLDER)
    else:
        files_in_dir = os.listdir(NEWDOSIFOLDER)
        for fid in files_in_dir:
            os.remove(f'{NEWDOSIFOLDER}/{fid}')
    RD_Files = []
    RS_Files = []
    for path, subdirs, files in os.walk(os.path.dirname(RDFolder)):
        for file in files:
            if (file.startswith('RTSTRUCT') & file.endswith('.txt')):
                RS_Files = RS_Files + [os.path.join(path, file)]
            if (file.startswith('RTDOSE') & file.endswith('.txt')):
                RD_Files = RD_Files + [os.path.join(path, file)]
    for rd in RD_Files:
        print(rd)
        rrd = str(os.path.basename(os.path.normpath(rd)))
        RTDose = pd.read_csv(rd, encoding = "ISO-8859-1", sep='\t',header=0)
        RTDose['Z'] = RTDose['Z'].round(1)
        Vars = RTDose.columns.tolist()
        ListRTDosex  = sorted(RTDose['X'].unique().tolist())
        ListXDiff =  [t - s for s, t in zip(ListRTDosex, ListRTDosex[1:])]
        ListXDiff = [round(e, 1) for e in ListXDiff]
        ListRTDosey  = sorted(RTDose['Y'].unique().tolist())
        ListYDiff =  [t - s for s, t in zip(ListRTDosey, ListRTDosey[1:])]
        ListYDiff = [round(e, 1) for e in ListYDiff]
        ListRTDosez  = sorted(RTDose['Z'].unique().tolist())
        ListZDiff =  [t - s for s, t in zip(ListRTDosez, ListRTDosez[1:])]
        ListZDiff = [round(e, 1) for e in ListZDiff]
        for rs in RS_Files:
            print(rs)
            #----------------------------------------------------------------------------
            rrs = str(os.path.basename(os.path.normpath(rs)))
            NewDosiName = rrd[:rrd.find('.txt')] + '_' + rrs[:rrs.find('.txt')] + '_.NewDosi'
            #----------------------------------------------------------------------------
            RTStruct = pd.read_csv(rs, encoding = "ISO-8859-1", sep='\t', header=0)
#            ListRTROIInterpretedType = RTStruct['RTROIInterpretedType'].unique().tolist()
            RTStruct['z'] = RTStruct['z'].round(1)
            #------------------------------------------------------------------------------------------------------------------------
            ListZRTStruct = sorted(RTStruct['z'].unique().tolist())
            ListZDiff =  [t - s for s, t in zip(ListZRTStruct, ListZRTStruct[1:])]
            ListZDiff = [round(e, 1) for e in ListZDiff]
            SliceThickness = mode(ListZDiff)
            ListZExpectedFull = list(np.arange(RTStruct['z'].min(), RTStruct['z'].max() + SliceThickness, SliceThickness, dtype=float))
            ListZExpectedFull = [round(e, 1) for e in ListZExpectedFull]
            #----------------------------------------------------------------------------
            # Selection of rois of interest
            RTStruct = RTStruct[RTStruct['RTROIInterpretedType'] == 'ORGAN']
            ListRTROIInterpretedType = RTStruct['RTROIInterpretedType'].unique().tolist()
            Contours = RTStruct[RTStruct['ROIName'].isin(['Heart', 'Lung_left', 'Lung_right'])]
            ListROIs = sorted(Contours['ROIName'].unique().tolist())
            print(ListRTROIInterpretedType)
            print(ListROIs)
            #----------------------------------------------------------------------------
            Dict_of_df = {}
            for roiname in ListROIs:
                key_name = str(roiname)
                columnsNames= Vars + [roiname]
                Dict_of_df[key_name] = copy.deepcopy(pd.DataFrame(columns = columnsNames))
            for r in ListROIs:
                Roi_df = pd.DataFrame()
                roi = Contours[Contours['ROIName'] == r]
                RoiVolume = 0
                OrganVolumeInDoseMatrix = 0
                ListZDisired = sorted([e for e in ListZExpectedFull if (roi['z'].min() <= e and e <= roi['z'].max())])
                ListZDisired = [round(e, 1) for e in ListZDisired]
                ListZroi = sorted(roi['z'].unique().tolist())
                ListZDiffroi =  [t - s for s, t in zip(ListZroi, ListZroi[1:])]
                ListZDiffroi = [round(e, 1) for e in ListZDiffroi]
                ListZDiffUniqueroi = list(set(ListZDiffroi))
                for zr in ListZDisired:
                    roi['Ecart'] = abs(roi['z'] - zr).round(1)
                    EcartMin = round(roi['Ecart'].min(), 1)
                    roi_at_z = roi[roi['Ecart']==EcartMin]
                    roi_at_z['z'] = round(zr, 1)
                    ListROIContourIndex = sorted(roi_at_z['ROIContourIndex'].unique().tolist())
                    for c in ListROIContourIndex:
                        Contour = roi_at_z[roi_at_z['ROIContourIndex'] == c]
                        Contour['Polygone'] = Contour[['x','y']].apply(tuple, axis=1)
                        if len(Contour['Polygone'].unique().tolist()) >= 4:
                            Polygone = geometry.Polygon(Contour['Polygone'].unique().tolist())
                            RoiVolume = RoiVolume + (Polygone.area * mode(ListZDiff))/1000
                        # DOSES -----------------------------------------------------------------------------------------
                        ListRDdz = [abs(x-zr) for x in ListRTDosez]
                        ListRDdz = [round(e, 1) for e in ListRDdz]
                        dzmin = min(ListRDdz)
                        z0 = ListRTDosez[ListRDdz.index(dzmin)]
                        df0 = RTDose[RTDose['Z']==z0]
                        df0['Z'] = round(zr, 1)
                        df0['point'] = df0[['X','Y']].apply(tuple, axis=1)
                        contains = np.vectorize(lambda p: int(Polygone.contains(geometry.Point(p))), signature='(n)->()')
                        ListPoints = df0['point'].tolist()
                        Contient = contains(np.array(ListPoints))
                        df0[r] = Contient
                        # --------------------------------------------------------------------------------------------------------
                        df0 = df0[['X', 'Y', 'Z', 'DoseGy', r]]
                        df0 = df0[df0[r] == 1]
                        Roi_df = pd.concat([Roi_df, df0], ignore_index=True)
                Roi_df = Roi_df.drop_duplicates(subset=['X', 'Y', 'Z'], keep='last')
                OrganVolumeInDoseMatrix = (len(Roi_df)*mode(ListXDiff)*mode(ListYDiff)*mode(ListZDiff))/1000
                Dict_of_df[r] = pd.concat([Dict_of_df[r], Roi_df], ignore_index=True)
                print(r, 'ListZDiffUniqueRoi =', ListZDiffUniqueroi, ' RoiVolume: ', round(RoiVolume,1), ' OrganVolumeInDoseMatrix: ', round(OrganVolumeInDoseMatrix, 1))
                #----------------------------------------------------------------------------------------------------------------------------
                #Dosimetric metrics
                Dmin  = Dict_of_df[r]['DoseGy'].min()
                Dmean = Dict_of_df[r]['DoseGy'].mean()
                Dmax  = Dict_of_df[r]['DoseGy'].max()
                D98PCT= Dict_of_df[r]['DoseGy'].quantile(0.02)
                D50PCT= Dict_of_df[r]['DoseGy'].quantile(0.50)
                D02PCT= Dict_of_df[r]['DoseGy'].quantile(0.98)
                data = {
                        'RTSTRUCT': [rs],
                        'RTDOSE': [rd],
                        'ROIName': [r],
                        'VoxX': [mode(ListXDiff)],
                        'VoxY': [mode(ListYDiff)],
                        'VoxZ': [mode(ListZDiff)],
                        'ListZDiffUniqueroi': [ListZDiffUniqueroi],
                        'VolumeFomRS': [RoiVolume],
                        'VolumeFomRD': [OrganVolumeInDoseMatrix],
                        'Dmin': [Dmin],
                        'Dmean': [Dmean],
                        'Dmax': [Dmax],
                        'D98PCT': [D98PCT],
                        'D50PCT': [D50PCT],
                        'D02PCT': [D02PCT]
                       }
                df = pd.DataFrame.from_dict(data, orient='columns')
                ROIVolumeConsistency_df = pd.concat([ROIVolumeConsistency_df,df], ignore_index=True)
                #----------------------------------------------------------------------------------------------------------------------------
            pickle.dump(Dict_of_df, open(os.path.join(NEWDOSIFOLDER, NewDosiName), "wb"))  # save it into a file named save.p
Outtxt = os.path.join(Projet, 'ROIVolumeConsistency_df.txt')
ROIVolumeConsistency_df.to_csv(Outtxt, sep='\t', encoding='utf-8', index=False)
end_time = datetime.now()
print('---------------------------------------------------------------------------------------------------------------------------------------')
print('Duration: {}'.format(end_time - start_time))
print('---------------------------------------------------------------------------------------------------------------------------------------')


